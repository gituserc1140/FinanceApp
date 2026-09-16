"""MoneyOS UK Streamlit entrypoint."""

from __future__ import annotations

import streamlit as st

from database.init_db import initialize_database
from pages.cash_flow import render_cash_flow_page
from pages.dashboard import render_dashboard_page
from pages.fire_calculator import render_fire_calculator_page
from pages.goals import render_goals_page
from pages.health_score import render_health_score_page
from pages.net_worth import render_net_worth_page
from pages.side_hustle import render_side_hustle_page
from pages.subscription_audit import render_subscription_audit_page


PAGES = {
    "Dashboard": render_dashboard_page,
    "Net Worth Tracker": render_net_worth_page,
    "Financial Goal Planner": render_goals_page,
    "Financial Health Score": render_health_score_page,
    "FIRE Calculator": render_fire_calculator_page,
    "Subscription Audit": render_subscription_audit_page,
    "Cash Flow Forecast": render_cash_flow_page,
    "Side Hustle Tracker": render_side_hustle_page,
}


def _inject_styles() -> None:
    st.markdown(
        """
        <style>
        .block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
        [data-testid="stMetricValue"] {font-size: 1.8rem;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    """Run the MoneyOS UK app."""
    st.set_page_config(page_title="MoneyOS UK", page_icon="💷", layout="wide")
    _inject_styles()

    initialize_database()

    st.sidebar.title("MoneyOS UK")
    st.sidebar.caption("Personal finance dashboard for UK users")
    selected_page = st.sidebar.radio("Navigate", list(PAGES.keys()))

    PAGES[selected_page]()


if __name__ == "__main__":
    main()
