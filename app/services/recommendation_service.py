from app.repositories.recommendation_repository import (
    RecommendationRepository,
)

from app.schemas.recommendation import (RecommendationInternal, RecommendationResponse,)

from app.core.logger import get_logger


logger = get_logger(log_name="recommendation_service", log_folder="services")


class RecommendationService:

    def __init__(self):
        self.repository = RecommendationRepository()

    def get_product_recommendations(self, product_id: int) -> RecommendationResponse:

        logger.info(f"Processing recommendations for product_id={product_id}")

        recommendations = self.repository.get_product_recommendations(product_id=product_id)

        recommendation_objects = [RecommendationInternal(**row) for row in recommendations]

        return RecommendationResponse(product_id=product_id, recommendations=recommendation_objects)
        