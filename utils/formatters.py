"""Formatting utilities."""

from __future__ import annotations


def format_gbp(value: float) -> str:
    """Format number into GBP currency string."""
    return f"£{value:,.2f}"
