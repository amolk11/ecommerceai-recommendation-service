from app.repositories.recommendation_repository import RecommendationRepository


def test_repository_returns_list():

    repository = RecommendationRepository()

    result = repository.get_product_recommendations(product_id=35)

    assert isinstance(result, list)
    
    
def test_repository_returns_expected_columns():

    repository = RecommendationRepository()

    result = repository.get_product_recommendations(product_id=35)

    assert len(result) > 0

    row = result[0]

    assert "product_id" in row
    assert "recommended_product_id" in row
    assert "co_purchase_count" in row
    assert "support" in row
    assert "confidence" in row
    assert "lift" in row
    assert "recommendation_score" in row
    assert "recommendation_rank" in row
    
    
def test_repository_returns_empty_list_for_unknown_product():

    repository = RecommendationRepository()

    result = repository.get_product_recommendations(product_id=22)

    assert result == []
    
    
def test_repository_returns_ranked_results():

    repository = RecommendationRepository()

    result = repository.get_product_recommendations(product_id=35)

    ranks = [row["recommendation_rank"] for row in result]

    assert ranks == sorted(ranks)
