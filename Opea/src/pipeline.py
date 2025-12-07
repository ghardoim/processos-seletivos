from argparse import ArgumentParser
from datetime import datetime as dt
from typing import Tuple
import pandas as pd

from logging import getLogger
from os.path import dirname
from os import makedirs

from pyspark.sql import functions as F
from src.utils.aws import athena_results_to_csv, create_and_run_crawler, run_athena_query
from src.utils.spark import build_spark, deduplicate_latest, merge_delta, write_raw
from src.validations import validate_clientes, validate_enderecos
from src.utils.logs import setup_logging
from src.utils.config import Config

LOGGER = getLogger(__name__)

def load_excel(file_path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:

    xls = pd.ExcelFile(file_path) 
    return (pd.read_excel(xls, tab) for tab in ["clientes", "enderecos"])

def log_validation_errors(errors, log_path: str) -> None:
    if not errors: return
    makedirs(dirname(log_path), exist_ok=True)

    with open(log_path, "w", encoding="utf-8") as handle:
        handle.write("linha,campo,valor,motivo\n")
        for err in errors:
            handle.write(f"{err['linha']},{err['campo']},{err['valor']},{err['motivo']}\n")
    LOGGER.warning("Validation produced %s errors. See %s", len(errors), log_path)

def to_spark_dates(df):
    for dtcolumn in { "data_evento", "data_nascimento" }:
        if dtcolumn in df.columns:
            df = df.withColumn(dtcolumn, F.to_timestamp(dtcolumn))
    return df

def ingest_to_raw(cfg: Config, spark, clientes_df: pd.DataFrame, enderecos_df: pd.DataFrame, data_proc: str) -> None:

    valid_clientes, cliente_errors = validate_clientes(clientes_df)
    valid_enderecos, endereco_errors = validate_enderecos(enderecos_df, valid_clientes["id_cliente"].unique())
    log_validation_errors(cliente_errors + endereco_errors, "logs/validation_errors.log")

    clientes_spark = to_spark_dates(spark.createDataFrame(valid_clientes))
    enderecos_spark = to_spark_dates(spark.createDataFrame(valid_enderecos))

    LOGGER.info("Writing %s clientes and %s enderecos to raw", clientes_spark.count(), enderecos_spark.count())
    write_raw(clientes_spark, cfg.raw_clientes_path, data_proc)
    write_raw(enderecos_spark, cfg.raw_enderecos_path, data_proc)

def stage_entities(cfg: Config, spark, data_proc: str) -> None:

    entities = [
        ("cliente", cfg.raw_clientes_path, cfg.stage_clientes_path, "id_cliente"),
        ("endereco", cfg.raw_enderecos_path, cfg.stage_enderecos_path, "id_endereco"),
    ]
    for _, raw_path, stage_path, key in entities:
        raw = spark.read.parquet(raw_path).filter(F.col("data_processamento") == data_proc)
        latest = deduplicate_latest(raw, [key], "data_evento").withColumn(
            "data_atualizacao", F.current_timestamp()
        )
        merge_delta(latest, stage_path)

def build_analytics(cfg: Config, spark) -> None:
    clientes = spark.read.parquet(cfg.stage_clientes_path).filter(F.col("status") == "ativo")
    enderecos = spark.read.parquet(cfg.stage_enderecos_path)
    for dt_column in {"data_atualizacao", "data_evento", "data_processamento"}:
        enderecos = enderecos.withColumnRenamed(dt_column, f"{dt_column}_endereco")

    joined = clientes.join(enderecos, on="id_cliente", how="left")
    analytics_df = (
        joined.withColumn("idade", F.floor(F.datediff(F.current_date(), F.col("data_nascimento")) / F.lit(365.25)))
            .withColumn("estado", F.coalesce(F.col("estado"), F.lit("SEM_UF")))
    )

    (
        analytics_df.repartition("estado")
            .sortWithinPartitions("estado", "nome")
            .write.mode("overwrite")
            .option("compression", "snappy")
            .partitionBy("estado")
            .parquet(cfg.analytics_clientes_path)
    )

def run_athena_validation(cfg: Config, csv_output: str = "resultado_athena.csv") -> None:

    athena_results_to_csv(run_athena_query(cfg, "SELECT * FROM clientes"), csv_output)
    LOGGER.info("Athena results saved to %s", csv_output)

def parse_args():
    parser = ArgumentParser(description="Pipeline de dados Opea")
    parser.add_argument("--input", default="dados_entrada.xlsx", help="Caminho do Excel de entrada")
    parser.add_argument("--skip-athena", action="store_true", help="Não executar validação Athena")
    parser.add_argument("--skip-crawler", action="store_true", help="Não criar/executar crawler")
    return parser.parse_args()

def main():
    setup_logging()
    args = parse_args()
    cfg = Config.from_env()
    data_proc = dt.now().strftime("%Y-%m-%d")
    LOGGER.info("Pipeline iniciado para data_processamento=%s", data_proc)

    clientes_df, enderecos_df = load_excel(args.input)
    spark = build_spark(cfg)

    ingest_to_raw(cfg, spark, clientes_df, enderecos_df, data_proc)
    stage_entities(cfg, spark, data_proc)
    build_analytics(cfg, spark)

    if not args.skip_crawler:
        create_and_run_crawler(cfg)
    if not args.skip_athena:
        run_athena_validation(cfg)

    LOGGER.info("Pipeline finalizado")

if __name__ == "__main__":
    main()
