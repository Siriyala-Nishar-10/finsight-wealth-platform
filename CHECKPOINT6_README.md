# Checkpoint 3 — Core Model + Experimentation

## What This Does

Upgrades the Checkpoint 2 baseline into the core model and tests it
properly: a constrained max-Sharpe MPT optimizer with a cash/debt sleeve,
tuned over 12 hyperparameter configurations per risk profile (36 runs
logged with MLflow) and scored with a walk-forward (out-of-sample)
backtest instead of in-sample fit.

## Run

```bash
source venv/Scripts/activate
pip install pandas numpy scipy scikit-learn matplotlib mlflow jupyter
cd notebooks
# open week6_core_model_experiments.ipynb and Run All, then:
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

Open http://127.0.0.1:5000 and select the `finsight-week6-mpt` experiment
(Model training view). Screenshots are saved in `docs/`.

## Data

Same data pack as Checkpoint 2:

- `data/finsight_portfolio_data.csv` — 180 trading days (Jan–Sep 2025)
  of closing prices for 8 NSE stocks + Nifty 50 benchmark.
- `data/finsight_risk_profiles.csv` — risk archetypes with capital, equity
  bounds, target return and max drawdown. Only the 3 profiles in the brief
  (conservative, moderate, aggressive) are optimized.

## Model

Constrained max-Sharpe mean-variance optimizer (scipy SLSQP, 5 random
starts) over 8 stocks + a cash/debt sleeve earning an assumed 6% p.a.
Weights sum to 1, each stock is capped at `max_weight`, and total equity
must lie within the profile's `min_equity_pct` and `max_equity_pct`.

## Experiments

12 configurations x 3 risk profiles = 36 MLflow runs.

| Hyperparameter | Values              | Why                                                                                          |
| -------------- | ------------------- | -------------------------------------------------------------------------------------------- |
| `cov_method`   | sample, ledoit_wolf | 180 daily points for 8 assets: sample covariance is noisy                                    |
| `ret_shrink`   | 0, 0.5, 1.0         | mean returns over ~9 months are very noisy (1.0 = every stock gets the same expected return) |
| `max_weight`   | 0.25, 0.40          | single-stock concentration cap                                                               |

**Evaluation:** walk-forward backtest. Fit on a rolling 90-day window,
hold 21 trading days, roll forward. Only out-of-sample returns are scored.
Baseline = equal-weight stocks at the mid-point equity %, remainder in cash.

## Results Summary

Mean out-of-sample Sharpe across the 3 profiles (higher is better):

| cov_method            | ret_shrink | max_weight | OOS Sharpe     |
| --------------------- | ---------- | ---------- | -------------- |
| **ledoit_wolf**       | **0.5**    | **0.40**   | **-0.258**     |
| ledoit_wolf           | 0.0        | 0.40       | -0.299         |
| ledoit_wolf           | 0.0        | 0.25       | -0.306         |
| ledoit_wolf           | 0.5        | 0.25       | -0.325         |
| ledoit_wolf           | 1.0        | 0.40       | -0.553         |
| sample                | 0.0        | 0.40       | -0.655         |
| sample                | 1.0        | 0.25       | -1.398 (worst) |
| equal-weight baseline | —          | —          | -0.871         |

**Best configuration:** Ledoit-Wolf covariance, return shrinkage 0.5, max
weight 0.40. Best single runs: conservative -0.225, moderate -0.247.

Average effect of each hyperparameter (OOS Sharpe):

| Setting                  | Mean OOS Sharpe          |
| ------------------------ | ------------------------ |
| ledoit_wolf vs sample    | -0.487 vs -0.860         |
| ret_shrink 0 / 0.5 / 1.0 | -0.492 / -0.516 / -1.013 |
| max_weight 0.25 vs 0.40  | -0.784 vs -0.563         |

### Final portfolios (best config, fit on full sample)

| Risk Profile | Equity | Cash | Expected Return | Volatility | Sharpe |
| ------------ | ------ | ---- | --------------- | ---------- | ------ |
| Conservative | 40%    | 60%  | 11.4%           | 5.9%       | 0.905  |
| Moderate     | 70%    | 30%  | 15.4%           | 10.4%      | 0.905  |
| Aggressive   | 84%    | 16%  | 17.3%           | 12.5%      | 0.905  |

**Stock weights (% of total portfolio):**

| Profile      | INFY  | ICICIBANK | HCLTECH | Cash  |
| ------------ | ----- | --------- | ------- | ----- |
| Conservative | 15.1% | 19.0%     | 5.9%    | 60.0% |
| Moderate     | 26.3% | 33.2%     | 10.4%   | 30.1% |
| Aggressive   | 31.8% | 40.0%     | 12.5%   | 15.7% |

## Important, Honest Findings

**1. The profiles now produce different portfolios (Checkpoint 2 issue fixed).**
The cash sleeve gives the optimizer a lower-risk asset, so `min_equity_pct`
and `max_equity_pct` now bind. Every profile holds the same stock mix
(INFY / ICICIBANK / HCLTECH) and differs in how much sits in cash, which is
why the Sharpe is the same (0.905) across profiles. For the aggressive
profile, ICICIBANK hits the 40% single-stock cap, so equity stops at 84%
even though the profile allows up to 95%.

**2. Return shrinkage fixes the unrealistic returns from Checkpoint 2.**
Checkpoint 2 showed 32.89% expected return and Sharpe 1.708 from raw
9-month means. With shrinkage, expected returns drop to 11–17% and the
in-sample Sharpe to 0.905. The lower number is more realistic, not worse.

**3. Out-of-sample Sharpe is negative for every configuration.**
In the test window, stock returns were below the 6% cash rate, so every
config scores below zero. The ranking still matters: the best config
(-0.258) is far better than the equal-weight baseline (-0.871), and
Ledoit-Wolf beat the sample covariance in every profile. The in-sample 0.905
should not be read as a forecast.

**4. Short history limits the evidence.**
About 8 months of data gives roughly 4 rebalances in the test period. The
results show relative ranking of configurations, not expected future returns.

**5. Data issues handled.**
`very_aggressive` has `max_equity_pct = 110` in the raw CSV, which is
clipped to 100%. All 8 tickers are equities, so the cash sleeve (6% p.a.,
an assumption) is what lets the equity bounds work. The conservative
profile's 2.5% max-drawdown target is very tight; 30 of the 36 runs stayed
within their profile's limit, and the best config met it in all 3 profiles.

## What's Implemented

- `src/experiment.py` — estimators (sample / Ledoit-Wolf, return
  shrinkage), constrained max-Sharpe optimizer with cash sleeve,
  walk-forward backtest, baseline, experiment grid with MLflow logging
- `notebooks/week6_core_model_experiments.ipynb` — documented notebook:
  setup, experiments, hyperparameter analysis, final portfolios, INR
  allocation per profile
- `docs/` — MLflow runs table and run-comparison screenshots

## Output

- `notebooks/experiment_results.csv` — all 36 runs with params and metrics
- MLflow experiment `finsight-week6-mpt` (stored in `notebooks/mlflow.db`,
  not committed)
- `docs/` screenshots as evidence

## Next Steps (Checkpoint 4)

- Add bonds and a gold ETF so the non-equity part is a real asset class
  rather than a flat 6% cash assumption
- Extend price history to several years for a longer, more reliable
  walk-forward test
- Build the FastAPI endpoint (risk profile + capital in, allocation in INR
  out) and the interactive Plotly/Streamlit dashboard
- Integration tests and unit tests for the optimizer constraints

## Author

Siriyala Nishar
