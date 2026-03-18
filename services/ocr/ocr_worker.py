import json
import os
from datetime import datetime, timezone
from io import BytesIO
from typing import Any, Dict, List

import boto3
import pytesseract
from PIL import Image


s3 = boto3.client("s3")
RESULT_BUCKET = os.environ.get("RESULT_BUCKET", "UNKNOWN")
PROCESSED_BUCKET = os.environ.get("PROCESSED_BUCKET", "UNKNOWN")
OCR_INPUT = os.environ.get("OCR_INPUT", "/tmp/ocr_input.json")
OCR_OUTPUT = os.environ.get("OCR_OUTPUT", "/tmp/ocr_output.json")
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


def load_input(payload_path: str) -> Dict[str, Any]:
    if INPUT_S3_BUCKET and INPUT_S3_KEY:
        response = s3.get_object(Bucket=INPUT_S3_BUCKET, Key=INPUT_S3_KEY)
        return json.loads(response["Body"].read().decode("utf-8"))

    if not payload_path or not os.path.exists(payload_path):
        return empty_payload()

    with open(payload_path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_output(result: Dict[str, Any], output_path: str) -> None:
    if OUTPUT_S3_BUCKET and OUTPUT_S3_KEY:
        s3.put_object(
            Bucket=OUTPUT_S3_BUCKET,
            Key=OUTPUT_S3_KEY,
            Body=json.dumps(result, indent=2).encode("utf-8"),
            ContentType="application/json"
        )
        return

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)


def get_text_ocr_plan(event: Dict[str, Any]) -> Dict[str, Any]:
    execution_plan = dict(event.get("execution_plan", {}))
    capability_plan = dict(execution_plan.get("capability_plan", {}))
    text_ocr_plan = dict(capability_plan.get("TEXT_OCR", {}))

    if not text_ocr_plan:
        return {
            "provider": "tesseract",
            "provider_type": "open_source",
            "execution_mode": "primary",
            "fallback_allowed": True,
            "fallback_provider": "aws_textract_detect_document_text",
            "decision_reason": "default_text_ocr_plan_v1"
        }

    return text_ocr_plan


def run_tesseract_on_image(image_bytes: bytes) -> Dict[str, Any]:
    """
    Controlled OCR baseline using local Tesseract.
    """
    with Image.open(BytesIO(image_bytes)) as img:
        text = pytesseract.image_to_string(img).strip()

    confidence = 0.0 if not text else 0.75

    return {
        "text": text,
        "confidence": confidence
    }


def run_selected_ocr_provider(image_bytes: bytes, text_ocr_plan: Dict[str, Any]) -> Dict[str, Any]:
    provider = text_ocr_plan.get("provider", "tesseract")

    if provider == "tesseract":
        result = run_tesseract_on_image(image_bytes)
        result.update({
            "provider": "tesseract",
            "provider_type": text_ocr_plan.get("provider_type", "open_source"),
            "engine_name": "tesseract",
            "engine_version": "execution_plan_v1"
        })
        return result

    raise ValueError(
        f"OCR provider '{provider}' is not yet implemented in this worker baseline."
    )


def process_page(page: Dict[str, Any], text_ocr_plan: Dict[str, Any]) -> Dict[str, Any]:
    processed_key = page.get("processed_key", "UNKNOWN")

    source_obj = s3.get_object(
        Bucket=PROCESSED_BUCKET,
        Key=processed_key
    )
    image_bytes = source_obj["Body"].read()

    ocr_result = run_selected_ocr_provider(image_bytes, text_ocr_plan)

    page_evaluation = dict(page.get("evaluation", {}))
    page_evaluation.update({
        "ocr_completed": True,
        "ocr_provider": ocr_result["provider"],
        "ocr_quality_score": ocr_result["confidence"],
        "required_fields_present": bool(ocr_result["text"])
    })

    page_routing = dict(page.get("routing_decision", {}))
    page_routing.update({
        "selected_capability_path": "TEXT_OCR",
        "primary_provider_summary": ocr_result["provider"],
        "fallback_used": False,
        "current_route_state": "ocr_completed"
    })

    enriched_page = dict(page)
    enriched_page.update({
        "page_number": page.get("page_number", 1),
        "extracted_text": ocr_result["text"],
        "line_block_word_confidence": {
            "page_confidence": ocr_result["confidence"]
        },
        "engine_name": ocr_result["engine_name"],
        "engine_version": ocr_result["engine_version"],
        "provider": ocr_result["provider"],
        "routing_decision": page_routing,
        "evaluation": page_evaluation
    })

    metadata = dict(page.get("metadata", {})) if isinstance(page.get("metadata", {}), dict) else {}
    metadata.update({
        "stage": "ocr",
        "result_bucket": RESULT_BUCKET,
        "source_processed_key": processed_key,
        "provider_type": ocr_result["provider_type"]
    })
    enriched_page["metadata"] = metadata

    return enriched_page


def build_manifest_update(event: Dict[str, Any], text_ocr_plan: Dict[str, Any]) -> Dict[str, Any]:
    now = utc_now_iso()
    manifest_update = dict(event.get("manifest_update", {}))
    pipeline_history = list(manifest_update.get("pipeline_history", []))
    service_status = dict(event.get("service_status", manifest_update.get("service_status", {})))

    service_status["ocr"] = "completed"

    pipeline_history.append({
        "stage": "ocr",
        "status": "completed_real_increment",
        "timestamp": now,
        "engine_name": text_ocr_plan.get("provider", "tesseract"),
        "engine_version": "execution_plan_v1",
        "provider": text_ocr_plan.get("provider", "tesseract"),
        "notes": "OCR executed using execution-plan-controlled provider selection baseline."
    })

    manifest_update.update({
        "manifest_id": event.get("manifest_id", manifest_update.get("manifest_id", "UNKNOWN")),
        "pipeline_status": "processing",
        "last_updated": now,
        "partial_execution_flags": manifest_update.get("partial_execution_flags", {}),
        "service_status": service_status,
        "pipeline_history": pipeline_history
    })

    return manifest_update


