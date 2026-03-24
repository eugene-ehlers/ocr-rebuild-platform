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


def get_text_ocr_plan(payload: Dict[str, Any]) -> Dict[str, Any]:
    execution_plan = dict(payload.get("execution_plan", {}))
    capability_plan = dict(execution_plan.get("capability_plan", {}))
    return dict(capability_plan.get("TEXT_OCR", {}))


def evaluate_page(page: Dict[str, Any], text_ocr_plan: Dict[str, Any]) -> Dict[str, Any]:
    text = (page.get("extracted_text", "") or "").strip()
    confidence = (
        page.get("line_block_word_confidence", {}).get("page_confidence", 0.0)
        if isinstance(page.get("line_block_word_confidence", {}), dict)
        else 0.0
    )

    fallback_allowed = bool(text_ocr_plan.get("fallback_allowed", False))

    page_decision = "ACCEPT"
    page_reason = "ocr_quality_acceptable_v1"

    if not text:
        page_decision = "ESCALATE_EXTERNAL" if fallback_allowed else "FAIL_QUALITY_GATE"
        page_reason = "no_text_extracted_v1"
    elif len(text) < 10:
        page_decision = "ESCALATE_EXTERNAL" if fallback_allowed else "FAIL_QUALITY_GATE"
        page_reason = "text_length_below_threshold_v1"
    elif confidence < 0.7:
        page_decision = "ESCALATE_EXTERNAL" if fallback_allowed else "FAIL_QUALITY_GATE"
        page_reason = "ocr_confidence_below_threshold_v1"

    page_evaluation = dict(page.get("evaluation", {}))
    page_evaluation.update({
        "gate2_quality_decision": page_decision,
        "gate2_quality_reason": page_reason
    })

    page_routing = dict(page.get("routing_decision", {}))
    page_routing.update({
        "last_gate_applied": "2",
        "gate2_quality_decision": page_decision,
        "gate2_quality_reason": page_reason
    })

    updated_page = dict(page)
    updated_page["evaluation"] = page_evaluation
    updated_page["routing_decision"] = page_routing
    return updated_page


def update_execution_plan(payload: Dict[str, Any], overall_decision: str, overall_reason: str) -> Dict[str, Any]:
    execution_plan = dict(payload.get("execution_plan", {}))
    decision_gate_history = list(execution_plan.get("decision_gate_history", []))

    decision_gate_history.append({
        "gate_id": "2",
        "gate_name": "Extraction Quality and Fallback Decision",
        "decision_engine_id": "2",
        "decision_state": overall_decision,
        "decision_reason": overall_reason,
        "plan_change_summary": "Gate 2 quality evaluation completed for OCR outputs.",
        "timestamp": utc_now_iso()
    })

    if overall_decision == "ESCALATE_EXTERNAL":
        plan_status = "adjusted"
    elif overall_decision == "FAIL_QUALITY_GATE":
        plan_status = "failed"
    else:
        plan_status = execution_plan.get("plan_status", "in_progress")

    execution_plan.update({
        "plan_status": plan_status,
        "decision_gate_history": decision_gate_history
    })
    return execution_plan


def build_manifest_update(payload: Dict[str, Any], overall_decision: str, overall_reason: str) -> Dict[str, Any]:
    now = utc_now_iso()
    manifest_update = dict(payload.get("manifest_update", {}))
    pipeline_history = list(manifest_update.get("pipeline_history", []))

    pipeline_history.append({
        "stage": "gate2_quality_evaluation",
        "status": overall_decision.lower(),
        "timestamp": now,
        "engine_name": "gate2_quality_evaluator",
        "engine_version": "v1",
        "notes": overall_reason
    })

    manifest_update.update({
        "last_updated": now,
        "pipeline_status": "failed" if overall_decision == "FAIL_QUALITY_GATE" else manifest_update.get("pipeline_status", "processing"),
        "pipeline_history": pipeline_history
    })
    return manifest_update


