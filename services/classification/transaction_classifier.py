from __future__ import annotations

from typing import Any, Dict, List

CLASSIFIER_MODEL_ID = "txn_classifier_baseline_v1_13Apr2026"

CATEGORY_RULES = [
    ("salary_or_income", ["salary", "payroll", "wage", "deposit", "bonus"]),
    ("rent", ["rent", "rental", "landlord"]),
    ("insurance", ["insurance", "policy", "insure"]),
    ("loan_repayment", ["loan", "repay", "instalment", "installment", "credit card"]),
    ("groceries", ["grocery", "grocer", "supermarket", "shoprite", "checkers", "pick n pay"]),
    ("transport", ["fuel", "petrol", "uber", "taxi", "transport"]),
    ("utilities", ["electric", "water", "utility", "municipal"]),
    ("cash_withdrawal", ["atm", "cash withdrawal", "cash wd", "wdl"]),
    ("entertainment", ["movie", "cinema", "restaurant", "takeaway", "entertainment", "dining"]),
    ("medical", ["medical", "clinic", "doctor", "pharmacy"]),
    ("education", ["school", "tuition", "education"]),
    ("savings_or_investment", ["saving", "investment", "unit trust"]),
    ("fees_and_charges", ["fee", "charge", "commission"]),
]

def classify_transaction(txn: Dict[str, Any]) -> Dict[str, Any]:
    desc = str(txn.get("description") or "").lower()

    for category, tokens in CATEGORY_RULES:
        if any(token in desc for token in tokens):
            return {
                "primary_category": category,
                "classification_confidence": 0.80,
                "classification_model_id": CLASSIFIER_MODEL_ID,
                "classification_method": "rules_v1",
                "matched_tokens": [t for t in tokens if t in desc],
            }

    return {
        "primary_category": "unclassified",
        "classification_confidence": 0.50,
        "classification_model_id": CLASSIFIER_MODEL_ID,
        "classification_method": "rules_v1",
        "matched_tokens": [],
    }

def classify_transactions(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    items = [classify_transaction(txn) for txn in transactions]
    avg_conf = round(
        sum(item["classification_confidence"] for item in items) / len(items), 2
    ) if items else 0.0

    return {
        "classified_transactions": items,
        "classified_transactions_metadata": {
            "classification_model_id": CLASSIFIER_MODEL_ID,
            "classification_method": "rules_v1",
            "total_classified": len(items),
            "average_confidence": avg_conf,
        },
    }
