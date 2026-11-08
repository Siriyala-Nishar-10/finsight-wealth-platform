import os

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

st.set_page_config(page_title="FinSight Wealth", page_icon="💰", layout="wide")
st.title("💰 FinSight Wealth Platform")
st.caption("MPT portfolio optimization · Educational project demonstration")

api_url = os.getenv("FINSIGHT_API_URL", "http://127.0.0.1:8000")
profile = st.selectbox("Select your risk profile", ["conservative", "moderate", "aggressive"])
capital = st.number_input("Investment capital (INR)", min_value=1000.0, value=100000.0, step=5000.0)

if st.button("Optimize portfolio", type="primary"):
    try:
        response = requests.post(
            f"{api_url}/optimize",
            json={"capital": capital, "risk_profile": profile},
            timeout=60,
        )
        response.raise_for_status()
        result = response.json()
        st.session_state["portfolio_result"] = result
    except requests.RequestException as exc:
        st.error(f"Could not reach the optimization API: {exc}")

result = st.session_state.get("portfolio_result")
if result:
    st.subheader(f"Optimized portfolio — {result['risk_profile'].title()}")
    c1, c2, c3 = st.columns(3)
    c1.metric("Expected annual return", f"{result['expected_return_percent']:.2f}%")
    c2.metric("Annualized volatility", f"{result['volatility_percent']:.2f}%")
    c3.metric("Sharpe ratio", f"{result['sharpe_ratio']:.3f}")

    rows = []
    for asset, values in result["allocation"].items():
        rows.append({
            "Asset": asset.replace("_", " ").title(),
            "Allocation (%)": values["weight_percent"],
            "Amount (INR)": values["amount_inr"],
        })
    allocation_df = pd.DataFrame(rows)

    left, right = st.columns(2)
    with left:
        st.plotly_chart(
            px.pie(allocation_df, names="Asset", values="Allocation (%)",
                   title="Portfolio allocation", hole=0.35),
            use_container_width=True,
        )
    with right:
        st.plotly_chart(
            px.bar(allocation_df, x="Asset", y="Allocation (%)",
                   title="Asset weights", text_auto=".2f"),
            use_container_width=True,
        )

    st.subheader("Allocation details")
    st.dataframe(allocation_df, use_container_width=True, hide_index=True)
    st.caption(
        "The expected return and volatility are model estimates, not guarantees. "
        "The cash/debt sleeve uses an assumed 6% annual return."
    )
    st.download_button(
        "Download allocation CSV",
        allocation_df.to_csv(index=False).encode("utf-8"),
        file_name=f"finsight_{profile}_allocation.csv",
        mime="text/csv",
    )
