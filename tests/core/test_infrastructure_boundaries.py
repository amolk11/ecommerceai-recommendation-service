import pytest

from app.core.config import settings
from app.core import database
from app.dependencies.repository import get_recommendation_repository
from app.repositories.recommendation_repository import RecommendationRepository


def test_database_access_requires_db_url(monkeypatch):
    database._create_engine.cache_clear()
    monkeypatch.setattr(settings, "db_url", None)

    with pytest.raises(RuntimeError, match="DB_URL is required"):
        database.get_engine()

    database._create_engine.cache_clear()


def test_repository_provider_returns_repository():
    assert isinstance(get_recommendation_repository(), RecommendationRepository)
