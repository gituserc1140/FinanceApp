"""FIRE calculator page."""

from __future__ import annotations

import plotly.express as px
import streamlit as st

from services.fire_service import calculate_fire
from utils.formatters import format_gbp


def render_fire_calculator_page() -> None:
    """Render FIRE calculator."""
    st.title("FIRE Calculator")

    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=18, max_value=80, value=30)
        salary = st.number_input("Monthly salary (£)", min_value=0.0, value=3200.0, step=100.0)
        savings = st.number_input("Current savings/investments (£)", min_value=0.0, value=20000.0, step=500.0)
    with col2:
        expenses = st.number_input("Monthly expenses (£)", min_value=0.0, value=2100.0, step=100.0)
        annual_return = st.number_input("Expected annual return (%)", min_value=0.0, max_value=20.0, value=5.0, step=0.1)

    output = calculate_fire(
        age=int(age),
        salary=float(salary),
        savings=float(savings),
        monthly_expenses=float(expenses),
        annual_return_percent=float(annual_return),
    )

    c1, c2 = st.columns(2)
    c1.metric("FIRE Number", format_gbp(float(output["fire_number"])))
    c2.metric("Estimated Retirement Age", int(output["estimated_retirement_age"]))

    projection = output["projection"]
    fig = px.line(projection, x="Age", y="Projected Wealth", title="Wealth Growth Projection")
    st.plotly_chart(fig, use_container_width=True)
