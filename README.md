# FinSight Wealth Platform — Portfolio Optimization Engine

A portfolio optimization engine for a SEBI-registered robo-advisory
platform. Accepts a user's risk profile and capital amount, and returns
an optimized asset allocation using Modern Portfolio Theory (MPT), with
an interactive dashboard showing expected return vs. risk.

## Client
FinTech / Wealth Management, Mumbai — 60 employees, SEBI-registered.

## Project Status
🚧 In Progress — Checkpoint 1 (Research + Architecture Design)

## Tech Stack
- Python 3.11
- Pandas, NumPy, SciPy (optimization)
- FastAPI (API layer)
- Plotly/Streamlit (dashboard)
- Jupyter (documented notebook, final deliverable)

## Project Structure
```
finsight-wealth-platform/
├── data/              # raw and processed price/returns data
├── notebooks/         # exploration and final documented notebook
├── src/
│   ├── __init__.py
│   ├── config.py       # configuration (paths, risk thresholds)
│   ├── data_loader.py  # fetch/clean historical price data
│   ├── optimizer.py    # MPT mean-variance optimization logic
│   └── risk_engine.py  # maps risk profile -> constraints
├── tests/              # unit tests
├── RESEARCH.md         # Checkpoint 1 research + architecture doc
├── requirements.txt
└── README.md
```

## Setup
```bash
python -m venv venv
source venv/Scripts/activate      # Windows Git Bash
pip install -r requirements.txt
```

## Milestones
- [x] Checkpoint 1 (Wk 1) — Research + architecture design
- [ ] Checkpoint 2 (Wk 3) — Data pipeline + baseline model
- [ ] Checkpoint 3 (Wk 6) — Core model + experimentation
- [ ] Checkpoint 4 (Wk 9) — Integration + testing
- [ ] Checkpoint 5 (Wk 12) — Final demo + model card

See `RESEARCH.md` for the detailed architecture design and reference
papers reviewed for Checkpoint 1.

## Author
Siriyala Nishar — AI/ML Intern, Cynaris Solutions
