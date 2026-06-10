import pytest

from fastapi.testclient import TestClient

from main import app

from app.dependencies.recommendation import get_recommendation_service
from app.dependencies.auth import get_current_client
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


class MockCache:
    def get(self, key: str):
        return None

    def set(self, key: str, value, ttl: int):
        pass


def override_recommendation_service():

    return RecommendationService(
        repository=MockRecommendationRepository(), cache=MockCache()
    )


def override_get_current_client():
    return {"client_id": 1, "client_name": "test-client", "is_active": True}


@pytest.fixture
def client():

    app.dependency_overrides[get_recommendation_service] = (
        override_recommendation_service
    )

    yield TestClient(app)

    app.dependency_overrides.clear()


@pytest.fixture
def authenticated_client():

    app.dependency_overrides[get_recommendation_service] = (
        override_recommendation_service
    )

    app.dependency_overrides[get_current_client] = override_get_current_client

    yield TestClient(app)

    app.dependency_overrides.clear()
