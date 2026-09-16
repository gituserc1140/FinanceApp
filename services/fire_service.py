"""FIRE calculator business logic."""

from __future__ import annotations

import pandas as pd


def calculate_fire(
    age: int,
    annual_salary: float,
    savings: float,
    monthly_expenses: float,
    annual_return_percent: float,
) -> dict[str, float | int | None | pd.DataFrame]:
    """Calculate FIRE metrics and wealth projections."""
    annual_expenses = monthly_expenses * 12
    fire_number = annual_expenses * 25

    annual_savings = max(annual_salary - annual_expenses, 0.0)
    growth_rate = annual_return_percent / 100

    wealth = savings
    projection_rows = []

    retirement_age: int | None = None
    for year in range(0, 51):
        current_age = age + year
        projection_rows.append({"Age": current_age, "Projected Wealth": wealth})
        if wealth >= fire_number and retirement_age is None:
            retirement_age = current_age
        wealth = (wealth + annual_savings) * (1 + growth_rate)

    projection = pd.DataFrame(projection_rows)

    return {
        "fire_number": fire_number,
        "estimated_retirement_age": retirement_age,
        "projection": projection,
    }
