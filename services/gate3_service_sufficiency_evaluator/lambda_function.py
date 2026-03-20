import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List

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


def determine_required_enrichments(payload: Dict[str, Any]) -> List[str]:
    requested_services = dict(payload.get("requested_services", {}))
    service_status = dict(payload.get("service_status", {}))

    ordered_candidates = [
        ("table_extraction", "table_extraction"),
        ("logo_recognition", "logo_recognition"),
        ("fraud_detection", "fraud_detection")
    ]

    required = []
    for request_key, service_key in ordered_candidates:
        if requested_services.get(request_key, False) and service_status.get(service_key) != "completed":
            required.append(service_key)

    return required


def update_execution_plan(payload: Dict[str, Any], overall_decision: str, overall_reason: str, required_enrichments: List[str]) -> Dict[str, Any]:
    execution_plan = dict(payload.get("execution_plan", {}))
    decision_gate_history = list(execution_plan.get("decision_gate_history", []))

    decision_gate_history.append({
        "gate_id": "3",
        "gate_name": "Service Sufficiency and Enrichment Decision",
        "decision_engine_id": "3",
        "decision_state": overall_decision,
        "decision_reason": overall_reason,
        "plan_change_summary": "Gate 3 service sufficiency evaluation completed.",
        "timestamp": utc_now_iso()
    })

    execution_plan.update({
        "plan_status": "in_progress" if required_enrichments else "ready_for_final_validation",
        "decision_gate_history": decision_gate_history,
        "remaining_enrichment_capabilities": required_enrichments
    })
    return execution_plan


def build_manifest_update(payload: Dict[str, Any], overall_decision: str, overall_reason: str) -> Dict[str, Any]:
    now = utc_now_iso()
    manifest_update = dict(payload.get("manifest_update", {}))
    pipeline_history = list(manifest_update.get("pipeline_history", []))

    pipeline_history.append({
        "stage": "gate3_service_sufficiency",
        "status": overall_decision.lower(),
        "timestamp": now,
        "engine_name": "gate3_service_sufficiency_evaluator",
        "engine_version": "v1",
        "notes": overall_reason
    })

    manifest_update.update({
        "last_updated": now,
        "pipeline_history": pipeline_history
    })
    return manifest_update


def build_routing_decision(payload: Dict[str, Any], overall_decision: str, overall_reason: str, required_enrichments: List[str]) -> Dict[str, Any]:
    routing_decision = dict(payload.get("routing_decision", {}))
    next_stage = required_enrichments[0] if required_enrichments else "aggregation"

    routing_decision.update({
        "last_gate_applied": "3",
        "current_route_state": "gate3_completed",
        "decision_basis": overall_reason,
        "gate3_service_sufficiency_decision": overall_decision,
        "gate3_required_enrichments": required_enrichments,
        "gate3_next_stage": next_stage,
        "gate3_ready_for_aggregation": len(required_enrichments) == 0
    })
    return routing_decision


def build_evaluation(payload: Dict[str, Any], overall_decision: str, overall_reason: str, required_enrichments: List[str]) -> Dict[str, Any]:
    evaluation = dict(payload.get("evaluation", {}))
    evaluation.update({
        "gate3_completed": True,
        "gate3_service_sufficiency_decision": overall_decision,
        "gate3_service_sufficiency_reason": overall_reason,
        "gate3_required_enrichments": required_enrichments,
        "gate3_ready_for_aggregation": len(required_enrichments) == 0
    })
    return evaluation


def build_execution_state(payload: Dict[str, Any]) -> Dict[str, Any]:
    execution_state = dict(payload.get("execution_state", {}))
    completed_stages = list(execution_state.get("completed_stages", []))

    if "gate3_service_sufficiency" not in completed_stages:
        completed_stages.append("gate3_service_sufficiency")

    execution_state.update({
        "current_stage": "gate3_service_sufficiency",
        "completed_stages": completed_stages
    })
    return execution_state


def evaluate_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    required_enrichments = determine_required_enrichments(payload)

    if required_enrichments:
        overall_decision = "ENRICHMENT_REQUIRED"
        overall_reason = "one_or_more_requested_services_not_yet_completed_v1"
    else:
        overall_decision = "READY_FOR_AGGREGATION"
        overall_reason = "all_requested_services_completed_or_not_required_v1"

    result = dict(payload)
    result["execution_plan"] = update_execution_plan(payload, overall_decision, overall_reason, required_enrichments)
    result["routing_decision"] = build_routing_decision(payload, overall_decision, overall_reason, required_enrichments)
    result["evaluation"] = build_evaluation(payload, overall_decision, overall_reason, required_enrichments)
    result["manifest_update"] = build_manifest_update(payload, overall_decision, overall_reason)
    result["execution_state"] = build_execution_state(payload)
    return result


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    payload = load_input(event)
    result = evaluate_payload(payload)
    write_output(result, event)
    return result
