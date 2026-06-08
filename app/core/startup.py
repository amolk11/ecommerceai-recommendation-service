from sqlalchemy import text

from app.core.database import get_engine
from app.core.logger import get_logger

logger = get_logger(
    log_name="startup",
    log_folder="system",
)


def validate_database_connection() -> None:
    """
    Validate database connectivity during application startup.
    """

    with get_engine().connect() as conn:
        conn.execute(text("SELECT 1"))

    logger.info("Database connection successful")
    