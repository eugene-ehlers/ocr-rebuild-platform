from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional
import uuid

from services.decision_engine.engine import execute_service_family
from services.decision_engine.request_store import (
    get_customer_consent_records,
    get_request,
    revoke_customer_consent,
    save_consent_record,
    save_request,
    update_request,
)


SUPPORTED_SERVICE_FAMILIES = {
    "financial_management": {
        "service_code_aliases": {
            "financial_management",
            "transaction_parsing",
            "category_classification",
            "cash_flow_classification",
            "debt_detection",
            "behavioural_analysis",
            "benchmarking",
            "reporting_explanation",
            "translation",
        }
    },
    "fica": {
        "service_code_aliases": {
            "fica",
            "fica_compliance",
            "transaction_compliance_classification",
            "document_validation",
            "identity_owner_verification",
        }
    },
    "credit_decision": {
        "service_code_aliases": {
            "credit_decision",
            "affordability",
            "prevet",
            "bureau_assessment",
            "offer_generation",
        }
    },
}


EXPECTED_DOCUMENT_TYPES = {
    "financial_management": {"bank_statement"},
    "fica": {"identity_document", "proof_of_address"},
    "credit_decision": {"bank_statement", "identity_document"},
}

DEFAULT_VALIDITY_SECONDS = {
    "processing": 60 * 60 * 24 * 30,
    "disclosure": 60 * 60 * 24 * 7,
}


@dataclass
class OrchestrationContext:
    request_id: str
    customer_id: str
    service_code: str
    service_family: str
    document_ids: List[str]
    disclose_to_third_party: bool
    created_at: str


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse_iso(ts: Optional[str]) -> Optional[datetime]:
    if not ts:
        return None
    return datetime.fromisoformat(ts)


def _new_request_id() -> str:
    return f"req_{uuid.uuid4().hex[:12]}"


def _new_consent_id() -> str:
    return f"consent_{uuid.uuid4().hex[:10]}"


def _resolve_service_family(service_code: str) -> str:
    normalized = (service_code or "").strip().lower()
    for family, cfg in SUPPORTED_SERVICE_FAMILIES.items():
        if normalized in cfg["service_code_aliases"]:
            return family
    raise ValueError(f"Unsupported service_code: {service_code}")


def _build_context(payload: Dict[str, Any]) -> OrchestrationContext:
    customer_id = str(payload.get("customerId", "")).strip()
    service_code = str(payload.get("serviceCode", "")).strip()
    document_ids = payload.get("documentIds", [])
    disclose = bool(payload.get("discloseToThirdParty", False))

    if not customer_id:
        raise ValueError("customerId is required")
    if not service_code:
        raise ValueError("serviceCode is required")
    if not isinstance(document_ids, list) or not document_ids:
        raise ValueError("documentIds must be a non-empty list")

    service_family = _resolve_service_family(service_code)

    return OrchestrationContext(
        request_id=_new_request_id(),
        customer_id=customer_id,
        service_code=service_code,
        service_family=service_family,
        document_ids=[str(x) for x in document_ids],
        disclose_to_third_party=disclose,
        created_at=_utc_now(),
    )


def _base_response(
    *,
    success: bool,
    status: str,
    message: str,
    data: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "success": success,
        "status": status,
        "message": message,
        "data": data,
    }


def _find_reusable_consent(customer_id: str, consent_type: str) -> Optional[Dict[str, Any]]:
    records = get_customer_consent_records(customer_id)
    candidates = [
        r for r in records
        if r.get("consent_type") == consent_type
    ]
    if not candidates:
        return None

    candidates.sort(key=lambda r: r.get("captured_at") or "", reverse=True)
    for record in candidates:
        if record.get("status") == "valid" and not record.get("is_expired") and not record.get("revoked", False):
            return record
    return None


