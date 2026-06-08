import pytest

from fastapi.testclient import TestClient

from main import app

from app.dependencies.recommendation import get_recommendation_service
from app.services.recommendation_service import RecommendationService


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


@pytest.fixture
def client():

    app.dependency_overrides[get_recommendation_service] = override_recommendation_service

    yield TestClient(app)

    app.dependency_overrides.clear()
    