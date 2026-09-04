# Research + Architecture Design — FinSight Wealth Platform

## 1. Reference Papers / Repos Reviewed

### a) Modern Portfolio Theory (MPT) — Markowitz (1952), "Portfolio Selection"
The foundational paper behind mean-variance optimization. Key idea: for a
given level of risk (portfolio variance), there exists a portfolio
allocation that maximizes expected return — plotting these across risk
levels forms the "efficient frontier." This is the core theory this
project will implement.

### b) PyPortfolioOpt (open-source library, GitHub: robertmartin8/PyPortfolioOpt)
A well-documented Python library implementing MPT, Black-Litterman, and
risk models. Reviewed to understand standard implementation patterns:
covariance shrinkage (Ledoit-Wolf), the `EfficientFrontier` object
pattern, and how Sharpe ratio maximization is typically coded. Will use
this as a structural reference, not a dependency, since the task
requires building the optimization logic ourselves.

### c) "Deep Reinforcement Learning for Portfolio Management" (Jiang et al., 2017)
Explores an RL alternative to MPT — treating allocation as a sequential
decision problem with a policy network. Reviewed as the RL option
mentioned in the brief; noted for later comparison, but MPT is the
better starting point given the 12-week timeline and interpretability
requirements for a SEBI-registered advisory product (regulators prefer
explainable models over black-box RL policies).

## 2. Chosen Approach: MPT (Mean-Variance Optimization)

**Why MPT over RL for this project:**
- Faster to implement correctly within the milestone timeline
- Fully explainable — critical for a regulated wealth management client
- Sharpe ratio and efficient frontier are industry-standard, expected
  deliverables per the acceptance criteria
- RL noted as a possible Phase 2 extension, not required for MVP

## 3. Model Architecture

```
User Input (risk profile: Low/Medium/High, capital amount)
        │
        ▼
┌─────────────────────┐
│  Data Pipeline       │  Historical price data → daily returns →
│  (src/data_loader)   │  annualized expected returns + covariance matrix
└─────────┬────────────┘
          ▼
┌─────────────────────┐
│  Optimization Engine │  Mean-Variance Optimization (MPT)
│  (src/optimizer)     │  Maximize Sharpe Ratio subject to risk constraint
└─────────┬────────────┘
          ▼
┌─────────────────────┐
│  Risk Scoring        │  Map risk profile → target volatility band
│  (src/risk_engine)   │  Low: conservative allocation constraints
└─────────┬────────────┘  Medium/High: progressively looser constraints
          ▼
┌─────────────────────┐
│  Dashboard (FastAPI  │  Interactive: expected return vs. risk (volatility)
│  + Plotly/Streamlit) │  chart, allocation breakdown, Sharpe ratio display
└─────────────────────┘
```

## 4. Evaluation Metrics

- **Sharpe Ratio** — (expected portfolio return − risk-free rate) / portfolio
  volatility. Primary metric per acceptance criteria.
- **Expected Annual Return** — weighted sum of asset expected returns.
- **Portfolio Volatility (Std Dev)** — derived from the covariance matrix
  and allocation weights.
- **Diversification check** — no single asset should exceed a max weight
  threshold (avoids degenerate single-asset "optimal" portfolios).

## 5. Data Pipeline Skeleton

See `src/data_loader.py`, `src/optimizer.py`, `src/risk_engine.py` —
stub functions with type hints and docstrings, to be implemented in
Checkpoint 2 (Data pipeline + baseline model).

## 6. Tech Stack

- **Core:** Python 3.11, Pandas, NumPy
- **Optimization:** SciPy (`scipy.optimize`) for constrained mean-variance
  optimization
- **API:** FastAPI to serve optimization results
- **Dashboard:** Plotly/Streamlit for the interactive risk vs. return chart
- **Notebook:** Jupyter (documented, per acceptance criteria) for
  exploration and the final demo notebook

## Author
Siriyala Nishar — AI/ML Intern, Cynaris Solutions
