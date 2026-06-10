import json
import pytest

from app.services.recommendation_service import RecommendationService
from tests.conftest import MockRecommendationRepository, MockCache
from app.exceptions.repository import RecommendationRepositoryError


def test_get_product_recommendations_returns_response():

    repository = MockRecommendationRepository()

    service = RecommendationService(repository=repository, cache=MockCache())

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

    service = RecommendationService(repository=repository, cache=MockCache())

    response = service.get_product_recommendations(product_id=100, limit=3)

    assert response.recommendation_count == 3

    assert len(response.recommendations) == 3
    
    
class MockEmptyRecommendationRepository:

    def get_product_recommendations(self, product_id: int):
        return []


def test_empty_recommendations():

    repository = MockEmptyRecommendationRepository()

    service = RecommendationService(repository=repository, cache=MockCache())

    response = service.get_product_recommendations(product_id=100, limit=10)

    assert response.product_id == 100

    assert response.recommendation_count == 0

    assert response.recommendations == []
    
    
class MockCacheHit:

    def get(self, key):

        response = {
            "product_id": 100,
            "recommendation_count": 1,
            "recommendations": [
                {
                    "product_id": 100,
                    "recommended_product_id": 1,
                    "co_purchase_count": 100,
                    "support": 0.10,
                    "confidence": 0.80,
                    "lift": 2.0,
                    "recommendation_score": 0.95,
                    "recommendation_rank": 1,
                }
            ],
        }

        return json.dumps(response)

    def set(self, key, value, ttl):
        pass
    
    
class FailingRepository:

    def get_product_recommendations(self, product_id):

        raise AssertionError("Repository should not be called")
        

def test_cache_hit_returns_cached_response():

    service = RecommendationService(repository=FailingRepository(), cache=MockCacheHit())

    response = service.get_product_recommendations(product_id=100, limit=10)

    assert response.product_id == 100

    assert response.recommendation_count == 1
    
    
class TrackingCache:

    def __init__(self):

        self.was_set_called = False

    def get(self, key):

        return None

    def set(self, key, value, ttl):

        self.was_set_called = True
        
    
def test_cache_miss_stores_response():

    cache = TrackingCache()

    repository = MockRecommendationRepository()

    service = RecommendationService(repository=repository, cache=cache)

    service.get_product_recommendations(product_id=100, limit=10)

    assert cache.was_set_called


def test_build_cache_key():

    key = RecommendationService._build_cache_key(product_id=35, limit=10)

    assert key == "recommendations:35:10"

    
def test_repository_error_is_raised():

    service = RecommendationService(repository=FailingRepository(), cache=MockCache())

    with pytest.raises(RecommendationRepositoryError):

        service.get_product_recommendations(product_id=100, limit=10)
        