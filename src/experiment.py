"""Week 6 - Core model + experimentation (FinSight MPT engine).

Primary model: constrained max-Sharpe Mean-Variance (MPT) optimizer with a
cash/debt sleeve so that each risk profile's min/max equity % can be honoured.
Hyperparameters tuned and compared via walk-forward (out-of-sample) backtest.
Experiments are logged to MLflow when available (falls back to CSV only).
"""
import itertools, json, os
import numpy as np, pandas as pd
from scipy.optimize import minimize
from sklearn.covariance import LedoitWolf

TRADING_DAYS = 252
RF = 0.06                      # assumed annual risk-free / debt-sleeve return (India T-bill proxy)
ASSETS = ["RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK", "WIPRO", "BAJFINANCE", "HCLTECH"]


# ------------------------------------------------------------------ data
def load_data(folder):
    px = pd.read_csv(os.path.join(folder, "finsight_portfolio_data.csv"), parse_dates=["date"]).set_index("date")
    prof = pd.read_csv(os.path.join(folder, "finsight_risk_profiles.csv"))
    prof["min_equity_pct"] = prof["min_equity_pct"].clip(0, 100)
    prof["max_equity_pct"] = prof["max_equity_pct"].clip(0, 100)   # raw data has 110% for very_aggressive
    rets = px[ASSETS].pct_change().dropna()
    bench = px["market_nifty50"].pct_change().dropna()
    return rets, bench, prof


# ------------------------------------------------------------------ estimators
def estimate(rets, cov_method="sample", ret_shrink=0.0):
    mu = rets.mean().values * TRADING_DAYS
    if ret_shrink > 0:                                   # James-Stein style pull toward cross-sectional mean
        mu = (1 - ret_shrink) * mu + ret_shrink * mu.mean()
    if cov_method == "ledoit_wolf":
        cov = LedoitWolf().fit(rets.values).covariance_ * TRADING_DAYS
    else:
        cov = rets.cov().values * TRADING_DAYS
    return mu, cov


# ------------------------------------------------------------------ optimizer
def optimize(mu, cov, min_eq, max_eq, max_w, risk_aversion=None):
    """Weights over [8 stocks + cash]. objective: max Sharpe (risk_aversion=None) or max mu - 0.5*lambda*var."""
    n = len(mu)
    mu_a = np.append(mu, RF)
    cov_a = np.zeros((n + 1, n + 1)); cov_a[:n, :n] = cov

    def neg_obj(w):
        r, v = w @ mu_a, np.sqrt(w @ cov_a @ w) + 1e-12
        return -(r - 0.5 * risk_aversion * v ** 2) if risk_aversion else -(r - RF) / v

    cons = [{"type": "eq", "fun": lambda w: w.sum() - 1},
            {"type": "ineq", "fun": lambda w: w[:n].sum() - min_eq},
            {"type": "ineq", "fun": lambda w: max_eq - w[:n].sum()}]
    bounds = [(0, max_w)] * n + [(0, 1)]
    best = None
    for seed in range(5):                                # multi-start: SLSQP is sensitive to init
        rng = np.random.default_rng(seed)
        w0 = rng.dirichlet(np.ones(n + 1))
        res = minimize(neg_obj, w0, method="SLSQP", bounds=bounds, constraints=cons)
        if res.success and (best is None or res.fun < best.fun):
            best = res
    return best.x


def perf(daily):
    ann_r = (1 + daily).prod() ** (TRADING_DAYS / len(daily)) - 1
    ann_v = daily.std() * np.sqrt(TRADING_DAYS)
    cum = (1 + daily).cumprod()
    mdd = (cum / cum.cummax() - 1).min()
    return dict(ann_return=ann_r, ann_vol=ann_v, sharpe=(ann_r - RF) / ann_v, max_drawdown=mdd)


# ------------------------------------------------------------------ walk-forward backtest
def walk_forward(rets, profile, cfg, train=90, step=21):
    cash_daily = (1 + RF) ** (1 / TRADING_DAYS) - 1
    out, weights = [], []
    for t in range(train, len(rets) - 1, step):
        window = rets.iloc[max(0, t - train): t] if cfg.get("rolling", True) else rets.iloc[:t]
        mu, cov = estimate(window, cfg["cov_method"], cfg["ret_shrink"])
        w = optimize(mu, cov, profile.min_equity_pct / 100, profile.max_equity_pct / 100,
                     cfg["max_weight"], cfg.get("risk_aversion"))
        weights.append(w)
        fwd = rets.iloc[t: t + step]
        out.append(fwd.values @ w[:-1] + w[-1] * cash_daily)
    daily = pd.Series(np.concatenate(out), index=rets.index[train: train + sum(len(o) for o in out)])
    return daily, np.mean(weights, axis=0)


def baseline_equal_weight(rets, profile, train=90):
    cash_daily = (1 + RF) ** (1 / TRADING_DAYS) - 1
    eq = (profile.min_equity_pct + profile.max_equity_pct) / 200
    d = rets.iloc[train:]
    return pd.Series(eq * d.mean(axis=1).values + (1 - eq) * cash_daily, index=d.index)


# ------------------------------------------------------------------ experiment grid
GRID = dict(cov_method=["sample", "ledoit_wolf"], ret_shrink=[0.0, 0.5, 1.0], max_weight=[0.25, 0.40])


def run_experiments(folder, profiles=("conservative", "moderate", "aggressive"), use_mlflow=True):
    rets, bench, prof = load_data(folder)
    try:
        import mlflow
        mlflow.set_experiment("finsight-week6-mpt") if use_mlflow else None
    except ImportError:
        mlflow, use_mlflow = None, False
    rows = []
    for p in profiles:
        pr = prof[prof.risk_appetite == p].iloc[0]
        base = perf(baseline_equal_weight(rets, pr))
        for i, vals in enumerate(itertools.product(*GRID.values())):
            cfg = dict(zip(GRID.keys(), vals))
            daily, w = walk_forward(rets, pr, cfg)
            m = perf(daily)
            row = dict(profile=p, run=i, **cfg, **m,
                       drawdown_ok=bool(abs(m["max_drawdown"]) * 100 <= pr.max_drawdown_pct),
                       baseline_sharpe=base["sharpe"], avg_equity=float(w[:-1].sum()))
            rows.append(row)
            if use_mlflow:
                with mlflow.start_run(run_name=f"{p}-cfg{i}"):
                    mlflow.log_params({"profile": p, **cfg, "rf": RF, "train_window": 90, "rebalance_days": 21})
                    mlflow.log_metrics({k: float(v) for k, v in m.items()} | {"baseline_sharpe": base["sharpe"]})
    return pd.DataFrame(rows), rets, prof
