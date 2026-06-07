from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.api.v1.health import router as health_router
from app.api.v1.products import router as products_router
from app.core.config import settings
from app.core.database import get_engine
from app.core.logger import get_logger


logger = get_logger(
    log_name="startup",
    log_folder="system"
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Starting recommendation service")

    try:
        with get_engine().connect() as conn:
            conn.execute(text("SELECT 1"))

        logger.info("Database connection successful")

    except Exception as exc:
        logger.exception(
            "Database connection failed"
        )
        raise exc

    yield

    logger.info("Shutting down recommendation service")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(
    health_router,
    prefix="/api/v1",
    tags=["Health"],
)

app.include_router(
    products_router,
    prefix="/api/v1",
)
