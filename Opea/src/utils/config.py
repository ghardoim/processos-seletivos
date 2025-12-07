from dataclasses import dataclass
from typing import Optional
from os import getenv

from dotenv import load_dotenv
load_dotenv()

@dataclass
class Config:
    s3_bucket: str
    aws_region: str
    aws_access_key_id: str
    aws_secret_access_key: str
    user_prefix: str

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            *[getenv(env) for env in ["S3_BUCKET", "AWS_REGION", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "USER_PREFIX"]],
        )

    @property
    def _base_spark(self) -> str:
        return f"s3a://{self.s3_bucket}/{self.user_prefix}"

    @property
    def _base_s3(self) -> str:
        return f"s3://{self.s3_bucket}/{self.user_prefix}"

    @property
    def raw_clientes_path(self) -> str:
        return f"{self._base_spark}/raw/clientes"

    @property
    def raw_enderecos_path(self) -> str:
        return f"{self._base_spark}/raw/enderecos"

    @property
    def stage_clientes_path(self) -> str:
        return f"{self._base_spark}/stage/clientes"

    @property
    def stage_enderecos_path(self) -> str:
        return f"{self._base_spark}/stage/enderecos"

    @property
    def analytics_clientes_path(self) -> str:
        return f"{self._base_spark}/analytics/clientes"

    @property
    def athena_results_path(self) -> str:
        return f"{self._base_s3}/done/athena_results/"

    @property
    def analytics_clientes_crawler_path(self) -> str:
        return f"{self._base_s3}/analytics/clientes/"

    @property
    def glue_database(self) -> str:
        return self.user_prefix

    @property
    def glue_crawler_name(self) -> str:
        return f"{self.user_prefix}_crawler"

    @property
    def glue_crawler_role(self) -> Optional[str]:
        return getenv("GLUE_CRAWLER_ROLE", f"{self.user_prefix}_glue_crawler_role")
