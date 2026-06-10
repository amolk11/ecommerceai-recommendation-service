from unittest.mock import Mock, patch


def test_missing_api_key_returns_401(client):
    """
    Verify requests without API key are rejected.
    """

    response = client.get("/api/v1/products/37/recommendations")

    assert response.status_code == 401
    assert response.json()["detail"] == "API key is required"


@patch("app.dependencies.auth.validate_api_key")
@patch("app.dependencies.auth.get_platform_engine")
def test_invalid_api_key_returns_401(
    mock_engine,
    mock_validate,
    client,
):
    mock_validate.return_value = None

    mock_connection = Mock()
    mock_engine.return_value.connect.return_value.__enter__.return_value = (
        mock_connection
    )

    response = client.get(
        "/api/v1/products/37/recommendations",
        headers={"X-API-Key": "invalid_api_key"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid API key"


def test_authenticated_request_returns_200(authenticated_client):
    """
    Verify authenticated requests are allowed.
    """

    response = authenticated_client.get("/api/v1/products/37/recommendations")

    assert response.status_code == 200

    response_body = response.json()

    assert "product_id" in response_body
    assert "recommendations" in response_body
    assert "recommendation_count" in response_body
