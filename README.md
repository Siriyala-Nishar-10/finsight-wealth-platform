# FinSight Wealth Platform — Portfolio Optimization Engine
 
A portfolio optimization engine for a SEBI-registered robo-advisory
platform. Accepts a user's risk profile and capital amount, and returns
an optimized asset allocation using Modern Portfolio Theory (MPT), with
an interactive dashboard showing expected return vs. risk.
 
## Client
FinTech / Wealth Management, Mumbai — 60 employees, SEBI-registered.
 
## Project Status
🚧 In Progress — Checkpoint 3 (Core Model + Experimentation) complete
 
## Tech Stack
- Python 3.14
- Pandas, NumPy, SciPy (optimization)
- scikit-learn (Ledoit-Wolf covariance shrinkage)
- MLflow (experiment tracking)
- Matplotlib (dashboard chart)
- FastAPI (API layer — Checkpoint 4)
- Streamlit (interactive dashboard — Checkpoint 4)
- Jupyter (experiment notebook — Checkpoint 3, final documented notebook — Checkpoint 5)
## Project Structure
```
finsight-wealth-platform/
├── data/
│   ├── finsight_portfolio_data.csv   # 180 days NSE prices (8 stocks + Nifty50)
│   ├── finsight_risk_profiles.csv    # 4 investor risk archetypes
│   └── finsight_market_signals.csv   # market signals data pack
├── notebooks/
│   ├── week6_core_model_experiments.ipynb  # Checkpoint 3 experiments + MLflow logging
│   └── experiment_results.csv              # all 36 runs (params + metrics)
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data_loader.py    # loads prices, computes returns/covariance
│   ├── optimizer.py      # MPT max-Sharpe optimization (scipy SLSQP)
│   ├── risk_engine.py    # maps risk profile → constraints
│   └── experiment.py     # Checkpoint 3: core model, walk-forward backtest, MLflow experiments
├── tests/
├── run_optimization.py       # Checkpoint 2 script — runs pipeline for 3 profiles
├── risk_return_dashboard.png # expected return vs risk chart
├── RESEARCH.md               # Checkpoint 1 research + architecture
├── CHECKPOINT2_README.md     # Checkpoint 2 results + honest findings
├── CHECKPOINT6_README.md     # Checkpoint 3 (Week 6) results + honest findings
├── requirements.txt
└── README.md
```
 
## Setup
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows PowerShell
pip install -r requirements.txt
python run_optimization.py    # Checkpoint 2 baseline
```

To reproduce Checkpoint 3 (experiments):
```bash
cd notebooks
# open week6_core_model_experiments.ipynb in VS Code and Run All, then:
mlflow ui --backend-store-uri sqlite:///mlflow.db
```
Open http://127.0.0.1:5000, switch to **Model training**, and select the
`finsight-week6-mpt` experiment.
 
## Checkpoint 2 Results (Baseline Model)
- **Assets:** RELIANCE, TCS, HDFCBANK, INFY, ICICIBANK, WIPRO, BAJFINANCE, HCLTECH
- **Sharpe Ratio:** 1.708
- **Optimal Allocation:** ICICIBANK 44.4%, INFY 42.2%, HCLTECH 13.5%
- **Known limitations documented:** short 180-day sample inflates expected
  returns; all 3 risk profiles converge since equity-only universe has
  no lower-risk asset class yet — see `CHECKPOINT2_README.md`

## Checkpoint 3 Results (Core Model + Experimentation)
- **Model:** constrained max-Sharpe MPT optimizer over the 8 stocks plus a
  cash/debt sleeve (assumed 6% p.a.), honouring each profile's min/max equity %
- **Experiments:** 12 hyperparameter configs x 3 risk profiles = 36 MLflow runs
  (covariance: sample vs Ledoit-Wolf; return shrinkage: 0 / 0.5 / 1.0;
  max stock weight: 0.25 / 0.40)
- **Evaluation:** walk-forward backtest (90-day rolling fit, 21-day hold),
  scored on out-of-sample returns only
- **Best config:** Ledoit-Wolf covariance, return shrinkage 0.5, max weight 0.40
  — mean out-of-sample Sharpe -0.26 vs -0.87 for the equal-weight baseline

| Risk Profile | Equity | Cash | Expected Return | Volatility | Sharpe |
| ------------ | ------ | ---- | --------------- | ---------- | ------ |
| Conservative | 40%    | 60%  | 11.4%           | 5.9%       | 0.905  |
| Moderate     | 70%    | 30%  | 15.4%           | 10.4%      | 0.905  |
| Aggressive   | 84%    | 16%  | 17.3%           | 12.5%      | 0.905  |

- **Fixed from Checkpoint 2:** profiles now produce different portfolios (the
  cash sleeve makes the equity bounds bind), and return shrinkage brings
  expected returns down from 32% to a more realistic 11–17%
- **Known limitations documented:** out-of-sample Sharpe is negative for every
  config (test-window stock returns were below the 6% cash rate); only about
  8 months of data, so results show relative ranking of configs, not a
  forecast — see `CHECKPOINT6_README.md`
## Milestones
- [x] Checkpoint 1 (Wk 1) — Research + architecture design
- [x] Checkpoint 2 (Wk 3) — Data pipeline + baseline model
- [x] Checkpoint 3 (Wk 6) — Core model + experimentation
- [ ] Checkpoint 4 (Wk 9) — Integration + testing
- [ ] Checkpoint 5 (Wk 12) — Final demo + model card
## Author
Siriyala Nishar — AI/ML Intern, Cynaris Solutions
