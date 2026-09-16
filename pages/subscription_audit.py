"""Subscription audit page."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from services.subscription_service import detect_recurring_transactions, get_saved_subscriptions
from utils.formatters import format_gbp


def render_subscription_audit_page() -> None:
    """Render subscription audit page."""
    st.title("Subscription Audit Tool")
    st.caption("Upload a CSV bank statement with date, description, amount columns.")

    saved = get_saved_subscriptions()
    if not saved.empty:
        st.subheader("Saved Subscriptions")
        st.dataframe(saved, use_container_width=True)

    uploaded_file = st.file_uploader("Upload bank statement CSV", type=["csv"])
    if not uploaded_file:
        return

    try:
        statement_df = pd.read_csv(uploaded_file)
        recurring_df = detect_recurring_transactions(statement_df)
    except ValueError as validation_error:
        st.error(str(validation_error))
        return
    except Exception as error:  # pragma: no cover
        st.error(f"Unable to process statement: {error}")
        return

    if recurring_df.empty:
        st.warning("No recurring transactions detected from this file.")
        return

    st.subheader("Detected Recurring Expenses")
    st.dataframe(recurring_df, use_container_width=True)

    annual_total = float(recurring_df["annual_cost"].sum())
    largest = recurring_df.iloc[0]

    c1, c2 = st.columns(2)
    c1.metric("Estimated Annual Subscription Cost", format_gbp(annual_total))
    c2.metric("Largest Recurring Expense", f"{largest['merchant']} ({format_gbp(float(largest['annual_cost']))}/yr)")
