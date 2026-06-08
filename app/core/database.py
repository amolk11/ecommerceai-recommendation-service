from sqlalchemy import create_engine, URL
from sqlalchemy.engine import Engine

from app.core.config import settings

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=settings.db_user,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name,
)

engine: Engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    pool_recycle=1800,
)


def get_engine() -> Engine:
    """
    Return the application database engine.
    """

    return engine
