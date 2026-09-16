"""Financial goals page."""

from __future__ import annotations

import plotly.express as px
import streamlit as st

from services.goal_service import add_goal, forecast_goal_completion, get_goals, update_goal_progress
from utils.formatters import format_gbp


def render_goals_page() -> None:
    """Render goals planner page."""
    st.title("Financial Goal Planner")

    with st.form("add_goal_form"):
        name = st.text_input("Goal name")
        target_amount = st.number_input("Target amount (£)", min_value=1.0, step=100.0)
        current_amount = st.number_input("Current amount (£)", min_value=0.0, step=100.0)
        monthly_contribution = st.number_input("Monthly contribution (£)", min_value=0.0, step=50.0)
        target_date = st.date_input("Target date")
        submitted = st.form_submit_button("Create goal")

        if submitted and name:
            add_goal(name, target_amount, current_amount, monthly_contribution, target_date.isoformat())
            st.success("Goal created")
            st.rerun()

    goals_df = get_goals()
    if goals_df.empty:
        st.info("No goals yet. Add your first goal above.")
        return

    st.subheader("Goal Progress")
    for _, row in goals_df.iterrows():
        forecast = forecast_goal_completion(
            target_amount=float(row["target_amount"]),
            current_amount=float(row["current_amount"]),
            monthly_contribution=float(row["monthly_contribution"]),
        )

        st.markdown(f"**{row['name']}**")
        st.progress(forecast.completion_percentage / 100)
        st.caption(
            f"{format_gbp(float(row['current_amount']))} / {format_gbp(float(row['target_amount']))}"
        )
        if forecast.months_to_target is not None:
            st.write(f"Estimated completion: {forecast.months_to_target} months")
        else:
            st.write("Estimated completion: update monthly contribution to calculate forecast")

    st.subheader("Update Goal Amount")
    goal_options = {f"{row['name']} (ID {row['id']})": int(row["id"]) for _, row in goals_df.iterrows()}
    selected_goal_label = st.selectbox("Select goal to update", list(goal_options.keys()))
    selected_goal_id = goal_options[selected_goal_label]
    selected = goals_df.loc[goals_df["id"] == selected_goal_id].iloc[0]
    current_value = st.number_input("New current amount (£)", min_value=0.0, value=float(selected["current_amount"]))
    if st.button("Update progress"):
        update_goal_progress(selected_goal_id, current_value)
        st.success("Goal progress updated")
        st.rerun()

    progress_chart = goals_df.copy()
    progress_chart["remaining"] = progress_chart["target_amount"] - progress_chart["current_amount"]
    fig = px.bar(
        progress_chart,
        x="name",
        y=["current_amount", "remaining"],
        title="Savings Goal Progress",
        barmode="stack",
    )
    st.plotly_chart(fig, use_container_width=True)
