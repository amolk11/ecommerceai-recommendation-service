from unittest.mock import MagicMock, patch

import pytest

from app.core.startup import (
    validate_database_connection,
    validate_platform_connection,
    validate_redis_connection,
)


@patch("app.core.startup.get_engine")
def test_validate_database_connection_success(mock_get_engine):
    mock_conn = MagicMock()

    mock_get_engine.return_value.connect.return_value.__enter__.return_value = (
        mock_conn
    )

    validate_database_connection()

    mock_conn.execute.assert_called_once()


@patch("app.core.startup.RedisCache")
def test_validate_redis_connection_success(mock_cache):
    mock_cache.return_value.ping.return_value = True

    validate_redis_connection()

    mock_cache.return_value.ping.assert_called_once()


@patch("app.core.startup.RedisCache")
def test_validate_redis_connection_failure(mock_cache):
    mock_cache.return_value.ping.return_value = False

    with pytest.raises(RuntimeError, match="Redis connection failed"):
        validate_redis_connection()

    mock_cache.return_value.ping.assert_called_once()


@patch("platform_core.validation.validate_platform_infrastructure")
def test_validate_platform_connection_success(mock_validate):
    validate_platform_connection()

    mock_validate.assert_called_once()


@patch("platform_core.validation.validate_platform_infrastructure")
def test_validate_platform_connection_failure(mock_validate):
    mock_validate.side_effect = RuntimeError("Platform validation failed")

    with pytest.raises(RuntimeError, match="Platform validation failed"):
        validate_platform_connection()
        