# Checkpoint 2 — Data Pipeline + Baseline Model

## What This Does

Implements the full data pipeline and MPT optimization engine using
real client-provided NSE price data: loads prices, computes annualized
returns/covariance, optimizes max-Sharpe portfolios for 3 risk
profiles, and generates the risk-scoring dashboard (expected return
vs. risk chart with efficient frontier).

## Run

```bash
python -m venv venv
source venv/Scripts/activate
pip install pandas numpy scipy matplotlib
python run_optimization.py
```

## Data

- `data/finsight_portfolio_data.csv` — 180 trading days (Jan–Sep 2025)
  of closing prices for 8 NSE stocks (RELIANCE, TCS, HDFCBANK, INFY,
  ICICIBANK, WIPRO, BAJFINANCE, HCLTECH) + Nifty 50 benchmark.
- `data/finsight_risk_profiles.csv` — 4 investor risk archetypes with
  capital, equity allocation bounds, target return, and max drawdown.

## Results Summary

| Risk Profile | Target Return | Optimized Return | Volatility | Sharpe |
| ------------ | ------------- | ---------------- | ---------- | ------ |
| Conservative | 7.5%          | 32.89%           | 15.45%     | 1.708  |
| Moderate     | 9.0%          | 32.89%           | 15.45%     | 1.708  |
| Aggressive   | 10.2%         | 32.89%           | 15.45%     | 1.708  |

**Allocation (all 3 profiles):** ICICIBANK 44.4%, INFY 42.2%, HCLTECH 13.5%

## Important, Honest Findings (Not Bugs — Documented Limitations)

**1. All 3 risk profiles converge to the same portfolio.**
This is an explainable, correct result given the constraints, not an
error: the unconstrained max-Sharpe portfolio's volatility (15.45%)
falls _below_ even the conservative profile's target volatility
ceiling (~16%, derived from its max_equity_pct). Since the same
optimal portfolio already satisfies all three profiles' risk
tolerances, the optimizer correctly returns it for each. This will
naturally differentiate once non-equity asset classes (bonds, gold)
are added in a later checkpoint, giving the risk profiles' equity
allocation bounds real meaning — right now the investable universe is
100% equities, so there's no lower-risk alternative to allocate into.

**2. Expected returns (32%+ annualized) are unrealistically high.**
This comes from annualizing daily returns estimated over only 180
trading days (~9 months) — a genuinely short, noisy sample. A few
strong months for ICICIBANK/INFY get amplified ×252 into an annual
figure that overstates realistic long-term expectations. A production
system would use multiple years of history, or apply return
shrinkage, to produce more stable estimates. Documented here rather
than silently presented as reliable.

**3. `min_equity_pct` from the risk profile data is not yet used.**
Only `max_equity_pct` currently drives the volatility ceiling. Since
the investable universe is equity-only, a minimum equity floor has no
binding effect yet — will become relevant once bonds/gold are added.

## What's Implemented

- `src/data_loader.py` — loads prices, computes returns, annualizes
  returns/covariance, loads risk profiles
- `src/optimizer.py` — max-Sharpe optimization (scipy SLSQP),
  volatility-constrained optimization per risk profile, efficient
  frontier computation
- `src/risk_engine.py` — extracts constraints from a risk profile row
- `run_optimization.py` — ties it together, runs for 3 profiles,
  generates the dashboard chart

## Output

- `risk_return_dashboard.png` — expected return vs. risk chart with
  efficient frontier and all 3 risk profile portfolios marked

## Next Steps (Checkpoint 3)

- Source additional asset classes (government bonds, gold ETF) to
  give risk profile constraints real differentiating power
- Extend price history beyond 180 days for more stable return
  estimates, or apply shrinkage estimators (e.g. Ledoit-Wolf)
- Build the FastAPI endpoint and interactive dashboard (Plotly/Streamlit)

## Author

Siriyala Nishar
