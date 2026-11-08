# FinSight — Week 9 Integration & Testing

## What this adds

- FastAPI serving layer around the existing Week 6 `src/experiment.py` model.
- `/optimize`, `/risk-score`, `/portfolio/{risk_profile}`, and health endpoints.
- Streamlit dashboard with allocation charts and CSV export.
- Pytest API tests.
- Locust load-test scenario for 50 concurrent users.

## Required existing project files

Keep your existing:
- `src/experiment.py`
- `data/finsight_portfolio_data.csv`
- `data/finsight_risk_profiles.csv`

Copy the supplied `portfolio_service.py` into `src/`, and copy `api/`, `dashboard/`,
`tests/`, and `load_testing/` into the project root.

The Week 9 adapter calls the existing Week 6 functions `load_data`, `estimate`,
and `optimize`; it does not replace the model.

## Install (Windows PowerShell)

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements-week9.txt
```

Python 3.14 package compatibility can vary. If an install fails, capture the exact
package/error before changing Python versions or pinning dependencies.

## Run the API

From the repository root:

```powershell
uvicorn api.main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

Example request:

```json
{
  "capital": 100000,
  "risk_profile": "moderate"
}
```

## Run the dashboard

In a second terminal:

```powershell
streamlit run dashboard/app.py
```

Optional API URL override:

```powershell
$env:FINSIGHT_API_URL = "http://127.0.0.1:8000"
```

Optional data directory override:

```powershell
$env:FINSIGHT_DATA_DIR = "C:\\path\\to\\finsight-wealth-platform\\data"
```

## Run tests

From the repository root:

```powershell
pytest -v
```

The API tests stub the optimizer function, so they test request validation and API
behaviour without requiring the private project CSV data. Also run a manual end-to-end
test with the real data before submitting.

## Load test (50 concurrent users)

Start the API first. In another terminal:

```powershell
locust -f load_testing/locustfile.py --host http://127.0.0.1:8000
```

Open `http://localhost:8089`, set:
- Number of users: `50`
- Spawn rate: `10`

Run the test for a recorded duration (for example, 2–5 minutes). Save the Locust
statistics and record average, median, p95 latency, requests/second, and failures
in your Week 9 report. Report measured values only.

## Model and reporting notes

- Uses Week 6 best configuration: Ledoit-Wolf covariance, return shrinkage 0.5,
  maximum per-stock weight 0.40, and assumed cash/debt return 6%.
- The cash/debt sleeve is a modelling assumption, not a real bond instrument.
- The API calculates INR amounts from the capital entered by the user.
- Annualized expected return and volatility are estimates based on the supplied
  historical sample. They are not guaranteed outcomes or investment advice.
- The `/risk-score` endpoint exposes annualized volatility as a transparent
  volatility-based risk indicator; it does not invent a separate 0–100 risk score.
- The uploaded source `optimizer.py` is the older Checkpoint 2 optimizer. Week 9
  deliberately serves the Week 6 implementation in `experiment.py`.
