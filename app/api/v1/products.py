from fastapi import APIRouter
from fastapi import HTTPException

from app.core.logger import get_logger
from app.services.recommendation_service import RecommendationService


router = APIRouter(prefix="/products", tags=["Products"])

logger = get_logger(log_name="products", log_folder="api")

recommendation_service = RecommendationService()


@router.get("/{product_id}/recommendations")
def get_product_recommendations(product_id: int,):

    logger.info(f"Received recommendation request for product_id={product_id}")

    recommendations = (recommendation_service.get_product_recommendations(product_id=product_id))

    if not recommendations.recommendations:

        logger.warning(f"No recommendations found for product_id={product_id}")

        raise HTTPException(status_code=404,detail=(f"No recommendations found "
                                                    f"for product_id={product_id}"
                                                    ),
                            )

    return recommendations
