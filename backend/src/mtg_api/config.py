from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="MTG_")

    db_host: str = "127.0.0.1"
    db_port: int = 1433
    db_name: str = "mtg"
    db_user: str = "sa"
    db_password: SecretStr
    db_trust_server_certificate: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
