from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List


EXPECTED_SERVICE_FAMILY = "credit_decision"
EXPECTED_STAGE = "downstream_execution"
SUPPORTED_PLAN_VERSIONS = {"execution_plan_v1"}

CREDIT_OTC_001_ALLOWED_REQUESTS = {
    ("document_verification_fraud_check", "standard_internal_review", "internal"),
}

CREDIT_OTC_002_ALLOWED_REQUESTS = {
    ("affordability_assessment", "standard_affordability", "internal"),
}

CREDIT_OTC_003_ALLOWED_REQUESTS = {
    ("credit_risk_scoring", "standard_risk_assessment", "internal"),
}

CREDIT_OTC_004_ALLOWED_REQUESTS = {
    ("collections_timing_optimisation", "standard_collections_guidance", "internal"),
}

CREDIT_OTC_005_ALLOWED_REQUESTS = {
    ("customer_credit_decision_status", "customer_status_only", "customer"),
}

def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_float(value: Any) -> float:
    try:
        if value in (None, ""):
            return 0.0
        return round(float(value), 2)
    except Exception:
        return 0.0


def _normalize_type(raw_type: Any, amount: float) -> str:
    normalized = str(raw_type or "").strip().lower()
    if normalized in {"credit", "cr", "deposit", "inflow"}:
        return "credit"
    if normalized in {"debit", "dr", "withdrawal", "outflow"}:
        return "debit"
    return "credit" if amount >= 0 else "debit"


def _normalize_transaction(raw: Dict[str, Any], index: int) -> Dict[str, Any]:
    amount = _safe_float(raw.get("amount"))
    balance_raw = raw.get("balance")
    transaction_type = _normalize_type(raw.get("type"), amount)

    return {
        "transaction_id": str(raw.get("transaction_id") or raw.get("id") or f"txn-{index:04d}"),
        "date": str(raw.get("date") or ""),
        "description": str(raw.get("description") or raw.get("narration") or ""),
        "amount": amount,
        "type": transaction_type,
        "balance": _safe_float(balance_raw) if balance_raw not in (None, "") else None,
        "confidence": 0.95,
    }


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
        return {"status": "fail", "errors": errors}

    execution_plan = payload.get("execution_plan")
    if not isinstance(execution_plan, dict):
        errors.append("execution_plan_missing")
        return {"status": "fail", "errors": errors}

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

    return {"status": "pass" if not errors else "fail", "errors": errors}



