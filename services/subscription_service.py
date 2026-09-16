"""Subscription audit logic."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from database.connection import get_connection


@st.cache_data(ttl=60)
def get_saved_subscriptions(user_id: int = 1) -> pd.DataFrame:
    """Fetch saved subscriptions from database."""
    return pd.read_sql_query(
        "SELECT merchant, amount, billing_cycle, category, last_seen FROM subscriptions WHERE user_id = ? ORDER BY amount DESC",
        get_connection(),
        params=(user_id,),
    )


def detect_recurring_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """Detect recurring expenses from transaction dataframe."""
    working = df.copy()
    working.columns = [column.strip().lower() for column in working.columns]

    required_columns = {"date", "description", "amount"}
    if not required_columns.issubset(set(working.columns)):
        raise ValueError("CSV must include date, description, and amount columns.")

    working["date"] = pd.to_datetime(working["date"], errors="coerce")
    working["amount"] = pd.to_numeric(working["amount"], errors="coerce")
    working = working.dropna(subset=["date", "description", "amount"])

    grouped = (
        working.groupby(working["description"].str.strip().str.lower())
        .agg(
            count=("amount", "count"),
            avg_amount=("amount", "mean"),
            std_amount=("amount", "std"),
            first_seen=("date", "min"),
            last_seen=("date", "max"),
        )
        .reset_index()
        .rename(columns={"description": "merchant"})
    )

    grouped["avg_amount_abs"] = grouped["avg_amount"].abs()
    recurring = grouped[(grouped["count"] >= 3) & (grouped["avg_amount_abs"] > 0)].copy()
    recurring["std_amount"] = recurring["std_amount"].fillna(0)
    recurring = recurring[recurring["std_amount"] <= recurring["avg_amount_abs"] * 0.25]

    span_months = ((recurring["last_seen"] - recurring["first_seen"]).dt.days / 30.44).clip(lower=1)
    frequency_per_month = recurring["count"] / span_months
    recurring["annual_cost"] = recurring["avg_amount_abs"] * frequency_per_month * 12
    recurring = recurring.sort_values("annual_cost", ascending=False)
    return recurring
