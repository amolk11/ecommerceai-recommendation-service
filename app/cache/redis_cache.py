import redis

from app.cache.cache_manager import CacheManager
from app.core.config import settings


class RedisCache(CacheManager):

    def __init__(self):

        self.client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            decode_responses=True,
        )

    def get(self, key: str):

        return self.client.get(key)

    def set(self, key: str, value, ttl: int):

        self.client.set(name=key, value=value, ex=ttl)
        
        
    def ping(self) -> bool:

        return self.client.ping()
    