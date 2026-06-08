from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import get_engine
from app.core.logger import get_logger
from app.exceptions.repository import RecommendationRepositoryError


logger = get_logger(log_name="recommendation_repository", log_folder="repositories")


class RecommendationRepository:

    @staticmethod
    def get_product_recommendations(product_id: int) -> list[dict]:

        query = text("""
                SELECT
                    product_id_a AS product_id,
                    product_id_b AS recommended_product_id,
                    co_purchase_count,
                    support,
                    confidence,
                    lift,
                    recommendation_score,
                    recommendation_rank
                FROM serving.product_recommendations_top20
                WHERE product_id_a = :product_id
                ORDER BY recommendation_rank
            """)

        logger.info(f"Fetching recommendations for product_id={product_id}")

        try:

            with get_engine().connect() as conn:
            
                result = conn.execute(query, {"product_id": product_id})

                return result.mappings().all()

        except SQLAlchemyError as e:
        
            logger.exception(f"Failed to fetch recommendations for product_id={product_id}")

            raise RecommendationRepositoryError("Failed to fetch recommendations") from e
        