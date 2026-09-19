"""
Maps a client risk profile row to portfolio optimization constraints.
"""

import pandas as pd


def get_risk_constraints(profile_row: pd.Series) -> dict:
    """Extract optimization constraints from a risk profile row.

    Returns min/max equity allocation (used to bound single-asset
    concentration) and the target expected return / max drawdown for
    reference against the optimized portfolio's actual results.
    """
    return {
        "risk_appetite": profile_row["risk_appetite"],
        "min_equity_pct": profile_row["min_equity_pct"],
        "max_equity_pct": profile_row["max_equity_pct"],
        "target_expected_return_pct": profile_row["expected_return_pct"],
        "max_drawdown_pct": profile_row["max_drawdown_pct"],
        "capital_inr": profile_row["capital_inr"],
        "investment_horizon_yrs": profile_row["investment_horizon_yrs"],
    }