def _derive_record_status(record: Dict[str, Any]) -> str:
    if not record.get("required", False):
        return "not_required"
    if record.get("revoked", False):
        return "revoked"
    if not record.get("provided", False):
        return "missing"
    if not record.get("evidence_ref"):
        return "invalid"

    valid_until = _parse_iso(record.get("valid_until"))
    if valid_until and valid_until < datetime.now(timezone.utc):
        return "expired"

    return "valid"


def _build_new_consent_record(consent_type: str, provided: bool, payload: Dict[str, Any], required: bool) -> Dict[str, Any]:
    source = str(payload.get(f"{consent_type}ConsentSource", "ui_checkbox"))
    evidence_ref = str(payload.get(f"{consent_type}ConsentEvidenceRef", "")).strip()
    standing = bool(payload.get(f"{consent_type}StandingConsent", True))
    now = datetime.now(timezone.utc)

    validity_seconds = DEFAULT_VALIDITY_SECONDS[consent_type]
    valid_from = now.isoformat() if provided else None
    valid_until = (now + timedelta(seconds=validity_seconds)).isoformat() if provided and standing else now.isoformat() if provided else None

    record = {
        "consent_id": _new_consent_id(),
        "consent_type": consent_type,
        "required": required,
        "provided": provided,
        "status": "unknown",
        "captured_at": now.isoformat() if provided else None,
        "source": source if provided else None,
        "evidence_ref": evidence_ref if provided else None,
        "standing": standing if provided else False,
        "validity_window_seconds": validity_seconds if provided else None,
        "valid_from": valid_from,
        "valid_until": valid_until,
        "is_expired": False,
        "revoked": False,
        "revoked_at": None,
        "reused": False,
    }

    record["status"] = _derive_record_status(record)
    record["is_expired"] = record["status"] == "expired"
    return record


def _get_or_create_consent_record(customer_id: str, consent_type: str, provided: bool, payload: Dict[str, Any], required: bool) -> Dict[str, Any]:
    if provided:
        record = _build_new_consent_record(consent_type, provided, payload, required)
        save_consent_record(customer_id, record)
        return record

    reusable = _find_reusable_consent(customer_id, consent_type)
    if reusable:
        reused = dict(reusable)
        reused["reused"] = True
        reused["status"] = _derive_record_status(reused)
        reused["is_expired"] = reused["status"] == "expired"
        return reused

    record = _build_new_consent_record(consent_type, False, payload, required)
    return record


def _evaluate_consent(context: OrchestrationContext, payload: Dict[str, Any]) -> Dict[str, Any]:
    processing_provided = bool(payload.get("processingConsent", False))
    disclosure_provided = bool(payload.get("disclosureConsent", False))

    processing_record = _get_or_create_consent_record(
        context.customer_id, "processing", processing_provided, payload, True
    )
    disclosure_record = _get_or_create_consent_record(
        context.customer_id, "disclosure", disclosure_provided, payload, context.disclose_to_third_party
    )

    consent_records = [processing_record, disclosure_record]

    status = "pass" if all(
        (not r["required"]) or r["status"] == "valid"
        for r in consent_records
    ) else "fail"

    reasons: List[str] = []
    for record in consent_records:
        if not record["required"]:
            continue
        if record["status"] == "missing":
            reasons.append(f"{record['consent_type']}_consent_missing")
        elif record["status"] == "invalid":
            reasons.append(f"{record['consent_type']}_consent_invalid")
        elif record["status"] == "expired":
            reasons.append(f"{record['consent_type']}_consent_expired")
        elif record["status"] == "revoked":
            reasons.append(f"{record['consent_type']}_consent_revoked")

    return {
        "processing_consent_required": True,
        "disclosure_consent_required": context.disclose_to_third_party,
        "status": status,
        "reasons": reasons,
        "mode": "soft_enforcement",
        "consent_records": consent_records,
    }


def _infer_document_type(document_id: str) -> str:
    normalized = document_id.strip().lower()
    if "bank" in normalized or "statement" in normalized:
        return "bank_statement"
    if "id" in normalized or "identity" in normalized:
        return "identity_document"
    if "address" in normalized or "poa" in normalized or "proof" in normalized:
        return "proof_of_address"
    return "unknown"


