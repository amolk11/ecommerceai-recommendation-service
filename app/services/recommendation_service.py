from app.repositories.recommendation_repository import RecommendationRepository
from app.exceptions.repository import RecommendationRepositoryError
from app.schemas.recommendation import (RecommendationItem, RecommendationResponse,)
from app.core.logger import get_logger
from app.repositories.recommendation_repository import RecommendationRepository


logger = get_logger(log_name="recommendation_service", log_folder="services")


class RecommendationService:

    def __init__(self, repository: RecommendationRepository):
        self.repository = repository

    def get_product_recommendations(self, product_id: int, limit: int = 20) -> RecommendationResponse:

        logger.info(f"Processing recommendations for product_id={product_id}, limit={limit}")
        
        try:
            recommendations = self.repository.get_product_recommendations(product_id=product_id)
        except RecommendationRepositoryError:
            logger.exception(f"Repository failure for product_id={product_id}")
            raise
        
        recommendations = recommendations[:limit]
        
        recommendation_objects = [RecommendationItem(**row) for row in recommendations]
        
        logger.info(f"Returning {len(recommendation_objects)} recommendations for product_id={product_id} (requested_limit={limit})")

        return RecommendationResponse(product_id=product_id, recommendation_count=len(recommendation_objects), recommendations=recommendation_objects)
        