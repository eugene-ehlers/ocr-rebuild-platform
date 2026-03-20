import json
import os
from datetime import datetime, timezone
from typing import Any, Dict

import boto3


s3 = boto3.client("s3")
INPUT_S3_BUCKET = os.environ.get("INPUT_S3_BUCKET", "")
INPUT_S3_KEY = os.environ.get("INPUT_S3_KEY", "")
OUTPUT_S3_BUCKET = os.environ.get("OUTPUT_S3_BUCKET", "")
OUTPUT_S3_KEY = os.environ.get("OUTPUT_S3_KEY", "")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def empty_payload() -> Dict[str, Any]:
    return {
        "manifest_id": "UNKNOWN",
        "document_id": "UNKNOWN",
        "source_uri": "UNKNOWN",
        "pages": [],
        "manifest_update": {},
        "execution_state": {},
        "requested_services": {},
        "service_status": {},
        "execution_plan": {},
        "routing_decision": {},
        "evaluation": {}
    }


def load_input(event: Dict[str, Any]) -> Dict[str, Any]:
    if INPUT_S3_BUCKET and INPUT_S3_KEY:
        response = s3.get_object(Bucket=INPUT_S3_BUCKET, Key=INPUT_S3_KEY)
        return json.loads(response["Body"].read().decode("utf-8"))

    input_s3_bucket = event.get("input_s3_bucket", "")
    input_s3_key = event.get("input_s3_key", "")
    if input_s3_bucket and input_s3_key:
        response = s3.get_object(Bucket=input_s3_bucket, Key=input_s3_key)
        return json.loads(response["Body"].read().decode("utf-8"))

    return event if event else empty_payload()


def write_output(result: Dict[str, Any], event: Dict[str, Any]) -> None:
    output_bucket = event.get("output_s3_bucket", OUTPUT_S3_BUCKET)
    output_key = event.get("output_s3_key", OUTPUT_S3_KEY)

    if output_bucket and output_key:
        s3.put_object(
            Bucket=output_bucket,
            Key=output_key,
            Body=json.dumps(result, indent=2).encode("utf-8"),
            ContentType="application/json"
        )


def determine_final_decision(payload: Dict[str, Any]) -> Dict[str, str]:
    evaluation = dict(payload.get("evaluation", {}))
    requested_services = dict(payload.get("requested_services", {}))
    service_status = dict(payload.get("service_status", {}))
    canonical_document = dict(payload.get("canonical_document", {}))
    canonical_metadata = dict(canonical_document.get("metadata", {})) if isinstance(canonical_document.get("metadata", {}), dict) else {}

    page_count = canonical_metadata.get("page_count", 0)
    non_empty_pages = canonical_metadata.get("non_empty_pages", 0)

    requested_optional = [
        service_name for service_name, requested in requested_services.items()
        if service_name != "ocr" and requested is True
    ]
    incomplete_optional = [
        service_name for service_name in requested_optional
        if service_status.get(service_name) != "completed"
    ]

    if page_count == 0:
        return {
            "decision": "FINAL_REJECT",
            "reason": "no_pages_available_for_final_delivery_v1"
        }

    if non_empty_pages == 0:
        return {
            "decision": "ESCALATE",
            "reason": "no_non_empty_pages_available_for_final_delivery_v1"
        }

    if incomplete_optional:
        return {
            "decision": "FINAL_ACCEPT_WITH_QUALIFICATION",
            "reason": "requested_optional_services_incomplete_v1"
        }

    if evaluation.get("gate3_ready_for_aggregation", False):
        return {
            "decision": "FINAL_ACCEPT",
            "reason": "all_required_outputs_present_v1"
        }

    return {
        "decision": "FINAL_ACCEPT_WITH_QUALIFICATION",
        "reason": "final_state_accepted_with_runtime_qualification_v1"
    }


