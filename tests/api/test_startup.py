from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app


def test_test_environment_skips_infrastructure_validation():
    with (
        patch("main.validate_database_connection") as mock_validate_database,
        patch("main.validate_redis_connection") as mock_validate_redis,
        patch("main.validate_platform_connection") as mock_validate_platform,
        TestClient(app) as client,
    ):
        response = client.get("/api/v1/health")

    assert response.status_code == 200
    mock_validate_database.assert_not_called()
    mock_validate_redis.assert_not_called()
    mock_validate_platform.assert_not_called()
