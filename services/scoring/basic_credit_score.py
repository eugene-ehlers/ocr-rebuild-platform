from __future__ import annotations

from typing import Any, Dict, List

CREDIT_SCORE_MODEL_ID = "credit_score_baseline_v1_13Apr2026"

def build_credit_score(transactions: List[Dict[str, Any]], classifications: List[Dict[str, Any]]) -> Dict[str, Any]:
    credits = [t for t in transactions if t.get("type") == "credit"]
    debits = [t for t in transactions if t.get("type") == "debit"]

    income = round(sum(float(t.get("amount") or 0.0) for t in credits), 2)
    expenses = round(sum(float(t.get("amount") or 0.0) for t in debits), 2)
    net = round(income - expenses, 2)

    salary_like = any(
        c.get("primary_category") == "salary_or_income"
        for c in classifications
    )

    score = 500
    if income > 0:
        score += 80
    if net > 0:
        score += 60
    if salary_like:
        score += 40
    if expenses > income and income > 0:
        score -= 80
    if not credits:
        score -= 120

    score = max(300, min(850, score))

    band = "poor"
    if score >= 750:
        band = "excellent"
    elif score >= 680:
        band = "good"
    elif score >= 620:
        band = "fair"

    return {
        "credit_score": score,
        "score_band": band,
        "score_factors": {
            "income_total": income,
            "expense_total": expenses,
            "net_cashflow": net,
            "salary_like_income_present": salary_like,
            "credit_transaction_count": len(credits),
            "debit_transaction_count": len(debits),
        },
        "scoring_model_id": CREDIT_SCORE_MODEL_ID,
        "scoring_method": "scorecard_v1",
    }
