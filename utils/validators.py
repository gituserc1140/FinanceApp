"""Validation and parsing helpers."""

from __future__ import annotations


def non_negative(value: float) -> float:
    """Return non-negative number with floor at zero."""
    return max(value, 0.0)
