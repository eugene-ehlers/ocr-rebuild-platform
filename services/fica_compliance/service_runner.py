from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


EXPECTED_SERVICE_FAMILY = "fica"
EXPECTED_STAGE = "downstream_execution"
SUPPORTED_PLAN_VERSIONS = {"execution_plan_v1"}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_dict(value: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _safe_list(value: Any) -> List[Any]:
    return value if isinstance(value, list) else []


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


def _normalize_selector(payload: Dict[str, Any]) -> Dict[str, Any]:
    orchestration_context = _safe_dict(payload.get("orchestration_context"))
    return {
        "analysis_type": str(orchestration_context.get("analysis_type") or payload.get("analysis_type") or "").strip().lower(),
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
    }


def _validate_selector(selector: Dict[str, Any]) -> Dict[str, Any]:
    errors: List[str] = []

    governed_outcome_code = selector["governed_outcome_code"]
    governed_outcome_intent = selector["governed_outcome_intent"]

    allowed = {
        "FICA-OTC-001": "extract_identity_document_fields",
        "FICA-OTC-002": "assess_identity_field_consistency",
        "FICA-OTC-003": "extract_proof_of_address_fields",
        "FICA-OTC-004": "assess_proof_of_address_validity_and_recency",
        "FICA-OTC-005": "extract_business_registration_fields",
        "FICA-OTC-006": "assess_business_ownership_or_authority_consistency",
    }

    if not governed_outcome_code:
        errors.append("governed_outcome_code_missing")
    if governed_outcome_code not in allowed:
        errors.append("unsupported_fica_governed_outcome_code")

    expected_intent = allowed.get(governed_outcome_code)
    if expected_intent and governed_outcome_intent != expected_intent:
        errors.append("governed_outcome_intent_mismatch")

    return {
        "status": "pass" if not errors else "fail",
        "errors": errors,
        "matched_governed_outcome_code": governed_outcome_code if not errors else None,
        "matched_outcome_intent": governed_outcome_intent if not errors else None,
    }


def _document_trace(payload: Dict[str, Any], outcome_code: str, outcome_intent: str) -> Dict[str, Any]:
    document = _safe_dict(payload.get("document"))
    request = _safe_dict(payload.get("request"))

    return {
        "audit_trace": {
            "processing_timestamp": _utc_now(),
            "service_status": str(payload.get("service_status") or "completed"),
            "execution_state": "completed",
            "outcome_code": outcome_code,
        },
        "section_confidence_trace": {
            "ocr_section_present": bool(_safe_dict(_safe_dict(payload.get("substrates")).get("ocr"))),
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
        "decision_trace": {
            "matched_governed_outcome_code": outcome_code,
            "matched_outcome_intent": outcome_intent,
            "selector_basis": "orchestration_context.governed_outcome_code",
        },
    }


def _required_traceability_present(outcome: Dict[str, Any]) -> bool:
    for key in (
        "audit_trace",
        "section_confidence_trace",
        "provenance_trace",
        "consent_trace",
        "document_version_trace",
    ):
        if not isinstance(outcome.get(key), dict):
            return False
    if not isinstance(outcome.get("fail_closed_reasons"), list):
        return False
    return True


def _get_ocr_structured(payload: Dict[str, Any], key: str) -> Dict[str, Any]:
    substrates = _safe_dict(payload.get("substrates"))
    ocr = _safe_dict(substrates.get("ocr"))
    structured = _safe_dict(ocr.get("structured_fields"))
    return _safe_dict(structured.get(key))


def _get_rule(payload: Dict[str, Any], *keys: str) -> Any:
    current: Any = payload
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def _base_current_outcome(
    outcome_code: str,
    outcome_family: str,
    outcome_intent: str,
    outcome_payload: Dict[str, Any],
    payload: Dict[str, Any],
    fail_closed_reasons: Optional[List[str]] = None,
) -> Dict[str, Any]:
    trace = _document_trace(payload, outcome_code, outcome_intent)
    return {
        "outcome_code": outcome_code,
        "outcome_family": outcome_family,
        "outcome_payload": outcome_payload,
        "audit_trace": trace["audit_trace"],
        "section_confidence_trace": trace["section_confidence_trace"],
        "provenance_trace": trace["provenance_trace"],
        "consent_trace": trace["consent_trace"],
        "document_version_trace": trace["document_version_trace"],
        "decision_trace": trace["decision_trace"],
        "fail_closed_reasons": fail_closed_reasons or [],
    }


def _reject(
    payload: Dict[str, Any],
    execution_plan_ack: Dict[str, Any],
    validation: Dict[str, Any],
    selector_validation: Optional[Dict[str, Any]],
    summary: str,
    details: Dict[str, Any],
) -> Dict[str, Any]:
    result = {"summary": summary}
    result.update(details)
    return {
        "service": "fica_compliance",
        "status": "rejected",
        "execution_plan_ack": execution_plan_ack,
        "execution_plan_validation": validation,
        "selector_validation": selector_validation,
        "received_payload": payload,
        "result": result,
    }


def _emit_success(
    payload: Dict[str, Any],
    execution_plan_ack: Dict[str, Any],
    validation: Dict[str, Any],
    selector_validation: Dict[str, Any],
    outcome_key: str,
    current_outcome: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "service": "fica_compliance",
        "status": "executed",
        "execution_plan_ack": execution_plan_ack,
        "execution_plan_validation": validation,
        "selector_validation": selector_validation,
        "received_payload": payload,
        "result": {
            "summary": f"FICA compliance worker executed governed {current_outcome['outcome_code']} with OCR-first runtime payload.",
            outcome_key: current_outcome,
        },
    }


def _build_fica_otc_001(payload: Dict[str, Any]) -> Dict[str, Any]:
    structured = _get_ocr_structured(payload, "identity")
    name = structured.get("full_name") or structured.get("name")
    id_number = structured.get("id_number") or structured.get("document_number")
    dob = structured.get("date_of_birth")
    fail_closed_reasons: List[str] = []

    if not structured:
        fail_closed_reasons.append("missing_identity_ocr_substrate")
    if not name and not id_number:
        fail_closed_reasons.append("missing_identity_anchor_fields")

    outcome_payload = {
        "outcome_intent": "extract_identity_document_fields",
        "extraction_status": "succeeded" if not fail_closed_reasons else "failed",
        "extracted_identity": {
            "full_name": name,
            "id_number": id_number,
            "date_of_birth": dob,
        },
        "overall_confidence": 0.9 if not fail_closed_reasons else 0.0,
    }

    return _base_current_outcome(
        "FICA-OTC-001",
        "proof_verification",
        "extract_identity_document_fields",
        outcome_payload,
        payload,
        fail_closed_reasons,
    )


def _build_fica_otc_002(payload: Dict[str, Any]) -> Dict[str, Any]:
    structured = _get_ocr_structured(payload, "identity")
    subject = _safe_dict(payload.get("subject"))
    fail_closed_reasons: List[str] = []

    if not structured:
        fail_closed_reasons.append("missing_identity_substrate")
    if not subject.get("id_number") and not subject.get("first_name") and not subject.get("last_name"):
        fail_closed_reasons.append("missing_required_subject_fields")

    extracted_name = str(structured.get("full_name") or structured.get("name") or "").strip().lower()
    subject_name = f"{subject.get('first_name', '')} {subject.get('last_name', '')}".strip().lower()
    extracted_id = str(structured.get("id_number") or structured.get("document_number") or "").strip()
    subject_id = str(subject.get("id_number") or "").strip()
    extracted_dob = str(structured.get("date_of_birth") or "").strip()
    subject_dob = str(subject.get("date_of_birth") or "").strip()

    name_match = bool(extracted_name and subject_name and extracted_name == subject_name)
    id_match = bool(extracted_id and subject_id and extracted_id == subject_id)
    dob_match = bool(extracted_dob and subject_dob and extracted_dob == subject_dob)

    mismatch_reasons: List[str] = []
    if subject_name and not name_match:
        mismatch_reasons.append("name_mismatch")
    if subject_id and not id_match:
        mismatch_reasons.append("id_number_mismatch")
    if subject_dob and not dob_match:
        mismatch_reasons.append("dob_mismatch")

    determination = "match" if (id_match or name_match) and not mismatch_reasons else "manual_review"

    outcome_payload = {
        "outcome_intent": "assess_identity_field_consistency",
        "identity_match_determination": determination,
        "name_match_flag": name_match,
        "id_number_match_flag": id_match,
        "dob_match_flag": dob_match,
        "mismatch_reasons": mismatch_reasons,
        "summary": "Identity field consistency evaluated against OCR-derived identity substrate.",
        "overall_confidence": 0.88 if not fail_closed_reasons else 0.0,
    }

    return _base_current_outcome(
        "FICA-OTC-002",
        "analytical",
        "assess_identity_field_consistency",
        outcome_payload,
        payload,
        fail_closed_reasons,
    )


def _build_fica_otc_003(payload: Dict[str, Any]) -> Dict[str, Any]:
    structured = _get_ocr_structured(payload, "proof_of_address")
    address = structured.get("address")
    document_date = structured.get("document_date")
    issuer_name = structured.get("issuer_name")
    fail_closed_reasons: List[str] = []

    if not structured:
        fail_closed_reasons.append("missing_proof_of_address_ocr_substrate")
    if not address:
        fail_closed_reasons.append("missing_address_content")
    if not document_date:
        fail_closed_reasons.append("missing_document_date")

    outcome_payload = {
        "outcome_intent": "extract_proof_of_address_fields",
        "extraction_status": "succeeded" if not fail_closed_reasons else "failed",
        "extracted_address": {
            "address": address,
            "document_date": document_date,
            "issuer_name": issuer_name,
        },
        "overall_confidence": 0.9 if not fail_closed_reasons else 0.0,
    }

    return _base_current_outcome(
        "FICA-OTC-003",
        "proof_verification",
        "extract_proof_of_address_fields",
        outcome_payload,
        payload,
        fail_closed_reasons,
    )


def _build_fica_otc_004(payload: Dict[str, Any]) -> Dict[str, Any]:
    structured = _get_ocr_structured(payload, "proof_of_address")
    max_age_days = _get_rule(payload, "rules", "proof_of_address", "max_age_days")
    fail_closed_reasons: List[str] = []

    if not structured:
        fail_closed_reasons.append("missing_proof_of_address_substrate")
    if max_age_days is None:
        fail_closed_reasons.append("missing_proof_of_address_max_age_rule")

    document_age_days = structured.get("document_age_days")
    if document_age_days is None:
        fail_closed_reasons.append("missing_document_age_days")

    address_present = bool(structured.get("address"))
    issuer_present = bool(structured.get("issuer_name"))
    recency_pass = False
    if isinstance(document_age_days, (int, float)) and isinstance(max_age_days, (int, float)):
        recency_pass = document_age_days <= max_age_days

    determination = "valid" if address_present and recency_pass and not fail_closed_reasons else "manual_review"

    outcome_payload = {
        "outcome_intent": "assess_proof_of_address_validity_and_recency",
        "address_validity_determination": determination,
        "recency_pass_flag": recency_pass,
        "address_completeness_flag": address_present,
        "issuer_acceptance_flag": issuer_present,
        "document_age_days": document_age_days,
        "summary": "Proof-of-address validity and recency evaluated against OCR-derived substrate and governed rule.",
        "overall_confidence": 0.86 if not fail_closed_reasons else 0.0,
    }

    return _base_current_outcome(
        "FICA-OTC-004",
        "analytical",
        "assess_proof_of_address_validity_and_recency",
        outcome_payload,
        payload,
        fail_closed_reasons,
    )


def _build_fica_otc_005(payload: Dict[str, Any]) -> Dict[str, Any]:
    structured = _get_ocr_structured(payload, "business_registration")
    company_name = structured.get("company_name")
    registration_number = structured.get("registration_number")
    representative_name = structured.get("representative_name")
    fail_closed_reasons: List[str] = []

    if not structured:
        fail_closed_reasons.append("missing_business_registration_ocr_substrate")
    if not company_name:
        fail_closed_reasons.append("missing_company_name")
    if not registration_number:
        fail_closed_reasons.append("missing_registration_number")

    outcome_payload = {
        "outcome_intent": "extract_business_registration_fields",
        "extraction_status": "succeeded" if not fail_closed_reasons else "failed",
        "extracted_business": {
            "company_name": company_name,
            "registration_number": registration_number,
            "representative_name": representative_name,
        },
        "overall_confidence": 0.89 if not fail_closed_reasons else 0.0,
    }

    return _base_current_outcome(
        "FICA-OTC-005",
        "proof_verification",
        "extract_business_registration_fields",
        outcome_payload,
        payload,
        fail_closed_reasons,
    )


def _build_fica_otc_006(payload: Dict[str, Any]) -> Dict[str, Any]:
    structured = _get_ocr_structured(payload, "business_registration")
    subject = _safe_dict(payload.get("subject"))
    fail_closed_reasons: List[str] = []

    if not structured:
        fail_closed_reasons.append("missing_business_registration_substrate")
    if not subject.get("company_name") and not subject.get("registration_number"):
        fail_closed_reasons.append("missing_claimed_company_anchors")

    extracted_company = str(structured.get("company_name") or "").strip().lower()
    claimed_company = str(subject.get("company_name") or "").strip().lower()
    extracted_reg = str(structured.get("registration_number") or "").strip()
    claimed_reg = str(subject.get("registration_number") or "").strip()

    company_match = bool(extracted_company and claimed_company and extracted_company == claimed_company)
    reg_match = bool(extracted_reg and claimed_reg and extracted_reg == claimed_reg)
    represented_person_found = bool(structured.get("representative_name"))

    gaps: List[str] = []
    if claimed_company and not company_match:
        gaps.append("company_name_mismatch")
    if claimed_reg and not reg_match:
        gaps.append("registration_number_mismatch")
    if not represented_person_found:
        gaps.append("representative_authority_not_found")

    if claimed_company and not company_match and claimed_reg and not reg_match:
        fail_closed_reasons.append("no_matching_company_anchor")
    if not represented_person_found:
        fail_closed_reasons.append("missing_representative_authority_evidence")

    determination = "consistent" if not fail_closed_reasons and (company_match or reg_match) else "manual_review"

    outcome_payload = {
        "outcome_intent": "assess_business_ownership_or_authority_consistency",
        "business_consistency_determination": determination,
        "company_name_match_flag": company_match,
        "registration_match_flag": reg_match,
        "represented_person_found_flag": represented_person_found,
        "gaps": gaps,
        "summary": "Business registration consistency evaluated against OCR-derived business substrate.",
        "overall_confidence": 0.85 if not fail_closed_reasons else 0.0,
    }

    return _base_current_outcome(
        "FICA-OTC-006",
        "analytical",
        "assess_business_ownership_or_authority_consistency",
        outcome_payload,
        payload,
        fail_closed_reasons,
    )


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

    if current_outcome.get("fail_closed_reasons"):
        errors.append("fail_closed_reasons_present")

    return {"status": "pass" if not errors else "fail", "errors": errors}


def run(payload: Dict[str, Any]) -> Dict[str, Any]:
    execution_plan_ack = _build_execution_plan_ack(payload)
    validation = _validate_execution_plan(payload, EXPECTED_SERVICE_FAMILY)

    if validation["status"] != "pass":
        return _reject(
            payload,
            execution_plan_ack,
            validation,
            None,
            "Worker rejected payload due to execution plan validation failure.",
            {},
        )

    selector = _normalize_selector(payload)
    selector_validation = _validate_selector(selector)

    if selector_validation["status"] != "pass":
        return _reject(
            payload,
            execution_plan_ack,
            validation,
            selector_validation,
            "Worker rejected payload because no governed FICA selector matched an implemented OCR-first outcome.",
            {},
        )

    matched_code = selector_validation["matched_governed_outcome_code"]

    builders = {
        "FICA-OTC-001": (_build_fica_otc_001, ["extraction_status", "extracted_identity", "overall_confidence"]),
        "FICA-OTC-002": (_build_fica_otc_002, ["identity_match_determination", "summary", "overall_confidence"]),
        "FICA-OTC-003": (_build_fica_otc_003, ["extraction_status", "extracted_address", "overall_confidence"]),
        "FICA-OTC-004": (_build_fica_otc_004, ["address_validity_determination", "summary", "overall_confidence"]),
        "FICA-OTC-005": (_build_fica_otc_005, ["extraction_status", "extracted_business", "overall_confidence"]),
        "FICA-OTC-006": (_build_fica_otc_006, ["business_consistency_determination", "summary", "overall_confidence"]),
    }

    builder, required_payload_keys = builders[matched_code]
    current_outcome = builder(payload)

    if current_outcome.get("fail_closed_reasons"):
        return _reject(
            payload,
            execution_plan_ack,
            validation,
            selector_validation,
            f"Worker rejected payload because selected {matched_code} failed closed under governed OCR-first rules.",
            {
                "current_outcome": current_outcome,
            },
        )

    contract_validation = _validate_current_outcome_shape(current_outcome, required_payload_keys)
    if contract_validation["status"] != "pass":
        return _reject(
            payload,
            execution_plan_ack,
            validation,
            selector_validation,
            f"Worker rejected payload because the generated {matched_code} outcome failed internal contract validation.",
            {
                "contract_validation": contract_validation,
                "current_outcome": current_outcome,
            },
        )

    outcome_key = matched_code.lower().replace("-", "_")
    return _emit_success(
        payload,
        execution_plan_ack,
        validation,
        selector_validation,
        outcome_key,
        current_outcome,
    )
