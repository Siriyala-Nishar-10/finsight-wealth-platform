# FinSight Wealth Platform — Portfolio Optimization Engine
 
A portfolio optimization engine for a SEBI-registered robo-advisory
platform. Accepts a user's risk profile and capital amount, and returns
an optimized asset allocation using Modern Portfolio Theory (MPT), with
an interactive dashboard showing expected return vs. risk.
 
## Client
FinTech / Wealth Management, Mumbai — 60 employees, SEBI-registered.
 
## Project Status
🚧 In Progress — Checkpoint 2 (Data Pipeline + Baseline Model) complete
 
## Tech Stack
- Python 3.14
- Pandas, NumPy, SciPy (optimization)
- Matplotlib (dashboard chart)
- FastAPI (API layer — Checkpoint 4)
- Streamlit (interactive dashboard — Checkpoint 4)
- Jupyter (documented notebook — Checkpoint 5)
## Project Structure
```
finsight-wealth-platform/
├── data/
│   ├── finsight_portfolio_data.csv   # 180 days NSE prices (8 stocks + Nifty50)
│   └── finsight_risk_profiles.csv    # 4 investor risk archetypes
├── notebooks/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data_loader.py    # loads prices, computes returns/covariance
│   ├── optimizer.py      # MPT max-Sharpe optimization (scipy SLSQP)
│   └── risk_engine.py    # maps risk profile → constraints
├── tests/
├── run_optimization.py       # main script — runs pipeline for 3 profiles
├── risk_return_dashboard.png # expected return vs risk chart
├── RESEARCH.md               # Checkpoint 1 research + architecture
├── CHECKPOINT2_README.md     # Checkpoint 2 results + honest findings
├── requirements.txt
└── README.md
```
 
## Setup
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows PowerShell
pip install -r requirements.txt
python run_optimization.py
```
 
## Checkpoint 2 Results (Baseline Model)
- **Assets:** RELIANCE, TCS, HDFCBANK, INFY, ICICIBANK, WIPRO, BAJFINANCE, HCLTECH
- **Sharpe Ratio:** 1.708
- **Optimal Allocation:** ICICIBANK 44.4%, INFY 42.2%, HCLTECH 13.5%
- **Known limitations documented:** short 180-day sample inflates expected
  returns; all 3 risk profiles converge since equity-only universe has
  no lower-risk asset class yet — see `CHECKPOINT2_README.md`
## Milestones
- [x] Checkpoint 1 (Wk 1) — Research + architecture design
- [x] Checkpoint 2 (Wk 3) — Data pipeline + baseline model
- [ ] Checkpoint 3 (Wk 6) — Core model + experimentation
- [ ] Checkpoint 4 (Wk 9) — Integration + testing
- [ ] Checkpoint 5 (Wk 12) — Final demo + model card
## Author
Siriyala Nishar — AI/ML Intern, Cynaris Solutions
 
