from fastapi import Header, HTTPException, status

from platform_core.auth import validate_api_key

from app.core.database import get_platform_engine

from app.metrics.metrics import (
    AUTH_REQUESTS_TOTAL,
    AUTH_SUCCESS_TOTAL,
    AUTH_MISSING_API_KEY_TOTAL,
    AUTH_INVALID_API_KEY_TOTAL,
)


def get_current_client(
    x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> dict:

    AUTH_REQUESTS_TOTAL.inc()

    if not x_api_key:

        AUTH_MISSING_API_KEY_TOTAL.inc()

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="API key is required")

    engine = get_platform_engine()

    with engine.connect() as connection:
        client = validate_api_key(connection=connection, api_key=x_api_key)

    if client is None:

        AUTH_INVALID_API_KEY_TOTAL.inc()

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")

    AUTH_SUCCESS_TOTAL.inc()

    return client
