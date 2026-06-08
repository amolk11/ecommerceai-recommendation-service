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


def test_get_product_recommendations_returns_response():

    repository = MockRecommendationRepository()

    service = RecommendationService(repository=repository)

    response = service.get_product_recommendations(product_id=100, limit=10)

    assert response.product_id == 100

    assert response.recommendation_count == 1

    assert len(response.recommendations) == 1
    
    
class MockRecommendationRepositoryMany:

    def get_product_recommendations(self,product_id: int):

        return [
            {
                "product_id": product_id,
                "recommended_product_id": i,
                "co_purchase_count": 100,
                "support": 0.10,
                "confidence": 0.80,
                "lift": 2.0,
                "recommendation_score": 0.95,
                "recommendation_rank": i,
            }
            for i in range(1, 6)
        ]
        

def test_limit_is_applied():

    repository = MockRecommendationRepositoryMany()

    service = RecommendationService(repository=repository)

    response = service.get_product_recommendations(product_id=100, limit=3)

    assert response.recommendation_count == 3

    assert len(response.recommendations) == 3
    
    
class MockEmptyRecommendationRepository:

    def get_product_recommendations(self, product_id: int):
        return []


def test_empty_recommendations():

    repository = MockEmptyRecommendationRepository()

    service = RecommendationService(repository=repository)

    response = service.get_product_recommendations(product_id=100, limit=10)

    assert response.product_id == 100

    assert response.recommendation_count == 0

    assert response.recommendations == []
    