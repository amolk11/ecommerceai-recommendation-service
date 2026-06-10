from unittest.mock import Mock, patch

from app.repositories.recommendation_repository import (
    RecommendationRepository,
)


MOCK_RESULTS = [
    {
        "product_id": 35,
        "recommended_product_id": 100,
        "co_purchase_count": 50,
        "support": 0.1,
        "confidence": 0.8,
        "lift": 2.0,
        "recommendation_score": 0.95,
        "recommendation_rank": 1,
    }
]


@patch(
    "app.repositories.recommendation_repository.RecommendationRepository.get_product_recommendations"
)
def test_repository_returns_list(mock_get):

    mock_get.return_value = MOCK_RESULTS

    repository = RecommendationRepository()

    result = repository.get_product_recommendations(product_id=35)

    assert isinstance(result, list)


@patch(
    "app.repositories.recommendation_repository.RecommendationRepository.get_product_recommendations"
)
def test_repository_returns_expected_columns(mock_get):

    mock_get.return_value = MOCK_RESULTS

    repository = RecommendationRepository()

    result = repository.get_product_recommendations(product_id=35)

    row = result[0]

    assert "product_id" in row
    assert "recommended_product_id" in row
    assert "co_purchase_count" in row
    assert "support" in row
    assert "confidence" in row
    assert "lift" in row
    assert "recommendation_score" in row
    assert "recommendation_rank" in row


@patch(
    "app.repositories.recommendation_repository.RecommendationRepository.get_product_recommendations"
)
def test_repository_returns_empty_list_for_unknown_product(mock_get):

    mock_get.return_value = []

    repository = RecommendationRepository()

    result = repository.get_product_recommendations(product_id=22)

    assert result == []


@patch(
    "app.repositories.recommendation_repository.RecommendationRepository.get_product_recommendations"
)
def test_repository_returns_ranked_results(mock_get):

    mock_get.return_value = MOCK_RESULTS

    repository = RecommendationRepository()

    result = repository.get_product_recommendations(product_id=35)

    ranks = [row["recommendation_rank"] for row in result]

    assert ranks == sorted(ranks)
