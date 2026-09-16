"""Database connection helpers for SQLite."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import streamlit as st


DB_PATH = Path(__file__).resolve().parents[1] / "moneyos_uk.db"


@st.cache_resource
def get_connection() -> sqlite3.Connection:
    """Return cached SQLite connection."""
    connection = sqlite3.connect(DB_PATH, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection
