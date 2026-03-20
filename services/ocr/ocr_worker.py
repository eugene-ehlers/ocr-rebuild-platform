from __future__ import annotations

import json
import os
from typing import Any, Dict, List

import boto3
import pytesseract
from PIL import Image

s3 = boto3.client("s3")

INPUT_BUCKET = os.environ.get("INPUT_BUCKET", "")
OUTPUT_BUCKET = os.environ.get("OUTPUT_BUCKET", "")

EXPECTED_STAGE = "ocr"
SUPPORTED_PLAN_VERSIONS = {"execution_plan_v1"}
OCR_CAPABILITY_REF = "TEXT_OCR"


def _build_execution_plan_ack(payload: Dict[str, Any]) -> Dict[str, Any]:
    execution_plan = payload.get("execution_plan") or {}
    orchestration_context = payload.get("orchestration_context") or {}

    capability_plan = execution_plan.get("capability_plan") or {}
    capability_ref_seen = None
    if isinstance(capability_plan, dict) and OCR_CAPABILITY_REF in capability_plan:
        capability_ref_seen = OCR_CAPABILITY_REF

    return {
        "present": bool(execution_plan),
        "plan_id": execution_plan.get("plan_id"),
        "plan_version": execution_plan.get("plan_version"),
        "plan_status_seen": execution_plan.get("plan_status"),
        "current_stage_seen": orchestration_context.get("current_stage"),
        "service_stage_seen": EXPECTED_STAGE,
        "capability_ref_seen": capability_ref_seen,
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

    capability_plan = execution_plan.get("capability_plan")
    if capability_plan is None:
        errors.append("capability_plan_missing")
    elif not isinstance(capability_plan, dict):
        errors.append("capability_plan_missing")
    else:
        ocr_capability = capability_plan.get(OCR_CAPABILITY_REF)
        if ocr_capability is None:
            errors.append("ocr_capability_missing")
        elif not isinstance(ocr_capability, dict):
            errors.append("ocr_capability_missing")
        elif ocr_capability.get("enabled") is not True:
            errors.append("capability_not_enabled_in_execution_plan")

    return {"status": "pass" if not errors else "fail", "errors": errors}


def _rejection_response(payload: Dict[str, Any], ack: Dict[str, Any], validation: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "service": "ocr",
        "status": "rejected",
        "execution_plan_ack": ack,
        "execution_plan_validation": validation,
        "received_payload": payload,
        "result": {
            "summary": "OCR rejected payload due to execution plan validation failure.",
        },
        "execution_plan": dict(payload.get("execution_plan", {})) if isinstance(payload, dict) else {},
        "orchestration_context": dict(payload.get("orchestration_context", {})) if isinstance(payload, dict) else {},
    }


def _perform_ocr(bucket: str, key: str) -> Dict[str, Any]:
    local_input = "/tmp/ocr_input"
    s3.download_file(bucket, key, local_input)

    with Image.open(local_input) as img:
        extracted_text = pytesseract.image_to_string(img)

    output_key = f"ocr/{os.path.basename(key)}.json"
    output_body = {
        "text": extracted_text,
        "source_bucket": bucket,
        "source_key": key,
    }

    s3.put_object(
        Bucket=OUTPUT_BUCKET or bucket,
        Key=output_key,
        Body=json.dumps(output_body, indent=2).encode("utf-8"),
        ContentType="application/json",
    )

    return {
        "output_bucket": OUTPUT_BUCKET or bucket,
        "output_key": output_key,
        "text_length": len(extracted_text),
    }


def main(payload: Dict[str, Any]) -> Dict[str, Any]:
    ack = _build_execution_plan_ack(payload if isinstance(payload, dict) else {})
    validation = _validate_execution_plan(payload)

    if validation["status"] != "pass":
        return _rejection_response(payload if isinstance(payload, dict) else {}, ack, validation)

    bucket = payload.get("bucket") or INPUT_BUCKET
    key = payload.get("key")
    if not bucket or not key:
        return {
            "service": "ocr",
            "status": "failed",
            "execution_plan_ack": ack,
            "execution_plan_validation": validation,
            "error": "Missing bucket or key",
            "execution_plan": dict(payload.get("execution_plan", {})),
            "orchestration_context": dict(payload.get("orchestration_context", {})),
        }

    ocr_result = _perform_ocr(bucket, key)

    response = dict(payload)
    response.update({
        "service": "ocr",
        "status": "executed",
        "execution_plan_ack": ack,
        "execution_plan_validation": validation,
        "ocr_result": ocr_result,
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
            "execution_plan": {
                "plan_id": "plan_local_ocr_001",
                "plan_version": "execution_plan_v1",
                "plan_status": "running",
                "capability_plan": {
                    "TEXT_OCR": {
                        "enabled": True
                    }
                },
            },
            "orchestration_context": {
                "current_stage": "ocr",
            },
        }
        print(json.dumps(main(sample_payload), indent=2))
