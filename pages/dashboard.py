"""Dashboard page."""

from __future__ import annotations

import streamlit as st

from services.dashboard_service import get_dashboard_metrics
from services.insights_service import generate_insights
from utils.formatters import format_gbp


def render_dashboard_page() -> None:
    """Render the dashboard page."""
    st.title("Dashboard")

    try:
        metrics = get_dashboard_metrics()
    except Exception as error:  # pragma: no cover
        st.error(f"Unable to load dashboard metrics: {error}")
        return

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Assets", format_gbp(metrics["total_assets"]))
    col2.metric("Total Liabilities", format_gbp(metrics["total_liabilities"]))
    col3.metric("Net Worth", format_gbp(metrics["net_worth"]))
    col4.metric("Savings Rate", f"{metrics['savings_rate']:.1f}%")

    st.subheader("Monthly Summary")
    row1, row2, row3 = st.columns(3)
    row1.metric("Income", format_gbp(metrics["monthly_income"]))
    row2.metric("Expenses", format_gbp(metrics["monthly_expenses"]))
    row3.metric("Savings", format_gbp(metrics["monthly_savings"]))

    st.subheader("Financial Insights")
    for insight in generate_insights():
        st.info(insight)
