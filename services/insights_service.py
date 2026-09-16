"""Rule-based insights engine (no paid AI APIs)."""

from __future__ import annotations

from services.cashflow_service import get_monthly_cashflow
from services.goal_service import get_goals


def generate_insights(user_id: int = 1) -> list[str]:
    """Generate deterministic financial insights."""
    cashflow = get_monthly_cashflow(user_id=user_id)
    goals = get_goals(user_id=user_id)

    insights: list[str] = []

    if len(cashflow) >= 2:
        latest = cashflow.iloc[-1]
        previous = cashflow.iloc[-2]
        rate_delta = ((latest["savings"] / latest["income"] * 100) - (previous["savings"] / previous["income"] * 100)) if latest["income"] > 0 and previous["income"] > 0 else 0
        if abs(rate_delta) >= 1:
            direction = "increased" if rate_delta > 0 else "decreased"
            insights.append(f"Your savings rate {direction} by {abs(rate_delta):.1f}% this month.")

    if not cashflow.empty:
        latest_month = cashflow.iloc[-1]["month"]
        latest_expenses = cashflow.iloc[-1]["expenses"]
        if latest_expenses > 0:
            from database.connection import get_connection

            subscription_spend = get_connection().execute(
                "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE user_id = ? AND type='expense' AND category='Subscriptions' AND strftime('%Y-%m', date)=?",
                (user_id, latest_month),
            ).fetchone()[0]
            share = subscription_spend / latest_expenses * 100
            insights.append(f"Subscriptions account for {share:.1f}% of expenses.")

    if not goals.empty:
        goals_with_forecasts = goals.copy()
        goals_with_forecasts["remaining"] = (
            goals_with_forecasts["target_amount"] - goals_with_forecasts["current_amount"]
        ).clip(lower=0)
        goals_with_forecasts = goals_with_forecasts[
            (goals_with_forecasts["monthly_contribution"] > 0) & (goals_with_forecasts["remaining"] > 0)
        ].copy()
        if not goals_with_forecasts.empty:
            goals_with_forecasts["months_to_goal"] = (
                goals_with_forecasts["remaining"] / goals_with_forecasts["monthly_contribution"]
            )
            top_goal = goals_with_forecasts.sort_values("months_to_goal").iloc[0]
            months = int(top_goal["months_to_goal"] + 0.999)
            insights.append(f"You are on track to reach your {top_goal['name']} goal in about {months} months.")

    if not insights:
        insights.append("Add more transactions to unlock richer trend insights.")

    return insights[:4]
