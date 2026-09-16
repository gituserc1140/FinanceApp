"""SQLite schema and demo seed data."""

from __future__ import annotations

from datetime import date

import streamlit as st

from database.connection import get_connection


def initialize_database() -> None:
    """Create required tables and insert demo data when empty."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            monthly_income REAL DEFAULT 0,
            monthly_expenses REAL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            value REAL NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS liabilities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            value REAL NOT NULL,
            interest_rate REAL DEFAULT 0,
            updated_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS net_worth_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            snapshot_date TEXT NOT NULL,
            assets_total REAL NOT NULL,
            liabilities_total REAL NOT NULL,
            net_worth REAL NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            target_amount REAL NOT NULL,
            current_amount REAL NOT NULL,
            monthly_contribution REAL NOT NULL,
            target_date TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            merchant TEXT NOT NULL,
            amount REAL NOT NULL,
            billing_cycle TEXT NOT NULL,
            last_seen TEXT,
            category TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS side_hustles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            month TEXT NOT NULL,
            revenue REAL NOT NULL,
            expenses REAL NOT NULL,
            ad_spend REAL NOT NULL,
            platform_fees REAL NOT NULL,
            estimated_tax REAL NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        """
    )

    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        today = date.today()

        cursor.execute(
            "INSERT INTO users (id, name, monthly_income, monthly_expenses) VALUES (1, ?, ?, ?)",
            ("Demo User", 3200, 2100),
        )

        cursor.executemany(
            "INSERT INTO assets (user_id, name, category, value, updated_at) VALUES (1, ?, ?, ?, ?)",
            [
                ("Emergency Cash", "Cash", 5500, today.isoformat()),
                ("S&S ISA", "Investments", 14800, today.isoformat()),
                ("Workplace Pension", "Pension", 22300, today.isoformat()),
            ],
        )

        cursor.executemany(
            "INSERT INTO liabilities (user_id, name, category, value, interest_rate, updated_at) VALUES (1, ?, ?, ?, ?, ?)",
            [
                ("Credit Card", "Consumer Debt", 1200, 23.5, today.isoformat()),
                ("Student Loan", "Education", 9800, 5.0, today.isoformat()),
            ],
        )

        cursor.executemany(
            "INSERT INTO net_worth_snapshots (user_id, snapshot_date, assets_total, liabilities_total, net_worth) VALUES (1, ?, ?, ?, ?)",
            [
                ("2026-04-01", 36000, 12500, 23500),
                ("2026-05-01", 38000, 12100, 25900),
                ("2026-06-01", 39500, 11600, 27900),
                ("2026-07-01", 41000, 11200, 29800),
                ("2026-08-01", 42500, 10900, 31600),
            ],
        )

        cursor.executemany(
            "INSERT INTO goals (user_id, name, target_amount, current_amount, monthly_contribution, target_date, created_at) VALUES (1, ?, ?, ?, ?, ?, ?)",
            [
                ("Emergency Fund (6 months)", 12600, 5500, 500, "2027-02-28", today.isoformat()),
                ("House Deposit", 30000, 9000, 750, "2028-12-31", today.isoformat()),
            ],
        )

        cursor.executemany(
            "INSERT INTO transactions (user_id, date, description, category, amount, type) VALUES (1, ?, ?, ?, ?, ?)",
            [
                ("2026-06-05", "Salary", "Income", 3200, "income"),
                ("2026-06-06", "Rent", "Housing", 1100, "expense"),
                ("2026-06-08", "Groceries", "Food", 320, "expense"),
                ("2026-06-12", "ISA Contribution", "Savings", 500, "savings"),
                ("2026-07-05", "Salary", "Income", 3200, "income"),
                ("2026-07-06", "Rent", "Housing", 1100, "expense"),
                ("2026-07-08", "Groceries", "Food", 340, "expense"),
                ("2026-07-12", "ISA Contribution", "Savings", 520, "savings"),
                ("2026-08-05", "Salary", "Income", 3200, "income"),
                ("2026-08-06", "Rent", "Housing", 1100, "expense"),
                ("2026-08-08", "Groceries", "Food", 335, "expense"),
                ("2026-08-11", "Gym", "Subscriptions", 30, "expense"),
                ("2026-08-12", "ISA Contribution", "Savings", 550, "savings"),
                ("2026-09-05", "Salary", "Income", 3200, "income"),
                ("2026-09-06", "Rent", "Housing", 1100, "expense"),
                ("2026-09-08", "Groceries", "Food", 345, "expense"),
                ("2026-09-10", "Streaming Service", "Subscriptions", 12.99, "expense"),
                ("2026-09-12", "ISA Contribution", "Savings", 580, "savings"),
            ],
        )

        cursor.executemany(
            "INSERT INTO subscriptions (user_id, merchant, amount, billing_cycle, last_seen, category) VALUES (1, ?, ?, ?, ?, ?)",
            [
                ("Netflix", 10.99, "Monthly", "2026-09-02", "Entertainment"),
                ("Spotify", 11.99, "Monthly", "2026-09-03", "Entertainment"),
                ("Gym Membership", 30.00, "Monthly", "2026-09-11", "Health"),
            ],
        )

        cursor.executemany(
            "INSERT INTO side_hustles (user_id, month, revenue, expenses, ad_spend, platform_fees, estimated_tax) VALUES (1, ?, ?, ?, ?, ?, ?)",
            [
                ("2026-07", 1350, 280, 120, 95, 170),
                ("2026-08", 1480, 300, 135, 102, 185),
                ("2026-09", 1620, 320, 160, 120, 205),
            ],
        )

    conn.commit()
    st.cache_data.clear()
