from locust import HttpUser, task, between
import random
import os


class RecommendationUser(HttpUser):
    host = "http://localhost:8000"

    wait_time = between(1, 3)

    headers = {"X-API-Key": os.getenv("TEST_API_KEY")}

    PRODUCT_IDS = [
        1,
        3,
        4,
        8,
        9,
        10,
        11,
        12,
        18,
        23,
        25,
        26,
        27,
        28,
        29,
        32,
        34,
        35,
        36,
        37,
    ]

    @task
    def get_recommendations(self):
        product_id = random.choice(self.PRODUCT_IDS)

        self.client.get(
            f"/api/v1/products/{product_id}/recommendations",
            headers=self.headers,
            name="/recommendations",
        )
