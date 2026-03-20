from __future__ import annotations

import json
import os
from typing import Any, Dict, List

import boto3

s3 = boto3.client("s3")

OUTPUT_BUCKET = os.environ.get("OUTPUT_BUCKET", "")
EXPECTED_STAGE = "aggregation"
SUPPORTED_PLAN_VERSIONS = {"execution_plan_v1"}


def _build_execution_plan_ack(payload: Dict[str, Any]) -> Dict[str, Any]:
    execution_plan = payload.get("execution_plan") or {}
    orchestration_context = payload.get("orchestration_context") or {}

    return {
        "present": bool(execution_plan),
        "plan_id": execution_plan.get("plan_id"),
        "plan_version": execution_plan.get("plan_version"),
        "plan_status_seen": execution_plan.get("plan_status"),
        "current_stage_seen": orchestration_context.get("current_stage"),
        "service_stage_seen": EXPECTED_STAGE,
    }


def _validate_execution_plan(payload: Any) -> Dict[str, Any]:
    errors: List[str] = []

    if not isinstance(payload, dict):
        return {"status": "fail", "errors": ["payload_not_dict"]}

    execution_plan = payload.get("execution_plan")
    if execution_plan is None:
        return {"status": "fail", "errors": ["execution_plan_missing"]}
    if not isinstance(execution_plan, dict):
        return {"status": "fail", "errors": ["execution_plan_not_dict"]}

    if not execution_plan.get("plan_id"):
        errors.append("execution_plan_id_missing")

    plan_version = execution_plan.get("plan_version")
    if not plan_version:
        errors.append("execution_plan_version_missing")
    elif plan_version not in SUPPORTED_PLAN_VERSIONS:
        errors.append("execution_plan_version_unsupported")

    if not execution_plan.get("plan_status"):
        errors.append("execution_plan_status_missing")

    orchestration_context = payload.get("orchestration_context")
    if orchestration_context is None:
        return {"status": "fail", "errors": errors + ["orchestration_context_missing"]}
    if not isinstance(orchestration_context, dict):
        return {"status": "fail", "errors": errors + ["orchestration_context_not_dict"]}

    current_stage = orchestration_context.get("current_stage")
    if not current_stage:
        errors.append("orchestration_stage_missing")
    elif current_stage != EXPECTED_STAGE:
        errors.append("orchestration_stage_invalid")

    return {"status": "pass" if not errors else "fail", "errors": errors}


def _rejection_response(payload: Dict[str, Any], ack: Dict[str, Any], validation: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "service": "aggregation",
        "status": "rejected",
        "execution_plan_ack": ack,
        "execution_plan_validation": validation,
        "received_payload": payload,
        "result": {
            "summary": "Aggregation rejected payload due to execution plan validation failure.",
        },
        "execution_plan": dict(payload.get("execution_plan", {})) if isinstance(payload, dict) else {},
        "orchestration_context": dict(payload.get("orchestration_context", {})) if isinstance(payload, dict) else {},
    }


def _build_aggregated_result(payload: Dict[str, Any]) -> Dict[str, Any]:
    result = {
        "document_id": payload.get("document_id"),
        "source_bucket": payload.get("bucket"),
        "source_key": payload.get("key"),
        "ocr_result": payload.get("ocr_result"),
        "table_extraction_result": payload.get("table_extraction_result"),
        "logo_recognition_result": payload.get("logo_recognition_result"),
        "fraud_detection_result": payload.get("fraud_detection_result"),
        "execution_plan": payload.get("execution_plan", {}),
    }

    present_sections = [
        name for name in [
            "ocr_result",
            "table_extraction_result",
            "logo_recognition_result",
            "fraud_detection_result",
        ]
        if payload.get(name) is not None
    ]

    result["aggregation_summary"] = {
        "present_sections": present_sections,
        "present_section_count": len(present_sections),
    }
    return result


def _persist_result(result: Dict[str, Any], output_bucket: str, output_key: str) -> Dict[str, Any]:
    s3.put_object(
        Bucket=output_bucket,
        Key=output_key,
        Body=json.dumps(result, indent=2).encode("utf-8"),
        ContentType="application/json",
    )
    return {
        "output_bucket": output_bucket,
        "output_key": output_key,
    }


def main(payload: Dict[str, Any]) -> Dict[str, Any]:
    ack = _build_execution_plan_ack(payload if isinstance(payload, dict) else {})
    validation = _validate_execution_plan(payload)

    if validation["status"] != "pass":
        return _rejection_response(payload if isinstance(payload, dict) else {}, ack, validation)

    output_bucket = payload.get("output_bucket") or OUTPUT_BUCKET or payload.get("bucket")
    output_key = payload.get("output_key")
    if not output_bucket or not output_key:
        return {
            "service": "aggregation",
            "status": "failed",
            "execution_plan_ack": ack,
            "execution_plan_validation": validation,
            "error": "Missing output_bucket/output_key and no fallback bucket available",
            "execution_plan": dict(payload.get("execution_plan", {})),
            "orchestration_context": dict(payload.get("orchestration_context", {})),
        }

    aggregated_result = _build_aggregated_result(payload)
    persistence_result = _persist_result(aggregated_result, output_bucket, output_key)

    response = dict(payload)
    response.update({
        "service": "aggregation",
        "status": "executed",
        "execution_plan_ack": ack,
        "execution_plan_validation": validation,
        "aggregation_result": {
            "persistence": persistence_result,
            "summary": aggregated_result.get("aggregation_summary", {}),
        },
    })
    return response


if __name__ == "__main__":
    raw_payload = os.environ.get("PAYLOAD", "")
    if raw_payload:
        print(json.dumps(main(json.loads(raw_payload)), indent=2))
    else:
        sample_payload = {
            "bucket": "ocr-rebuild-program",
            "key": "raw/sample.png",
            "output_bucket": "ocr-rebuild-program",
            "output_key": "aggregation/sample.json",
            "document_id": "doc_local_agg_001",
            "ocr_result": {"text_length": 123},
            "execution_plan": {
                "plan_id": "plan_local_agg_001",
                "plan_version": "execution_plan_v1",
                "plan_status": "running",
            },
            "orchestration_context": {
                "current_stage": "aggregation",
            },
        }
        print(json.dumps(main(sample_payload), indent=2))
