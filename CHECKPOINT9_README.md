# FinSight — Week 9 Integration & Testing

## 1. What This Adds

Week 9 integrates the existing Week 6 portfolio optimization model into a working API and dashboard.

Implemented components:

- FastAPI serving layer around the existing Week 6 `src/experiment.py` model.
- `/optimize`, `/risk-score`, `/portfolio/{risk_profile}`, and health endpoints.
- Streamlit dashboard with portfolio allocation charts and CSV export.
- Pytest API integration tests.
- Locust load-testing scenario configured for 50 concurrent users.

**Implementation status:** Completed. API and dashboard are running successfully.

## 2. Required Existing Project Files

The following existing files were retained:

- `src/experiment.py`
- `data/finsight_portfolio_data.csv`
- `data/finsight_risk_profiles.csv`

The following Week 9 components were added:

- `src/portfolio_service.py`
- `api/`
- `dashboard/`
- `tests/`
- `load_testing/`
- `requirements-week9.txt`
- `CHECKPOINT9_README.md`

The Week 9 adapter calls the existing Week 6 functions `load_data`, `estimate`, and `optimize`. It does not replace the original model.

## 3. Environment and Installation

**Environment:**

- Operating System: Windows
- Python: 3.14.7
- Virtual environment: `venv`

Activate the environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements-week9.txt
```

The Week 9 environment and required dependencies were configured successfully.

## 4. Run the API

From the repository root:

```powershell
uvicorn api.main:app --reload
```

**API URL:** http://127.0.0.1:8000

**Swagger documentation:** http://127.0.0.1:8000/docs

The API was started successfully, and the endpoints were verified through the Swagger interface.

Example optimization request:

```json
{
  "capital": 100000,
  "risk_profile": "moderate"
}
```

Implemented endpoints:

| Method | Endpoint                    | Purpose                         |
| ------ | --------------------------- | ------------------------------- |
| GET    | `/`                         | API information                 |
| GET    | `/health`                   | Health check                    |
| POST   | `/optimize`                 | Portfolio optimization          |
| POST   | `/risk-score`               | Volatility-based risk indicator |
| GET    | `/portfolio/{risk_profile}` | Retrieve portfolio information  |

## 5. Run the Dashboard

In a second terminal:

```powershell
.\venv\Scripts\Activate.ps1
streamlit run dashboard/app.py
```

**Dashboard URL:** http://localhost:8501

Optional API URL override:

```powershell
$env:FINSIGHT_API_URL = "http://127.0.0.1:8000"
```

Optional data directory override:

```powershell
$env:FINSIGHT_DATA_DIR = "C:\path\to\finsight-wealth-platform\data"
```

### Dashboard Verification

The Streamlit dashboard was launched successfully and returned portfolio optimization results.

Observed Conservative profile results:

| Metric                 | Result |
| ---------------------- | -----: |
| Expected annual return | 11.38% |
| Annualized volatility  |  5.94% |
| Sharpe ratio           |  0.905 |

The dashboard also displayed the portfolio allocation chart and investment disclaimer.

## 6. Run Automated Tests

Execute:

```powershell
pytest -v
```

### Test Results

<pre>
Platform: Windows
Python: 3.14.7
Pytest: 9.2.0

Collected: 6 tests

test_health_endpoint                 PASSED
test_optimize_valid_request          PASSED
test_all_three_profiles_are_accepted PASSED
test_zero_capital_is_rejected        PASSED
test_unknown_profile_is_rejected     PASSED
test_risk_score_endpoint             PASSED

6 passed, 1 warning
</pre>

**Result: 6/6 tests passed.**

The tests cover API health, valid optimization requests, supported risk profiles, input validation, unknown profiles, and risk-score functionality.

Note: The tests stub the optimizer function. A separate manual end-to-end test with the actual project data is also required.

One Starlette deprecation warning was reported concerning the HTTPX test-client integration. It did not cause any test failures.

## 7. Load Testing — 50 Concurrent Users

Start the API first:

```powershell
uvicorn api.main:app --reload
```

In another terminal:

```powershell
locust -f load_testing/locustfile.py --host http://127.0.0.1:8000
```

Open:

http://localhost:8089

Test configuration:

- Number of users: 50
- Spawn rate: 10 users/second
- Host: `http://127.0.0.1:8000`

### Actual Load-Test Results

| Metric                | Measured result |
| --------------------- | --------------: |
| Total requests        |             148 |
| Failed requests       |               0 |
| Failure rate          |              0% |
| Requests per second   |            11.2 |
| Average response time |     1,845.14 ms |
| Median response time  |        1,900 ms |
| 95th percentile       |        3,300 ms |
| 99th percentile       |        3,800 ms |
| Minimum response time |           88 ms |
| Maximum response time |        3,834 ms |

### Endpoint-wise Results

| Endpoint               | Requests | Failures |   Median |      p95 |
| ---------------------- | -------: | -------: | -------: | -------: |
| `/health`              |       75 |        0 | 1,500 ms | 3,300 ms |
| `/optimize [moderate]` |       73 |        0 | 2,400 ms | 3,400 ms |

**Load-test observation:** The API handled the recorded 50-user test without request failures. Response latency, particularly for portfolio optimization, remains an area for improvement.

These are measured results from the completed test run, not performance guarantees.

## 8. Model and Reporting Notes

The implementation uses the Week 6 best configuration:

- Ledoit-Wolf covariance estimation.
- Return shrinkage: 0.5.
- Maximum per-stock weight: 0.40.
- Assumed cash/debt return: 6%.

Important modelling considerations:

- The cash/debt sleeve is a modelling assumption, not a real bond instrument.
- The API calculates INR allocation amounts based on the capital entered by the user.
- Annualized expected return and volatility are estimates based on the supplied historical sample.
- These estimates are not guaranteed investment outcomes or investment advice.
- The `/risk-score` endpoint exposes annualized volatility as a transparent volatility-based risk indicator. It does not invent a separate 0–100 risk score.
- The uploaded `optimizer.py` is the older Checkpoint 2 optimizer. Week 9 deliberately serves the Week 6 implementation in `experiment.py`.

## 9. Git and GitHub Submission

The Week 9 implementation was committed and pushed successfully.

**Final commit:**

```text
354c736 feat: complete Week 9 integration testing and portfolio API
```

Repository:

https://github.com/Siriyala-Nishar-10/finsight-wealth-platform

## 10. Week 9 Completion Summary

| Task                                          | Status      |
| --------------------------------------------- | ----------- |
| FastAPI integration                           | Completed   |
| Week 6 model adapter                          | Completed   |
| API endpoints                                 | Completed   |
| Streamlit dashboard                           | Completed   |
| Portfolio allocation visualization            | Verified    |
| Pytest API testing                            | 6/6 passed  |
| Locust load testing                           | Completed   |
| 50 concurrent-user test                       | 0% failures |
| Git commit and push                           | Completed   |
| Manual verification of all dashboard profiles | Pending     |

### Final Status

**Week 9 integration and automated testing are completed.** The API, dashboard, test suite, and load-testing workflow are operational, and the implementation has been pushed to GitHub.

Before final submission, manually verify the Conservative, Moderate, and Aggressive dashboard profiles using the actual project data.

---

**Next Phase: Week 10 — Production Readiness and Deployment**

Planned activities:

1. Improve API response performance.
2. Strengthen input validation and error handling.
3. Improve dashboard usability.
4. Configure environment variables and secrets safely.
5. Prepare deployment.
6. Update project documentation and demo materials.
