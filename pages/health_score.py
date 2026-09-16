"""Financial health score page."""

from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from services.health_service import calculate_health_score, health_recommendations


def render_health_score_page() -> None:
    """Render financial health scoring page."""
    st.title("Financial Health Score")

    result = calculate_health_score()

    st.metric("Overall Score", f"{result.score}/100")

    fig = go.Figure(
        go.Bar(
            x=["Emergency Fund", "Debt Ratio", "Savings Rate", "Investment Habits"],
            y=[
                result.emergency_fund_score,
                result.debt_ratio_score,
                result.savings_rate_score,
                result.investment_habit_score,
            ],
            marker_color=["#3b82f6", "#8b5cf6", "#10b981", "#f97316"],
        )
    )
    fig.update_layout(title="Score Breakdown (each out of 25)", yaxis_range=[0, 25])
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "Emergency Fund: "
        f"{result.emergency_fund_score}/25 | "
        f"Debt Ratio: {result.debt_ratio_score}/25 | "
        f"Savings Rate: {result.savings_rate_score}/25 | "
        f"Investment Habits: {result.investment_habit_score}/25"
    )

    st.subheader("Personalised Recommendations")
    for recommendation in health_recommendations(result):
        st.write(f"- {recommendation}")
