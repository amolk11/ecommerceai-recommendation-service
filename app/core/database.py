from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from app.core.config import settings


@lru_cache(maxsize=1)
def _create_engine() -> Engine:
    if not settings.db_url:
        raise RuntimeError("DB_URL is required for database access")

    return create_engine(
        settings.db_url,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        pool_recycle=1800,
    )


def get_engine() -> Engine:
    """
    Return the ecommerce database engine.
    """
    return _create_engine()