def build_routing_decision(payload: Dict[str, Any], overall_decision: str, overall_reason: str, text_ocr_plan: Dict[str, Any]) -> Dict[str, Any]:
    routing_decision = dict(payload.get("routing_decision", {}))
    fallback_used = bool(routing_decision.get("fallback_used", False))

    fallback_provider = str(routing_decision.get("selected_provider_summary", "")).strip()
    if not fallback_used:
        fallback_provider = ""

    routing_decision.update({
        "last_gate_applied": "2",
        "current_route_state": "gate2_failed" if overall_decision == "FAIL_QUALITY_GATE" else "gate2_completed",
        "fallback_used": fallback_used,
        "fallback_provider": fallback_provider,
        "decision_basis": overall_reason,
        "gate2_overall_decision": overall_decision
    })
    return routing_decision


def build_evaluation(payload: Dict[str, Any], pages: List[Dict[str, Any]], overall_decision: str, overall_reason: str) -> Dict[str, Any]:
    evaluation = dict(payload.get("evaluation", {}))
    quality_scores = [
        page.get("line_block_word_confidence", {}).get("page_confidence", 0.0)
        for page in pages
        if isinstance(page, dict) and isinstance(page.get("line_block_word_confidence", {}), dict)
    ]
    evaluation.update({
        "gate2_completed": True,
        "gate2_overall_decision": overall_decision,
        "gate2_overall_reason": overall_reason,
        "gate2_fail_closed": overall_decision == "FAIL_QUALITY_GATE",
        "average_page_confidence": (sum(quality_scores) / len(quality_scores)) if quality_scores else 0.0
    })
    return evaluation


def build_execution_state(payload: Dict[str, Any]) -> Dict[str, Any]:
    execution_state = dict(payload.get("execution_state", {}))
    completed_stages = list(execution_state.get("completed_stages", []))

    if "gate2_quality_evaluation" not in completed_stages:
        completed_stages.append("gate2_quality_evaluation")

    execution_state.update({
        "current_stage": "gate2_quality_evaluation",
        "completed_stages": completed_stages
    })
    return execution_state


def evaluate_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    text_ocr_plan = get_text_ocr_plan(payload)
    pages = payload.get("pages", [])
    evaluated_pages: List[Dict[str, Any]] = []

    decisions = []
    for page in pages:
        if not isinstance(page, dict):
            continue
        updated_page = evaluate_page(page, text_ocr_plan)
        evaluated_pages.append(updated_page)
        decisions.append(updated_page.get("evaluation", {}).get("gate2_quality_decision", "ACCEPT"))

    overall_decision = "ACCEPT_PRIMARY_RESULT"
    overall_reason = "all_pages_acceptable_v1"

    if "FAIL_QUALITY_GATE" in decisions:
        overall_decision = "FAIL_QUALITY_GATE"
        overall_reason = "one_or_more_pages_failed_quality_gate_without_governed_fallback_v1"
    elif "ESCALATE_EXTERNAL" in decisions:
        overall_decision = "ESCALATE_EXTERNAL"
        overall_reason = "one_or_more_pages_require_external_fallback_v1"
    elif "PARTIAL_ACCEPT" in decisions:
        overall_decision = "PARTIAL_ACCEPT"
        overall_reason = "one_or_more_pages_only_partially_acceptable_v1"

    result = dict(payload)
    result["pages"] = evaluated_pages
    result["execution_plan"] = update_execution_plan(payload, overall_decision, overall_reason)
    result["routing_decision"] = build_routing_decision(payload, overall_decision, overall_reason, text_ocr_plan)
    result["evaluation"] = build_evaluation(payload, evaluated_pages, overall_decision, overall_reason)
    result["manifest_update"] = build_manifest_update(payload, overall_decision, overall_reason)
    result["execution_state"] = build_execution_state(payload)
    return result


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    payload = load_input(event)
    result = evaluate_payload(payload)
    write_output(result, event)
    return result
