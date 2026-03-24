from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple


EXPECTED_SERVICE_FAMILY = "financial_management"
EXPECTED_STAGE = "downstream_execution"
SUPPORTED_PLAN_VERSIONS = {"execution_plan_v1"}


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _build_execution_plan_ack(payload: Dict[str, Any]) -> Dict[str, Any]:
    execution_plan = payload.get("execution_plan") or {}
    orchestration_context = payload.get("orchestration_context") or {}

    return {
        "present": bool(execution_plan),
        "plan_id": execution_plan.get("plan_id"),
        "plan_version": execution_plan.get("plan_version"),
        "service_family_seen": execution_plan.get("service_family"),
        "orchestration_stage_seen": orchestration_context.get("current_stage"),
        "plan_status_seen": orchestration_context.get("plan_status"),
    }


def _validate_execution_plan(payload: Any, expected_service_family: str) -> Dict[str, Any]:
    errors: List[str] = []

    if not isinstance(payload, dict):
        errors.append("payload_not_dict")
        return {
            "status": "fail",
            "errors": errors,
        }

    execution_plan = payload.get("execution_plan")
    if not isinstance(execution_plan, dict):
        errors.append("execution_plan_missing")
        return {
            "status": "fail",
            "errors": errors,
        }

    plan_version = execution_plan.get("plan_version")
    if not plan_version:
        errors.append("execution_plan_version_missing")
    elif plan_version not in SUPPORTED_PLAN_VERSIONS:
        errors.append("execution_plan_version_unsupported")

    service_family = execution_plan.get("service_family")
    if not service_family:
        errors.append("execution_plan_service_family_missing")
    elif service_family != expected_service_family:
        errors.append("execution_plan_service_family_mismatch")

    orchestration_context = payload.get("orchestration_context")
    if not isinstance(orchestration_context, dict):
        errors.append("orchestration_context_missing")
    else:
        current_stage = orchestration_context.get("current_stage")
        if not current_stage:
            errors.append("orchestration_stage_missing")
        elif current_stage != EXPECTED_STAGE:
            errors.append("orchestration_stage_invalid")

    return {
        "status": "pass" if not errors else "fail",
        "errors": errors,
    }


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _normalize_type(raw_type: Any, amount: float) -> str:
    normalized = str(raw_type or "").strip().lower()
    if normalized in {"debit", "credit"}:
        return normalized
    return "credit" if amount >= 0 else "debit"


def _normalize_transaction(raw: Dict[str, Any], index: int) -> Dict[str, Any]:
    amount = _safe_float(raw.get("amount"))
    balance_raw = raw.get("balance")
    transaction_type = _normalize_type(raw.get("type"), amount)

    return {
        "transaction_id": str(
            raw.get("transaction_id")
            or raw.get("id")
            or f"txn-{index:04d}"
        ),
        "date": str(raw.get("date") or ""),
        "description": str(raw.get("description") or raw.get("narration") or ""),
        "amount": amount,
        "type": transaction_type,
        "balance": _safe_float(balance_raw) if balance_raw not in (None, "") else None,
        "confidence": 0.95,
    }


def _classify_transaction(parsed: Dict[str, Any]) -> Dict[str, Any]:
    description = parsed["description"].lower()
    transaction_type = parsed["type"]

    primary_category = "fees and charges"
    secondary_category = None

    if transaction_type == "credit":
        if any(token in description for token in ["salary", "payroll", "wage"]):
            primary_category = "salary or income"
        elif any(token in description for token in ["transfer", "deposit"]):
            primary_category = "transfers"
        else:
            primary_category = "salary or income"
    else:
        if any(token in description for token in ["rent", "rental", "landlord"]):
            primary_category = "rent"
        elif any(token in description for token in ["insurance", "insure", "policy"]):
            primary_category = "insurance"
        elif any(token in description for token in ["loan", "repay", "instalment", "installment", "credit card"]):
            primary_category = "loan repayment"
        elif any(token in description for token in ["grocery", "grocer", "supermarket", "shoprite", "checkers", "pick n pay"]):
            primary_category = "groceries"
        elif any(token in description for token in ["fuel", "petrol", "uber", "taxi", "transport"]):
            primary_category = "transport"
            if any(token in description for token in ["fuel", "petrol"]):
                secondary_category = "fuel"
        elif any(token in description for token in ["electric", "water", "utility", "municipal"]):
            primary_category = "utilities"
        elif any(token in description for token in ["atm", "cash withdrawal", "cash wd"]):
            primary_category = "cash withdrawal"
        elif any(token in description for token in ["movie", "cinema", "restaurant", "takeaway", "entertainment", "dining"]):
            primary_category = "entertainment"
        elif any(token in description for token in ["medical", "clinic", "doctor", "pharmacy"]):
            primary_category = "medical"
        elif any(token in description for token in ["school", "tuition", "education"]):
            primary_category = "education"
        elif any(token in description for token in ["saving", "investment", "unit trust"]):
            primary_category = "savings or investment"
        elif any(token in description for token in ["fee", "charge", "commission"]):
            primary_category = "fees and charges"

    return {
        "transaction_id": parsed["transaction_id"],
        "primary_category": primary_category,
        "secondary_category": secondary_category,
        "classification_confidence": 0.89,
        "classification_method": "rules",
    }


