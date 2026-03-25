from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple


EXPECTED_SERVICE_FAMILY = "financial_management"
EXPECTED_STAGE = "downstream_execution"
SUPPORTED_PLAN_VERSIONS = {"execution_plan_v1"}


ALLOWED_MULTI_PERIOD_SCOPES = {
    "single_period_only",
    "multi_period_required",
    "comparative_required",
    "advanced_obligation_context_required",
}

ALLOWED_MULTI_PERIOD_REASON_CODES = {
    "over_multiple_statements",
    "rolling_period_view",
    "compare_prior_period",
    "stability_over_time",
    "health_tracking_over_time",
}

ALLOWED_MISSING_PERIOD_FLAGS = {
    "PRIOR_STATEMENT_HISTORY_MISSING",
    "PRIOR_PERIOD_COMPARISON_UNAVAILABLE",
    "PERIOD_GROUPING_INCOMPLETE",
    "NON_CONTIGUOUS_PERIOD_SEQUENCE",
}

ALLOWED_EXCLUSION_FLAGS = {
    "EXCLUDED_INCOMPLETE_PERIOD",
    "EXCLUDED_UNCOMPARABLE_PERIOD",
    "EXCLUDED_MISSING_SUBSTRATE",
}


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


def _resolve_selected_runtime_lock(payload: Dict[str, Any]) -> Dict[str, Any]:
    execution_plan = payload.get("execution_plan")
    if not isinstance(execution_plan, dict):
        return {}

    runtime_lock = execution_plan.get("governed_runtime_lock")
    if not isinstance(runtime_lock, dict):
        return {}

    return runtime_lock


