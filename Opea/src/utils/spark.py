from src.utils.config import Config
from logging import getLogger
from typing import List

from pyspark.sql import DataFrame, SparkSession, functions as F, Window

LOGGER = getLogger(__name__)

def build_spark(cfg: Config, app_name: str = "opea_pipeline") -> SparkSession:
    """Aqui eu poderia descrever o que está acontecendo. Mas convenhamos, a gente sabe que isso aqui foi googlado."""

    jars_path = "/opt/spark/jars/hadoop-aws-3.3.4.jar:/opt/spark/jars/aws-java-sdk-bundle-1.12.262.jar"
    builder = (
        SparkSession.builder.appName(app_name)
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.hadoop.fs.AbstractFileSystem.s3a.impl", "org.apache.hadoop.fs.s3a.S3A")
        .config("spark.hadoop.fs.s3a.access.key", cfg.aws_access_key_id)
        .config("spark.hadoop.fs.s3a.secret.key", cfg.aws_secret_access_key)
        .config("spark.hadoop.fs.s3a.endpoint", f"s3.{cfg.aws_region}.amazonaws.com")
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "true")
        .config("spark.jars", jars_path.replace(":", ","))
        .config("spark.driver.extraClassPath", jars_path)
        .config("spark.executor.extraClassPath", jars_path)
    )
    return builder.getOrCreate()

def write_raw(df: DataFrame, path: str, data_processamento: str) -> None:
    (
        df.withColumn("data_processamento", F.lit(data_processamento))
            .coalesce(1)
            .write.mode("append")
            .partitionBy("data_processamento")
            .option("compression", "snappy")
            .parquet(path)
    )

def deduplicate_latest(df: DataFrame, key_cols: List[str], event_col: str = "data_evento") -> DataFrame:

    window = Window.partitionBy(*key_cols).orderBy(F.col(event_col).desc())
    return df.withColumn("_rn", F.row_number().over(window)).filter(F.col("_rn") == 1).drop("_rn")

def merge_delta(df: DataFrame, path: str) -> None:
    (
        df.coalesce(1)
            .write.mode("overwrite")
            .option("overwriteSchema", "true")
            .parquet(path)
    )
