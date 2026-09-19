"""
Data loading and preprocessing for the FinSight portfolio optimizer.
Uses real client-provided NSE price data (finsight_portfolio_data.csv).
"""

from pathlib import Path
import pandas as pd

TRADING_DAYS_PER_YEAR = 252


def load_price_data(csv_path: Path) -> pd.DataFrame:
    """Load historical asset price data from CSV.

    Expects a wide-format CSV: first column 'date', remaining columns
    are ticker prices (one column per asset, including the market
    benchmark 'market_nifty50').
    """
    df = pd.read_csv(csv_path, parse_dates=["date"], index_col="date")
    return df


def compute_daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Convert a wide price DataFrame into daily percentage returns."""
    return prices.pct_change().dropna()


def annualize_returns_and_covariance(
    daily_returns: pd.DataFrame,
) -> tuple[pd.Series, pd.DataFrame]:
    """Annualize mean daily returns and the covariance matrix.

    Note: only 180 trading days (~9 months) of history are available,
    so these are short-sample estimates — a real production system
    would use several years of history for more stable estimates.
    """
    annual_returns = daily_returns.mean() * TRADING_DAYS_PER_YEAR
    annual_cov = daily_returns.cov() * TRADING_DAYS_PER_YEAR
    return annual_returns, annual_cov


def load_risk_profiles(csv_path: Path) -> pd.DataFrame:
    """Load the client's 4 investor risk archetypes."""
    return pd.read_csv(csv_path)
