"""Cash flow and projection service."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from database.connection import get_connection


@st.cache_data(ttl=60)
def get_monthly_cashflow(user_id: int = 1) -> pd.DataFrame:
    """Return monthly income, expense and savings totals."""
    query = """
        SELECT strftime('%Y-%m', date) AS month,
               SUM(CASE WHEN type='income' THEN amount ELSE 0 END) AS income,
               SUM(CASE WHEN type='expense' THEN amount ELSE 0 END) AS expenses,
               SUM(CASE WHEN type='savings' THEN amount ELSE 0 END) AS savings
        FROM transactions
        WHERE user_id = ?
        GROUP BY month
        ORDER BY month
    """
    return pd.read_sql_query(query, get_connection(), params=(user_id,))


def forecast_cashflow(cashflow_df: pd.DataFrame, months: int) -> pd.DataFrame:
    """Project cashflow for requested number of months based on recent average."""
    if cashflow_df.empty:
        return pd.DataFrame(columns=["month", "income", "expenses", "savings"])

    recent = cashflow_df.tail(min(len(cashflow_df), 3))
    avg_income = float(recent["income"].mean())
    avg_expenses = float(recent["expenses"].mean())
    avg_savings = float(recent["savings"].mean())

    latest_month = pd.to_datetime(cashflow_df["month"] + "-01").max()
    rows = []
    for step in range(1, months + 1):
        month_value = (latest_month + pd.DateOffset(months=step)).strftime("%Y-%m")
        rows.append(
            {
                "month": month_value,
                "income": avg_income,
                "expenses": avg_expenses,
                "savings": avg_savings,
            }
        )

    return pd.DataFrame(rows)
