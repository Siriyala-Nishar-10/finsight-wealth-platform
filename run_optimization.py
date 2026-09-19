"""
FinSight Wealth Platform — Checkpoint 2
Portfolio optimization for 3 risk profiles using real NSE stock data.

Author: Siriyala Nishar
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import matplotlib.pyplot as plt
from data_loader import (
    load_price_data, compute_daily_returns,
    annualize_returns_and_covariance, load_risk_profiles,
)
from optimizer import optimize_for_risk_profile, compute_efficient_frontier
from risk_engine import get_risk_constraints


def main():
    data_dir = Path(__file__).parent / "data"

    prices = load_price_data(data_dir / "finsight_portfolio_data.csv")
    # exclude the market benchmark from the investable asset universe
    asset_prices = prices.drop(columns=["market_nifty50"])
    print(f"Loaded {asset_prices.shape[0]} trading days for {asset_prices.shape[1]} assets")

    daily_returns = compute_daily_returns(asset_prices)
    expected_returns, cov_matrix = annualize_returns_and_covariance(daily_returns)

    print("\nAnnualized expected returns:")
    print(expected_returns.round(4))

    risk_profiles = load_risk_profiles(data_dir / "finsight_risk_profiles.csv")
    print(f"\nLoaded {len(risk_profiles)} risk profiles")

    # Run optimization for 3 risk profiles (conservative, moderate, aggressive)
    selected_profiles = risk_profiles[
        risk_profiles["risk_appetite"].isin(["conservative", "moderate", "aggressive"])
    ]

    results = {}
    print("\n" + "=" * 60)
    for _, profile in selected_profiles.iterrows():
        constraints = get_risk_constraints(profile)
        result = optimize_for_risk_profile(
            expected_returns, cov_matrix,
            constraints["min_equity_pct"], constraints["max_equity_pct"],
        )
        results[constraints["risk_appetite"]] = result

        print(f"\nRisk Profile: {constraints['risk_appetite'].upper()}")
        print(f"  Capital: Rs {constraints['capital_inr']:,.0f}")
        print(f"  Target expected return: {constraints['target_expected_return_pct']}%")
        print(f"  Optimized expected return: {result['expected_return']*100:.2f}%")
        print(f"  Optimized volatility: {result['volatility']*100:.2f}%")
        print(f"  Sharpe ratio: {result['sharpe_ratio']:.3f}")
        print(f"  Allocation:")
        for asset, weight in sorted(result["weights"].items(), key=lambda x: -x[1]):
            if weight > 0.001:
                print(f"    {asset}: {weight*100:.1f}%")

    # Dashboard: expected return vs risk chart for all 3 profiles + efficient frontier
    frontier = compute_efficient_frontier(expected_returns, cov_matrix)

    plt.figure(figsize=(9, 6))
    plt.plot(frontier["volatility"] * 100, frontier["return"] * 100, "b--",
             label="Efficient Frontier", alpha=0.6)

    colors = {"conservative": "green", "moderate": "orange", "aggressive": "red"}
    for profile_name, result in results.items():
        plt.scatter(
            result["volatility"] * 100, result["expected_return"] * 100,
            s=150, color=colors[profile_name], label=profile_name.capitalize(),
            edgecolors="black", zorder=5,
        )

    plt.xlabel("Volatility / Risk (%)")
    plt.ylabel("Expected Annual Return (%)")
    plt.title("Risk Scoring Dashboard: Expected Return vs Risk")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(Path(__file__).parent / "risk_return_dashboard.png", dpi=120)
    plt.close()
    print("\nSaved risk_return_dashboard.png")

    print("\n" + "=" * 60)
    print("Checkpoint 2 baseline complete: portfolios optimized for 3 risk")
    print("profiles, Sharpe ratios computed, dashboard chart generated.")


if __name__ == "__main__":
    main()
