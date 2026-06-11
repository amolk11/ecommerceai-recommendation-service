from unittest.mock import Mock, patch

import redis
import pytest

from app.cache.redis_cache import RedisCache


@pytest.fixture
def mock_redis():
    with patch("app.cache.redis_cache.redis.Redis") as redis_cls:
        client = Mock()
        redis_cls.return_value = client

        yield client


def test_get_success(mock_redis):
    mock_redis.get.return_value = "cached_data"

    cache = RedisCache()
    result = cache.get("key1")

    assert result == "cached_data"
    mock_redis.get.assert_called_once_with("key1")


def test_get_redis_exception(mock_redis):
    mock_redis.get.side_effect = redis.RedisError()

    cache = RedisCache()
    result = cache.get("key1")

    assert result is None


def test_set_success(mock_redis):
    cache = RedisCache()

    cache.set("key1", "value1", 300)

    mock_redis.set.assert_called_once_with(
        name="key1",
        value="value1",
        ex=300,
    )


def test_set_redis_exception(mock_redis):
    mock_redis.set.side_effect = redis.RedisError()

    cache = RedisCache()
    cache.set("key1", "value1", 300)

    mock_redis.set.assert_called_once()


def test_ping_success(mock_redis):
    mock_redis.ping.return_value = True

    cache = RedisCache()

    assert cache.ping() is True


def test_ping_failure(mock_redis):
    mock_redis.ping.side_effect = redis.RedisError()

    cache = RedisCache()

    assert cache.ping() is False
