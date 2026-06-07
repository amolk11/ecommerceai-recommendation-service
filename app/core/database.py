from sqlalchemy import create_engine, URL
from sqlalchemy.engine import Engine

import os
from dotenv import load_dotenv

from app.core.config import settings

load_dotenv()

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"), 
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME"),
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
