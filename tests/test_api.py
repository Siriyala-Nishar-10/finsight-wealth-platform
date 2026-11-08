from fastapi.testclient import TestClient
import api.main as api_main

client = TestClient(api_main.app)


def fake_result(risk_profile, capital):
    return {
        "risk_profile": risk_profile,
        "capital_inr": capital,
        "allocation": {
            "RELIANCE": {"weight": 0.4, "weight_percent": 40.0, "amount_inr": capital * 0.4},
            "CASH_DEBT_SLEEVE": {"weight": 0.6, "weight_percent": 60.0, "amount_inr": capital * 0.6},
        },
        "expected_return_percent": 10.0,
        "volatility_percent": 8.0,
        "annualized_volatility": 0.08,
        "sharpe_ratio": 0.5,
        "profile_limits": {"max_drawdown_pct": 10.0},
    }


def setup_function():
    api_main.optimize_portfolio = fake_result


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_optimize_valid_request():
    response = client.post("/optimize", json={"capital": 100000, "risk_profile": "moderate"})
    assert response.status_code == 200
    body = response.json()
    assert body["capital_inr"] == 100000
    assert body["risk_profile"] == "moderate"


def test_all_three_profiles_are_accepted():
    for profile in ["conservative", "moderate", "aggressive"]:
        response = client.post("/optimize", json={"capital": 50000, "risk_profile": profile})
        assert response.status_code == 200
        assert response.json()["risk_profile"] == profile


def test_zero_capital_is_rejected():
    response = client.post("/optimize", json={"capital": 0, "risk_profile": "moderate"})
    assert response.status_code == 422


def test_unknown_profile_is_rejected():
    response = client.post("/optimize", json={"capital": 100000, "risk_profile": "very_aggressive"})
    assert response.status_code == 422


def test_risk_score_endpoint():
    response = client.post("/risk-score", json={"capital": 100000, "risk_profile": "conservative"})
    assert response.status_code == 200
    assert response.json()["volatility_percent"] == 8.0
