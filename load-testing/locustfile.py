from locust import HttpUser, task, between
import os
class RecommendationUser(HttpUser):
    wait_time = between(1, 3)


    headers = {
        "X-API-Key": "cai_sk_-o0rnmmPz5QJCkvaNE_nJzRTyxTIvTJFDJMqAJBfcFk"
    }

    @task
    def get_recommendations(self):
        self.client.get(
            "/api/v1/products/24852/recommendations",
            headers=self.headers,
            name="/recommendations"
        )
