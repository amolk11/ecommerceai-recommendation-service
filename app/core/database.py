from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from app.core.config import settings


# Ecommerce Database
ecommerce_engine: Engine = create_engine(
    settings.db_url,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    pool_recycle=1800,
)


# Platform Database
platform_engine: Engine = create_engine(
    settings.platform_db_url,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_recycle=1800,
)


def get_engine() -> Engine:
    """
    Return the ecommerce database engine.
    """
    return ecommerce_engine


def get_platform_engine() -> Engine:
    """
    Return the platform database engine.
    """
    return platform_engine
