"""
Mean-Variance (MPT) portfolio optimization logic.
Maximizes Sharpe ratio subject to a risk profile's equity/volatility
constraints, using scipy.optimize.
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize


def _portfolio_performance(
    weights: np.ndarray, expected_returns: pd.Series, cov_matrix: pd.DataFrame
) -> tuple[float, float]:
    """Return (expected annual return, annual volatility) for given weights."""
    port_return = np.dot(weights, expected_returns)
    port_vol = np.sqrt(weights.T @ cov_matrix.values @ weights)
    return port_return, port_vol


def _negative_sharpe(
    weights: np.ndarray,
    expected_returns: pd.Series,
    cov_matrix: pd.DataFrame,
    risk_free_rate: float,
) -> float:
    """Objective function: negative Sharpe ratio (scipy minimizes)."""
    port_return, port_vol = _portfolio_performance(weights, expected_returns, cov_matrix)
    return -(port_return - risk_free_rate) / port_vol


def optimize_max_sharpe(
    expected_returns: pd.Series,
    cov_matrix: pd.DataFrame,
    risk_free_rate: float = 0.065,
    max_single_weight: float = 0.40,
) -> dict:
    """Find the portfolio weights that maximize the Sharpe ratio.

    Constraints: weights sum to 1 (fully invested), weights >= 0 (no
    short-selling), and no single asset exceeds max_single_weight
    (diversification requirement).
    """
    n = len(expected_returns)
    init_weights = np.repeat(1 / n, n)
    bounds = tuple((0, max_single_weight) for _ in range(n))
    constraints = ({"type": "eq", "fun": lambda w: np.sum(w) - 1},)

    result = minimize(
        _negative_sharpe,
        init_weights,
        args=(expected_returns, cov_matrix, risk_free_rate),
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
    )

    weights = result.x
    port_return, port_vol = _portfolio_performance(weights, expected_returns, cov_matrix)
    sharpe = (port_return - risk_free_rate) / port_vol

    return {
        "weights": dict(zip(expected_returns.index, weights.round(4))),
        "expected_return": round(port_return, 4),
        "volatility": round(port_vol, 4),
        "sharpe_ratio": round(sharpe, 4),
    }


def optimize_for_risk_profile(
    expected_returns: pd.Series,
    cov_matrix: pd.DataFrame,
    min_equity_pct: float,
    max_equity_pct: float,
    risk_free_rate: float = 0.065,
) -> dict:
    """Optimize a portfolio matching the risk profile's target volatility.

    KNOWN LIMITATION (documented for Checkpoint 2 baseline): min/max
    equity percentages describe portfolio-level equity allocation
    within a broader multi-asset-class product, not single-stock
    concentration limits. Since this dataset contains only equities,
    we approximate risk differentiation via a target-volatility
    constraint scaled from max_equity_pct: lower max_equity_pct implies
    a lower target volatility ceiling. This is a simplification to
    revisit in Checkpoint 3 once asset classes beyond equities
    (bonds/gold) are available to give min/max_equity_pct real meaning.
    """
    # Scale max_equity_pct (10-110 range in the data) to a target
    # volatility ceiling, roughly spanning conservative -> aggressive
    target_vol_ceiling = 0.08 + (max_equity_pct / 100) * 0.20

    n = len(expected_returns)
    init_weights = np.repeat(1 / n, n)
    bounds = tuple((0, 1) for _ in range(n))
    constraints = (
        {"type": "eq", "fun": lambda w: np.sum(w) - 1},
        {
            "type": "ineq",
            "fun": lambda w: target_vol_ceiling
            - np.sqrt(w.T @ cov_matrix.values @ w),
        },
    )

    result = minimize(
        _negative_sharpe,
        init_weights,
        args=(expected_returns, cov_matrix, risk_free_rate),
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
    )

    weights = result.x
    port_return, port_vol = _portfolio_performance(weights, expected_returns, cov_matrix)
    sharpe = (port_return - risk_free_rate) / port_vol

    return {
        "weights": dict(zip(expected_returns.index, weights.round(4))),
        "expected_return": round(port_return, 4),
        "volatility": round(port_vol, 4),
        "sharpe_ratio": round(sharpe, 4),
        "target_vol_ceiling": round(target_vol_ceiling, 4),
    }


def compute_efficient_frontier(
    expected_returns: pd.Series, cov_matrix: pd.DataFrame, n_points: int = 25
) -> pd.DataFrame:
    """Compute the efficient frontier: minimum-variance portfolio for
    a range of target returns, for the expected-return-vs-risk chart.
    """
    n = len(expected_returns)
    target_returns = np.linspace(expected_returns.min(), expected_returns.max(), n_points)
    frontier = []

    for target in target_returns:
        constraints = (
            {"type": "eq", "fun": lambda w: np.sum(w) - 1},
            {"type": "eq", "fun": lambda w, t=target: np.dot(w, expected_returns) - t},
        )
        bounds = tuple((0, 1) for _ in range(n))
        init_weights = np.repeat(1 / n, n)

        result = minimize(
            lambda w: np.sqrt(w.T @ cov_matrix.values @ w),
            init_weights,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
        )
        if result.success:
            frontier.append({"return": target, "volatility": result.fun})

    return pd.DataFrame(frontier)
