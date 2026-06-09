import redis
import time

from app.cache.cache_manager import CacheManager
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger(log_name="redis_cache", log_folder="cache")


class RedisCache(CacheManager):

    def __init__(self):
        
        self.client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            decode_responses=True,
        )

    def get(self, key: str):
        try:
            start = time.perf_counter()
            result = self.client.get(key)
            redis_time = time.perf_counter() - start
            logger.info(f"Redis GET took {redis_time:.3f}s")
            return result
        except redis.RedisError:
            logger.exception(f"Redis GET failed for key={key}")
            return None

    def set(self, key: str, value, ttl: int):
        try:
            self.client.set(name=key, value=value, ex=ttl)
        except redis.RedisError:
            logger.exception(f"Redis SET failed for key={key}")

    def ping(self) -> bool:
        try:
            return self.client.ping()
        except redis.RedisError:
            logger.exception("Redis ping failed")
            return False
        