def _assess_document(document_id: str, expected_types: set[str]) -> Dict[str, Any]:
    inferred_type = _infer_document_type(document_id)
    quality_status = "acceptable" if len(document_id.strip()) >= 6 else "poor"
    freshness_status = "unknown"
    completeness_status = "unknown"

    reasons: List[str] = []
    readiness_score = 100

    if inferred_type == "unknown":
        reasons.append("document_type_unknown")
        readiness_score -= 30

    if inferred_type not in expected_types and inferred_type != "unknown":
        reasons.append("document_type_not_expected_for_service")
        readiness_score -= 20

    if quality_status != "acceptable":
        reasons.append("document_identifier_quality_poor")
        readiness_score -= 20

    if inferred_type in {"bank_statement", "identity_document", "proof_of_address"}:
        completeness_status = "assumed_present"
    else:
        completeness_status = "unknown"

    readiness_score = max(0, readiness_score)

    status = "pass" if readiness_score >= 70 and not any(
        reason in {"document_type_not_expected_for_service"} for reason in reasons
    ) else "fail"

    return {
        "document_id": document_id,
        "inferred_type": inferred_type,
        "expected_for_service": inferred_type in expected_types,
        "quality_status": quality_status,
        "freshness_status": freshness_status,
        "completeness_status": completeness_status,
        "readiness_score": readiness_score,
        "status": status,
        "reasons": reasons,
    }


def _evaluate_documents(context: OrchestrationContext) -> Dict[str, Any]:
    expected_types = EXPECTED_DOCUMENT_TYPES.get(context.service_family, set())
    assessments = [_assess_document(doc_id, expected_types) for doc_id in context.document_ids]

    reasons: List[str] = []
    if not context.document_ids:
        reasons.append("documents_missing")

    supplied_types = {a["inferred_type"] for a in assessments if a["inferred_type"] != "unknown"}
    missing_expected_types = sorted(list(expected_types - supplied_types))

    if missing_expected_types:
        reasons.append("required_document_types_missing")

    failing_docs = [a for a in assessments if a["status"] == "fail"]
    avg_score = int(sum(a["readiness_score"] for a in assessments) / len(assessments)) if assessments else 0

    overall_status = "pass" if not reasons and not failing_docs and avg_score >= 70 else "fail"

    return {
        "document_ids_received": context.document_ids,
        "document_count": len(context.document_ids),
        "assessments": assessments,
        "expected_document_types": sorted(list(expected_types)),
        "missing_expected_document_types": missing_expected_types,
        "average_readiness_score": avg_score,
        "status": overall_status,
        "reasons": reasons,
        "mode": "soft_enforcement",
    }


def _build_enforcement(consent_check: Dict[str, Any], document_check: Dict[str, Any]) -> Dict[str, Any]:
    overall = "pass" if consent_check["status"] == "pass" and document_check["status"] == "pass" else "fail"
    return {
        "consent": consent_check,
        "documents": document_check,
        "overall_status": overall,
        "enforcement_mode": "soft",
        "blocks_execution": False,
    }


