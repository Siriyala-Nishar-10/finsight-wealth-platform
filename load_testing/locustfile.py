from locust import HttpUser, task, between


class FinSightUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def optimize_moderate_portfolio(self):
        self.client.post(
            "/optimize",
            json={"capital": 100000, "risk_profile": "moderate"},
            name="/optimize [moderate]",
        )

    @task
    def check_health(self):
        self.client.get("/health")
