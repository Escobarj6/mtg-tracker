from sqlalchemy import URL, create_engine

from mtg_api.config import settings


def build_url() -> URL:
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


engine = create_engine(build_url(), pool_pre_ping=True)
