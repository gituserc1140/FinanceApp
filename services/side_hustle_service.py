"""Side hustle tracker service."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from database.connection import get_connection


@st.cache_data(ttl=60)
def get_side_hustle_records(user_id: int = 1) -> pd.DataFrame:
    """Return side hustle monthly records."""
    return pd.read_sql_query(
        "SELECT id, month, revenue, expenses, ad_spend, platform_fees, estimated_tax FROM side_hustles WHERE user_id = ? ORDER BY date(month || '-01')",
        get_connection(),
        params=(user_id,),
    )


def add_side_hustle_record(
    month: str,
    revenue: float,
    expenses: float,
    ad_spend: float,
    platform_fees: float,
    estimated_tax: float,
    user_id: int = 1,
) -> None:
    """Insert side hustle monthly record."""
    conn = get_connection()
    conn.execute(
        "INSERT INTO side_hustles (user_id, month, revenue, expenses, ad_spend, platform_fees, estimated_tax) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (user_id, month, revenue, expenses, ad_spend, platform_fees, estimated_tax),
    )
    conn.commit()
    st.cache_data.clear()


def calculate_profitability(df: pd.DataFrame) -> pd.DataFrame:
    """Compute profit and margin metrics."""
    if df.empty:
        return df

    output = df.copy()
    output["total_costs"] = output[["expenses", "ad_spend", "platform_fees", "estimated_tax"]].sum(axis=1)
    output["profit"] = output["revenue"] - output["total_costs"]
    output["profit_margin"] = 0.0
    valid_revenue = output["revenue"] > 0
    output.loc[valid_revenue, "profit_margin"] = (
        output.loc[valid_revenue, "profit"] / output.loc[valid_revenue, "revenue"] * 100
    )
    output["break_even_revenue"] = output["total_costs"]
    return output