def build_execution_state(event: Dict[str, Any]) -> Dict[str, Any]:
    execution_state = dict(event.get("execution_state", {}))
    completed_stages = list(execution_state.get("completed_stages", []))

    if "ocr" not in completed_stages:
        completed_stages.append("ocr")

    return {
        "current_stage": "ocr",
        "completed_stages": completed_stages,
        "failed_stages": list(execution_state.get("failed_stages", [])),
        "skipped_stages": list(execution_state.get("skipped_stages", []))
    }


def build_routing_decision(event: Dict[str, Any], text_ocr_plan: Dict[str, Any], ocr_pages: List[Dict[str, Any]]) -> Dict[str, Any]:
    routing_decision = dict(event.get("routing_decision", {}))
    routing_decision.update({
        "selected_strategy": routing_decision.get("selected_strategy", "baseline_v1"),
        "primary_provider_summary": text_ocr_plan.get("provider", "tesseract"),
        "fallback_used": False,
        "selected_capability_path": "TEXT_OCR",
        "decision_basis": text_ocr_plan.get("decision_reason", "default_text_ocr_plan_v1"),
        "current_route_state": "ocr_completed",
        "last_gate_applied": routing_decision.get("last_gate_applied", "2"),
        "ocr_pages_processed": len(ocr_pages)
    })
    return routing_decision


def build_evaluation(event: Dict[str, Any], ocr_pages: List[Dict[str, Any]]) -> Dict[str, Any]:
    evaluation = dict(event.get("evaluation", {}))
    page_confidences = [
        page.get("line_block_word_confidence", {}).get("page_confidence", 0.0)
        for page in ocr_pages
        if isinstance(page, dict)
    ]
    non_empty_pages = sum(1 for page in ocr_pages if (page.get("extracted_text", "") or "").strip())
    total_pages = len(ocr_pages)
    quality_score = sum(page_confidences) / len(page_confidences) if page_confidences else 0.0

    evaluation.update({
        "ocr_completed": True,
        "quality_score": quality_score,
        "completeness_score": (non_empty_pages / total_pages) if total_pages else 0.0,
        "required_fields_present": non_empty_pages > 0,
        "confidence_summary": {
            "page_confidences": page_confidences,
            "average_page_confidence": quality_score
        },
        "routing_acceptance_reason": evaluation.get(
            "routing_acceptance_reason",
            "ocr_completed_under_execution_plan_v1"
        )
    })
    return evaluation


def run(event: Dict[str, Any]) -> Dict[str, Any]:
    pages = event.get("pages", [])
    ocr_pages: List[Dict[str, Any]] = []
    text_ocr_plan = get_text_ocr_plan(event)

    for index, page in enumerate(pages, start=1):
        if not isinstance(page, dict):
            page = {"page_number": index}
        ocr_pages.append(process_page(page, text_ocr_plan))

    manifest_update = build_manifest_update(event, text_ocr_plan)
    execution_state = build_execution_state(event)
    routing_decision = build_routing_decision(event, text_ocr_plan, ocr_pages)
    evaluation = build_evaluation(event, ocr_pages)

    return {
        "manifest_id": event.get("manifest_id", "UNKNOWN"),
        "document_id": event.get("document_id", "UNKNOWN"),
        "source_uri": event.get("source_uri", "UNKNOWN"),
        "source_bucket": event.get("source_bucket", "UNKNOWN"),
        "source_batch_uri": event.get("source_batch_uri", event.get("source_uri", "UNKNOWN")),
        "document_type": event.get("document_type", "UNKNOWN"),
        "expected_document_type": event.get("expected_document_type", "UNKNOWN"),
        "ingestion_timestamp": event.get("ingestion_timestamp", utc_now_iso()),
        "creation_timestamp": event.get("creation_timestamp", utc_now_iso()),
        "processing_parameters": event.get("processing_parameters", {}),
        "requested_services": event.get("requested_services", {}),
        "service_status": manifest_update.get("service_status", event.get("service_status", {})),
        "execution_state": execution_state,
        "documents": event.get("documents", []),
        "pages": ocr_pages,
        "execution_plan": dict(event.get("execution_plan", {})),
        "routing_decision": routing_decision,
        "evaluation": evaluation,
        "metadata": {
            "stage": "ocr",
            "engine_name": text_ocr_plan.get("provider", "tesseract"),
            "engine_version": "execution_plan_v1",
            "partial_execution": False,
            "notes": "OCR executed using execution-plan-aware provider selection baseline."
        },
        "manifest_update": manifest_update
    }


def main() -> None:
    payload = load_input(OCR_INPUT)
    result = run(payload)
    write_output(result, OCR_OUTPUT)

    if OUTPUT_S3_BUCKET and OUTPUT_S3_KEY:
        print(json.dumps({
            "status": "OCR worker completed",
            "output_s3_bucket": OUTPUT_S3_BUCKET,
            "output_s3_key": OUTPUT_S3_KEY
        }))
    else:
        print(json.dumps({"status": "OCR worker completed", "output_path": OCR_OUTPUT}))


if __name__ == "__main__":
    main()
