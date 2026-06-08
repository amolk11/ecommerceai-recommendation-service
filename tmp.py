from app.cache.redis_cache import RedisCache

cache = RedisCache()

cache.set(
    key="test",
    value="hello",
    ttl=60,
)

print(cache.get("test"))