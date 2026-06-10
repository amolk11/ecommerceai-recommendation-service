import json
import time

from app.repositories.recommendation_repository import RecommendationRepository
from app.exceptions.repository import RecommendationRepositoryError
from app.schemas.recommendation import (
    RecommendationItem,
    RecommendationResponse,
)
from app.core.logger import get_logger
from app.cache.redis_cache import RedisCache
from app.core.config import settings
from app.metrics.metrics import (
    REQUEST_COUNT,
    CACHE_HITS,
    CACHE_MISSES,
    REQUEST_DURATION,
)


logger = get_logger(log_name="recommendation_service", log_folder="services")


class RecommendationService:
    def __init__(self, repository: RecommendationRepository, cache: RedisCache):
        self.repository = repository
        self.cache = cache

    def get_product_recommendations(
        self, product_id: int, limit: int = 20
    ) -> RecommendationResponse:

        start_time = time.perf_counter()

        try:
            logger.info(
                f"Processing recommendations for product_id={product_id}, limit={limit}"
            )
            REQUEST_COUNT.inc()

            cache_key = self._build_cache_key(product_id=product_id, limit=limit)

            cached_response = self.cache.get(cache_key)

            if cached_response:
                logger.info(f"Cache hit for key={cache_key}")
                CACHE_HITS.inc()

                logger.info(
                    f"Serving recommendations from Redis cache for product_id={product_id}"
                )

                return RecommendationResponse(**json.loads(cached_response))

            logger.info(f"Cache miss for key={cache_key}")
            CACHE_MISSES.inc()

            logger.info(
                f"Fetching recommendations from PostgreSQL for product_id={product_id}"
            )

            try:
                recommendations = self.repository.get_product_recommendations(
                    product_id=product_id
                )

            except RecommendationRepositoryError:
                logger.exception(f"Repository failure for product_id={product_id}")

                raise

            recommendations = recommendations[:limit]

            recommendation_objects = [
                RecommendationItem(**row) for row in recommendations
            ]

            response = RecommendationResponse(
                product_id=product_id,
                recommendation_count=len(recommendation_objects),
                recommendations=recommendation_objects,
            )

            self.cache.set(
                key=cache_key,
                value=json.dumps(response.model_dump()),
                ttl=settings.cache_ttl,
            )

            logger.info(
                f"Returning {len(recommendation_objects)} recommendations for product_id={product_id} (requested_limit={limit})"
            )

            return response

        finally:
            REQUEST_DURATION.observe(time.perf_counter() - start_time)

    @staticmethod
    def _build_cache_key(product_id: int, limit: int) -> str:

        return f"recommendations:{product_id}:{limit}"
