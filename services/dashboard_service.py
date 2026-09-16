"""Dashboard metric service."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from database.connection import get_connection


@st.cache_data(ttl=60)
def get_dashboard_metrics(user_id: int = 1) -> dict[str, float]:
    """Return high-level dashboard metrics."""
    conn = get_connection()

    assets = pd.read_sql_query(
        "SELECT COALESCE(SUM(value), 0) AS total FROM assets WHERE user_id = ?",
        conn,
        params=(user_id,),
    )["total"].iloc[0]
    liabilities = pd.read_sql_query(
        "SELECT COALESCE(SUM(value), 0) AS total FROM liabilities WHERE user_id = ?",
        conn,
        params=(user_id,),
    )["total"].iloc[0]

    monthly = pd.read_sql_query(
        """
        SELECT strftime('%Y-%m', date) AS month,
               SUM(CASE WHEN type='income' THEN amount ELSE 0 END) AS income,
               SUM(CASE WHEN type='expense' THEN amount ELSE 0 END) AS expenses,
               SUM(CASE WHEN type='savings' THEN amount ELSE 0 END) AS savings
        FROM transactions
        WHERE user_id = ?
        GROUP BY month
        ORDER BY month DESC
        LIMIT 1
        """,
        conn,
        params=(user_id,),
    )

    if monthly.empty:
        income = expenses = savings = 0.0
    else:
        income = float(monthly["income"].iloc[0])
        expenses = float(monthly["expenses"].iloc[0])
        explicit_savings = float(monthly["savings"].iloc[0])
        derived_savings = income - expenses
        savings = explicit_savings if explicit_savings > 0 else derived_savings

    savings_rate = (savings / income * 100) if income > 0 else 0.0

    return {
        "total_assets": float(assets),
        "total_liabilities": float(liabilities),
        "net_worth": float(assets - liabilities),
        "savings_rate": float(savings_rate),
        "monthly_income": income,
        "monthly_expenses": expenses,
        "monthly_savings": savings,
    }
