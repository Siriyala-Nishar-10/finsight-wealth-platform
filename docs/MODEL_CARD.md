# FinSight Wealth Platform — Model Card
**Version:** Checkpoint 5 documentation draft  
**Author:** Siriyala Nishar  
**Project:** Cynaris Solutions AI/ML Internship  
**Model family:** Constrained Modern Portfolio Theory (MPT), maximum-Sharpe optimization

## 1. Intended use
FinSight demonstrates portfolio-allocation research for three illustrative investor risk profiles (Conservative, Moderate, Aggressive). It accepts a capital amount and a risk profile and uses historical asset returns, covariance estimates, profile constraints, and a cash/debt sleeve to produce a candidate allocation.

**This is an educational project prototype, not an investment recommendation or a production robo-adviser.** It must not be used to make real investment decisions or promise returns.

## 2. Model and method
- Portfolio optimizer: constrained maximum-Sharpe MPT using SciPy SLSQP (as documented in the project README).
- Equity universe: RELIANCE, TCS, HDFCBANK, INFY, ICICIBANK, WIPRO, BAJFINANCE, HCLTECH.
- Cash/debt sleeve: assumed 6% annual return in the documented Week 6 experiment.
- Covariance options evaluated: sample covariance and Ledoit–Wolf shrinkage.
- Return shrinkage values evaluated: 0, 0.5, 1.0.
- Maximum individual stock weight values evaluated: 0.25 and 0.40.
- Experiment count reported: 12 configurations × 3 profiles = 36 MLflow runs.
- Evaluation approach reported: walk-forward backtest with a 90-day rolling fit and 21-day hold; scores use out-of-sample returns.

## 3. Data
The project README describes the supplied data pack as approximately 180 days of NSE price observations for eight equities plus Nifty 50, together with risk-profile and market-signal files.

Before any external or production use, document the exact source, retrieval date, licensing, missing-value handling, corporate-action treatment, trading-calendar alignment, and whether prices are adjusted. The short sample is not sufficient to establish stable long-term expected returns.

## 4. Reported evaluation
The following figures are transcribed from the repository README and are **not independently re-run as part of this documentation bundle**.

| Risk profile | Equity allocation | Cash allocation | Expected return | Volatility | Sharpe |
|---|---:|---:|---:|---:|---:|
| Conservative | 40% | 60% | 11.4% | 5.9% | 0.905 |
| Moderate | 70% | 30% | 15.4% | 10.4% | 0.905 |
| Aggressive | 84% | 16% | 17.3% | 12.5% | 0.905 |

The README also reports a best experiment configuration of Ledoit–Wolf covariance, 0.5 return shrinkage, and 0.40 maximum stock weight. Its mean out-of-sample Sharpe was reported as -0.26 versus -0.87 for the equal-weight baseline.

**Interpretation:** the reported negative out-of-sample Sharpe indicates that the tested strategy did not outperform the assumed cash return over that test window on a risk-adjusted basis. The positive profile-level Sharpe figures above are model estimates and should not be confused with realized out-of-sample performance.

## 5. Limitations and risks
- Only a short historical sample is described; estimates can be unstable and highly sensitive to the selected period.
- Historical returns and covariance do not guarantee future performance.
- The assumed 6% cash/debt return is a simplifying assumption, not a live risk-free rate.
- The documented universe is equity-heavy and does not represent a diversified investable universe across asset classes.
- Transaction costs, taxes, liquidity, slippage, market impact, rebalancing frequency, and changing correlations may not be fully represented.
- Optimizers can produce concentrated allocations and amplify estimation error.
- Risk-profile labels and constraints are simplified; they are not a substitute for a regulated suitability assessment.
- The project does not establish suitability for any individual investor.

## 6. Bias and fairness review
A formal demographic fairness audit is **not evidenced by the repository summary**. The optimizer uses portfolio and market inputs rather than demographic attributes, but this alone does not prove absence of disparate impact. Before production use:
1. Verify that protected or sensitive attributes are neither collected nor used unnecessarily.
2. Assess whether risk-profile mapping and product constraints create systematically different outcomes for user groups.
3. Test stability across market regimes, investment horizons, and capital ranges.
4. Have compliance and qualified financial-risk professionals review suitability, disclosures, and monitoring.
5. Record audit datasets, methodology, results, reviewer, and remediation.

## 7. Monitoring and operational controls
Monitor input-data freshness and completeness, optimizer convergence/failure rates, allocation constraint violations, concentration, turnover, realized versus expected volatility, realized versus expected returns, and out-of-sample risk-adjusted performance. Alert on stale data, missing assets, solver failures, extreme allocations, and sustained model drift. Maintain versioned datasets, configuration, model artifacts, and reproducible experiment logs.

## 8. Deployment and safe operation
Follow the repository's README for environment setup and the existing API/dashboard entry points. Run tests and smoke checks before deployment. Keep secrets in environment variables, validate all API inputs, apply authentication and rate limits where appropriate, and do not expose personal financial data in logs. A production release requires security, privacy, regulatory, and professional review beyond this internship project.

## 9. Change log
- Checkpoint 5: consolidated intended use, method, repository-reported metrics, limitations, fairness-audit status, monitoring, and deployment cautions.
