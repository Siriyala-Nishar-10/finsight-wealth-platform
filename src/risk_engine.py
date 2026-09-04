"""
Maps a user's risk profile (Low/Medium/High) to portfolio constraints.
To be implemented in Checkpoint 2/3.
"""

from enum import Enum


class RiskProfile(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


def get_risk_constraints(profile: RiskProfile) -> dict:
    """Return target volatility band and max single-asset weight
    for a given risk profile.

    TODO (Checkpoint 2): define actual thresholds, e.g.:
    LOW    -> max_volatility=0.10, max_single_weight=0.20
    MEDIUM -> max_volatility=0.18, max_single_weight=0.35
    HIGH   -> max_volatility=0.30, max_single_weight=0.50
    """
    raise NotImplementedError("Implement in Checkpoint 2")
