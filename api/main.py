from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.portfolio_service import optimize_portfolio

app = FastAPI(
    title="FinSight Wealth Platform API",
    description="MPT portfolio optimization using the Week 6 best configuration.",
    version="1.0.0",
)

RiskProfile = Literal["conservative", "moderate", "aggressive"]


class OptimizeRequest(BaseModel):
    capital: float = Field(gt=0, description="Investment capital in INR")
    risk_profile: RiskProfile


@app.get("/")
def health():
    return {"status": "ok", "service": "FinSight Portfolio Optimization API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/optimize")
def optimize(request: OptimizeRequest):
    try:
        return optimize_portfolio(
            risk_profile=request.risk_profile,
            capital=request.capital,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/risk-score")
def risk_score(request: OptimizeRequest):
    try:
        result = optimize_portfolio(
            risk_profile=request.risk_profile,
            capital=request.capital,
        )
        return {
            "risk_profile": result["risk_profile"],
            "annualized_volatility": result["annualized_volatility"],
            "volatility_percent": result["volatility_percent"],
            "max_drawdown_limit_percent": result["profile_limits"]["max_drawdown_pct"],
            "interpretation": (
                "Volatility is the model's annualized standard-deviation estimate; "
                "it is not a probability of loss or a guaranteed maximum drawdown."
            ),
        }
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/portfolio/{risk_profile}")
def portfolio_by_profile(risk_profile: RiskProfile, capital: float = 100000):
    try:
        return optimize_portfolio(risk_profile=risk_profile, capital=capital)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
