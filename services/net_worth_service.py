"""Net worth management service."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from database.connection import get_connection


@st.cache_data(ttl=60)
def get_assets(user_id: int = 1) -> pd.DataFrame:
    """Fetch assets."""
    return pd.read_sql_query(
        "SELECT id, name, category, value, updated_at FROM assets WHERE user_id = ? ORDER BY value DESC",
        get_connection(),
        params=(user_id,),
    )


@st.cache_data(ttl=60)
def get_liabilities(user_id: int = 1) -> pd.DataFrame:
    """Fetch liabilities."""
    return pd.read_sql_query(
        "SELECT id, name, category, value, interest_rate, updated_at FROM liabilities WHERE user_id = ? ORDER BY value DESC",
        get_connection(),
        params=(user_id,),
    )


@st.cache_data(ttl=60)
def get_snapshots(user_id: int = 1) -> pd.DataFrame:
    """Fetch net worth snapshots."""
    return pd.read_sql_query(
        "SELECT snapshot_date, assets_total, liabilities_total, net_worth FROM net_worth_snapshots WHERE user_id = ? ORDER BY snapshot_date",
        get_connection(),
        params=(user_id,),
    )


def add_asset(name: str, category: str, value: float, user_id: int = 1) -> None:
    """Insert a new asset row."""
    conn = get_connection()
    conn.execute(
        "INSERT INTO assets (user_id, name, category, value, updated_at) VALUES (?, ?, ?, ?, date('now'))",
        (user_id, name, category, value),
    )
    conn.commit()
    st.cache_data.clear()


def add_liability(name: str, category: str, value: float, interest_rate: float, user_id: int = 1) -> None:
    """Insert a new liability row."""
    conn = get_connection()
    conn.execute(
        "INSERT INTO liabilities (user_id, name, category, value, interest_rate, updated_at) VALUES (?, ?, ?, ?, ?, date('now'))",
        (user_id, name, category, value, interest_rate),
    )
    conn.commit()
    st.cache_data.clear()


def update_asset(asset_id: int, value: float) -> None:
    """Update an asset value."""
    conn = get_connection()
    conn.execute("UPDATE assets SET value = ?, updated_at = date('now') WHERE id = ?", (value, asset_id))
    conn.commit()
    st.cache_data.clear()


def update_liability(liability_id: int, value: float) -> None:
    """Update a liability value."""
    conn = get_connection()
    conn.execute("UPDATE liabilities SET value = ?, updated_at = date('now') WHERE id = ?", (value, liability_id))
    conn.commit()
    st.cache_data.clear()


def create_snapshot(user_id: int = 1) -> None:
    """Create current net worth snapshot."""
    conn = get_connection()

    assets_total = conn.execute("SELECT COALESCE(SUM(value), 0) FROM assets WHERE user_id = ?", (user_id,)).fetchone()[0]
    liabilities_total = conn.execute("SELECT COALESCE(SUM(value), 0) FROM liabilities WHERE user_id = ?", (user_id,)).fetchone()[0]
    net_worth = assets_total - liabilities_total

    existing = conn.execute(
        "SELECT id FROM net_worth_snapshots WHERE user_id = ? AND snapshot_date = date('now')",
        (user_id,),
    ).fetchone()
    if existing:
        conn.execute(
            "UPDATE net_worth_snapshots SET assets_total = ?, liabilities_total = ?, net_worth = ? WHERE id = ?",
            (assets_total, liabilities_total, net_worth, existing["id"]),
        )
    else:
        conn.execute(
            "INSERT INTO net_worth_snapshots (user_id, snapshot_date, assets_total, liabilities_total, net_worth) VALUES (?, date('now'), ?, ?, ?)",
            (user_id, assets_total, liabilities_total, net_worth),
        )
    conn.commit()
    st.cache_data.clear()
