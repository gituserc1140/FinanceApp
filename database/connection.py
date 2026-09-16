"""Database connection helpers for SQLite."""

from __future__ import annotations

import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parents[1] / "moneyos_uk.db"


def get_connection() -> sqlite3.Connection:
    """Return a fresh SQLite connection."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection
