from pydantic import BaseModel


class RecommendationInternal(BaseModel):
    product_id: int
    recommended_product_id: int

    co_purchase_count: int

    support: float
    confidence: float
    lift: float

    recommendation_score: float
    recommendation_rank: int


class RecommendationResponse(BaseModel):
    product_id: int
    recommendations: list[RecommendationInternal]
    