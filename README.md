
# FinSight Wealth Platform — Portfolio Optimization Engine

A portfolio optimization engine for a SEBI-registered robo-advisory platform. Accepts an investor's risk profile and capital amount and returns an optimized illustrative asset allocation using Modern Portfolio Theory (MPT), with an interactive dashboard showing expected return versus risk.

## Client

**Domain:** FinTech / Wealth Management  
**Location:** Mumbai  
**Organization:** SEBI-registered wealth management organization

## Project Status

**Checkpoint 5 — Final Demo + Model Card Preparation**

- [x] Checkpoint 1 (Week 1) — Research + Architecture Design
- [x] Checkpoint 2 (Week 3) — Data Pipeline + Baseline Model
- [x] Checkpoint 3 (Week 6) — Core Model + Experimentation
- [x] Checkpoint 4 (Week 9) — Integration + Testing
- [ ] Checkpoint 5 (Week 12) — Final Demo + Model Card

Checkpoints 1–4 are approved in the Cynaris project tracker. Checkpoint 5 remains pending mentor review until the live demo, model card, final code, and passing CI evidence have been submitted and accepted.

## Tech Stack

- Python (use the verified project environment version)
- Pandas and NumPy — Data processing
- SciPy — Portfolio optimization
- scikit-learn — Ledoit-Wolf covariance shrinkage
- MLflow — Experiment tracking
- Matplotlib — Risk-return visualization
- FastAPI — REST API integration
- Streamlit — Interactive dashboard
- Jupyter Notebook — Experimentation and reproducibility
- Pytest — Automated testing
- GitHub Actions — Continuous Integration

## Project Structure

```text
finsight-wealth-platform/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── api/
│
├── dashboard/
│
├── data/
│   ├── finsight_portfolio_data.csv
│   ├── finsight_risk_profiles.csv
│   └── finsight_market_signals.csv
│
├── docs/
│   ├── MODEL_CARD.md
│   ├── CHECKPOINT5_SUBMISSION.md
│   └── DEMO_SCRIPT.md
│
├── evidence/
│
├── load_testing/
│
├── notebooks/
│   ├── week6_core_model_experiments.ipynb
│   ├── checkpoint5_reproducibility.ipynb
│   └── experiment_results.csv
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data_loader.py
│   ├── optimizer.py
│   ├── risk_engine.py
│   └── experiment.py
│
├── tests/
│
├── run_optimization.py
├── risk_return_dashboard.png
├── RESEARCH.md
├── CHECKPOINT2_README.md
├── CHECKPOINT6_README.md
├── CHECKPOINT9_README.md
├── README_FINAL_PATCH.md
├── requirements.txt
├── requirements-week9.txt
└── README.md
```

## Core Features

- Modern Portfolio Theory-based portfolio optimization.
- Constrained maximum-Sharpe optimization using SciPy SLSQP.
- Three investor risk profiles: Conservative, Moderate, and Aggressive.
- Cash/debt allocation sleeve.
- Ledoit-Wolf covariance shrinkage.
- Return shrinkage experimentation.
- Walk-forward backtesting.
- MLflow experiment tracking.
- Expected return versus volatility visualization.
- FastAPI integration.
- Streamlit interactive dashboard.
- Automated testing and CI workflow.

## Setup

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run the baseline optimization:

```powershell
python run_optimization.py
```

## Checkpoint 3 — Core Model + Experimentation

The core model uses constrained maximum-Sharpe MPT optimization over eight equities and a cash/debt sleeve with an assumed annual return of 6%.

### Experiment configuration

- 12 hyperparameter configurations.
- 3 investor risk profiles.
- 36 MLflow experiment runs.
- Sample covariance versus Ledoit-Wolf covariance.
- Return shrinkage: 0, 0.5, and 1.0.
- Maximum individual stock weight: 0.25 and 0.40.
- Walk-forward evaluation: 90-day rolling fit and 21-day hold.
- Evaluation based on out-of-sample returns.

### Best configuration

- Covariance: Ledoit-Wolf
- Return shrinkage: 0.5
- Maximum stock weight: 0.40
- Mean out-of-sample Sharpe: -0.26
- Equal-weight baseline: -0.87

### Reported Portfolio Results

| Risk Profile | Equity | Cash | Expected Return | Volatility | Sharpe |
|---|---:|---:|---:|---:|---:|
| Conservative | 40% | 60% | 11.4% | 5.9% | 0.905 |
| Moderate | 70% | 30% | 15.4% | 10.4% | 0.905 |
| Aggressive | 84% | 16% | 17.3% | 12.5% | 0.905 |

These figures are historical model estimates, not guaranteed returns or realized investment performance.

### Known Limitations

- Only approximately 180 days of historical market observations.
- Negative out-of-sample Sharpe for the reported best configuration.
- Assumed 6% cash/debt return.
- Simplified investment universe.
- Transaction costs, taxes, liquidity, and market impact may not be fully represented.

The results indicate relative model performance over the selected test window, not a reliable future forecast.

## Checkpoint 4 — Integration + Testing

Checkpoint 4 integrates the portfolio optimization engine with the application layer.

Key components:

- FastAPI-based API layer.
- Streamlit interactive dashboard.
- Portfolio optimization endpoints.
- Risk-profile-based allocation outputs.
- Integration and automated testing.
- Load-testing infrastructure.

### Test Verification

Latest reported local test result:

```text
python -m pytest -q

...... [100%]

6 passed in 2.95s
```

## Checkpoint 5 — Final Demo + Model Card

Checkpoint 5 focuses on final documentation, reproducibility, and demonstration.

### Deliverables

**1. Model Card — `docs/MODEL_CARD.md`**

Documents:
- Intended use and model methodology.
- Dataset description.
- Reported evaluation metrics.
- Model limitations.
- Bias and fairness audit status.
- Monitoring strategy.
- Deployment considerations.

**2. Five-Minute Demo — `docs/DEMO_SCRIPT.md`**

Demonstrates:
- Project introduction.
- Investor inputs.
- Portfolio optimization.
- Risk-return visualization.
- Experiment results.
- API and dashboard integration.
- Model limitations.

**3. Submission Documentation — `docs/CHECKPOINT5_SUBMISSION.md`**

Contains the final submission summary and evidence checklist.

**4. Reproducibility Notebook**

`notebooks/checkpoint5_reproducibility.ipynb`

Provides diagnostic analysis of existing experiment results.

**5. Continuous Integration**

`.github/workflows/ci.yml`

Automates dependency installation and test execution through GitHub Actions.

### Required Final Evidence

- Five-minute live demonstration recording.
- Successful local test output.
- Passing GitHub Actions CI run.
- API and dashboard screenshots.
- Completed reproducibility notebook.
- Final GitHub repository and code submission.

## Running Experiments

Open:

```text
notebooks/week6_core_model_experiments.ipynb
```

Run all cells to reproduce the documented experiments.

Launch MLflow:

```powershell
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

Open:

```text
http://127.0.0.1:5000
```

Select the `finsight-week6-mpt` experiment.

## Automated Testing

Run the test suite:

```powershell
python -m pytest -q
```

Check code quality where Ruff is configured:

```powershell
ruff check .
```

## Author

**Siriyala Nishar**  
AI/ML Intern — Cynaris Solutions

## Disclaimer

FinSight Wealth Platform is an educational portfolio optimization prototype developed for internship learning and demonstration purposes. It is not financial advice, an investment recommendation, or a production-ready robo-advisory service.

All portfolio allocations and expected returns are illustrative and depend on historical market data, optimization constraints, and model assumptions. Production use would require additional validation, security, regulatory compliance, and qualified financial-risk review.