def _safe_dict(value: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _safe_list(value: Any) -> List[Any]:
    return value if isinstance(value, list) else []


GOVERNED_CREDIT_OUTCOME_MAP = {
    "Credit-OTC-001": {
        "outcome_intent": "extract_payslip_fields",
        "analysis_type": "payslip_ocr_extraction",
    },
    "Credit-OTC-002": {
        "outcome_intent": "assess_payslip_income_validity",
        "analysis_type": "payslip_income_validity_check",
    },
    "Credit-OTC-003": {
        "outcome_intent": "extract_bank_statement_fields",
        "analysis_type": "bank_statement_ocr_extraction",
    },
    "Credit-OTC-004": {
        "outcome_intent": "assess_bank_statement_income_signal",
        "analysis_type": "bank_statement_income_signal_assessment",
    },
    "Credit-OTC-005": {
        "outcome_intent": "assess_bank_statement_expense_signal",
        "analysis_type": "bank_statement_expense_signal_assessment",
    },
    "Credit-OTC-006": {
        "outcome_intent": "assess_payslip_to_bank_income_consistency",
        "analysis_type": "payslip_to_bank_income_consistency",
    },
    "Credit-OTC-007": {
        "outcome_intent": "produce_ocr_based_affordability_snapshot",
        "analysis_type": "ocr_based_affordability_snapshot",
    },
    "Credit-OTC-008": {
        "outcome_intent": "assess_credit_document_pack_completeness",
        "analysis_type": "credit_document_pack_completeness",
    },
    "Credit-OTC-009": {
        "outcome_intent": "produce_ocr_based_credit_recommendation",
        "analysis_type": "ocr_based_credit_recommendation",
    },
}

LEGACY_FALLBACK_ALLOWED_REQUESTS = {}


def _normalize_selector(payload: Dict[str, Any]) -> Dict[str, str]:
    orchestration_context = _safe_dict(payload.get("orchestration_context"))
    return {
        "analysis_type": str(
            orchestration_context.get("analysis_type") or payload.get("analysis_type") or ""
        ).strip().lower(),
        "audience_mode": str(payload.get("audience_mode") or "internal").strip().lower(),
        "governed_outcome_code": str(
            orchestration_context.get("governed_outcome_code")
            or payload.get("governed_outcome_code")
            or ""
        ).strip(),
        "governed_outcome_intent": str(
            orchestration_context.get("governed_outcome_intent")
            or payload.get("governed_outcome_intent")
            or ""
        ).strip(),
        "requested_service": str(payload.get("requested_service") or "").strip().lower(),
        "requested_option_set": str(payload.get("requested_option_set") or "").strip().lower(),
    }


def _validate_selector(selector: Dict[str, str]) -> Dict[str, Any]:
    errors: List[str] = []

    governed_outcome_code = selector["governed_outcome_code"]
    governed_outcome_intent = selector["governed_outcome_intent"]
    analysis_type = selector["analysis_type"]

    if governed_outcome_code:
        governed = GOVERNED_CREDIT_OUTCOME_MAP.get(governed_outcome_code)
        if not governed:
            errors.append("unsupported_credit_governed_outcome_code")
        else:
            if not governed_outcome_intent:
                errors.append("governed_outcome_intent_missing")
            elif governed_outcome_intent != governed["outcome_intent"]:
                errors.append("governed_outcome_intent_mismatch")

            if not analysis_type:
                errors.append("analysis_type_missing")
            elif analysis_type != governed["analysis_type"]:
                errors.append("analysis_type_mismatch")

        return {
            "status": "pass" if not errors else "fail",
            "errors": errors,
            "matched_governed_outcome_code": governed_outcome_code if not errors else None,
            "matched_outcome_intent": governed_outcome_intent if not errors else None,
        }

    key = (
        selector["requested_service"],
        selector["requested_option_set"],
        selector["audience_mode"],
    )
    legacy_match = LEGACY_FALLBACK_ALLOWED_REQUESTS.get(key)
    if legacy_match:
        matched_code, matched_intent = legacy_match
        return {
            "status": "pass",
            "errors": [],
            "matched_governed_outcome_code": matched_code,
            "matched_outcome_intent": matched_intent,
        }

    errors.append("governed_outcome_code_missing")
    return {
        "status": "fail",
        "errors": errors,
        "matched_governed_outcome_code": None,
        "matched_outcome_intent": None,
    }


def _build_document_validation_findings(payload: Dict[str, Any]) -> Dict[str, Any]:

    document_ids = payload.get("document_ids")
    document_metadata = payload.get("document_metadata")
    evidence_linkage_available = bool(document_ids) and isinstance(document_ids, list)

    fraud_integrity_flags: List[str] = []
    if not evidence_linkage_available:
        fraud_integrity_flags.append("source_document_linkage_missing")

    metadata_present = isinstance(document_metadata, dict) and bool(document_metadata)
    if not metadata_present:
        fraud_integrity_flags.append("document_metadata_missing")

    document_validity_status = "valid" if evidence_linkage_available and metadata_present else "manual_review"
    validation_confidence = 0.9 if document_validity_status == "valid" else 0.55

    return {
        "document_validity_status": document_validity_status,
        "document_validity_confidence": round(validation_confidence, 2),
        "fraud_integrity_flags": fraud_integrity_flags,
        "input_evidence_linkage": {
            "document_ids_present": evidence_linkage_available,
            "document_count": len(document_ids) if isinstance(document_ids, list) else 0,
            "document_metadata_present": metadata_present,
        },
    }


def _build_parsed_transactions(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    raw_transactions = payload.get("transactions")
    if not isinstance(raw_transactions, list):
        return []
    return [
        _normalize_transaction(raw, idx)
        for idx, raw in enumerate(raw_transactions, start=1)
        if isinstance(raw, dict)
    ]




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


def _classify_cash_flow(parsed: Dict[str, Any], classified: Dict[str, Any]) -> Dict[str, Any]:
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


def _build_credit_substrate(payload: Dict[str, Any]) -> Dict[str, Any]:
    parsed_transactions = _build_parsed_transactions(payload)
    classified_transactions = [_classify_transaction(item) for item in parsed_transactions]
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
        "net_cash_flow": round(income_total - fixed_expense_total - variable_expense_total - discretionary_total, 2),
    }

    debt_positions = payload.get("debt_positions")
    if not isinstance(debt_positions, list):
        debt_positions = []
    debt_positions = [item for item in debt_positions if isinstance(item, dict)]

    account_context = payload.get("account_context")
    if not isinstance(account_context, dict):
        account_context = {}

    prior_statement_history = payload.get("prior_statement_history")
    if not isinstance(prior_statement_history, dict):
        prior_statement_history = {}

    affordability_inputs = payload.get("affordability_inputs")
    affordability_inputs_present = isinstance(affordability_inputs, dict) and bool(affordability_inputs)

    risk_score_components = payload.get("risk_score_components")
    risk_score_components_present = isinstance(risk_score_components, dict) and bool(risk_score_components)

    timing_features = payload.get("timing_features")
    timing_features_present = isinstance(timing_features, dict) and bool(timing_features)

    return {
        "parsed_transactions": parsed_transactions,
        "classified_transactions": classified_transactions,
        "cash_flow_summary": cash_flow_summary,
        "debt_positions": debt_positions,
        "account_context": account_context,
        "prior_statement_history": prior_statement_history,
        "affordability_inputs": affordability_inputs if affordability_inputs_present else None,
        "affordability_inputs_present": affordability_inputs_present,
        "risk_score_components": risk_score_components if risk_score_components_present else None,
        "risk_score_components_present": risk_score_components_present,
        "timing_features": timing_features if timing_features_present else None,
        "timing_features_present": timing_features_present,
    }


def _build_credit_otc_002_contract_validation_stub(substrate: Dict[str, Any]) -> Dict[str, Any]:
    errors: List[str] = []

    if not isinstance(substrate.get("parsed_transactions"), list) or not substrate.get("parsed_transactions"):
        errors.append("credit_otc_002_parsed_transactions_missing")
    if not isinstance(substrate.get("classified_transactions"), list) or not substrate.get("classified_transactions"):
        errors.append("credit_otc_002_classified_transactions_missing")
    if not isinstance(substrate.get("cash_flow_summary"), dict) or not substrate.get("cash_flow_summary"):
        errors.append("credit_otc_002_cash_flow_summary_missing")
    if not isinstance(substrate.get("debt_positions"), list) or not substrate.get("debt_positions"):
        errors.append("credit_otc_002_debt_positions_missing")
    if not substrate.get("affordability_inputs_present"):
        errors.append("credit_otc_002_affordability_inputs_missing")

    return {"status": "pass" if not errors else "fail", "errors": errors}


def _build_credit_otc_002_fail_closed_result(
    payload: Dict[str, Any],
    selector_validation: Dict[str, Any],
    substrate: Dict[str, Any],
    contract_validation: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "service": "credit_decision",
        "status": "rejected",
        "selector_validation": selector_validation,
        "contract_validation": contract_validation,
        "received_payload": payload,
        "result": {
            "summary": "Worker rejected payload because CREDIT-OTC-002 cannot be emitted without governed affordability_inputs and complete affordability contract basis.",
            "missing_governed_dependency": "affordability_inputs",
            "credit_otc_002_substrate_evidence": {
                "parsed_transaction_count": len(substrate.get("parsed_transactions", [])),
                "classified_transaction_count": len(substrate.get("classified_transactions", [])),
                "cash_flow_summary_present": isinstance(substrate.get("cash_flow_summary"), dict) and bool(substrate.get("cash_flow_summary")),
                "debt_position_count": len(substrate.get("debt_positions", [])),
                "account_context_present": isinstance(substrate.get("account_context"), dict) and bool(substrate.get("account_context")),
                "prior_statement_history_present": isinstance(substrate.get("prior_statement_history"), dict) and bool(substrate.get("prior_statement_history")),
                "affordability_inputs_present": bool(substrate.get("affordability_inputs_present")),
            },
        },
    }


def _get_credit_rule(payload: Dict[str, Any], *keys: str) -> Any:
    current: Any = payload
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def _get_bank_statement_structured(payload: Dict[str, Any]) -> Dict[str, Any]:
    substrates = _safe_dict(payload.get("substrates"))
    ocr = _safe_dict(substrates.get("ocr"))
    structured_fields = _safe_dict(ocr.get("structured_fields"))
    return _safe_dict(structured_fields.get("bank_statement"))


def _normalize_statement_transactions(raw_transactions: Any) -> List[Dict[str, Any]]:
    if not isinstance(raw_transactions, list):
        return []
    return [
        _normalize_transaction(item, idx)
        for idx, item in enumerate(raw_transactions, start=1)
        if isinstance(item, dict)
    ]


def _build_credit_trace(
    payload: Dict[str, Any],
    outcome_code: str,
    outcome_intent: str,
    finalization_reason: str,
) -> Dict[str, Any]:
    document = _safe_dict(payload.get("document"))
    request = _safe_dict(payload.get("request"))
    substrates = _safe_dict(payload.get("substrates"))
    ocr = _safe_dict(substrates.get("ocr"))

    return {
        "audit_trace": {
            "processing_timestamp": _utc_now(),
            "service_status": str(payload.get("service_status") or "completed"),
            "execution_state": "completed",
            "finalization_reason": finalization_reason,
            "outcome_code": outcome_code,
        },
        "section_confidence_trace": {
            "ocr_section_present": bool(ocr),
            "document_type_present": bool(document.get("document_type")),
        },
        "provenance_trace": {
            "document_id": document.get("document_id"),
            "document_type": document.get("document_type"),
            "request_outcome_code": request.get("outcome_code"),
        },
        "consent_trace": {
            "consent_reference": request.get("consent_reference"),
        },
        "document_version_trace": {
            "document_id": document.get("document_id"),
            "file_format": document.get("file_format"),
        },
    }


def _base_credit_current_outcome(
    outcome_code: str,
    outcome_family: str,
    outcome_intent: str,
    outcome_payload: Dict[str, Any],
    payload: Dict[str, Any],
    finalization_reason: str,
    fail_closed_reasons: List[str],
) -> Dict[str, Any]:
    trace = _build_credit_trace(payload, outcome_code, outcome_intent, finalization_reason)
    return {
        "outcome_code": outcome_code,
        "outcome_family": outcome_family,
        "outcome_payload": outcome_payload,
        "audit_trace": trace["audit_trace"],
        "section_confidence_trace": trace["section_confidence_trace"],
        "provenance_trace": trace["provenance_trace"],
        "consent_trace": trace["consent_trace"],
        "document_version_trace": trace["document_version_trace"],
        "fail_closed_reasons": list(fail_closed_reasons),
    }


def _required_traceability_present(current_outcome: Dict[str, Any]) -> bool:
    for key in (
        "audit_trace",
        "section_confidence_trace",
        "provenance_trace",
        "consent_trace",
        "document_version_trace",
    ):
        if not isinstance(current_outcome.get(key), dict):
            return False
    return isinstance(current_outcome.get("fail_closed_reasons"), list)


def _validate_current_outcome_shape(current_outcome: Any, required_payload_keys: List[str]) -> Dict[str, Any]:
    errors: List[str] = []

    if not isinstance(current_outcome, dict):
        return {"status": "fail", "errors": ["current_outcome_not_dict"]}

    for key in ("outcome_code", "outcome_family", "outcome_payload"):
        if key not in current_outcome:
            errors.append(f"{key}_missing")

    if not _required_traceability_present(current_outcome):
        errors.append("traceability_missing")

    outcome_payload = current_outcome.get("outcome_payload")
    if not isinstance(outcome_payload, dict):
        errors.append("outcome_payload_not_dict")
    else:
        for key in required_payload_keys:
            if key not in outcome_payload:
                errors.append(f"outcome_payload_{key}_missing")

    return {"status": "pass" if not errors else "fail", "errors": errors}


def _reject_current_outcome(
    payload: Dict[str, Any],
    execution_plan_ack: Dict[str, Any],
    validation: Dict[str, Any],
    selector_validation: Dict[str, Any],
    contract_validation: Dict[str, Any],
    summary: str,
    current_outcome: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "service": "credit_decision",
        "status": "rejected",
        "execution_plan_ack": execution_plan_ack,
        "execution_plan_validation": validation,
        "selector_validation": selector_validation,
        "contract_validation": contract_validation,
        "received_payload": payload,
        "result": {
            "summary": summary,
            "current_outcome": current_outcome,
        },
    }


def _emit_current_outcome(
    payload: Dict[str, Any],
    execution_plan_ack: Dict[str, Any],
    validation: Dict[str, Any],
    selector_validation: Dict[str, Any],
    outcome_key: str,
    current_outcome: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "service": "credit_decision",
        "status": "executed",
        "execution_plan_ack": execution_plan_ack,
        "execution_plan_validation": validation,
        "selector_validation": selector_validation,
        "received_payload": payload,
        "result": {
            "summary": f"Credit decision worker executed governed {current_outcome['outcome_code']} with OCR-first runtime payload.",
            outcome_key: current_outcome,
        },
    }


def _build_credit_otc_003_current_outcome(payload: Dict[str, Any]) -> Dict[str, Any]:
    document = _safe_dict(payload.get("document"))
    substrates = _safe_dict(payload.get("substrates"))
    ocr = _safe_dict(substrates.get("ocr"))
    structured = _get_bank_statement_structured(payload)

    raw_text = str(ocr.get("raw_text") or "").strip()
    page_traces = _safe_list(ocr.get("page_traces"))
    engine_metadata = _safe_dict(ocr.get("engine_metadata"))
    statement_transactions = _normalize_statement_transactions(
        structured.get("transactions") or payload.get("transactions")
    )

    statement_period_start = structured.get("statement_period_start")
    statement_period_end = structured.get("statement_period_end")
    transaction_evidence_present = bool(statement_transactions)

    fail_closed_reasons: List[str] = []
    if not document:
        fail_closed_reasons.append("missing_document_payload")
    if str(document.get("document_type") or "").strip().lower() != "bank_statement":
        fail_closed_reasons.append("unsupported_document_type")
    if not raw_text or not page_traces or not engine_metadata:
        fail_closed_reasons.append("ocr_failure")
    if not statement_period_start or not statement_period_end:
        fail_closed_reasons.append("missing_statement_period")
    if not transaction_evidence_present:
        fail_closed_reasons.append("missing_transaction_evidence")

    extracted_bank_statement = {
        "bank_name": structured.get("bank_name"),
        "account_holder_name": structured.get("account_holder_name"),
        "account_number_masked": structured.get("account_number_masked"),
        "statement_period_start": statement_period_start,
        "statement_period_end": statement_period_end,
        "transaction_count": len(statement_transactions),
    }

    outcome_payload = {
        "outcome_intent": "extract_bank_statement_fields",
        "extraction_status": "succeeded" if not fail_closed_reasons else "failed",
        "extracted_bank_statement": extracted_bank_statement,
        "overall_confidence": 0.92 if not fail_closed_reasons else 0.0,
    }

    current_outcome = _base_credit_current_outcome(
        "Credit-OTC-003",
        "proof_verification",
        "extract_bank_statement_fields",
        outcome_payload,
        payload,
        "bank_statement_extraction_completed",
        fail_closed_reasons,
    )
    if not _required_traceability_present(current_outcome):
        current_outcome["fail_closed_reasons"].append("missing_traceability")
    return current_outcome


def _build_credit_otc_004_current_outcome(payload: Dict[str, Any]) -> Dict[str, Any]:
    structured = _get_bank_statement_structured(payload)
    rules = _safe_dict(_get_credit_rule(payload, "rules", "credit", "bank_income_rules"))
    statement_transactions = _normalize_statement_transactions(
        structured.get("transactions") or payload.get("transactions")
    )

    fail_closed_reasons: List[str] = []
    if not structured:
        fail_closed_reasons.append("missing_bank_statement_substrate")
    if not rules:
        fail_closed_reasons.append("bank_income_rules_missing")

    credit_transactions = [t for t in statement_transactions if t.get("type") == "credit"]
    if not credit_transactions:
        fail_closed_reasons.append("insufficient_transaction_data")

    salary_like_reference_flag = any(
        any(token in str(item.get("description") or "").lower() for token in ["salary", "payroll", "wage"])
        for item in credit_transactions
    )
    recurring_credit_count = len(credit_transactions)
    estimated_recurring_income = round(sum(float(item.get("amount") or 0.0) for item in credit_transactions), 2)
    min_recurring_credit_count = int(rules.get("min_recurring_credit_count") or 1)
    minimum_income_amount = float(rules.get("minimum_income_amount") or 0.0)

    positive_signal = (
        recurring_credit_count >= min_recurring_credit_count
        and estimated_recurring_income >= minimum_income_amount
    )
    bank_income_signal_determination = "present" if positive_signal and not fail_closed_reasons else "manual_review"
    signal_score = round(min(1.0, 0.35 + (0.2 * recurring_credit_count) + (0.1 if salary_like_reference_flag else 0.0)), 2)
    if fail_closed_reasons:
        signal_score = 0.0

    outcome_payload = {
        "outcome_intent": "assess_bank_statement_income_signal",
        "bank_income_signal_determination": bank_income_signal_determination,
        "recurring_credit_count": recurring_credit_count,
        "estimated_recurring_income": estimated_recurring_income,
        "salary_like_reference_flag": salary_like_reference_flag,
        "signal_score": signal_score,
        "summary": "Bank statement income signal assessed from governed OCR-first bank statement substrate.",
        "overall_confidence": 0.9 if not fail_closed_reasons else 0.0,
    }

    current_outcome = _base_credit_current_outcome(
        "Credit-OTC-004",
        "analytical",
        "assess_bank_statement_income_signal",
        outcome_payload,
        payload,
        "bank_statement_income_signal_completed",
        fail_closed_reasons,
    )
    if not _required_traceability_present(current_outcome):
        current_outcome["fail_closed_reasons"].append("missing_traceability")
    return current_outcome




def _get_payslip_structured(payload: Dict[str, Any]) -> Dict[str, Any]:
    substrates = _safe_dict(payload.get("substrates"))
    ocr = _safe_dict(substrates.get("ocr"))
    structured_fields = _safe_dict(ocr.get("structured_fields"))
    return _safe_dict(structured_fields.get("payslip"))


def _build_credit_otc_002_current_outcome(payload: Dict[str, Any]) -> Dict[str, Any]:
    structured = _get_payslip_structured(payload)
    rules = _safe_dict(_get_credit_rule(payload, "rules", "credit", "payslip_rules"))

    gross_income = structured.get("gross_income")
    net_income = structured.get("net_income")
    pay_period = structured.get("pay_period")
    employer_name = structured.get("employer_name")

    fail_closed_reasons: List[str] = []
    if not structured:
        fail_closed_reasons.append("missing_payslip_substrate")
    if gross_income in (None, "") and net_income in (None, ""):
        fail_closed_reasons.append("required_income_anchor_missing")
    if not pay_period:
        fail_closed_reasons.append("missing_pay_period")
    if not rules:
        fail_closed_reasons.append("missing_payslip_rules")

    income_anchor = gross_income if gross_income not in (None, "") else net_income
    minimum_income = rules.get("minimum_income") if isinstance(rules, dict) else None

    validity_determination = "manual_review"
    if not fail_closed_reasons:
        try:
            income_value = float(income_anchor)
            min_value = float(minimum_income) if minimum_income not in (None, "") else 0.0
            validity_determination = "valid" if income_value >= min_value else "manual_review"
        except Exception:
            validity_determination = "manual_review"

    outcome_payload = {
        "outcome_intent": "assess_payslip_income_validity",
        "income_validity_determination": validity_determination,
        "gross_income": gross_income,
        "net_income": net_income,
        "pay_period": pay_period,
        "employer_name": employer_name,
        "summary": "Payslip income validity evaluated from governed OCR-first payslip substrate.",
        "overall_confidence": 0.9 if not fail_closed_reasons else 0.0,
    }

    current_outcome = _base_credit_current_outcome(
        "Credit-OTC-002",
        "analytical",
        "assess_payslip_income_validity",
        outcome_payload,
        payload,
        "payslip_income_validity_completed",
        fail_closed_reasons,
    )
    if not _required_traceability_present(current_outcome):
        current_outcome["fail_closed_reasons"].append("missing_traceability")
    return current_outcome


def _build_credit_otc_005_current_outcome(payload: Dict[str, Any]) -> Dict[str, Any]:
    structured = _get_bank_statement_structured(payload)
    rules = _safe_dict(_get_credit_rule(payload, "rules", "credit", "bank_expense_rules"))
    statement_transactions = _normalize_statement_transactions(
        structured.get("transactions") or payload.get("transactions")
    )

    fail_closed_reasons: List[str] = []
    if not structured:
        fail_closed_reasons.append("missing_bank_statement_substrate")
    if not rules:
        fail_closed_reasons.append("bank_expense_rules_missing")

    debit_transactions = [t for t in statement_transactions if t.get("type") == "debit"]
    if not debit_transactions:
        fail_closed_reasons.append("insufficient_transaction_data")

    recurring_obligation_count = 0
    high_risk_debit_flags: List[str] = []
    estimated_recurring_expenses = 0.0

    keywords = ["loan", "repay", "instalment", "installment", "credit card", "rent", "insurance"]
    threshold = float(rules.get("high_risk_debit_threshold") or 5000.0) if isinstance(rules, dict) else 5000.0

    for item in debit_transactions:
        desc = str(item.get("description") or "").lower()
        amt = abs(float(item.get("amount") or 0.0))
        estimated_recurring_expenses += amt
        if any(k in desc for k in keywords):
            recurring_obligation_count += 1
        if amt >= threshold and "high_value_debit" not in high_risk_debit_flags:
            high_risk_debit_flags.append("high_value_debit")

    expense_signal = "present" if debit_transactions and not fail_closed_reasons else "manual_review"
    signal_score = round(min(1.0, 0.3 + (0.1 * len(debit_transactions)) + (0.15 * recurring_obligation_count)), 2)
    if fail_closed_reasons:
        signal_score = 0.0

    outcome_payload = {
        "outcome_intent": "assess_bank_statement_expense_signal",
        "bank_expense_signal_determination": expense_signal,
        "estimated_recurring_expenses": round(estimated_recurring_expenses, 2),
        "recurring_obligation_count": recurring_obligation_count,
        "high_risk_debit_flags": high_risk_debit_flags,
        "signal_score": signal_score,
        "summary": "Bank statement expense signal assessed from governed OCR-first bank statement substrate.",
        "overall_confidence": 0.89 if not fail_closed_reasons else 0.0,
    }

    current_outcome = _base_credit_current_outcome(
        "Credit-OTC-005",
        "analytical",
        "assess_bank_statement_expense_signal",
        outcome_payload,
        payload,
        "bank_statement_expense_signal_completed",
        fail_closed_reasons,
    )
    if not _required_traceability_present(current_outcome):
        current_outcome["fail_closed_reasons"].append("missing_traceability")
    return current_outcome




def _get_analytics_substrate(payload: Dict[str, Any], key: str) -> Dict[str, Any]:
    substrates = _safe_dict(payload.get("substrates"))
    analytics = _safe_dict(substrates.get("analytics"))
    return _safe_dict(analytics.get(key))


def _normalize_completed_outcomes(raw: Any) -> List[str]:
    if isinstance(raw, dict):
        return [str(k) for k, v in raw.items() if v]
    if isinstance(raw, list):
        return [str(item) for item in raw if item not in (None, "")]
    return []


def _normalize_document_types(raw: Any) -> List[str]:
    results: List[str] = []
    if not isinstance(raw, list):
        return results
    for item in raw:
        if isinstance(item, dict):
            doc_type = item.get("document_type")
            if doc_type:
                results.append(str(doc_type).strip().lower())
        elif item not in (None, ""):
            results.append(str(item).strip().lower())
    return results


def _build_credit_otc_001_current_outcome(payload: Dict[str, Any]) -> Dict[str, Any]:
    document = _safe_dict(payload.get("document"))
    substrates = _safe_dict(payload.get("substrates"))
    ocr = _safe_dict(substrates.get("ocr"))
    structured = _get_payslip_structured(payload)

    raw_text = str(ocr.get("raw_text") or "").strip()
    page_traces = _safe_list(ocr.get("page_traces"))
    engine_metadata = _safe_dict(ocr.get("engine_metadata"))

    gross_income = structured.get("gross_income")
    net_income = structured.get("net_income")
    pay_period = structured.get("pay_period")
    employer_name = structured.get("employer_name")

    fail_closed_reasons: List[str] = []
    if not document:
        fail_closed_reasons.append("missing_document_payload")
    if str(document.get("document_type") or "").strip().lower() != "payslip":
        fail_closed_reasons.append("unsupported_document_type")
    if not raw_text or not page_traces or not engine_metadata:
        fail_closed_reasons.append("ocr_failure")
    if gross_income in (None, "") and net_income in (None, ""):
        fail_closed_reasons.append("required_income_anchor_missing")

    outcome_payload = {
        "outcome_intent": "extract_payslip_fields",
        "extraction_status": "succeeded" if not fail_closed_reasons else "failed",
        "extracted_payslip": {
            "gross_income": gross_income,
            "net_income": net_income,
            "pay_period": pay_period,
            "employer_name": employer_name,
        },
        "overall_confidence": 0.92 if not fail_closed_reasons else 0.0,
    }

    current_outcome = _base_credit_current_outcome(
        "Credit-OTC-001",
        "proof_verification",
        "extract_payslip_fields",
        outcome_payload,
        payload,
        "payslip_extraction_completed",
        fail_closed_reasons,
    )
    if not _required_traceability_present(current_outcome):
        current_outcome["fail_closed_reasons"].append("missing_traceability")
    return current_outcome


def _build_credit_otc_006_current_outcome(payload: Dict[str, Any]) -> Dict[str, Any]:
    payslip = _get_payslip_structured(payload)
    bank_statement = _get_bank_statement_structured(payload)
    rules = _safe_dict(_get_credit_rule(payload, "rules", "credit", "income_consistency_rules"))

    fail_closed_reasons: List[str] = []
    if not payslip:
        fail_closed_reasons.append("missing_payslip_substrate")
    if not bank_statement:
        fail_closed_reasons.append("missing_bank_statement_substrate")
    if not rules:
        fail_closed_reasons.append("missing_income_consistency_rules")

    payslip_income = payslip.get("gross_income")
    if payslip_income in (None, ""):
        payslip_income = payslip.get("net_income")
    if payslip_income in (None, ""):
        fail_closed_reasons.append("missing_payslip_income_anchor")

    transactions = _normalize_statement_transactions(
        bank_statement.get("transactions") or payload.get("transactions")
    )
    credit_transactions = [t for t in transactions if t.get("type") == "credit"]
    if not credit_transactions:
        fail_closed_reasons.append("insufficient_bank_transaction_data")

    estimated_bank_income = round(sum(float(t.get("amount") or 0.0) for t in credit_transactions), 2)
    tolerance_amount = float(rules.get("tolerance_amount") or 1500.0) if isinstance(rules, dict) else 1500.0
    salary_like_reference_flag = any(
        any(token in str(item.get("description") or "").lower() for token in ["salary", "payroll", "wage"])
        for item in credit_transactions
    )

    determination = "manual_review"
    variance_amount = None
    if not fail_closed_reasons:
        try:
            payslip_income_value = float(payslip_income)
            variance_amount = round(abs(payslip_income_value - estimated_bank_income), 2)
            determination = "consistent" if variance_amount <= tolerance_amount else "manual_review"
        except Exception:
            fail_closed_reasons.append("income_comparison_failed")

    outcome_payload = {
        "outcome_intent": "assess_payslip_to_bank_income_consistency",
        "income_consistency_determination": determination,
        "payslip_income_amount": payslip_income,
        "estimated_bank_income": estimated_bank_income,
        "variance_amount": variance_amount,
        "salary_like_reference_flag": salary_like_reference_flag,
        "summary": "Payslip-to-bank income consistency evaluated from governed OCR-first cross-document substrates.",
        "overall_confidence": 0.9 if not fail_closed_reasons else 0.0,
    }

    current_outcome = _base_credit_current_outcome(
        "Credit-OTC-006",
        "analytical",
        "assess_payslip_to_bank_income_consistency",
        outcome_payload,
        payload,
        "payslip_to_bank_income_consistency_completed",
        fail_closed_reasons,
    )
    if not _required_traceability_present(current_outcome):
        current_outcome["fail_closed_reasons"].append("missing_traceability")
    return current_outcome


def _build_credit_otc_007_current_outcome(payload: Dict[str, Any]) -> Dict[str, Any]:
    bank_income_signal = _get_analytics_substrate(payload, "bank_income_signal")
    bank_expense_signal = _get_analytics_substrate(payload, "bank_expense_signal")
    rules = _safe_dict(_get_credit_rule(payload, "rules", "credit", "affordability_rules"))

    fail_closed_reasons: List[str] = []
    if not bank_income_signal:
        fail_closed_reasons.append("missing_bank_income_signal_substrate")
    if not bank_expense_signal:
        fail_closed_reasons.append("missing_bank_expense_signal_substrate")
    if not rules:
        fail_closed_reasons.append("missing_affordability_rules")

    estimated_income = float(bank_income_signal.get("estimated_recurring_income") or 0.0)
    estimated_expense = float(bank_expense_signal.get("estimated_recurring_expenses") or 0.0)
    disposable_income = round(estimated_income - estimated_expense, 2)
    minimum_disposable_income = float(rules.get("minimum_disposable_income") or 0.0) if isinstance(rules, dict) else 0.0

    affordability_status = "manual_review"
    affordability_score = 0.0
    if not fail_closed_reasons:
        affordability_status = "affordable" if disposable_income >= minimum_disposable_income else "manual_review"
        denominator = estimated_income if estimated_income > 0 else 1.0
        affordability_score = round(max(0.0, min(1.0, disposable_income / denominator)), 2)

    outcome_payload = {
        "outcome_intent": "produce_ocr_based_affordability_snapshot",
        "affordability_snapshot_status": affordability_status,
        "estimated_recurring_income": estimated_income,
        "estimated_recurring_expenses": estimated_expense,
        "disposable_income_estimate": disposable_income,
        "affordability_score": affordability_score,
        "summary": "OCR-first affordability snapshot generated from governed upstream analytical substrates.",
        "overall_confidence": 0.89 if not fail_closed_reasons else 0.0,
    }

    current_outcome = _base_credit_current_outcome(
        "Credit-OTC-007",
        "analytical",
        "produce_ocr_based_affordability_snapshot",
        outcome_payload,
        payload,
        "ocr_affordability_snapshot_completed",
        fail_closed_reasons,
    )
    if not _required_traceability_present(current_outcome):
        current_outcome["fail_closed_reasons"].append("missing_traceability")
    return current_outcome


def _build_credit_otc_008_current_outcome(payload: Dict[str, Any]) -> Dict[str, Any]:
    required_document_set = _get_credit_rule(payload, "rules", "credit", "required_document_set")
    documents_submitted = payload.get("documents_submitted")
    substrates = _safe_dict(payload.get("substrates"))
    completed_outcomes = _normalize_completed_outcomes(substrates.get("completed_outcomes"))

    required_docs = [str(item).strip().lower() for item in required_document_set] if isinstance(required_document_set, list) else []
    submitted_docs = _normalize_document_types(documents_submitted)

    fail_closed_reasons: List[str] = []
    if not required_docs:
        fail_closed_reasons.append("missing_required_document_set")
    if not submitted_docs:
        fail_closed_reasons.append("missing_documents_submitted")
    if not completed_outcomes:
        fail_closed_reasons.append("missing_completed_outcomes")

    missing_required_documents = sorted([doc for doc in required_docs if doc not in submitted_docs])
    determination = "complete" if not missing_required_documents and not fail_closed_reasons else "manual_review"

    outcome_payload = {
        "outcome_intent": "assess_credit_document_pack_completeness",
        "document_pack_completeness_determination": determination,
        "required_document_set": required_docs,
        "submitted_document_types": submitted_docs,
        "missing_required_documents": missing_required_documents,
        "summary": "Credit document pack completeness assessed from governed OCR-first pack requirements and completed outcomes.",
        "overall_confidence": 0.9 if not fail_closed_reasons else 0.0,
    }

    current_outcome = _base_credit_current_outcome(
        "Credit-OTC-008",
        "analytical",
        "assess_credit_document_pack_completeness",
        outcome_payload,
        payload,
        "credit_document_pack_completeness_completed",
        fail_closed_reasons,
    )
    if not _required_traceability_present(current_outcome):
        current_outcome["fail_closed_reasons"].append("missing_traceability")
    return current_outcome


def _build_credit_otc_009_current_outcome(payload: Dict[str, Any]) -> Dict[str, Any]:
    affordability_snapshot = _get_analytics_substrate(payload, "affordability_snapshot")
    document_pack_completeness = _get_analytics_substrate(payload, "document_pack_completeness")
    rules = _safe_dict(_get_credit_rule(payload, "rules", "credit", "recommendation_rules"))

    fail_closed_reasons: List[str] = []
    if not affordability_snapshot:
        fail_closed_reasons.append("missing_affordability_snapshot_substrate")
    if not document_pack_completeness:
        fail_closed_reasons.append("missing_document_pack_completeness_substrate")
    if not rules:
        fail_closed_reasons.append("missing_recommendation_rules")

    affordability_status = str(
        affordability_snapshot.get("affordability_snapshot_status")
        or affordability_snapshot.get("affordability_status")
        or "manual_review"
    ).strip().lower()
    pack_status = str(
        document_pack_completeness.get("document_pack_completeness_determination")
        or document_pack_completeness.get("document_pack_status")
        or "manual_review"
    ).strip().lower()

    blocking_flags: List[str] = []
    primary_reasons: List[str] = []

    if affordability_status != "affordable":
        blocking_flags.append("affordability_not_confirmed")
        primary_reasons.append("Affordability snapshot did not confirm affordable status.")
    if pack_status != "complete":
        blocking_flags.append("document_pack_incomplete")
        primary_reasons.append("Document pack completeness was not complete.")

    recommendation = "approve" if not blocking_flags and not fail_closed_reasons else "manual_review"

    outcome_payload = {
        "outcome_intent": "produce_ocr_based_credit_recommendation",
        "credit_recommendation_determination": recommendation,
        "primary_reasons": primary_reasons,
        "blocking_flags": blocking_flags,
        "supporting_metrics": {
            "affordability_status": affordability_status,
            "document_pack_status": pack_status,
        },
        "summary": "OCR-first credit recommendation generated from governed upstream OCR-first outputs.",
        "overall_confidence": 0.9 if not fail_closed_reasons else 0.0,
    }

    current_outcome = _base_credit_current_outcome(
        "Credit-OTC-009",
        "analytical",
        "produce_ocr_based_credit_recommendation",
        outcome_payload,
        payload,
        "ocr_credit_recommendation_completed",
        fail_closed_reasons,
    )
    if not _required_traceability_present(current_outcome):
        current_outcome["fail_closed_reasons"].append("missing_traceability")
    return current_outcome


def _build_credit_otc_005_contract_validation_stub(payload: Dict[str, Any]) -> Dict[str, Any]:

    errors: List[str] = []

    internal_credit_decision = payload.get("internal_credit_decision")
    decision_summary_basis = payload.get("decision_summary_basis")
    internal_decision_record = payload.get("internal_decision_record")

    if not isinstance(internal_credit_decision, dict) or not internal_credit_decision:
        errors.append("credit_otc_005_internal_credit_decision_missing")
    if not isinstance(decision_summary_basis, dict) or not decision_summary_basis:
        errors.append("credit_otc_005_decision_summary_basis_missing")
    if not isinstance(internal_decision_record, dict) or not internal_decision_record:
        errors.append("credit_otc_005_internal_decision_record_missing")

    return {"status": "pass" if not errors else "fail", "errors": errors}


def _build_credit_otc_005_fail_closed_result(
    payload: Dict[str, Any],
    selector_validation: Dict[str, Any],
    contract_validation: Dict[str, Any],
) -> Dict[str, Any]:
    internal_credit_decision = payload.get("internal_credit_decision")
    decision_summary_basis = payload.get("decision_summary_basis")
    internal_decision_record = payload.get("internal_decision_record")

    return {
        "service": "credit_decision",
        "status": "rejected",
        "selector_validation": selector_validation,
        "contract_validation": contract_validation,
        "received_payload": payload,
        "result": {
            "summary": "Worker rejected payload because CREDIT-OTC-005 cannot be emitted without governed internal_credit_decision, decision_summary_basis, and internal_decision_record basis.",
            "missing_governed_dependency": "internal_credit_decision",
            "credit_otc_005_substrate_evidence": {
                "internal_credit_decision_present": isinstance(internal_credit_decision, dict) and bool(internal_credit_decision),
                "decision_summary_basis_present": isinstance(decision_summary_basis, dict) and bool(decision_summary_basis),
                "internal_decision_record_present": isinstance(internal_decision_record, dict) and bool(internal_decision_record),
            },
        },
    }


def _build_fraud_findings(parsed_transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    fraud_integrity_flags: List[str] = []
    flagged_items: List[Dict[str, Any]] = []

    for txn in parsed_transactions:
        amount = abs(txn["amount"])
        txn_flags: List[str] = []

        if amount >= 10000:
            txn_flags.append("high_value_transaction")
        if txn["type"] == "debit" and "cash" in txn["description"].lower() and amount >= 2000:
            txn_flags.append("high_cash_activity")
        if not txn["date"]:
            txn_flags.append("transaction_date_missing")

        if txn_flags:
            flagged_items.append({
                "transaction_id": txn["transaction_id"],
                "amount": amount,
                "description": txn["description"],
                "flags": txn_flags,
            })
            for flag in txn_flags:
                if flag not in fraud_integrity_flags:
                    fraud_integrity_flags.append(flag)

    if flagged_items:
        fraud_score = round(min(0.95, 0.35 + (0.15 * len(flagged_items))), 2)
    else:
        fraud_score = 0.1

    return {
        "fraud_score": fraud_score,
        "fraud_integrity_flags": fraud_integrity_flags,
        "flagged_items": flagged_items,
    }


def _build_credit_otc_001_internal(
    payload: Dict[str, Any],
    selector_validation: Dict[str, Any],
    document_validation_findings: Dict[str, Any],
    parsed_transactions: List[Dict[str, Any]],
    fraud_findings: Dict[str, Any],
) -> Dict[str, Any]:
    flags = list(document_validation_findings.get("fraud_integrity_flags", []))
    for flag in fraud_findings.get("fraud_integrity_flags", []):
        if flag not in flags:
            flags.append(flag)

    flagged_items = list(fraud_findings.get("flagged_items", []))
    fraud_score = fraud_findings.get("fraud_score")
    manual_review = bool(flags) or (fraud_score is not None and fraud_score >= 0.5)

    integrity_status = "manual_review" if manual_review else "clear"
    integrity_assessment_summary = (
        f"Integrity review assessed {len(parsed_transactions)} transactions and identified {len(flagged_items)} flagged anomalies."
        if flagged_items
        else "Integrity review found no material fraud or document-integrity anomalies in the current payload."
    )

    escalation_guidance = (
        ["Escalate for internal review because fraud or integrity indicators were detected."]
        if manual_review
        else ["No escalation required from the current integrity review output."]
    )

    overall_confidence = round(
        (
            float(document_validation_findings.get("document_validity_confidence") or 0.0)
            + max(0.0, 1.0 - float(fraud_score or 0.0))
        ) / 2,
        2,
    )

    return {
        "outcome_intent": "assess_document_and_transaction_integrity",
        "integrity_status": integrity_status,
        "manual_review": manual_review,
        "fraud_score": fraud_score,
        "fraud_integrity_flags": flags,
        "integrity_assessment_summary": integrity_assessment_summary,
        "escalation_guidance": escalation_guidance,
        "audit_trace": {
            "processing_timestamp": _utc_now(),
            "service_status": str(payload.get("service_status") or "completed"),
            "execution_state": "completed",
            "finalization_reason": "credit_integrity_assessment_completed",
        },
        "input_evidence_linkage": {
            **dict(document_validation_findings.get("input_evidence_linkage", {})),
            "parsed_transaction_count": len(parsed_transactions),
            "fraud_flagged_item_count": len(flagged_items),
        },
        "decision_trace": {
            "selector_basis": "requested_service+requested_option_set+audience_mode",
            "matched_governed_outcome_code": selector_validation.get("matched_governed_outcome_code"),
            "matched_outcome_intent": selector_validation.get("matched_outcome_intent"),
            "document_validity_status": document_validation_findings.get("document_validity_status"),
            "fraud_flagged_item_count": len(flagged_items),
        },
        "overall_confidence": overall_confidence,
    }


def _validate_credit_otc_001_internal_contract(outcome: Any) -> Dict[str, Any]:
    errors: List[str] = []

    if not isinstance(outcome, dict):
        return {"status": "fail", "errors": ["credit_otc_001_not_dict"]}

    if outcome.get("outcome_intent") != "assess_document_and_transaction_integrity":
        errors.append("credit_otc_001_outcome_intent_invalid")
    if outcome.get("integrity_status") is None:
        errors.append("credit_otc_001_integrity_status_missing")
    if outcome.get("manual_review") is None:
        errors.append("credit_otc_001_manual_review_missing")
    if outcome.get("fraud_score") is None:
        errors.append("credit_otc_001_fraud_score_missing")
    if not isinstance(outcome.get("fraud_integrity_flags"), list):
        errors.append("credit_otc_001_fraud_integrity_flags_missing")
    if not isinstance(outcome.get("integrity_assessment_summary"), str):
        errors.append("credit_otc_001_integrity_assessment_summary_missing")
    if not isinstance(outcome.get("escalation_guidance"), list):
        errors.append("credit_otc_001_escalation_guidance_missing")
    if outcome.get("overall_confidence") is None:
        errors.append("credit_otc_001_overall_confidence_missing")
    for key in ("audit_trace", "input_evidence_linkage", "decision_trace"):
        if not isinstance(outcome.get(key), dict):
            errors.append(f"credit_otc_001_{key}_missing")

    return {"status": "pass" if not errors else "fail", "errors": errors}


def run(payload: Dict[str, Any]) -> Dict[str, Any]:
    execution_plan_ack = _build_execution_plan_ack(payload)
    validation = _validate_execution_plan(payload, EXPECTED_SERVICE_FAMILY)

    if validation["status"] != "pass":
        return {
            "service": "credit_decision",
            "status": "rejected",
            "execution_plan_ack": execution_plan_ack,
            "execution_plan_validation": validation,
            "received_payload": payload,
            "result": {"summary": "Worker rejected payload due to execution plan validation failure."},
        }

    selector = _normalize_selector(payload)
    selector_validation = _validate_selector(selector)

    if selector_validation["status"] != "pass":
        return {
            "service": "credit_decision",
            "status": "rejected",
            "execution_plan_ack": execution_plan_ack,
            "execution_plan_validation": validation,
            "selector_validation": selector_validation,
            "received_payload": payload,
            "result": {"summary": "Worker rejected payload because no governed Credit request selector matched an implemented outcome."},
        }

    if selector_validation.get("matched_governed_outcome_code") == "Credit-OTC-002":
        current_outcome = _build_credit_otc_002_current_outcome(payload)
        if current_outcome.get("fail_closed_reasons"):
            contract_validation = {"status": "fail", "errors": list(current_outcome.get("fail_closed_reasons", []))}
            return _reject_current_outcome(
                payload,
                execution_plan_ack,
                validation,
                selector_validation,
                contract_validation,
                "Worker rejected payload because selected Credit-OTC-002 failed closed under governed payslip income validity rules.",
                current_outcome,
            )

        contract_validation = _validate_current_outcome_shape(
            current_outcome,
            [
                "income_validity_determination",
                "gross_income",
                "net_income",
                "pay_period",
                "employer_name",
                "summary",
                "overall_confidence",
            ],
        )
        if contract_validation["status"] != "pass":
            return _reject_current_outcome(
                payload,
                execution_plan_ack,
                validation,
                selector_validation,
                contract_validation,
                "Worker rejected payload because the generated Credit-OTC-002 outcome failed internal contract validation.",
                current_outcome,
            )

        return _emit_current_outcome(
            payload,
            execution_plan_ack,
            validation,
            selector_validation,
            "credit_otc_002",
            current_outcome,
        )

    
    if selector_validation.get("matched_governed_outcome_code") == "Credit-OTC-003":
        current_outcome = _build_credit_otc_003_current_outcome(payload)
        if current_outcome.get("fail_closed_reasons"):
            contract_validation = {"status": "fail", "errors": list(current_outcome.get("fail_closed_reasons", []))}
            return _reject_current_outcome(
                payload,
                execution_plan_ack,
                validation,
                selector_validation,
                contract_validation,
                "Worker rejected payload because selected Credit-OTC-003 failed closed under governed bank statement extraction rules.",
                current_outcome,
            )

        contract_validation = _validate_current_outcome_shape(
            current_outcome,
            ["extraction_status", "extracted_bank_statement", "overall_confidence"],
        )
        if contract_validation["status"] != "pass":
            return _reject_current_outcome(
                payload,
                execution_plan_ack,
                validation,
                selector_validation,
                contract_validation,
                "Worker rejected payload because the generated Credit-OTC-003 outcome failed internal contract validation.",
                current_outcome,
            )

        return _emit_current_outcome(
            payload,
            execution_plan_ack,
            validation,
            selector_validation,
            "credit_otc_003",
            current_outcome,
        )

    if selector_validation.get("matched_governed_outcome_code") == "Credit-OTC-004":
        current_outcome = _build_credit_otc_004_current_outcome(payload)
        if current_outcome.get("fail_closed_reasons"):
            contract_validation = {"status": "fail", "errors": list(current_outcome.get("fail_closed_reasons", []))}
            return _reject_current_outcome(
                payload,
                execution_plan_ack,
                validation,
                selector_validation,
                contract_validation,
                "Worker rejected payload because selected Credit-OTC-004 failed closed under governed bank income signal rules.",
                current_outcome,
            )

        contract_validation = _validate_current_outcome_shape(
            current_outcome,
            [
                "bank_income_signal_determination",
                "recurring_credit_count",
                "estimated_recurring_income",
                "salary_like_reference_flag",
                "signal_score",
                "summary",
                "overall_confidence",
            ],
        )
        if contract_validation["status"] != "pass":
            return _reject_current_outcome(
                payload,
                execution_plan_ack,
                validation,
                selector_validation,
                contract_validation,
                "Worker rejected payload because the generated Credit-OTC-004 outcome failed internal contract validation.",
                current_outcome,
            )

        return _emit_current_outcome(
            payload,
            execution_plan_ack,
            validation,
            selector_validation,
            "credit_otc_004",
            current_outcome,
        )

    if selector_validation.get("matched_governed_outcome_code") == "Credit-OTC-005":
        current_outcome = _build_credit_otc_005_current_outcome(payload)
        if current_outcome.get("fail_closed_reasons"):
            contract_validation = {"status": "fail", "errors": list(current_outcome.get("fail_closed_reasons", []))}
            return _reject_current_outcome(
                payload,
                execution_plan_ack,
                validation,
                selector_validation,
                contract_validation,
                "Worker rejected payload because selected Credit-OTC-005 failed closed under governed bank expense signal rules.",
                current_outcome,
            )

        contract_validation = _validate_current_outcome_shape(
            current_outcome,
            [
                "bank_expense_signal_determination",
                "estimated_recurring_expenses",
                "recurring_obligation_count",
                "high_risk_debit_flags",
                "signal_score",
                "summary",
                "overall_confidence",
            ],
        )
        if contract_validation["status"] != "pass":
            return _reject_current_outcome(
                payload,
                execution_plan_ack,
                validation,
                selector_validation,
                contract_validation,
                "Worker rejected payload because the generated Credit-OTC-005 outcome failed internal contract validation.",
                current_outcome,
            )

        return _emit_current_outcome(
            payload,
            execution_plan_ack,
            validation,
            selector_validation,
            "credit_otc_005",
            current_outcome,
        )

    if selector_validation.get("matched_governed_outcome_code") == "Credit-OTC-006":
        current_outcome = _build_credit_otc_006_current_outcome(payload)
        if current_outcome.get("fail_closed_reasons"):
            contract_validation = {"status": "fail", "errors": list(current_outcome.get("fail_closed_reasons", []))}
            return _reject_current_outcome(
                payload,
                execution_plan_ack,
                validation,
                selector_validation,
                contract_validation,
                "Worker rejected payload because selected Credit-OTC-006 failed closed under governed payslip-to-bank income consistency rules.",
                current_outcome,
            )

        contract_validation = _validate_current_outcome_shape(
            current_outcome,
            [
                "income_consistency_determination",
                "payslip_income_amount",
                "estimated_bank_income",
                "variance_amount",
                "salary_like_reference_flag",
                "summary",
                "overall_confidence",
            ],
        )
        if contract_validation["status"] != "pass":
            return _reject_current_outcome(
                payload,
                execution_plan_ack,
                validation,
                selector_validation,
                contract_validation,
                "Worker rejected payload because the generated Credit-OTC-006 outcome failed internal contract validation.",
                current_outcome,
            )

        return _emit_current_outcome(
            payload,
            execution_plan_ack,
            validation,
            selector_validation,
            "credit_otc_006",
            current_outcome,
        )

    if selector_validation.get("matched_governed_outcome_code") == "Credit-OTC-007":
        current_outcome = _build_credit_otc_007_current_outcome(payload)
        if current_outcome.get("fail_closed_reasons"):
            contract_validation = {"status": "fail", "errors": list(current_outcome.get("fail_closed_reasons", []))}
            return _reject_current_outcome(
                payload,
                execution_plan_ack,
                validation,
                selector_validation,
                contract_validation,
                "Worker rejected payload because selected Credit-OTC-007 failed closed under governed OCR-first affordability snapshot rules.",
                current_outcome,
            )

        contract_validation = _validate_current_outcome_shape(
            current_outcome,
            [
                "affordability_snapshot_status",
                "estimated_recurring_income",
                "estimated_recurring_expenses",
                "disposable_income_estimate",
                "affordability_score",
                "summary",
                "overall_confidence",
            ],
        )
        if contract_validation["status"] != "pass":
            return _reject_current_outcome(
                payload,
                execution_plan_ack,
                validation,
                selector_validation,
                contract_validation,
                "Worker rejected payload because the generated Credit-OTC-007 outcome failed internal contract validation.",
                current_outcome,
            )

        return _emit_current_outcome(
            payload,
            execution_plan_ack,
            validation,
            selector_validation,
            "credit_otc_007",
            current_outcome,
        )

    if selector_validation.get("matched_governed_outcome_code") == "Credit-OTC-008":
        current_outcome = _build_credit_otc_008_current_outcome(payload)
        if current_outcome.get("fail_closed_reasons"):
            contract_validation = {"status": "fail", "errors": list(current_outcome.get("fail_closed_reasons", []))}
            return _reject_current_outcome(
                payload,
                execution_plan_ack,
                validation,
                selector_validation,
                contract_validation,
                "Worker rejected payload because selected Credit-OTC-008 failed closed under governed document pack completeness rules.",
                current_outcome,
            )

        contract_validation = _validate_current_outcome_shape(
            current_outcome,
            [
                "document_pack_completeness_determination",
                "required_document_set",
                "submitted_document_types",
                "missing_required_documents",
                "summary",
                "overall_confidence",
            ],
        )
        if contract_validation["status"] != "pass":
            return _reject_current_outcome(
                payload,
                execution_plan_ack,
                validation,
                selector_validation,
                contract_validation,
                "Worker rejected payload because the generated Credit-OTC-008 outcome failed internal contract validation.",
                current_outcome,
            )

        return _emit_current_outcome(
            payload,
            execution_plan_ack,
            validation,
            selector_validation,
            "credit_otc_008",
            current_outcome,
        )

    if selector_validation.get("matched_governed_outcome_code") == "Credit-OTC-009":
        current_outcome = _build_credit_otc_009_current_outcome(payload)
        if current_outcome.get("fail_closed_reasons"):
            contract_validation = {"status": "fail", "errors": list(current_outcome.get("fail_closed_reasons", []))}
            return _reject_current_outcome(
                payload,
                execution_plan_ack,
                validation,
                selector_validation,
                contract_validation,
                "Worker rejected payload because selected Credit-OTC-009 failed closed under governed OCR-first recommendation rules.",
                current_outcome,
            )

        contract_validation = _validate_current_outcome_shape(
            current_outcome,
            [
                "credit_recommendation_determination",
                "primary_reasons",
                "blocking_flags",
                "supporting_metrics",
                "summary",
                "overall_confidence",
            ],
        )
        if contract_validation["status"] != "pass":
            return _reject_current_outcome(
                payload,
                execution_plan_ack,
                validation,
                selector_validation,
                contract_validation,
                "Worker rejected payload because the generated Credit-OTC-009 outcome failed internal contract validation.",
                current_outcome,
            )

        return _emit_current_outcome(
            payload,
            execution_plan_ack,
            validation,
            selector_validation,
            "credit_otc_009",
            current_outcome,
        )

    if selector_validation.get("matched_governed_outcome_code") == "Credit-OTC-001":
        current_outcome = _build_credit_otc_001_current_outcome(payload)
        if current_outcome.get("fail_closed_reasons"):
            contract_validation = {"status": "fail", "errors": list(current_outcome.get("fail_closed_reasons", []))}
            return _reject_current_outcome(
                payload,
                execution_plan_ack,
                validation,
                selector_validation,
                contract_validation,
                "Worker rejected payload because selected Credit-OTC-001 failed closed under governed payslip extraction rules.",
                current_outcome,
            )

        contract_validation = _validate_current_outcome_shape(
            current_outcome,
            ["extraction_status", "extracted_payslip", "overall_confidence"],
        )
        if contract_validation["status"] != "pass":
            return _reject_current_outcome(
                payload,
                execution_plan_ack,
                validation,
                selector_validation,
                contract_validation,
                "Worker rejected payload because the generated Credit-OTC-001 outcome failed internal contract validation.",
                current_outcome,
            )

        return _emit_current_outcome(
            payload,
            execution_plan_ack,
            validation,
            selector_validation,
            "credit_otc_001",
            current_outcome,
        )

    return {
        "service": "credit_decision",
        "status": "rejected",
        "execution_plan_ack": execution_plan_ack,
        "execution_plan_validation": validation,
        "selector_validation": selector_validation,
        "received_payload": payload,
        "result": {
            "summary": "Worker rejected payload because selected governed Credit outcome is not implemented.",
        },
    }

