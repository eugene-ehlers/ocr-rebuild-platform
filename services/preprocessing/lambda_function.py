from __future__ import annotations

import json
import os
from typing import Any, Dict, List

import boto3
from PIL import Image, ImageFilter, ImageOps

s3 = boto3.client("s3")

PROCESSED_BUCKET = os.environ.get("PROCESSED_BUCKET", "")
EXPECTED_STAGE = "preprocessing"
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
        "service": "preprocessing",
        "status": "rejected",
        "execution_plan_ack": ack,
        "execution_plan_validation": validation,
        "received_payload": payload,
        "result": {
            "summary": "Preprocessing rejected payload due to execution plan validation failure.",
        },
        "execution_plan": dict(payload.get("execution_plan", {})) if isinstance(payload, dict) else {},
        "orchestration_context": dict(payload.get("orchestration_context", {})) if isinstance(payload, dict) else {},
    }


def process_image(bucket: str, key: str) -> Dict[str, Any]:
    local_input = "/tmp/input_image"
    local_output = "/tmp/processed_image.png"

    s3.download_file(bucket, key, local_input)

    with Image.open(local_input) as img:
        img = img.convert("L")
        img = ImageOps.autocontrast(img)
        img = img.filter(ImageFilter.MedianFilter(size=3))
        img.save(local_output)

    output_key = f"processed/{os.path.basename(key)}.png"
    s3.upload_file(local_output, PROCESSED_BUCKET or bucket, output_key)

    return {
        "processed_bucket": PROCESSED_BUCKET or bucket,
        "processed_key": output_key,
    }


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    ack = _build_execution_plan_ack(event if isinstance(event, dict) else {})
    validation = _validate_execution_plan(event)

    if validation["status"] != "pass":
        return _rejection_response(event if isinstance(event, dict) else {}, ack, validation)

    bucket = event.get("bucket")
    key = event.get("key")
    if not bucket or not key:
        return {
            "service": "preprocessing",
            "status": "failed",
            "execution_plan_ack": ack,
            "execution_plan_validation": validation,
            "error": "Missing bucket or key",
            "execution_plan": dict(event.get("execution_plan", {})),
            "orchestration_context": dict(event.get("orchestration_context", {})),
        }

    result = process_image(bucket, key)

    response = dict(event)
    response.update({
        "service": "preprocessing",
        "status": "executed",
        "execution_plan_ack": ack,
        "execution_plan_validation": validation,
        "preprocessing_result": result,
    })
    return response


if __name__ == "__main__":
    sample_event = {
        "bucket": "ocr-rebuild-program",
        "key": "raw/sample.png",
        "execution_plan": {
            "plan_id": "plan_local_pre_001",
            "plan_version": "execution_plan_v1",
            "plan_status": "running",
        },
        "orchestration_context": {
            "current_stage": "preprocessing",
        },
    }
    print(json.dumps(lambda_handler(sample_event, None), indent=2))
