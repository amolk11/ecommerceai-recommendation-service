class RepositoryError(Exception):
    """Base repository exception."""


class RecommendationRepositoryError(RepositoryError):
    """Recommendation repository exception."""
    