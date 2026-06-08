from app.cache.redis_cache import RedisCache


def get_cache() -> RedisCache:

    return RedisCache()
