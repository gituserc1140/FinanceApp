"""Side hustle tracker page."""

from __future__ import annotations

from datetime import date

import plotly.express as px
import streamlit as st

from services.side_hustle_service import add_side_hustle_record, calculate_profitability, get_side_hustle_records
from utils.formatters import format_gbp


def render_side_hustle_page() -> None:
    """Render side hustle profitability page."""
    st.title("Side Hustle Profit Tracker")

    with st.form("side_hustle_form"):
        month_value = st.date_input("Month", value=date.today(), format="YYYY/MM/DD")
        month = month_value.strftime("%Y-%m")
        revenue = st.number_input("Revenue (£)", min_value=0.0, step=50.0)
        expenses = st.number_input("Expenses (£)", min_value=0.0, step=50.0)
        ad_spend = st.number_input("Advertising spend (£)", min_value=0.0, step=50.0)
        platform_fees = st.number_input("Platform fees (£)", min_value=0.0, step=25.0)
        estimated_tax = st.number_input("Estimated tax (£)", min_value=0.0, step=25.0)
        submitted = st.form_submit_button("Add monthly record")

        if submitted:
            add_side_hustle_record(month, revenue, expenses, ad_spend, platform_fees, estimated_tax)
            st.success("Record added")
            st.rerun()

    records_df = get_side_hustle_records()
    profitability_df = calculate_profitability(records_df)

    if profitability_df.empty:
        st.info("No side hustle records available.")
        return

    st.dataframe(profitability_df, use_container_width=True)

    latest = profitability_df.iloc[-1]
    c1, c2, c3 = st.columns(3)
    c1.metric("Monthly Profit", format_gbp(float(latest["profit"])))
    c2.metric("Profit Margin", f"{float(latest['profit_margin']):.1f}%")
    c3.metric("Break-even Revenue", format_gbp(float(latest["break_even_revenue"])))

    fig = px.bar(
        profitability_df,
        x="month",
        y=["revenue", "total_costs", "profit"],
        title="Side Hustle Profitability",
        barmode="group",
    )
    st.plotly_chart(fig, use_container_width=True)