def _build_remediation_prompts(enforcement: Dict[str, Any]) -> List[Dict[str, str]]:
    prompts: List[Dict[str, str]] = []

    for reason in enforcement["consent"]["reasons"]:
        if reason == "processing_consent_missing":
            prompts.append({
                "reason": reason,
                "suggestedAction": "Capture valid processing consent before production execution.",
            })
        elif reason == "disclosure_consent_missing":
            prompts.append({
                "reason": reason,
                "suggestedAction": "Capture valid disclosure consent before third-party sharing.",
            })
        elif reason == "processing_consent_invalid":
            prompts.append({
                "reason": reason,
                "suggestedAction": "Provide valid processing consent evidence reference and source.",
            })
        elif reason == "disclosure_consent_invalid":
            prompts.append({
                "reason": reason,
                "suggestedAction": "Provide valid disclosure consent evidence reference and source.",
            })
        elif reason == "processing_consent_expired":
            prompts.append({
                "reason": reason,
                "suggestedAction": "Refresh expired processing consent before execution.",
            })
        elif reason == "disclosure_consent_expired":
            prompts.append({
                "reason": reason,
                "suggestedAction": "Refresh expired disclosure consent before sharing.",
            })
        elif reason == "processing_consent_revoked":
            prompts.append({
                "reason": reason,
                "suggestedAction": "Capture a new processing consent because the previous one was revoked.",
            })
        elif reason == "disclosure_consent_revoked":
            prompts.append({
                "reason": reason,
                "suggestedAction": "Capture a new disclosure consent because the previous one was revoked.",
            })

    for reason in enforcement["documents"]["reasons"]:
        if reason == "documents_missing":
            prompts.append({
                "reason": reason,
                "suggestedAction": "Upload the required documents before execution.",
            })
        elif reason == "required_document_types_missing":
            missing = enforcement["documents"].get("missing_expected_document_types", [])
            prompts.append({
                "reason": reason,
                "suggestedAction": f"Provide missing document types required for this service: {', '.join(missing)}.",
            })

    for assessment in enforcement["documents"].get("assessments", []):
        for reason in assessment.get("reasons", []):
            if reason == "document_type_unknown":
                prompts.append({
                    "reason": reason,
                    "suggestedAction": f"Clarify or relabel document {assessment['document_id']} so its type can be identified.",
                })
            elif reason == "document_type_not_expected_for_service":
                prompts.append({
                    "reason": reason,
                    "suggestedAction": f"Replace document {assessment['document_id']} with one expected for this service.",
                })
            elif reason == "document_identifier_quality_poor":
                prompts.append({
                    "reason": reason,
                    "suggestedAction": f"Improve document identifier or source quality for {assessment['document_id']}.",
                })

    deduped: List[Dict[str, str]] = []
    seen = set()
    for prompt in prompts:
        key = (prompt["reason"], prompt["suggestedAction"])
        if key not in seen:
            seen.add(key)
            deduped.append(prompt)
    return deduped


def _execute(context: OrchestrationContext) -> Dict[str, Any]:
    execution_payload = {
        "request_id": context.request_id,
        "customer_id": context.customer_id,
        "service_code": context.service_code,
        "service_family": context.service_family,
        "document_ids": context.document_ids,
        "disclose_to_third_party": context.disclose_to_third_party,
        "timestamp": _utc_now(),
    }
    return execute_service_family(context.service_family, execution_payload)


def get_catalog() -> Dict[str, Any]:
    items = [
        {
            "serviceCode": "financial_management",
            "serviceName": "Financial Management",
            "serviceFamily": "financial_management",
            "requiresProcessingConsent": True,
            "requiresDisclosureConsent": False,
        },
        {
            "serviceCode": "fica",
            "serviceName": "FICA Compliance",
            "serviceFamily": "fica",
            "requiresProcessingConsent": True,
            "requiresDisclosureConsent": False,
        },
        {
            "serviceCode": "credit_decision",
            "serviceName": "Credit Decision",
            "serviceFamily": "credit_decision",
            "requiresProcessingConsent": True,
            "requiresDisclosureConsent": True,
        },
    ]

    return _base_response(
        success=True,
        status="ready",
        message="Service catalog retrieved.",
        data={"items": items},
    )


