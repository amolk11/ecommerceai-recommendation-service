from fastapi.testclient import TestClient

from app.dependencies.recommendation import get_recommendation_service
from app.services.recommendation_service import RecommendationService

from main import app


def test_health_endpoint(client):

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    

class MockRecommendationRepository:

    def get_product_recommendations(self, product_id: int):

        return [
            {
                "product_id": product_id,
                "recommended_product_id": 1,
                "co_purchase_count": 100,
                "support": 0.10,
                "confidence": 0.80,
                "lift": 2.0,
                "recommendation_score": 0.95,
                "recommendation_rank": 1,
            }
        ]
        
        
def override_recommendation_service():

    return RecommendationService(repository=MockRecommendationRepository())


app.dependency_overrides[get_recommendation_service] = override_recommendation_service


def test_get_recommendations(client):

    response = client.get("/api/v1/products/100/recommendations")

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == 100

    assert data["recommendation_count"] == 1

    assert len(data["recommendations"]) == 1
    
    
def test_invalid_product_id(client):

    response = client.get("/api/v1/products/-1/recommendations")

    assert response.status_code == 422
    
    
def test_invalid_limit(client):

    response = client.get("/api/v1/products/100/recommendations?limit=100")

    assert response.status_code == 422
    