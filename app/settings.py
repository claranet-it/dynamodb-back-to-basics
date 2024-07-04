import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

env = os.environ.get("ENV", "dev")


class Settings(BaseSettings):
    use_local_infra: bool = False
    aws_region: str = "eu-west-2"
    local_aws_access_key_id: str = "local"
    local_aws_secret_access_key: str = "local"
    local_dynamodb_endpoint_url: str = "http://localhost:8000"

    dynamodb_default_query_limit: int = 10

    model_config = SettingsConfigDict(env_file=f".env.{env}")


@lru_cache
def get_settings():
    return Settings()