def update_execution_plan(payload: Dict[str, Any], final_decision: str, final_reason: str) -> Dict[str, Any]:
    execution_plan = dict(payload.get("execution_plan", {}))
    decision_gate_history = list(execution_plan.get("decision_gate_history", []))

    decision_gate_history.append({
        "gate_id": "4",
        "gate_name": "Final Validation and Delivery Decision",
        "decision_engine_id": "4",
        "decision_state": final_decision,
        "decision_reason": final_reason,
        "plan_change_summary": "Gate 4 final validation completed.",
        "timestamp": utc_now_iso()
    })

    execution_plan.update({
        "plan_status": "completed" if final_decision in ("FINAL_ACCEPT", "FINAL_ACCEPT_WITH_QUALIFICATION", "FINAL_ACCEPT_PARTIAL") else "escalated",
        "final_status": final_decision,
        "decision_gate_history": decision_gate_history
    })
    return execution_plan


def build_manifest_update(payload: Dict[str, Any], final_decision: str, final_reason: str) -> Dict[str, Any]:
    now = utc_now_iso()
    manifest_update = dict(payload.get("manifest_update", {}))
    pipeline_history = list(manifest_update.get("pipeline_history", []))

    pipeline_history.append({
        "stage": "gate4_final_validation",
        "status": final_decision.lower(),
        "timestamp": now,
        "engine_name": "gate4_final_validation_evaluator",
        "engine_version": "v1",
        "notes": final_reason
    })

    manifest_update.update({
        "pipeline_status": "completed" if final_decision in ("FINAL_ACCEPT", "FINAL_ACCEPT_WITH_QUALIFICATION", "FINAL_ACCEPT_PARTIAL") else "escalated",
        "last_updated": now,
        "pipeline_history": pipeline_history
    })
    return manifest_update


def build_routing_decision(payload: Dict[str, Any], final_decision: str, final_reason: str) -> Dict[str, Any]:
    routing_decision = dict(payload.get("routing_decision", {}))
    routing_decision.update({
        "last_gate_applied": "4",
        "current_route_state": "gate4_completed",
        "decision_basis": final_reason,
        "gate4_final_decision": final_decision,
        "delivery_ready": final_decision in ("FINAL_ACCEPT", "FINAL_ACCEPT_WITH_QUALIFICATION", "FINAL_ACCEPT_PARTIAL")
    })
    return routing_decision


def build_evaluation(payload: Dict[str, Any], final_decision: str, final_reason: str) -> Dict[str, Any]:
    evaluation = dict(payload.get("evaluation", {}))
    evaluation.update({
        "gate4_completed": True,
        "gate4_final_decision": final_decision,
        "gate4_final_reason": final_reason,
        "delivery_ready": final_decision in ("FINAL_ACCEPT", "FINAL_ACCEPT_WITH_QUALIFICATION", "FINAL_ACCEPT_PARTIAL")
    })
    return evaluation


def build_execution_state(payload: Dict[str, Any]) -> Dict[str, Any]:
    execution_state = dict(payload.get("execution_state", {}))
    completed_stages = list(execution_state.get("completed_stages", []))

    if "gate4_final_validation" not in completed_stages:
        completed_stages.append("gate4_final_validation")

    execution_state.update({
        "current_stage": "gate4_final_validation",
        "completed_stages": completed_stages
    })
    return execution_state


def evaluate_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    decision = determine_final_decision(payload)
    final_decision = decision["decision"]
    final_reason = decision["reason"]

    result = dict(payload)
    result["execution_plan"] = update_execution_plan(payload, final_decision, final_reason)
    result["routing_decision"] = build_routing_decision(payload, final_decision, final_reason)
    result["evaluation"] = build_evaluation(payload, final_decision, final_reason)
    result["manifest_update"] = build_manifest_update(payload, final_decision, final_reason)
    result["execution_state"] = build_execution_state(payload)
    return result


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    payload = load_input(event)
    result = evaluate_payload(payload)
    write_output(result, event)
    return result