def create_request(payload: Dict[str, Any]) -> Dict[str, Any]:
    context = _build_context(payload)

    consent_check = _evaluate_consent(context, payload)
    document_check = _evaluate_documents(context)
    enforcement = _build_enforcement(consent_check, document_check)
    remediation_prompts = _build_remediation_prompts(enforcement)

    downstream_execution = _execute(context)

    orchestration_record = {
        "request": asdict(context),
        "consent_check": consent_check,
        "consent_records": consent_check["consent_records"],
        "document_check": document_check,
        "enforcement": enforcement,
        "remediation_prompts": remediation_prompts,
        "routing": {
            "selected_service_family": context.service_family,
            "selected_service_code": context.service_code,
            "orchestration_layer": "services.decision_engine.frontend_request_orchestrator",
        },
        "request_status": "completed",
        "result_status": "available",
        "downstream_execution": downstream_execution,
        "last_updated": _utc_now(),
    }

    save_request(orchestration_record)

    return _base_response(
        success=True,
        status="executed_with_soft_enforcement",
        message="Request evaluated, executed, and persisted under soft enforcement with standing consent handling.",
        data=orchestration_record,
    )


def get_status(request_id: str) -> Dict[str, Any]:
    record = get_request(request_id)
    if not record:
        return _base_response(
            success=False,
            status="not_found",
            message="Request status not found.",
            data={"requestId": request_id},
        )

    return _base_response(
        success=True,
        status="ready",
        message="Request status retrieved.",
        data={
            "requestId": request_id,
            "requestStatus": record.get("request_status", "unknown"),
            "resultStatus": record.get("result_status", "unknown"),
            "serviceFamily": record["request"]["service_family"],
            "enforcementOverallStatus": record.get("enforcement", {}).get("overall_status"),
            "documentReadinessScore": record.get("document_check", {}).get("average_readiness_score"),
            "consentRecords": record.get("consent_records", []),
            "lastUpdated": record.get("last_updated"),
        },
    )


def get_remediation(request_id: str) -> Dict[str, Any]:
    record = get_request(request_id)
    if not record:
        return _base_response(
            success=False,
            status="not_found",
            message="Remediation prompts not found.",
            data={"requestId": request_id},
        )

    return _base_response(
        success=True,
        status="ready",
        message="Remediation prompts retrieved.",
        data={
            "requestId": request_id,
            "prompts": record.get("remediation_prompts", []),
        },
    )


def get_result(request_id: str) -> Dict[str, Any]:
    record = get_request(request_id)
    if not record:
        return _base_response(
            success=False,
            status="not_found",
            message="Result not found.",
            data={"requestId": request_id},
        )

    return _base_response(
        success=True,
        status="ready",
        message="Result retrieved.",
        data={
            "requestId": request_id,
            "resultStatus": record.get("result_status", "unknown"),
            "enforcement": record.get("enforcement"),
            "consentRecords": record.get("consent_records", []),
            "documentCheck": record.get("document_check"),
            "result": record.get("downstream_execution"),
        },
    )


def rerun_request(request_id: str) -> Dict[str, Any]:
    record = get_request(request_id)
    if not record:
        return _base_response(
            success=False,
            status="not_found",
            message="Rerun target not found.",
            data={"requestId": request_id},
        )

    context = OrchestrationContext(
        request_id=request_id,
        customer_id=record["request"]["customer_id"],
        service_code=record["request"]["service_code"],
        service_family=record["request"]["service_family"],
        document_ids=record["request"]["document_ids"],
        disclose_to_third_party=record["request"]["disclose_to_third_party"],
        created_at=record["request"]["created_at"],
    )

    downstream_execution = _execute(context)
    updated = update_request(
        request_id,
        {
            "downstream_execution": downstream_execution,
            "request_status": "completed",
            "result_status": "available",
            "last_updated": _utc_now(),
        },
    )

    return _base_response(
        success=True,
        status="executed",
        message="Rerun executed and persisted.",
        data={
            "requestId": request_id,
            "updatedRecord": updated,
        },
    )


def revoke_consent(consent_id: str) -> Dict[str, Any]:
    revoked = revoke_customer_consent(consent_id, _utc_now())
    if not revoked:
        return _base_response(
            success=False,
            status="not_found",
            message="Consent record not found for revocation.",
            data={"consentId": consent_id},
        )

    return _base_response(
        success=True,
        status="revoked",
        message="Consent record revoked.",
        data={"consentId": consent_id},
    )
