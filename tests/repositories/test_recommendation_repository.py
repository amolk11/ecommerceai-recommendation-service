from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.exceptions.repository import RecommendationRepositoryError
from app.repositories.recommendation_repository import RecommendationRepository


@patch("app.repositories.recommendation_repository.get_engine")
def test_get_product_recommendations_success(mock_get_engine):
    mock_rows = [
        {
            "product_id": 1,
            "recommended_product_id": 2,
            "recommendation_score": 0.95,
        }
    ]

    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = mock_rows

    mock_conn = MagicMock()
    mock_conn.execute.return_value = mock_result

    mock_get_engine.return_value.connect.return_value.__enter__.return_value = mock_conn

    result = RecommendationRepository.get_product_recommendations(1)

    assert result == mock_rows
    assert len(result) == 1
    assert result[0]["product_id"] == 1
    mock_conn.execute.assert_called_once()
    mock_result.mappings.assert_called_once()
    mock_result.mappings.return_value.all.assert_called_once()


@patch("app.repositories.recommendation_repository.get_engine")
def test_get_product_recommendations_sqlalchemy_error(mock_get_engine):
    mock_conn = MagicMock()
    mock_conn.execute.side_effect = SQLAlchemyError("DB Error")

    mock_get_engine.return_value.connect.return_value.__enter__.return_value = mock_conn

    with pytest.raises(RecommendationRepositoryError):
        RecommendationRepository.get_product_recommendations(1)
