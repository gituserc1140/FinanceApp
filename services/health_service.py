"""Financial health score service."""

from __future__ import annotations

from models.finance import FinancialHealthResult
from services.dashboard_service import get_dashboard_metrics
from services.net_worth_service import get_assets


def calculate_health_score(user_id: int = 1) -> FinancialHealthResult:
    """Calculate overall health score out of 100."""
    metrics = get_dashboard_metrics(user_id=user_id)
    assets_df = get_assets(user_id=user_id)

    monthly_expenses = metrics["monthly_expenses"]
    emergency_cash = float(assets_df.loc[assets_df["category"] == "Cash", "value"].sum()) if not assets_df.empty else 0.0

    emergency_months = emergency_cash / monthly_expenses if monthly_expenses > 0 else 0.0
    emergency_score = min(int((emergency_months / 6) * 25), 25)

    debt_ratio = (metrics["total_liabilities"] / metrics["total_assets"] * 100) if metrics["total_assets"] > 0 else 100.0
    debt_ratio_score = 25 if debt_ratio < 20 else 18 if debt_ratio < 35 else 10 if debt_ratio < 50 else 3

    savings_rate = metrics["savings_rate"]
    savings_score = 25 if savings_rate >= 20 else 18 if savings_rate >= 12 else 10 if savings_rate >= 5 else 3

    investment_value = float(assets_df.loc[assets_df["category"].isin(["Investments", "Pension"]), "value"].sum()) if not assets_df.empty else 0.0
    investment_ratio = (investment_value / metrics["total_assets"] * 100) if metrics["total_assets"] > 0 else 0.0
    investment_score = 25 if investment_ratio >= 40 else 18 if investment_ratio >= 20 else 10 if investment_ratio >= 10 else 4

    total = emergency_score + debt_ratio_score + savings_score + investment_score
    return FinancialHealthResult(
        score=total,
        emergency_fund_score=emergency_score,
        debt_ratio_score=debt_ratio_score,
        savings_rate_score=savings_score,
        investment_habit_score=investment_score,
    )


def health_recommendations(result: FinancialHealthResult) -> list[str]:
    """Return personalised recommendations."""
    recs: list[str] = []

    if result.emergency_fund_score < 18:
        recs.append("Build emergency savings to cover 3-6 months of essential expenses.")
    if result.debt_ratio_score < 18:
        recs.append("Prioritise paying down high-interest debt to improve debt ratio.")
    if result.savings_rate_score < 18:
        recs.append("Increase monthly savings contributions to target at least a 12% savings rate.")
    if result.investment_habit_score < 18:
        recs.append("Increase long-term investing through ISA and pension contributions.")

    if not recs:
        recs.append("Great progress. Continue your current strategy and review goals monthly.")

    return recs
