from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List
import uuid

from services.decision_engine.engine import execute_service_family
from services.decision_engine.request_store import get_request, save_request, update_request


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


def _new_request_id() -> str:
    return f"req_{uuid.uuid4().hex[:12]}"


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
    downstream_execution = _execute(context)

    orchestration_record = {
        "request": asdict(context),
        "consent_check": {
            "processing_consent_required": True,
            "disclosure_consent_required": context.disclose_to_third_party,
            "status": "placeholder_not_enforced_in_backend_phase12",
        },
        "document_check": {
            "document_ids_received": context.document_ids,
            "status": "placeholder_not_enforced_in_backend_phase12",
        },
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
        status="executed",
        message="Request created, executed, and persisted through backend orchestration.",
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

    prompts = []
    if record["consent_check"]["status"] != "enforced":
        prompts.append({
            "reason": "consent_not_enforced_yet",
            "suggestedAction": "Implement real consent validation in a later phase.",
        })
    if record["document_check"]["status"] != "enforced":
        prompts.append({
            "reason": "document_validation_not_enforced_yet",
            "suggestedAction": "Implement real document readiness validation in a later phase.",
        })

    return _base_response(
        success=True,
        status="ready",
        message="Remediation prompts retrieved.",
        data={
            "requestId": request_id,
            "prompts": prompts,
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
