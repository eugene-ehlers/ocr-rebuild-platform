from __future__ import annotations

from typing import Any, Dict


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


def run(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "service": "credit_decision",
        "status": "executed",
        "execution_plan_ack": _build_execution_plan_ack(payload),
        "received_payload": payload,
        "result": {
            "summary": "Credit decision worker executed with real orchestration payload.",
            "capabilities": [
                "affordability",
                "prevet",
                "bureau_assessment",
                "offer_generation",
            ],
        },
    }
