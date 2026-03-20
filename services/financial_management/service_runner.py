from __future__ import annotations

from typing import Any, Dict, List


EXPECTED_SERVICE_FAMILY = "financial_management"
EXPECTED_STAGE = "downstream_execution"
SUPPORTED_PLAN_VERSIONS = {"execution_plan_v1"}


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

    return {
        "service": "financial_management",
        "status": "executed",
        "execution_plan_ack": execution_plan_ack,
        "execution_plan_validation": validation,
        "received_payload": payload,
        "result": {
            "summary": "Financial management worker executed with real orchestration payload.",
            "capabilities": [
                "transaction_parsing",
                "category_classification",
                "cash_flow_classification",
                "debt_detection",
                "behavioural_analysis",
                "benchmarking",
                "reporting_explanation",
            ],
        },
    }
