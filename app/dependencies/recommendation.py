from fastapi import Depends

from app.dependencies.repository import get_recommendation_repository
from app.repositories.recommendation_repository import RecommendationRepository
from app.services.recommendation_service import RecommendationService


def get_recommendation_service(repository: RecommendationRepository = Depends(get_recommendation_repository)) -> RecommendationService:

    return RecommendationService(repository=repository)
