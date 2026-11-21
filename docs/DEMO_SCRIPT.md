# FinSight — 5-Minute Final Demo Script

**Presenter:** Siriyala Nishar  
**Target length:** approximately 5 minutes  
**Important:** Use the actual running application and actual outputs. Do not read sample values as live results unless the application displays them.

## 0:00–0:35 — Introduction
"Hello, I'm Siriyala Nishar, an AI/ML Intern at Cynaris Solutions. This is FinSight Wealth Platform, a portfolio-optimization prototype for a wealth-management use case. It uses Modern Portfolio Theory to demonstrate risk-profile-based asset allocation."

## 0:35–1:15 — Problem and inputs
"The system takes an investor risk profile and capital amount. It supports Conservative, Moderate, and Aggressive profiles. The goal is to illustrate how portfolio constraints can change the allocation and the expected risk-return trade-off."

Show the dashboard input controls. Enter a demonstration capital amount and select each profile in turn. Use synthetic/demo inputs only; do not enter real personal financial information.

## 1:15–2:15 — Optimization engine
"At the core is a constrained maximum-Sharpe MPT optimizer. The project evaluates expected returns and covariance estimates, applies profile constraints, and includes a cash/debt sleeve in the Week 6 model. The optimizer uses SciPy's SLSQP method, as documented in the project."

Show the allocation output and, if available, the asset weights. Explain that weights are model outputs for the selected historical sample, not recommendations.

## 2:15–3:00 — Risk-return visualization
"Here the dashboard compares expected return and volatility. The chart helps explain the trade-off: higher expected return estimates generally come with higher estimated volatility. The Sharpe ratio summarizes estimated excess return per unit of volatility under the model assumptions."

Show the chart and point out the three profile markers/series if present.

## 3:00–3:45 — Experiments and evaluation
"The experiment work compared sample covariance with Ledoit–Wolf shrinkage, several return-shrinkage settings, and maximum-weight constraints. The repository records 36 MLflow runs across the three profiles. The documented evaluation uses a walk-forward setup, with a 90-day rolling fit and 21-day hold."

Show the experiment notebook or MLflow results. State clearly that the README reports a negative mean out-of-sample Sharpe for the best configuration versus the equal-weight baseline; this is an important limitation, not a result to hide.

## 3:45–4:30 — API, tests, and integration
"Checkpoint 4 integrated the model into a serving layer and dashboard, with integration and load testing documented in the project. I will show the actual API health/optimization endpoint and test output available in this environment."

Show only verified live endpoints and test output. Do not claim a concurrency result unless the load-test report displays the measured latency and throughput.

## 4:30–5:00 — Limitations and close
"This is an educational prototype, not financial advice. Its results depend on a short historical sample and simplifying assumptions, including the cash/debt return. A production system would need broader data, transaction-cost modelling, robust monitoring, security, suitability controls, and regulatory review. Thank you."

## Recording checklist
- [ ] Close unrelated windows and hide secrets/tokens.
- [ ] Use demo or synthetic capital inputs only.
- [ ] Start API and dashboard using the repository's actual documented commands.
- [ ] Show all three profiles.
- [ ] Show the risk-return chart and Sharpe ratio.
- [ ] Show experiment evidence and actual test output.
- [ ] Mention limitations and negative out-of-sample result.
- [ ] Keep the recording within five minutes.
