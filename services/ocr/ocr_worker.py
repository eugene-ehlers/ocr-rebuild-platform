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


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_input(payload_path: str) -> Dict[str, Any]:
    if not payload_path or not os.path.exists(payload_path):
        return {
            "manifest_id": "UNKNOWN",
            "document_id": "UNKNOWN",
            "source_uri": "UNKNOWN",
            "pages": [],
            "manifest_update": {},
            "execution_state": {},
            "requested_services": {},
            "service_status": {}
        }

    with open(payload_path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_tesseract_on_image(image_bytes: bytes) -> Dict[str, Any]:
    """
    First controlled real OCR increment using local Tesseract.
    """
    with Image.open(BytesIO(image_bytes)) as img:
        text = pytesseract.image_to_string(img).strip()

    confidence = 0.0 if not text else 0.75

    return {
        "text": text,
        "confidence": confidence
    }


def process_page(page: Dict[str, Any]) -> Dict[str, Any]:
    processed_key = page.get("processed_key", "UNKNOWN")

    source_obj = s3.get_object(
        Bucket=PROCESSED_BUCKET,
        Key=processed_key
    )
    image_bytes = source_obj["Body"].read()

    ocr_result = run_tesseract_on_image(image_bytes)

    enriched_page = dict(page)
    enriched_page.update({
        "page_number": page.get("page_number", 1),
        "extracted_text": ocr_result["text"],
        "line_block_word_confidence": {
            "page_confidence": ocr_result["confidence"]
        },
        "engine_name": "tesseract",
        "engine_version": "initial_increment"
    })

    metadata = dict(page.get("metadata", {})) if isinstance(page.get("metadata", {}), dict) else {}
    metadata.update({
        "stage": "ocr",
        "result_bucket": RESULT_BUCKET,
        "source_processed_key": processed_key
    })
    enriched_page["metadata"] = metadata

    return enriched_page


def build_manifest_update(event: Dict[str, Any]) -> Dict[str, Any]:
    now = utc_now_iso()
    manifest_update = dict(event.get("manifest_update", {}))
    pipeline_history = list(manifest_update.get("pipeline_history", []))
    service_status = dict(event.get("service_status", manifest_update.get("service_status", {})))

    service_status["ocr"] = "completed"

    pipeline_history.append({
        "stage": "ocr",
        "status": "completed_real_increment",
        "timestamp": now,
        "engine_name": "tesseract",
        "engine_version": "initial_increment",
        "notes": "Real OCR text extraction executed with Tesseract."
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


def run(event: Dict[str, Any]) -> Dict[str, Any]:
    pages = event.get("pages", [])
    ocr_pages: List[Dict[str, Any]] = []

    for index, page in enumerate(pages, start=1):
        if not isinstance(page, dict):
            page = {"page_number": index}
        ocr_pages.append(process_page(page))

    manifest_update = build_manifest_update(event)
    execution_state = build_execution_state(event)

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
        "metadata": {
            "stage": "ocr",
            "engine_name": "tesseract",
            "engine_version": "initial_increment",
            "partial_execution": False,
            "notes": "Initial real OCR increment using local Tesseract."
        },
        "manifest_update": manifest_update
    }


def main() -> None:
    payload = load_input(OCR_INPUT)
    result = run(payload)

    with open(OCR_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(json.dumps({"status": "OCR worker completed", "output_path": OCR_OUTPUT}))


if __name__ == "__main__":
    main()
