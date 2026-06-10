from fastapi.testclient import TestClient

from app.dependencies.recommendation import get_recommendation_service
from app.services.recommendation_service import RecommendationService

from main import app


def test_health_endpoint(client):

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    

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
    