def _classify_cash_flow(
    parsed: Dict[str, Any],
    classified: Dict[str, Any],
) -> Dict[str, Any]:
    primary_category = classified["primary_category"]
    flow_type = "discretionary_expense"
    sub_type = primary_category
    recurrence = "irregular"

    if parsed["type"] == "credit":
        flow_type = "income"
        recurrence = "monthly" if primary_category == "salary or income" else "irregular"
    elif primary_category in {"rent", "insurance"}:
        flow_type = "fixed_expense"
        recurrence = "monthly"
    elif primary_category == "loan repayment":
        flow_type = "debt_related"
        recurrence = "monthly"
    elif primary_category in {"groceries", "utilities", "medical", "education", "transport"}:
        flow_type = "variable_expense"
    elif primary_category in {"savings or investment"}:
        flow_type = "savings_and_investments"

    return {
        "transaction_id": parsed["transaction_id"],
        "flow_type": flow_type,
        "sub_type": sub_type,
        "recurrence": recurrence,
        "confidence": 0.91,
    }


def _build_substrate(payload: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], Dict[str, Any], List[Dict[str, Any]], Dict[str, Any], Dict[str, float]]:
    raw_transactions = payload.get("transactions")
    if not isinstance(raw_transactions, list):
        raw_transactions = []

    parsed_transactions = [
        _normalize_transaction(raw, idx)
        for idx, raw in enumerate(raw_transactions, start=1)
        if isinstance(raw, dict)
    ]

    parsing_confidence = 0.0
    if parsed_transactions:
        parsing_confidence = round(
            sum(item["confidence"] for item in parsed_transactions) / len(parsed_transactions),
            2,
        )

    parsed_metadata = {
        "total_transactions": len(parsed_transactions),
        "parsing_confidence": parsing_confidence,
    }

    classified_transactions = [_classify_transaction(item) for item in parsed_transactions]

    classification_confidence_overall = 0.0
    if classified_transactions:
        classification_confidence_overall = round(
            sum(item["classification_confidence"] for item in classified_transactions) / len(classified_transactions),
            2,
        )

    classification_metadata = {
        "total_classified": len(classified_transactions),
        "classification_confidence_overall": classification_confidence_overall,
    }

    cash_flow_classification = [
        _classify_cash_flow(parsed, classified)
        for parsed, classified in zip(parsed_transactions, classified_transactions)
    ]

    income_total = round(sum(item["amount"] for item, flow in zip(parsed_transactions, cash_flow_classification) if flow["flow_type"] == "income"), 2)
    fixed_expense_total = round(sum(abs(item["amount"]) for item, flow in zip(parsed_transactions, cash_flow_classification) if flow["flow_type"] == "fixed_expense"), 2)
    variable_expense_total = round(sum(abs(item["amount"]) for item, flow in zip(parsed_transactions, cash_flow_classification) if flow["flow_type"] == "variable_expense"), 2)
    discretionary_total = round(sum(abs(item["amount"]) for item, flow in zip(parsed_transactions, cash_flow_classification) if flow["flow_type"] == "discretionary_expense"), 2)

    cash_flow_summary = {
        "income_total": income_total,
        "fixed_expense_total": fixed_expense_total,
        "variable_expense_total": variable_expense_total,
        "discretionary_total": discretionary_total,
        "net_cash_flow": round(
            income_total - fixed_expense_total - variable_expense_total - discretionary_total,
            2,
        ),
    }

    return (
        parsed_transactions,
        parsed_metadata,
        classified_transactions,
        classification_metadata,
        cash_flow_summary,
    )


