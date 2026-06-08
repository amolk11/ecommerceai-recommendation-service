from fastapi import Depends

from app.dependencies.repository import get_recommendation_repository
from app.repositories.recommendation_repository import RecommendationRepository
from app.services.recommendation_service import RecommendationService
from app.dependencies.cache import get_cache
from app.cache.redis_cache import RedisCache


def get_recommendation_service(repository: RecommendationRepository = Depends(get_recommendation_repository), 
                               cache: RedisCache = Depends(get_cache)) -> RecommendationService:

    return RecommendationService(repository=repository, cache=cache)
