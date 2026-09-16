"""Typed data models for MoneyOS UK."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class GoalForecast:
    """Goal progress and estimated completion details."""

    months_to_target: float | None
    completion_percentage: float


@dataclass(slots=True)
class FinancialHealthResult:
    """Financial health score result model."""

    score: int
    emergency_fund_score: int
    debt_ratio_score: int
    savings_rate_score: int
    investment_habit_score: int
