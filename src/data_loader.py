"""
Data loading and preprocessing for the FinSight portfolio optimizer.
To be implemented in Checkpoint 2.
"""

from pathlib import Path
import pandas as pd


def load_price_data(csv_path: Path) -> pd.DataFrame:
    """Load historical asset price data from CSV.

    Expected columns: date, asset_ticker, close_price
    Returns a wide-format DataFrame: index=date, columns=tickers.

    TODO (Checkpoint 2): implement loading from aiml_training_data.csv,
    handle missing dates/assets, pivot to wide format.
    """
    raise NotImplementedError("Implement in Checkpoint 2")


def compute_daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Convert a wide price DataFrame into daily percentage returns.

    TODO (Checkpoint 2): prices.pct_change().dropna()
    """
    raise NotImplementedError("Implement in Checkpoint 2")


def annualize_returns_and_covariance(
    daily_returns: pd.DataFrame,
) -> tuple[pd.Series, pd.DataFrame]:
    """Annualize mean daily returns and the covariance matrix.

    TODO (Checkpoint 2): mean * 252 trading days, cov * 252.
    """
    raise NotImplementedError("Implement in Checkpoint 2")
