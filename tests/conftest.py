import os
import socket

import pytest

from fastapi.testclient import TestClient

os.environ["APP_NAME"] = "ecommerceai-recommendation-service"
os.environ["APP_VERSION"] = "0.1.0"
os.environ["ENVIRONMENT"] = "test"
os.environ["STARTUP_VALIDATION_ENABLED"] = "false"
os.environ.setdefault("DB_URL", "postgresql+psycopg://unit:unit@localhost:5432/unit")
os.environ.setdefault(
    "PLATFORM_DB_URL", "postgresql+psycopg://unit:unit@localhost:5432/platform"
)
os.environ.setdefault("REDIS_HOST", "localhost")
os.environ.setdefault("REDIS_PORT", "6379")
os.environ.setdefault("CACHE_TTL", "3600")

from main import app  # noqa: E402

from app.dependencies.recommendation import get_recommendation_service  # noqa: E402
from app.dependencies.auth import get_current_client  # noqa: E402
from app.services.recommendation_service import RecommendationService  # noqa: E402


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


def pytest_collection_modifyitems(items):
    for item in items:
        if not any(
            item.get_closest_marker(marker) for marker in ("unit", "integration", "e2e")
        ):
            item.add_marker(pytest.mark.unit)


@pytest.fixture(autouse=True)
def block_network_for_unit_tests(monkeypatch, request):
    if request.node.get_closest_marker(
        "integration"
    ) or request.node.get_closest_marker("e2e"):
        return

    original_connect = socket.socket.connect
    original_connect_ex = socket.socket.connect_ex

    def is_allowed_testclient_socket(address):
        if not isinstance(address, tuple) or len(address) < 2:
            return False

        host, port = address[0], address[1]
        return host in {"127.0.0.1", "::1", "localhost"} and port not in {
            5432,
            6379,
        }

    def guarded_connect(sock, address):
        if is_allowed_testclient_socket(address):
            return original_connect(sock, address)

        raise AssertionError(f"Unit tests must not open network connections: {address}")

    def guarded_connect_ex(sock, address):
        if is_allowed_testclient_socket(address):
            return original_connect_ex(sock, address)

        raise AssertionError(f"Unit tests must not open network connections: {address}")

    monkeypatch.setattr(socket.socket, "connect", guarded_connect)
    monkeypatch.setattr(socket.socket, "connect_ex", guarded_connect_ex)


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
