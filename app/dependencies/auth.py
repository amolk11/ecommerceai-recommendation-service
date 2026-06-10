from fastapi import Header, HTTPException, status

from platform_core.auth import validate_api_key

from app.core.database import get_platform_engine


def get_current_client(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> dict:

    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is required",
            )

    engine = get_platform_engine()

    with engine.connect() as connection:
        client = validate_api_key(
            connection=connection,
            api_key=x_api_key,
        )

    if client is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    return client
