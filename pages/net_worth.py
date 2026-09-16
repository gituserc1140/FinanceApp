"""Net worth tracker page."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from services.net_worth_service import (
    add_asset,
    add_liability,
    create_snapshot,
    get_assets,
    get_liabilities,
    get_snapshots,
    update_asset,
    update_liability,
)
from utils.formatters import format_gbp


def render_net_worth_page() -> None:
    """Render net worth management page."""
    st.title("Net Worth Tracker")

    assets_df = get_assets()
    liabilities_df = get_liabilities()

    with st.expander("Add Asset"):
        with st.form("add_asset_form"):
            name = st.text_input("Asset name")
            category = st.selectbox("Category", ["Cash", "Investments", "Pension", "Property", "Other"])
            value = st.number_input("Value (£)", min_value=0.0, step=100.0)
            submitted = st.form_submit_button("Add asset")
            if submitted and name:
                add_asset(name, category, value)
                st.success("Asset added")
                st.rerun()

    with st.expander("Add Liability"):
        with st.form("add_liability_form"):
            name = st.text_input("Liability name")
            category = st.selectbox("Liability category", ["Consumer Debt", "Mortgage", "Education", "Other"])
            value = st.number_input("Balance (£)", min_value=0.0, step=100.0)
            interest = st.number_input("Interest rate (%)", min_value=0.0, max_value=100.0, step=0.1)
            submitted = st.form_submit_button("Add liability")
            if submitted and name:
                add_liability(name, category, value, interest)
                st.success("Liability added")
                st.rerun()

    total_assets = float(assets_df["value"].sum()) if not assets_df.empty else 0.0
    total_liabilities = float(liabilities_df["value"].sum()) if not liabilities_df.empty else 0.0

    c1, c2, c3 = st.columns(3)
    c1.metric("Assets", format_gbp(total_assets))
    c2.metric("Liabilities", format_gbp(total_liabilities))
    c3.metric("Net Worth", format_gbp(total_assets - total_liabilities))

    st.subheader("Edit Existing Values")
    edit1, edit2 = st.columns(2)

    with edit1:
        if not assets_df.empty:
            selected_asset = st.selectbox("Asset", assets_df["name"].tolist())
            asset_row = assets_df.loc[assets_df["name"] == selected_asset].iloc[0]
            new_asset_value = st.number_input("New asset value (£)", min_value=0.0, value=float(asset_row["value"]))
            if st.button("Update asset"):
                update_asset(int(asset_row["id"]), new_asset_value)
                st.success("Asset updated")
                st.rerun()

    with edit2:
        if not liabilities_df.empty:
            selected_liability = st.selectbox("Liability", liabilities_df["name"].tolist())
            liability_row = liabilities_df.loc[liabilities_df["name"] == selected_liability].iloc[0]
            new_liability_value = st.number_input("New liability value (£)", min_value=0.0, value=float(liability_row["value"]))
            if st.button("Update liability"):
                update_liability(int(liability_row["id"]), new_liability_value)
                st.success("Liability updated")
                st.rerun()

    st.subheader("Historical Net Worth")
    if st.button("Save Current Snapshot"):
        create_snapshot()
        st.success("Snapshot saved")
        st.rerun()

    snapshots_df = get_snapshots()
    if not snapshots_df.empty:
        snapshots_df["snapshot_date"] = pd.to_datetime(snapshots_df["snapshot_date"])
        trend_fig = px.line(
            snapshots_df,
            x="snapshot_date",
            y="net_worth",
            title="Net Worth Growth",
            markers=True,
        )
        st.plotly_chart(trend_fig, use_container_width=True)

    if not assets_df.empty:
        allocation_fig = px.pie(
            assets_df.groupby("category", as_index=False)["value"].sum(),
            names="category",
            values="value",
            title="Asset Allocation",
        )
        st.plotly_chart(allocation_fig, use_container_width=True)
