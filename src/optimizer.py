"""
Mean-Variance (MPT) portfolio optimization logic.
To be implemented in Checkpoint 3 (Core model + experimentation).
"""

import pandas as pd


def optimize_max_sharpe(
    expected_returns: pd.Series,
    cov_matrix: pd.DataFrame,
    risk_free_rate: float = 0.06,
) -> dict:
    """Find the portfolio weights that maximize the Sharpe ratio.

    Uses scipy.optimize.minimize with constraints: weights sum to 1,
    weights >= 0 (no short-selling), subject to risk profile bounds
    applied via risk_engine.

    TODO (Checkpoint 3): implement using scipy.optimize.minimize,
    negative Sharpe as the objective function to minimize.

    Returns: {"weights": {ticker: weight}, "expected_return": float,
              "volatility": float, "sharpe_ratio": float}
    """
    raise NotImplementedError("Implement in Checkpoint 3")


def compute_efficient_frontier(
    expected_returns: pd.Series,
    cov_matrix: pd.DataFrame,
    n_points: int = 50,
) -> pd.DataFrame:
    """Compute the efficient frontier for the return vs. risk chart.

    TODO (Checkpoint 3): for a range of target returns, find the
    minimum-variance portfolio at each — used for the dashboard chart.
    """
    raise NotImplementedError("Implement in Checkpoint 3")
