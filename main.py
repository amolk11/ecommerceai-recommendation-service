from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.health import router as health_router
from app.api.v1.products import router as products_router
from app.api.v1.metrics import router as metrics_router
from app.core.config import settings
from app.core.logger import get_logger
from app.exceptions.handlers import recommendation_repository_exception_handler
from app.exceptions.repository import RecommendationRepositoryError
from app.core.startup import validate_database_connection, validate_redis_connection
from app.middleware.request_timing import request_timing_middleware
from app.middleware.request_id import request_id_middleware

from platform_core.validation import validate_platform_infrastructure


logger = get_logger(log_name="startup", log_folder="system")


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Starting recommendation service")

    try:
        validate_database_connection()
        validate_redis_connection()
        validate_platform_infrastructure()

    except Exception:
        logger.exception("Database connection failed")
        raise

    yield

    logger.info("Shutting down recommendation service")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.middleware("http")(request_timing_middleware)
app.middleware("http")(request_id_middleware)

app.add_exception_handler(
    RecommendationRepositoryError,
    recommendation_repository_exception_handler,
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

app.include_router(
    metrics_router,
)
