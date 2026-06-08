from fastapi import APIRouter, Depends, HTTPException, Path, Query

from app.core.logger import get_logger
from app.services.recommendation_service import RecommendationService
from app.schemas.recommendation import RecommendationResponse
from app.exceptions.repository import RecommendationRepositoryError
from app.dependencies.recommendation import get_recommendation_service

router = APIRouter(prefix="/products", tags=["Products"])

logger = get_logger(log_name="products", log_folder="api")


@router.get("/{product_id}/recommendations", response_model=RecommendationResponse)
def get_product_recommendations(product_id: int = Path(gt=0, description="Product identifier"), 
                                limit: int = Query(default=10, ge=1, le=20, description="Maximum number of recommendations returned"), 
                                recommendation_service: RecommendationService = Depends(get_recommendation_service),
                                ):

    logger.info(f"Received recommendation request for product_id={product_id} with limit={limit}")
    
    recommendations = (recommendation_service.get_product_recommendations(product_id=product_id, limit=limit))
    
    if not recommendations.recommendations:
        logger.warning(f"No recommendations found for product_id={product_id}")
        raise HTTPException(status_code=404,detail=f"No recommendations found "
                                                    f"for product_id={product_id}")
    return recommendations
 