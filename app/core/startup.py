from sqlalchemy import text

from app.core.database import get_engine
from app.core.logger import get_logger
from app.cache.redis_cache import RedisCache

logger = get_logger(log_name="startup", log_folder="system")


def validate_database_connection() -> None:
    """
    Validate database connectivity during application startup.
    """

    with get_engine().connect() as conn:
        conn.execute(text("SELECT 1"))

    logger.info("Database connection successful")


def validate_redis_connection() -> None:
    """
    Validate Redis connectivity during application startup.
    """

    cache = RedisCache()

    if not cache.ping():
        raise RuntimeError("Redis connection failed")

    logger.info("Redis connection successful")


def validate_platform_connection() -> None:
    """
    Validate Platform Core infrastructure during application startup.
    """

    from platform_core.validation import validate_platform_infrastructure

    validate_platform_infrastructure()

    logger.info("Platform Core infrastructure validation successful")
