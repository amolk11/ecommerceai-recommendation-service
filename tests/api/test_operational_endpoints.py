from app.dependencies.recommendation import get_recommendation_service
from app.schemas.recommendation import RecommendationResponse
from main import app


class EmptyRecommendationService:
    def get_product_recommendations(self, product_id: int, limit: int = 20):
        return RecommendationResponse(
            product_id=product_id,
            recommendation_count=0,
            recommendations=[],
        )


def test_metrics_endpoint(authenticated_client):
    response = authenticated_client.get("/metrics")

    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]


def test_no_recommendations_returns_404(authenticated_client):
    app.dependency_overrides[get_recommendation_service] = EmptyRecommendationService

    response = authenticated_client.get("/api/v1/products/404/recommendations")

    assert response.status_code == 404
    assert response.json()["detail"] == "No recommendations found for product_id=404"
