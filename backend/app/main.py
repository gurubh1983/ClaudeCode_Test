from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from sqlalchemy import text

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger("strikegenius")
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting StrikeGenius backend")
    yield
    logger.info("Stopping StrikeGenius backend")


app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/health")
async def health():
    db_ok = False
    try:
        async with SessionLocal() as db:
            await db.execute(text("SELECT 1"))
            db_ok = True
    except Exception as exc:  # noqa: BLE001
        logger.warning("DB health check failed: %s", exc)
    return {"status": "ok", "database": "up" if db_ok else "down"}
