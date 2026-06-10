from app.dependencies.auth import get_current_client

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_missing_api_key_returns_401():
    """
    Verify requests without API key are rejected.
    """

    response = client.get("/api/v1/products/37/recommendations")

    assert response.status_code == 401
    assert response.json()["detail"] == "API key is required"


def test_invalid_api_key_returns_401():
    """
    Verify invalid API keys are rejected.
    """

    response = client.get(
        "/api/v1/products/37/recommendations", headers={"X-API-Key": "invalid_api_key"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid API key"


def mock_get_current_client():
    return {"client_id": 1, "client_name": "test-client"}


def test_authenticated_request_returns_200():
    """
    Verify authenticated requests are allowed.
    """
    app.dependency_overrides[get_current_client] = mock_get_current_client

    response = client.get("/api/v1/products/37/recommendations")

    assert response.status_code == 200

    response_body = response.json()

    assert "product_id" in response_body
    assert "recommendations" in response_body
    assert "recommendation_count" in response_body
