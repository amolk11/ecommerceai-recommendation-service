# tests/test_auth.py

import os

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

    response = client.get("/api/v1/products/37/recommendations", headers={"X-API-Key": "invalid_api_key"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid API key"


def test_valid_api_key_returns_200():
    """
    Verify valid API key allows access.
    """

    api_key = os.getenv("TEST_API_KEY")

    assert api_key is not None, ("TEST_API_KEY environment variable is not set")

    response = client.get("/api/v1/products/37/recommendations",headers={"X-API-Key": api_key})

    assert response.status_code == 200

    response_body = response.json()

    assert "product_id" in response_body
    assert "recommendations" in response_body
    assert "recommendation_count" in response_body
    