from app.repositories.recommendation_repository import RecommendationRepository


def get_recommendation_repository() -> RecommendationRepository:
    """
    Recommendation repository dependency provider.
    """

    return RecommendationRepository()
