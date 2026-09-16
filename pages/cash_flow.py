"""Cash flow forecast page."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from services.cashflow_service import forecast_cashflow, get_monthly_cashflow
from utils.formatters import format_gbp


def render_cash_flow_page() -> None:
    """Render cash flow and projections page."""
    st.title("Cash Flow Forecast")

    cashflow_df = get_monthly_cashflow()
    if cashflow_df.empty:
        st.info("No transactions yet. Add transaction data to generate forecasts.")
        return

    st.subheader("Historical Cash Flow")
    st.dataframe(cashflow_df, use_container_width=True)

    horizon = st.selectbox("Projection horizon", [3, 6, 12], index=0)
    projection_df = forecast_cashflow(cashflow_df, horizon)

    combined = pd.concat([cashflow_df.assign(data_type="Historical"), projection_df.assign(data_type="Forecast")], ignore_index=True)
    chart_df = combined.melt(
        id_vars=["month", "data_type"],
        value_vars=["income", "expenses", "savings"],
        var_name="metric",
        value_name="amount",
    )

    fig = px.line(
        chart_df,
        x="month",
        y="amount",
        color="metric",
        line_dash="data_type",
        title=f"{horizon}-Month Cash Flow Projection",
    )
    st.plotly_chart(fig, use_container_width=True)

    if not projection_df.empty:
        final_month = projection_df.iloc[-1]
        c1, c2, c3 = st.columns(3)
        c1.metric("Projected Income", format_gbp(float(final_month["income"])))
        c2.metric("Projected Expenses", format_gbp(float(final_month["expenses"])))
        c3.metric("Projected Savings", format_gbp(float(final_month["savings"])))
