import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Engine, text
from sqlalchemy.exc import SQLAlchemyError

from mtg_api.db import get_engine

logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])


@router.get("/health")
def health(engine: Annotated[Engine, Depends(get_engine)]) -> dict[str, str]:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except SQLAlchemyError:
        logger.exception("Database health check failed")
        raise HTTPException(status_code=503, detail="database unavailable")
    return {"status": "ok", "database": "available"}