def _build_statement_outcome(
    payload: Dict[str, Any],
    parsed_transactions: List[Dict[str, Any]],
    parsed_metadata: Dict[str, Any],
    classified_transactions: List[Dict[str, Any]],
    classification_metadata: Dict[str, Any],
    cash_flow_summary: Dict[str, float],
) -> Dict[str, Any]:
    document_metadata = payload.get("document_metadata")
    opening_balance = parsed_transactions[0]["balance"] if parsed_transactions and parsed_transactions[0]["balance"] is not None else None
    closing_balance = parsed_transactions[-1]["balance"] if parsed_transactions and parsed_transactions[-1]["balance"] is not None else None

    inflows = round(sum(item["amount"] for item in parsed_transactions if item["type"] == "credit"), 2)
    outflows = round(sum(abs(item["amount"]) for item in parsed_transactions if item["type"] == "debit"), 2)

    category_totals = {
        "fixed_expense": cash_flow_summary["fixed_expense_total"],
        "variable_expense": cash_flow_summary["variable_expense_total"],
        "discretionary": cash_flow_summary["discretionary_total"],
        "savings": round(
            sum(
                abs(item["amount"])
                for item, classified in zip(parsed_transactions, classified_transactions)
                if classified["primary_category"] == "savings or investment"
            ),
            2,
        ),
    }

    highlighted_transactions: List[Dict[str, Any]] = []
    for parsed, classified in zip(parsed_transactions, classified_transactions):
        if classified["primary_category"] in {"rent", "insurance", "loan repayment", "groceries", "entertainment"}:
            highlighted_transactions.append({
                "transaction_id": parsed["transaction_id"],
                "description": parsed["description"],
                "amount": abs(parsed["amount"]),
                "category": classified["primary_category"],
            })

    if not highlighted_transactions:
        for parsed, classified in zip(parsed_transactions[:3], classified_transactions[:3]):
            highlighted_transactions.append({
                "transaction_id": parsed["transaction_id"],
                "description": parsed["description"],
                "amount": abs(parsed["amount"]),
                "category": classified["primary_category"],
            })

    missing_data_flags: List[str] = []
    document_quality_flags: List[str] = []
    coverage_flags: List[str] = []

    if not parsed_transactions:
        missing_data_flags.append("parsed_transactions_missing")
    if not classified_transactions:
        missing_data_flags.append("classified_transactions_missing")
    if not cash_flow_summary:
        missing_data_flags.append("cash_flow_summary_missing")
    if not isinstance(document_metadata, dict):
        coverage_flags.append("document_metadata_unavailable")

    overall_confidence = round(
        (
            parsed_metadata.get("parsing_confidence", 0.0)
            + classification_metadata.get("classification_confidence_overall", 0.0)
        ) / 2,
        2,
    )

    section_confidence = {
        "balances": 0.95 if opening_balance is not None and closing_balance is not None else 0.7,
        "transactions": parsed_metadata.get("parsing_confidence", 0.0),
        "categories": classification_metadata.get("classification_confidence_overall", 0.0),
    }

    plain_language_explanation = (
        f"Your statement shows inflows of {inflows:.2f} and outflows of {outflows:.2f}. "
        f"Net cash flow for the period is {cash_flow_summary['net_cash_flow']:.2f}."
    )

    statement_summary = {
        "opening_balance": opening_balance,
        "closing_balance": closing_balance,
        "inflows": inflows,
        "outflows": outflows,
        "highlighted_transactions": highlighted_transactions,
        "category_totals": category_totals,
        "plain_language_explanation": plain_language_explanation,
    }

    balance_metrics = {
        "opening_balance": opening_balance,
        "closing_balance": closing_balance,
        "net_balance_change": round(
            ((closing_balance or 0.0) - (opening_balance or 0.0)),
            2,
        ) if opening_balance is not None and closing_balance is not None else None,
    }

    inflow_outflow_metrics = {
        "inflows": inflows,
        "outflows": outflows,
        "net_cash_flow": cash_flow_summary["net_cash_flow"],
    }

    service_status = dict(payload.get("service_status", {}))
    service_status["financial_management"] = "completed"

    return {
        "outcome_family": "analytical",
        "outcome_intent": "explain_document",
        "degradation_policy": "degrade_with_caveat",
        "missing_data_flags": missing_data_flags,
        "document_quality_flags": document_quality_flags,
        "coverage_flags": coverage_flags,
        "balance_metrics": balance_metrics,
        "inflow_outflow_metrics": inflow_outflow_metrics,
        "statement_summary": statement_summary,
        "overall_confidence": overall_confidence,
        "section_confidence": section_confidence,
        "processing_timestamp": _utc_now_iso(),
        "service_status": service_status,
    }


def run(payload: Dict[str, Any]) -> Dict[str, Any]:
    execution_plan_ack = _build_execution_plan_ack(payload)
    validation = _validate_execution_plan(payload, EXPECTED_SERVICE_FAMILY)

    if validation["status"] != "pass":
        return {
            "service": "financial_management",
            "status": "rejected",
            "execution_plan_ack": execution_plan_ack,
            "execution_plan_validation": validation,
            "received_payload": payload,
            "result": {
                "summary": "Worker rejected payload due to execution plan validation failure.",
            },
        }

    (
        parsed_transactions,
        parsed_metadata,
        classified_transactions,
        classification_metadata,
        cash_flow_summary,
    ) = _build_substrate(payload)

    fm_otc_001 = _build_statement_outcome(
        payload,
        parsed_transactions,
        parsed_metadata,
        classified_transactions,
        classification_metadata,
        cash_flow_summary,
    )

    return {
        "service": "financial_management",
        "status": "executed",
        "execution_plan_ack": execution_plan_ack,
        "execution_plan_validation": validation,
        "received_payload": payload,
        "result": {
            "summary": "Financial management worker executed with FM-OTC-001 governed outcome outputs.",
            "capabilities": [
                "transaction_parsing",
                "category_classification",
                "cash_flow_classification",
                "reporting_explanation",
            ],
            "parsed_transactions": parsed_transactions,
            "parsed_transactions_metadata": parsed_metadata,
            "classified_transactions": classified_transactions,
            "classified_transactions_metadata": classification_metadata,
            "cash_flow_summary": cash_flow_summary,
            "fm_otc_001": fm_otc_001,
        },
    }
