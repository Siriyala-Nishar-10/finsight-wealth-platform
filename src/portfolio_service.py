"""Serving adapter around the existing Week 6 MPT model.

Uses the selected Week 6 configuration:
Ledoit-Wolf covariance, 0.5 return shrinkage, 0.40 stock cap, 6% cash sleeve.
"""
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

from src.experiment import ASSETS, RF, estimate, load_data, optimize

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = Path(__import__("os").environ.get("FINSIGHT_DATA_DIR", PROJECT_ROOT / "data"))

BEST_CONFIG = {
    "cov_method": "ledoit_wolf",
    "ret_shrink": 0.5,
    "max_weight": 0.40,
}


@lru_cache(maxsize=2)
def _load_cached_data(data_dir: str):
    folder = Path(data_dir)
    required = [
        folder / "finsight_portfolio_data.csv",
        folder / "finsight_risk_profiles.csv",
    ]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        raise FileNotFoundError(
            "Required FinSight data files not found: " + ", ".join(missing)
        )
    returns, benchmark, profiles = load_data(str(folder))
    if len(returns) < 91:
        raise ValueError("At least 91 daily return observations are required.")
    return returns, profiles


def optimize_portfolio(risk_profile: str, capital: float, data_dir: Path = DATA_DIR):
    if capital <= 0:
        raise ValueError("capital must be greater than zero.")

    returns, profiles = _load_cached_data(str(Path(data_dir).resolve()))
    matching = profiles.loc[profiles["risk_appetite"].str.lower() == risk_profile.lower()]
    if matching.empty:
        raise ValueError(f"Risk profile '{risk_profile}' is not present in the risk-profile CSV.")

    profile = matching.iloc[0]
    mu, cov = estimate(
        returns[ASSETS],
        cov_method=BEST_CONFIG["cov_method"],
        ret_shrink=BEST_CONFIG["ret_shrink"],
    )

    min_equity = float(np.clip(profile["min_equity_pct"], 0, 100)) / 100
    max_equity = float(np.clip(profile["max_equity_pct"], 0, 100)) / 100

    if min_equity > max_equity:
        raise ValueError("Profile minimum equity allocation exceeds maximum equity allocation.")

    weights = optimize(
        mu,
        cov,
        min_eq=min_equity,
        max_eq=max_equity,
        max_w=BEST_CONFIG["max_weight"],
    )
    if weights is None or not np.isfinite(weights).all():
        raise RuntimeError("The optimizer did not find a valid solution.")

    weights = np.asarray(weights, dtype=float)
    if not np.isclose(weights.sum(), 1.0, atol=1e-5):
        raise RuntimeError("Optimizer returned weights that do not sum to 1.")

    stock_weights = weights[:-1]
    cash_weight = float(weights[-1])
    expected_return = float(stock_weights @ mu + cash_weight * RF)
    annualized_volatility = float(np.sqrt(stock_weights @ cov @ stock_weights))
    sharpe = (
        (expected_return - RF) / annualized_volatility
        if annualized_volatility > 1e-12
        else 0.0
    )

    allocation = {
        asset: {
            "weight": round(float(weight), 6),
            "weight_percent": round(float(weight * 100), 2),
            "amount_inr": round(float(weight * capital), 2),
        }
        for asset, weight in zip(ASSETS, stock_weights)
    }
    allocation["CASH_DEBT_SLEEVE"] = {
        "weight": round(cash_weight, 6),
        "weight_percent": round(cash_weight * 100, 2),
        "amount_inr": round(cash_weight * capital, 2),
        "assumed_annual_return": RF,
        "note": "Modelled cash/debt sleeve; not a sourced bond or deposit product.",
    }

    return {
        "risk_profile": risk_profile.lower(),
        "capital_inr": round(float(capital), 2),
        "allocation": allocation,
        "equity_allocation_percent": round(float(stock_weights.sum() * 100), 2),
        "cash_allocation_percent": round(cash_weight * 100, 2),
        "expected_annual_return": round(expected_return, 6),
        "expected_return_percent": round(expected_return * 100, 2),
        "annualized_volatility": round(annualized_volatility, 6),
        "volatility_percent": round(annualized_volatility * 100, 2),
        "sharpe_ratio": round(sharpe, 4),
        "profile_limits": {
            "min_equity_pct": round(min_equity * 100, 2),
            "max_equity_pct": round(max_equity * 100, 2),
            "max_drawdown_pct": float(profile["max_drawdown_pct"]),
            "target_expected_return_pct": float(profile["expected_return_pct"]),
        },
        "model_configuration": BEST_CONFIG,
        "risk_free_rate_assumption": RF,
        "disclaimer": (
            "Model estimates based on the supplied historical sample and stated "
            "assumptions. They are not guaranteed returns or investment advice."
        ),
    }
