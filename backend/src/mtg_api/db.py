from functools import lru_cache

from sqlalchemy import URL, Engine, create_engine

from mtg_api.config import Settings, get_settings


def build_url(settings: Settings) -> URL:
    query = {"driver": "ODBC Driver 18 for SQL Server"}
    if settings.db_trust_server_certificate:
        query["TrustServerCertificate"] = "yes"

    return URL.create(
        "mssql+pyodbc",
        username=settings.db_user,
        password=settings.db_password.get_secret_value(),
        host=settings.db_host,
        port=settings.db_port,
        database=settings.db_name,
        query=query,
    )


@lru_cache
def get_engine() -> Engine:
    return create_engine(build_url(get_settings()), pool_pre_ping=True)