def _validate_selected_runtime_lock(runtime_lock: Dict[str, Any]) -> Dict[str, Any]:
    errors: List[str] = []

    if not isinstance(runtime_lock, dict) or not runtime_lock:
        errors.append("governed_runtime_lock_missing")
        return {
            "status": "fail",
            "errors": errors,
        }

    if runtime_lock.get("service_family") != EXPECTED_SERVICE_FAMILY:
        errors.append("governed_runtime_lock_service_family_invalid")

    allowed_pairs = {
        ("FM-OTC-001", "fm_otc_001", "explain_document"),
        ("FM-OTC-002", "fm_otc_002", "analyse_cash_flow"),
        ("FM-OTC-003", "fm_otc_003", "analyse_spending_patterns"),
    }

    pair = (
        runtime_lock.get("governed_outcome_code"),
        runtime_lock.get("outcome_result_key"),
        runtime_lock.get("outcome_intent"),
    )
    if pair not in allowed_pairs:
        errors.append("governed_runtime_lock_outcome_invalid")

    return {
        "status": "pass" if not errors else "fail",
        "errors": errors,
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


def _build_substrate(
    payload: Dict[str, Any]
) -> Tuple[
    List[Dict[str, Any]],
    Dict[str, Any],
    List[Dict[str, Any]],
    Dict[str, Any],
    Dict[str, float],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
]:
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

    category_spend_summary = _build_category_spend_summary(
        parsed_transactions,
        classified_transactions,
    )
    category_spend_metrics = _build_category_spend_metrics(category_spend_summary)

    multi_period_substrate = _build_multi_period_substrate(
        payload,
        cash_flow_summary,
        category_spend_summary,
    )

    return (
        parsed_transactions,
        parsed_metadata,
        classified_transactions,
        classification_metadata,
        cash_flow_summary,
        category_spend_summary,
        category_spend_metrics,
        multi_period_substrate,
    )



def _dedupe_flags(values: List[str], allowed: set[str]) -> List[str]:
    result: List[str] = []
    for value in values:
        if value in allowed and value not in result:
            result.append(value)
    return result


def _normalize_multi_period_requirement_signal(payload: Dict[str, Any]) -> Dict[str, Any]:
    raw = payload.get("multi_period_requirement_signal")
    if not isinstance(raw, dict):
        return {
            "scope": "single_period_only",
            "reason_codes": [],
            "fail_closed": False,
        }

    scope = str(raw.get("scope") or "single_period_only").strip()
    if scope not in ALLOWED_MULTI_PERIOD_SCOPES:
        scope = "single_period_only"

    reason_codes: List[str] = []
    raw_reason_codes = raw.get("reason_codes")
    if isinstance(raw_reason_codes, list):
        for item in raw_reason_codes:
            code = str(item or "").strip()
            if code in ALLOWED_MULTI_PERIOD_REASON_CODES and code not in reason_codes:
                reason_codes.append(code)

    fail_closed = bool(raw.get("fail_closed", False))
    if scope == "single_period_only":
        fail_closed = False
    else:
        fail_closed = True

    return {
        "scope": scope,
        "reason_codes": reason_codes,
        "fail_closed": fail_closed,
    }


def _normalize_prior_statement_history(payload: Dict[str, Any]) -> Dict[str, Any]:
    raw = payload.get("prior_statement_history")
    if not isinstance(raw, dict):
        return {"periods": []}

    periods: List[Dict[str, Any]] = []
    raw_periods = raw.get("periods")
    if isinstance(raw_periods, list):
        for item in raw_periods:
            if not isinstance(item, dict):
                continue
            periods.append(
                {
                    "period_id": str(item.get("period_id") or "").strip(),
                    "period_start_date": str(item.get("period_start_date") or "").strip(),
                    "period_end_date": str(item.get("period_end_date") or "").strip(),
                    "statement_reference": str(item.get("statement_reference") or "").strip(),
                    "parsed_transactions": item.get("parsed_transactions") if isinstance(item.get("parsed_transactions"), list) else None,
                    "classified_transactions": item.get("classified_transactions") if isinstance(item.get("classified_transactions"), list) else None,
                    "cash_flow_summary": item.get("cash_flow_summary") if isinstance(item.get("cash_flow_summary"), dict) else None,
                    "debt_positions": item.get("debt_positions") if isinstance(item.get("debt_positions"), list) else None,
                    "account_context": item.get("account_context") if isinstance(item.get("account_context"), dict) else None,
                }
            )

    return {"periods": periods}


def _is_complete_current_period(period: Dict[str, Any]) -> bool:
    return bool(
        str(period.get("period_start_date") or "").strip()
        and str(period.get("period_end_date") or "").strip()
        and str(period.get("statement_reference") or "").strip()
    )


def _build_period_groupings(
    payload: Dict[str, Any],
    prior_statement_history: Dict[str, Any],
    missing_period_flags: List[str],
    exclusion_flags: List[str],
) -> Dict[str, Any]:
    document_metadata = payload.get("document_metadata")
    if not isinstance(document_metadata, dict):
        document_metadata = {}

    document_ids = payload.get("document_ids")
    current_statement_reference = str(
        document_metadata.get("statement_reference")
        or (document_ids[0] if isinstance(document_ids, list) and document_ids else "")
        or ""
    ).strip()

    current_period = {
        "period_start_date": str(document_metadata.get("period_start_date") or "").strip(),
        "period_end_date": str(document_metadata.get("period_end_date") or "").strip(),
        "statement_reference": current_statement_reference,
    }

    if not _is_complete_current_period(current_period):
        missing_period_flags.append("PERIOD_GROUPING_INCOMPLETE")

    prior_periods: List[Dict[str, str]] = []
    for item in prior_statement_history.get("periods", []):
        period_block = {
            "period_id": str(item.get("period_id") or "").strip(),
            "period_start_date": str(item.get("period_start_date") or "").strip(),
            "period_end_date": str(item.get("period_end_date") or "").strip(),
            "statement_reference": str(item.get("statement_reference") or "").strip(),
        }
        if not all(period_block.values()):
            exclusion_flags.append("EXCLUDED_INCOMPLETE_PERIOD")
            continue
        prior_periods.append(period_block)

    return {
        "grouping_basis": "statement_period",
        "current_period": current_period,
        "prior_periods": prior_periods,
    }


def _build_metric_value_map(cash_flow_summary: Dict[str, float]) -> Dict[str, float]:
    return {
        "income_total": round(_safe_float(cash_flow_summary.get("income_total")), 2),
        "fixed_expense_total": round(_safe_float(cash_flow_summary.get("fixed_expense_total")), 2),
        "variable_expense_total": round(_safe_float(cash_flow_summary.get("variable_expense_total")), 2),
        "discretionary_total": round(_safe_float(cash_flow_summary.get("discretionary_total")), 2),
        "net_cash_flow": round(_safe_float(cash_flow_summary.get("net_cash_flow")), 2),
    }


def _select_usable_prior_period(
    prior_statement_history: Dict[str, Any],
    exclusion_flags: List[str],
) -> Optional[Dict[str, Any]]:
    usable_periods: List[Dict[str, Any]] = []

    for item in prior_statement_history.get("periods", []):
        if not (
            str(item.get("period_id") or "").strip()
            and str(item.get("period_start_date") or "").strip()
            and str(item.get("period_end_date") or "").strip()
            and str(item.get("statement_reference") or "").strip()
        ):
            continue

        if not isinstance(item.get("cash_flow_summary"), dict):
            exclusion_flags.append("EXCLUDED_MISSING_SUBSTRATE")
            continue

        usable_periods.append(item)

    if not usable_periods:
        return None

    return usable_periods[0]


def _build_trend_metrics(
    cash_flow_summary: Dict[str, float],
    prior_statement_history: Dict[str, Any],
    exclusion_flags: List[str],
) -> List[Dict[str, Any]]:
    prior_period = _select_usable_prior_period(prior_statement_history, exclusion_flags)
    if not prior_period:
        return []

    usable_period_count = 0
    for item in prior_statement_history.get("periods", []):
        if (
            isinstance(item, dict)
            and isinstance(item.get("cash_flow_summary"), dict)
            and str(item.get("period_id") or "").strip()
            and str(item.get("period_start_date") or "").strip()
            and str(item.get("period_end_date") or "").strip()
            and str(item.get("statement_reference") or "").strip()
        ):
            usable_period_count += 1

    comparison_basis = "rolling_multi_period" if usable_period_count > 1 else "current_vs_prior"
    current_values = _build_metric_value_map(cash_flow_summary)
    prior_values = _build_metric_value_map(prior_period.get("cash_flow_summary") or {})

    trend_metrics: List[Dict[str, Any]] = []
    for metric_name, current_value in current_values.items():
        prior_value = prior_values.get(metric_name)
        absolute_change = round(current_value - prior_value, 2)
        percent_change = None
        if prior_value not in (None, 0):
            percent_change = round((absolute_change / prior_value) * 100.0, 2)

        direction = "flat"
        if current_value > prior_value:
            direction = "increase"
        elif current_value < prior_value:
            direction = "decrease"

        trend_metrics.append(
            {
                "metric_name": metric_name,
                "comparison_basis": comparison_basis,
                "current_value": current_value,
                "prior_value": prior_value,
                "absolute_change": absolute_change,
                "percent_change": percent_change,
                "direction": direction if prior_value is not None else "unknown",
            }
        )

    return trend_metrics




def _build_category_spend_summary(
    parsed_transactions: list,
    classified_transactions: list,
) -> dict:
    category_totals = {}

    for parsed, classified in zip(parsed_transactions, classified_transactions):
        category = classified.get("primary_category") or "unknown"
        amount = abs(parsed.get("amount") or 0.0)

        if parsed.get("type") == "debit":
            category_totals[category] = round(category_totals.get(category, 0.0) + amount, 2)

    return {
        "category_totals": category_totals
    }


def _build_category_spend_metrics(
    category_spend_summary: dict,
) -> dict:
    category_totals = category_spend_summary.get("category_totals", {})

    total_spend = round(sum(category_totals.values()), 2)

    category_percentages = {}
    for k, v in category_totals.items():
        if total_spend > 0:
            category_percentages[k] = round((v / total_spend) * 100.0, 2)
        else:
            category_percentages[k] = 0.0

    return {
        "total_spend": total_spend,
        "category_percentages": category_percentages,
    }




def _select_usable_prior_spend_period(
    prior_statement_history: Dict[str, Any],
    exclusion_flags: List[str],
) -> Optional[Dict[str, Any]]:
    usable_periods: List[Dict[str, Any]] = []

    for item in prior_statement_history.get("periods", []):
        if not (
            str(item.get("period_id") or "").strip()
            and str(item.get("period_start_date") or "").strip()
            and str(item.get("period_end_date") or "").strip()
            and str(item.get("statement_reference") or "").strip()
        ):
            continue

        parsed_transactions = item.get("parsed_transactions")
        classified_transactions = item.get("classified_transactions")

        if not isinstance(parsed_transactions, list) or not isinstance(classified_transactions, list):
            exclusion_flags.append("EXCLUDED_MISSING_SUBSTRATE")
            continue

        usable_periods.append(item)

    if not usable_periods:
        return None

    return usable_periods[0]


def _build_spending_trend_metrics(
    category_spend_summary: Dict[str, Any],
    prior_statement_history: Dict[str, Any],
    exclusion_flags: List[str],
) -> List[Dict[str, Any]]:
    prior_period = _select_usable_prior_spend_period(prior_statement_history, exclusion_flags)
    if not prior_period:
        return []

    usable_period_count = 0
    for item in prior_statement_history.get("periods", []):
        if (
            isinstance(item, dict)
            and isinstance(item.get("parsed_transactions"), list)
            and isinstance(item.get("classified_transactions"), list)
            and str(item.get("period_id") or "").strip()
            and str(item.get("period_start_date") or "").strip()
            and str(item.get("period_end_date") or "").strip()
            and str(item.get("statement_reference") or "").strip()
        ):
            usable_period_count += 1

    prior_category_spend_summary = _build_category_spend_summary(
        prior_period.get("parsed_transactions") or [],
        prior_period.get("classified_transactions") or [],
    )

    comparison_basis = "rolling_multi_period" if usable_period_count > 1 else "current_vs_prior"
    current_totals = category_spend_summary.get("category_totals", {})
    prior_totals = prior_category_spend_summary.get("category_totals", {})

    metric_names = sorted(set(current_totals.keys()) | set(prior_totals.keys()))
    trend_metrics: List[Dict[str, Any]] = []

    for metric_name in metric_names:
        current_value = round(float(current_totals.get(metric_name, 0.0) or 0.0), 2)
        prior_value = round(float(prior_totals.get(metric_name, 0.0) or 0.0), 2)
        absolute_change = round(current_value - prior_value, 2)

        percent_change = None
        if prior_value not in (None, 0):
            percent_change = round((absolute_change / prior_value) * 100.0, 2)

        direction = "flat"
        if current_value > prior_value:
            direction = "increase"
        elif current_value < prior_value:
            direction = "decrease"

        trend_metrics.append(
            {
                "metric_name": metric_name,
                "comparison_basis": comparison_basis,
                "current_value": current_value,
                "prior_value": prior_value,
                "absolute_change": absolute_change,
                "percent_change": percent_change,
                "direction": direction if prior_value is not None else "unknown",
            }
        )

    return trend_metrics


def _build_multi_period_substrate(
    payload: Dict[str, Any],
    cash_flow_summary: Dict[str, float],
    category_spend_summary: Dict[str, Any],
) -> Dict[str, Any]:
    multi_period_requirement_signal = _normalize_multi_period_requirement_signal(payload)
    prior_statement_history = _normalize_prior_statement_history(payload)

    missing_period_flags: List[str] = []
    exclusion_flags: List[str] = []

    period_groupings = _build_period_groupings(
        payload,
        prior_statement_history,
        missing_period_flags,
        exclusion_flags,
    )
    trend_metrics = _build_trend_metrics(
        cash_flow_summary,
        prior_statement_history,
        exclusion_flags,
    )
    spending_trend_metrics = _build_spending_trend_metrics(
        category_spend_summary,
        prior_statement_history,
        exclusion_flags,
    )

    scope = multi_period_requirement_signal["scope"]
    periods = prior_statement_history.get("periods", [])

    if scope in {"multi_period_required", "advanced_obligation_context_required"} and not periods:
        missing_period_flags.append("PRIOR_STATEMENT_HISTORY_MISSING")

    if scope == "comparative_required" and not spending_trend_metrics:
        missing_period_flags.append("PRIOR_PERIOD_COMPARISON_UNAVAILABLE")

    missing_period_flags = _dedupe_flags(missing_period_flags, ALLOWED_MISSING_PERIOD_FLAGS)
    exclusion_flags = _dedupe_flags(exclusion_flags, ALLOWED_EXCLUSION_FLAGS)

    substrate_fail_closed = False
    if multi_period_requirement_signal["fail_closed"]:
        if "PERIOD_GROUPING_INCOMPLETE" in missing_period_flags:
            substrate_fail_closed = True
        elif scope in {"multi_period_required", "advanced_obligation_context_required"} and "PRIOR_STATEMENT_HISTORY_MISSING" in missing_period_flags:
            substrate_fail_closed = True
        elif scope == "comparative_required" and "PRIOR_PERIOD_COMPARISON_UNAVAILABLE" in missing_period_flags:
            substrate_fail_closed = True
        elif scope == "comparative_required" and not spending_trend_metrics:
            substrate_fail_closed = True
        elif scope in {"multi_period_required", "advanced_obligation_context_required"} and not trend_metrics:
            substrate_fail_closed = True

    return {
        "multi_period_requirement_signal": multi_period_requirement_signal,
        "prior_statement_history": prior_statement_history,
        "period_groupings": period_groupings,
        "trend_metrics": trend_metrics,
        "spending_trend_metrics": spending_trend_metrics,
        "missing_period_flags": missing_period_flags,
        "exclusion_flags": exclusion_flags,
        "substrate_fail_closed": substrate_fail_closed,
    }


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



def _validate_cash_flow_outcome_internal_contract(
    outcome: Dict[str, Any],
    audience_mode: str,
) -> Dict[str, Any]:
    errors: List[str] = []

    if not isinstance(outcome, dict):
        return {
            "status": "fail",
            "errors": ["fm_otc_002_not_dict"],
        }

    if outcome.get("outcome_intent") != "analyse_cash_flow":
        errors.append("fm_otc_002_outcome_intent_invalid")

    missing_period_flags = outcome.get("missing_period_flags")
    if not isinstance(missing_period_flags, list):
        errors.append("fm_otc_002_missing_period_flags_missing")
    elif any(flag not in ALLOWED_MISSING_PERIOD_FLAGS for flag in missing_period_flags):
        errors.append("fm_otc_002_missing_period_flags_invalid")

    exclusion_flags = outcome.get("exclusion_flags")
    if not isinstance(exclusion_flags, list):
        errors.append("fm_otc_002_exclusion_flags_missing")
    elif any(flag not in ALLOWED_EXCLUSION_FLAGS for flag in exclusion_flags):
        errors.append("fm_otc_002_exclusion_flags_invalid")

    inflow_outflow_metrics = outcome.get("inflow_outflow_metrics")
    required_inflow_outflow_keys = {"inflows", "outflows", "net_cash_flow"}
    if not isinstance(inflow_outflow_metrics, dict):
        errors.append("fm_otc_002_inflow_outflow_metrics_missing")
    elif not required_inflow_outflow_keys.issubset(inflow_outflow_metrics.keys()):
        errors.append("fm_otc_002_inflow_outflow_metrics_incomplete")

    trend_metrics = outcome.get("trend_metrics")
    if not isinstance(trend_metrics, list):
        errors.append("fm_otc_002_trend_metrics_missing")

    cash_flow_summary = outcome.get("cash_flow_summary")
    required_cash_flow_summary_keys = {
        "income_total",
        "fixed_expense_total",
        "variable_expense_total",
        "discretionary_total",
        "net_cash_flow",
    }
    if not isinstance(cash_flow_summary, dict):
        errors.append("fm_otc_002_cash_flow_summary_missing")
    elif not required_cash_flow_summary_keys.issubset(cash_flow_summary.keys()):
        errors.append("fm_otc_002_cash_flow_summary_incomplete")

    if outcome.get("overall_confidence") is None:
        errors.append("fm_otc_002_overall_confidence_missing")

    if audience_mode == "internal":
        inclusion_exclusion_trace = outcome.get("inclusion_exclusion_trace")
        required_trace_keys = {
            "multi_period_scope",
            "included_prior_period_ids",
            "excluded_flags",
            "substrate_fail_closed",
        }
        if not isinstance(inclusion_exclusion_trace, dict):
            errors.append("fm_otc_002_inclusion_exclusion_trace_missing")
        elif not required_trace_keys.issubset(inclusion_exclusion_trace.keys()):
            errors.append("fm_otc_002_inclusion_exclusion_trace_incomplete")

    return {
        "status": "pass" if not errors else "fail",
        "errors": errors,
    }


def _build_cash_flow_outcome_internal(
    payload: Dict[str, Any],
    parsed_transactions: List[Dict[str, Any]],
    parsed_metadata: Dict[str, Any],
    classified_transactions: List[Dict[str, Any]],
    classification_metadata: Dict[str, Any],
    cash_flow_summary: Dict[str, float],
    multi_period_substrate: Dict[str, Any],
) -> Dict[str, Any]:
    inflows = round(sum(item["amount"] for item in parsed_transactions if item["type"] == "credit"), 2)
    outflows = round(sum(abs(item["amount"]) for item in parsed_transactions if item["type"] == "debit"), 2)

    overall_confidence = round(
        (
            parsed_metadata.get("parsing_confidence", 0.0)
            + classification_metadata.get("classification_confidence_overall", 0.0)
        ) / 2,
        2,
    )

    period_groupings = multi_period_substrate.get("period_groupings", {})
    prior_periods = period_groupings.get("prior_periods", []) if isinstance(period_groupings, dict) else []
    audience_mode = str(payload.get("audience_mode") or "internal").strip().lower()

    result = {
        "outcome_family": "analytical",
        "outcome_intent": "analyse_cash_flow",
        "degradation_policy": "degrade_with_caveat",
        "missing_period_flags": list(multi_period_substrate.get("missing_period_flags", [])),
        "exclusion_flags": list(multi_period_substrate.get("exclusion_flags", [])),
        "inflow_outflow_metrics": {
            "inflows": inflows,
            "outflows": outflows,
            "net_cash_flow": cash_flow_summary["net_cash_flow"],
        },
        "trend_metrics": list(multi_period_substrate.get("trend_metrics", [])),
        "cash_flow_summary": {
            "income_total": cash_flow_summary["income_total"],
            "fixed_expense_total": cash_flow_summary["fixed_expense_total"],
            "variable_expense_total": cash_flow_summary["variable_expense_total"],
            "discretionary_total": cash_flow_summary["discretionary_total"],
            "net_cash_flow": cash_flow_summary["net_cash_flow"],
        },
        "overall_confidence": overall_confidence,
    }

    if audience_mode == "internal":
        result["inclusion_exclusion_trace"] = {
            "multi_period_scope": (multi_period_substrate.get("multi_period_requirement_signal") or {}).get("scope"),
            "included_prior_period_ids": [
                item.get("period_id")
                for item in prior_periods
                if isinstance(item, dict) and item.get("period_id")
            ],
            "excluded_flags": list(multi_period_substrate.get("exclusion_flags", [])),
            "substrate_fail_closed": bool(multi_period_substrate.get("substrate_fail_closed", False)),
        }

    return result




def _validate_spending_outcome_internal_contract(
    outcome: Dict[str, Any],
    audience_mode: str,
) -> Dict[str, Any]:
    errors: List[str] = []

    if not isinstance(outcome, dict):
        return {
            "status": "fail",
            "errors": ["fm_otc_003_not_dict"],
        }

    if outcome.get("outcome_intent") != "analyse_spending_patterns":
        errors.append("fm_otc_003_outcome_intent_invalid")

    missing_data_flags = outcome.get("missing_data_flags")
    if not isinstance(missing_data_flags, list):
        errors.append("fm_otc_003_missing_data_flags_missing")

    caveat_flags = outcome.get("caveat_flags")
    if not isinstance(caveat_flags, list):
        errors.append("fm_otc_003_caveat_flags_missing")

    category_spend_metrics = outcome.get("category_spend_metrics")
    required_metric_keys = {"total_spend", "category_percentages"}
    if not isinstance(category_spend_metrics, dict):
        errors.append("fm_otc_003_category_spend_metrics_missing")
    elif not required_metric_keys.issubset(category_spend_metrics.keys()):
        errors.append("fm_otc_003_category_spend_metrics_incomplete")

    trend_metrics = outcome.get("trend_metrics")
    if not isinstance(trend_metrics, list):
        errors.append("fm_otc_003_trend_metrics_missing")

    spending_summary = outcome.get("spending_summary")
    required_summary_keys = {"category_totals", "top_spend_categories", "comparative_summary"}
    if not isinstance(spending_summary, dict):
        errors.append("fm_otc_003_spending_summary_missing")
    elif not required_summary_keys.issubset(spending_summary.keys()):
        errors.append("fm_otc_003_spending_summary_incomplete")

    if outcome.get("overall_confidence") is None:
        errors.append("fm_otc_003_overall_confidence_missing")
    if outcome.get("category_confidence") is None:
        errors.append("fm_otc_003_category_confidence_missing")
    if outcome.get("merchant_confidence") is None:
        errors.append("fm_otc_003_merchant_confidence_missing")

    if audience_mode == "internal":
        section_confidence_trace = outcome.get("section_confidence_trace")
        required_trace_keys = {
            "transactions",
            "categories",
            "comparison_basis",
            "included_prior_period_ids",
        }
        if not isinstance(section_confidence_trace, dict):
            errors.append("fm_otc_003_section_confidence_trace_missing")
        elif not required_trace_keys.issubset(section_confidence_trace.keys()):
            errors.append("fm_otc_003_section_confidence_trace_incomplete")

    return {
        "status": "pass" if not errors else "fail",
        "errors": errors,
    }


def _build_spending_outcome_internal(
    payload: Dict[str, Any],
    parsed_transactions: List[Dict[str, Any]],
    parsed_metadata: Dict[str, Any],
    classified_transactions: List[Dict[str, Any]],
    classification_metadata: Dict[str, Any],
    category_spend_summary: Dict[str, Any],
    category_spend_metrics: Dict[str, Any],
    multi_period_substrate: Dict[str, Any],
) -> Dict[str, Any]:
    audience_mode = str(payload.get("audience_mode") or "internal").strip().lower()
    spending_trend_metrics = list(multi_period_substrate.get("spending_trend_metrics", []))
    period_groupings = multi_period_substrate.get("period_groupings", {})
    prior_periods = period_groupings.get("prior_periods", []) if isinstance(period_groupings, dict) else []

    missing_data_flags: List[str] = []
    if not parsed_transactions:
        missing_data_flags.append("parsed_transactions_missing")
    if not classified_transactions:
        missing_data_flags.append("classified_transactions_missing")
    if not category_spend_summary.get("category_totals"):
        missing_data_flags.append("category_spend_summary_missing")
    if not spending_trend_metrics:
        missing_data_flags.append("trend_metrics_missing")

    caveat_flags: List[str] = []
    caveat_flags.extend(list(multi_period_substrate.get("missing_period_flags", [])))
    caveat_flags.extend(list(multi_period_substrate.get("exclusion_flags", [])))

    top_spend_categories = [
        {"category": category, "amount": amount}
        for category, amount in sorted(
            category_spend_summary.get("category_totals", {}).items(),
            key=lambda item: (-item[1], item[0]),
        )[:5]
    ]

    comparative_summary = {
        "comparison_basis": spending_trend_metrics[0]["comparison_basis"] if spending_trend_metrics else "current_vs_prior",
        "changed_categories": len(spending_trend_metrics),
    }

    overall_confidence = round(
        (
            parsed_metadata.get("parsing_confidence", 0.0)
            + classification_metadata.get("classification_confidence_overall", 0.0)
        ) / 2,
        2,
    )
    category_confidence = round(classification_metadata.get("classification_confidence_overall", 0.0), 2)
    merchant_confidence = round(classification_metadata.get("classification_confidence_overall", 0.0), 2)

    result = {
        "outcome_family": "analytical",
        "outcome_intent": "analyse_spending_patterns",
        "degradation_policy": "degrade_with_caveat",
        "missing_data_flags": missing_data_flags,
        "caveat_flags": caveat_flags,
        "category_spend_metrics": category_spend_metrics,
        "trend_metrics": spending_trend_metrics,
        "spending_summary": {
            "category_totals": category_spend_summary.get("category_totals", {}),
            "top_spend_categories": top_spend_categories,
            "comparative_summary": comparative_summary,
        },
        "overall_confidence": overall_confidence,
        "category_confidence": category_confidence,
        "merchant_confidence": merchant_confidence,
        "processing_timestamp": _utc_now_iso(),
        "service_status": dict(payload.get("service_status", {})),
    }

    result["service_status"]["financial_management"] = "completed"

    if audience_mode == "internal":
        result["section_confidence_trace"] = {
            "transactions": parsed_metadata.get("parsing_confidence", 0.0),
            "categories": classification_metadata.get("classification_confidence_overall", 0.0),
            "comparison_basis": comparative_summary["comparison_basis"],
            "included_prior_period_ids": [
                item.get("period_id")
                for item in prior_periods
                if isinstance(item, dict) and item.get("period_id")
            ],
        }

    return result


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

    selected_runtime_lock = _resolve_selected_runtime_lock(payload)
    selected_runtime_lock_validation = _validate_selected_runtime_lock(selected_runtime_lock)

    if selected_runtime_lock_validation["status"] != "pass":
        return {
            "service": "financial_management",
            "status": "rejected",
            "execution_plan_ack": execution_plan_ack,
            "execution_plan_validation": validation,
            "received_payload": payload,
            "result": {
                "summary": "Worker rejected payload due to governed runtime lock validation failure.",
                "runtime_lock_validation": selected_runtime_lock_validation,
            },
        }

    (
        parsed_transactions,
        parsed_metadata,
        classified_transactions,
        classification_metadata,
        cash_flow_summary,
        category_spend_summary,
        category_spend_metrics,
        multi_period_substrate,
    ) = _build_substrate(payload)

    fm_otc_001 = _build_statement_outcome(
        payload,
        parsed_transactions,
        parsed_metadata,
        classified_transactions,
        classification_metadata,
        cash_flow_summary,
    )

    _selected_cash_flow_outcome = _build_cash_flow_outcome_internal(
        payload,
        parsed_transactions,
        parsed_metadata,
        classified_transactions,
        classification_metadata,
        cash_flow_summary,
        multi_period_substrate,
    )

    _selected_cash_flow_validation = _validate_cash_flow_outcome_internal_contract(
        _selected_cash_flow_outcome,
        str(payload.get("audience_mode") or "internal").strip().lower(),
    )

    _selected_spending_outcome = _build_spending_outcome_internal(
        payload,
        parsed_transactions,
        parsed_metadata,
        classified_transactions,
        classification_metadata,
        category_spend_summary,
        category_spend_metrics,
        multi_period_substrate,
    )

    _selected_spending_validation = _validate_spending_outcome_internal_contract(
        _selected_spending_outcome,
        str(payload.get("audience_mode") or "internal").strip().lower(),
    )

    cash_flow_outcome_internal_status = "valid"
    cash_flow_outcome_internal_available = True
    cash_flow_outcome_internal_summary = "Internal FM-OTC-002 contract validation passed."

    if _selected_cash_flow_validation["status"] != "pass":
        cash_flow_outcome_internal_status = "invalid"
        cash_flow_outcome_internal_available = False
        cash_flow_outcome_internal_summary = "Internal FM-OTC-002 contract validation failed; FM-OTC-002 remains unavailable."

    spending_outcome_internal_status = "valid"
    spending_outcome_internal_available = True
    spending_outcome_internal_summary = "Internal FM-OTC-003 contract validation passed."

    if _selected_spending_validation["status"] != "pass":
        spending_outcome_internal_status = "invalid"
        spending_outcome_internal_available = False
        spending_outcome_internal_summary = "Internal FM-OTC-003 contract validation failed; FM-OTC-003 remains unavailable."

    selected_outcome_code = selected_runtime_lock.get("governed_outcome_code")
    selected_outcome_key = selected_runtime_lock.get("outcome_result_key")
    selected_outcome_intent = selected_runtime_lock.get("outcome_intent")

    outward_result = None
    outward_summary = None

    if selected_outcome_code == "FM-OTC-001":
        outward_result = {
            "fm_otc_001": fm_otc_001,
        }
        outward_summary = "Financial management worker executed with FM-OTC-001 governed outcome outputs."

    elif selected_outcome_code == "FM-OTC-002":
        if _selected_cash_flow_validation["status"] != "pass":
            return {
                "service": "financial_management",
                "status": "rejected",
                "execution_plan_ack": execution_plan_ack,
                "execution_plan_validation": validation,
                "received_payload": payload,
                "result": {
                    "summary": "Worker rejected payload because selected FM-OTC-002 outcome contract is invalid.",
                    "runtime_lock_validation": selected_runtime_lock_validation,
                    "cash_flow_outcome_internal_validation": _selected_cash_flow_validation,
                },
            }

        if bool(multi_period_substrate.get("substrate_fail_closed", False)):
            return {
                "service": "financial_management",
                "status": "rejected",
                "execution_plan_ack": execution_plan_ack,
                "execution_plan_validation": validation,
                "received_payload": payload,
                "result": {
                    "summary": "Worker rejected payload because selected FM-OTC-002 requires sufficient governed multi-period substrate.",
                    "runtime_lock_validation": selected_runtime_lock_validation,
                    "cash_flow_outcome_internal_validation": _selected_cash_flow_validation,
                    "multi_period_substrate": {
                        "multi_period_requirement_signal": multi_period_substrate.get("multi_period_requirement_signal"),
                        "missing_period_flags": multi_period_substrate.get("missing_period_flags", []),
                        "exclusion_flags": multi_period_substrate.get("exclusion_flags", []),
                        "substrate_fail_closed": multi_period_substrate.get("substrate_fail_closed", False),
                    },
                },
            }

        outward_result = {
            "fm_otc_002": _selected_cash_flow_outcome,
        }
        outward_summary = "Financial management worker executed with FM-OTC-002 governed outcome outputs."

    elif selected_outcome_code == "FM-OTC-003":
        if _selected_spending_validation["status"] != "pass":
            return {
                "service": "financial_management",
                "status": "rejected",
                "execution_plan_ack": execution_plan_ack,
                "execution_plan_validation": validation,
                "received_payload": payload,
                "result": {
                    "summary": "Worker rejected payload because selected FM-OTC-003 outcome contract is invalid.",
                    "runtime_lock_validation": selected_runtime_lock_validation,
                    "spending_outcome_internal_validation": _selected_spending_validation,
                },
            }

        if bool(multi_period_substrate.get("substrate_fail_closed", False)):
            return {
                "service": "financial_management",
                "status": "rejected",
                "execution_plan_ack": execution_plan_ack,
                "execution_plan_validation": validation,
                "received_payload": payload,
                "result": {
                    "summary": "Worker rejected payload because selected FM-OTC-003 requires sufficient governed comparative spending substrate.",
                    "runtime_lock_validation": selected_runtime_lock_validation,
                    "spending_outcome_internal_validation": _selected_spending_validation,
                    "multi_period_substrate": {
                        "multi_period_requirement_signal": multi_period_substrate.get("multi_period_requirement_signal"),
                        "missing_period_flags": multi_period_substrate.get("missing_period_flags", []),
                        "exclusion_flags": multi_period_substrate.get("exclusion_flags", []),
                        "substrate_fail_closed": multi_period_substrate.get("substrate_fail_closed", False),
                    },
                },
            }

        outward_result = {
            "fm_otc_003": _selected_spending_outcome,
        }
        outward_summary = "Financial management worker executed with FM-OTC-003 governed outcome outputs."

    else:
        return {
            "service": "financial_management",
            "status": "rejected",
            "execution_plan_ack": execution_plan_ack,
            "execution_plan_validation": validation,
            "received_payload": payload,
            "result": {
                "summary": "Worker rejected payload due to unsupported governed outcome selection.",
                "runtime_lock_validation": selected_runtime_lock_validation,
            },
        }

    if selected_outcome_key not in outward_result:
        return {
            "service": "financial_management",
            "status": "rejected",
            "execution_plan_ack": execution_plan_ack,
            "execution_plan_validation": validation,
            "received_payload": payload,
            "result": {
                "summary": "Worker rejected payload because outward governed outcome key did not match runtime lock.",
                "runtime_lock_validation": selected_runtime_lock_validation,
            },
        }

    selected_block = outward_result[selected_outcome_key]
    if not isinstance(selected_block, dict) or selected_block.get("outcome_intent") != selected_outcome_intent:
        return {
            "service": "financial_management",
            "status": "rejected",
            "execution_plan_ack": execution_plan_ack,
            "execution_plan_validation": validation,
            "received_payload": payload,
            "result": {
                "summary": "Worker rejected payload because outward governed outcome intent did not match runtime lock.",
                "runtime_lock_validation": selected_runtime_lock_validation,
            },
        }

    return {
        "service": "financial_management",
        "status": "executed",
        "execution_plan_ack": execution_plan_ack,
        "execution_plan_validation": validation,
        "received_payload": payload,
        "result": {
            "summary": outward_summary,
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
            **outward_result,
        },
    }
