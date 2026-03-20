from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List
import uuid


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


def _placeholder_downstream_execution(context: OrchestrationContext) -> Dict[str, Any]:
    family = context.service_family

    family_outputs = {
        "financial_management": {
            "service_family": "financial_management",
            "downstream_status": "placeholder_executed",
            "summary": "Financial Management placeholder execution completed.",
            "capabilities_hint": [
                "transaction_parsing",
                "category_classification",
                "cash_flow_classification",
                "debt_detection",
                "behavioural_analysis",
                "benchmarking",
                "reporting_explanation",
            ],
        },
        "fica": {
            "service_family": "fica",
            "downstream_status": "placeholder_executed",
            "summary": "FICA placeholder execution completed.",
            "capabilities_hint": [
                "transaction_compliance_classification",
                "document_validation",
                "identity_owner_verification",
            ],
        },
        "credit_decision": {
            "service_family": "credit_decision",
            "downstream_status": "placeholder_executed",
            "summary": "Credit Decision placeholder execution completed.",
            "capabilities_hint": [
                "affordability",
                "prevet",
                "bureau_assessment",
                "offer_generation",
            ],
        },
    }

    return family_outputs[family]


def create_request(payload: Dict[str, Any]) -> Dict[str, Any]:
    context = _build_context(payload)

    orchestration_record = {
        "request": asdict(context),
        "consent_check": {
            "processing_consent_required": True,
            "disclosure_consent_required": context.disclose_to_third_party,
            "status": "placeholder_not_enforced_in_backend_phase11",
        },
        "document_check": {
            "document_ids_received": context.document_ids,
            "status": "placeholder_not_enforced_in_backend_phase11",
        },
        "routing": {
            "selected_service_family": context.service_family,
            "selected_service_code": context.service_code,
            "orchestration_layer": "services.decision_engine.frontend_request_orchestrator",
        },
        "downstream_execution": _placeholder_downstream_execution(context),
    }

    return _base_response(
        success=True,
        status="orchestrated_placeholder",
        message="Request created and routed through backend orchestration placeholder.",
        data=orchestration_record,
    )


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
        status="placeholder",
        message="Service catalog retrieved.",
        data={"items": items},
    )


def get_status(request_id: str) -> Dict[str, Any]:
    return _base_response(
        success=True,
        status="placeholder",
        message="Request status retrieved.",
        data={
            "requestId": request_id,
            "requestStatus": "in_progress",
            "orchestrationStatus": "placeholder",
        },
    )


def get_remediation(request_id: str) -> Dict[str, Any]:
    return _base_response(
        success=True,
        status="placeholder",
        message="Remediation prompts retrieved.",
        data={
            "requestId": request_id,
            "prompts": [
                {
                    "reason": "placeholder_document_or_consent_gap",
                    "suggestedAction": "Complete consent and document readiness wiring in later phases.",
                }
            ],
        },
    )


def get_result(request_id: str) -> Dict[str, Any]:
    return _base_response(
        success=True,
        status="placeholder",
        message="Result retrieved.",
        data={
            "requestId": request_id,
            "resultStatus": "available",
            "result": {
                "summary": "Placeholder downstream result.",
                "source": "backend_orchestration_phase11",
            },
        },
    )


def rerun_request(request_id: str) -> Dict[str, Any]:
    return _base_response(
        success=True,
        status="placeholder",
        message="Rerun trigger accepted as placeholder.",
        data={
            "requestId": request_id,
            "rerunAccepted": True,
        },
    )
