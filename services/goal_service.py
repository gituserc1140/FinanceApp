"""Financial goal management service."""

from __future__ import annotations

import math

import pandas as pd
import streamlit as st

from database.connection import get_connection
from models.finance import GoalForecast


@st.cache_data(ttl=60)
def get_goals(user_id: int = 1) -> pd.DataFrame:
    """Fetch all goals."""
    return pd.read_sql_query(
        "SELECT id, name, target_amount, current_amount, monthly_contribution, target_date, created_at FROM goals WHERE user_id = ? ORDER BY created_at DESC",
        get_connection(),
        params=(user_id,),
    )


def add_goal(
    name: str,
    target_amount: float,
    current_amount: float,
    monthly_contribution: float,
    target_date: str,
    user_id: int = 1,
) -> None:
    """Create goal."""
    conn = get_connection()
    conn.execute(
        "INSERT INTO goals (user_id, name, target_amount, current_amount, monthly_contribution, target_date, created_at) VALUES (?, ?, ?, ?, ?, ?, date('now'))",
        (user_id, name, target_amount, current_amount, monthly_contribution, target_date),
    )
    conn.commit()
    st.cache_data.clear()


def update_goal_progress(goal_id: int, current_amount: float) -> None:
    """Update goal current amount."""
    conn = get_connection()
    conn.execute("UPDATE goals SET current_amount = ? WHERE id = ?", (current_amount, goal_id))
    conn.commit()
    st.cache_data.clear()


def forecast_goal_completion(target_amount: float, current_amount: float, monthly_contribution: float) -> GoalForecast:
    """Calculate goal completion forecast and progress."""
    completion = min((current_amount / target_amount * 100) if target_amount > 0 else 0.0, 100.0)

    if monthly_contribution <= 0 or current_amount >= target_amount:
        return GoalForecast(months_to_target=None, completion_percentage=completion)

    remaining = max(target_amount - current_amount, 0)
    months = math.ceil(remaining / monthly_contribution)
    return GoalForecast(months_to_target=months, completion_percentage=completion)
