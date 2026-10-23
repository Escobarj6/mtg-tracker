import logging

from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from mtg_api.db import engine

logger = logging.getLogger(__name__)

app = FastAPI(title="MTG Tracker API")


@app.get("/health")
def health() -> dict[str, str]:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except SQLAlchemyError:
        logger.exception("Database health check failed")
        raise HTTPException(status_code=503, detail="database unavailable")
    return {"status": "ok", "database": "ok"}
