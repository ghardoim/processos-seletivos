from typing import Dict, List, Optional
from src.utils.config import Config
from time import sleep

from botocore.exceptions import ClientError
from logging import getLogger
from boto3 import Session

LOGGER = getLogger(__name__)

def boto_session(cfg: Config) -> Session:
    return Session(aws_access_key_id=cfg.aws_access_key_id, aws_secret_access_key=cfg.aws_secret_access_key, region_name=cfg.aws_region)

def create_and_run_crawler(cfg: Config, target_path: Optional[str] = None) -> None:
    glue = boto_session(cfg).client("glue")
    path = target_path or cfg.analytics_clientes_crawler_path

    try:
        glue.get_crawler(Name=cfg.glue_crawler_name)
        LOGGER.info("Crawler %s already exists", cfg.glue_crawler_name)
    except ClientError as exc:
        if exc.response["Error"]["Code"] == "EntityNotFoundException":
            LOGGER.info("Creating crawler %s", cfg.glue_crawler_name)
            glue.create_crawler(
                Name=cfg.glue_crawler_name,
                Role=cfg.glue_crawler_role,
                DatabaseName=cfg.glue_database,
                Targets={"S3Targets": [{"Path": path}]},
            )
        else: raise

    LOGGER.info("Starting crawler %s", cfg.glue_crawler_name)
    glue.start_crawler(Name=cfg.glue_crawler_name)

    while True:

        resp = glue.get_crawler(Name=cfg.glue_crawler_name)
        state = resp["Crawler"]["State"]

        LOGGER.info("Crawler state=%s", state)
        if state.lower() == "ready": break
        sleep(10)

def run_athena_query(cfg: Config, query: str, output_path: Optional[str] = None) -> Dict:
    athena = boto_session(cfg).client("athena")
    output = cfg.athena_results_path or output_path

    LOGGER.info("Submitting Athena query to %s", output)
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={"Database": cfg.glue_database},
        ResultConfiguration={"OutputLocation": output},
    )

    execution_id = response["QueryExecutionId"]
    while True:

        resp = athena.get_query_execution(QueryExecutionId=execution_id)
        state = resp["QueryExecution"]["Status"]["State"]
        LOGGER.info("Athena query state=%s", state)

        if state in {"SUCCEEDED", "FAILED", "CANCELLED"}:
            if "SUCCEEDED" == state: break

            reason = resp["QueryExecution"]["Status"].get("StateChangeReason", "unknown")
            raise RuntimeError(f"Athena query failed: {reason}")
        sleep(5)

    return athena.get_query_results(QueryExecutionId=execution_id)

def athena_results_to_csv(result: Dict, csv_path: str) -> None:
    rows = result.get("ResultSet", {}).get("Rows", [])
    headers = [col["VarCharValue"] for col in rows[0]["Data"]]

    with open(csv_path, "w", encoding="utf-8") as handle:
        handle.write(",".join(headers) + "\n")

        for row in rows[1:]:
            values: List[str] = []
            for cell in row.get("Data", []):
                values.append(cell.get("VarCharValue", ""))
            handle.write(",".join(values) + "\n")
