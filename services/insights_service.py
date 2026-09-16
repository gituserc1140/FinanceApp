"""Rule-based insights engine (no paid AI APIs)."""

from __future__ import annotations

from services.cashflow_service import get_monthly_cashflow
from services.dashboard_service import get_dashboard_metrics
from services.goal_service import get_goals


def generate_insights(user_id: int = 1) -> list[str]:
    """Generate deterministic financial insights."""
    metrics = get_dashboard_metrics(user_id=user_id)
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

    subscription_share = (metrics["monthly_expenses"] and (metrics["monthly_expenses"] > 0))
    if subscription_share and not cashflow.empty:
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
        top_goal = goals.iloc[0]
        remaining = max(top_goal["target_amount"] - top_goal["current_amount"], 0)
        if top_goal["monthly_contribution"] > 0:
            months = int(remaining / top_goal["monthly_contribution"] + 0.999)
            insights.append(f"You are on track to reach your {top_goal['name']} goal in about {months} months.")

    if not insights:
        insights.append("Add more transactions to unlock richer trend insights.")

    return insights[:4]
