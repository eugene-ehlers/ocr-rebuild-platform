import json
import logging
import os
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Set

import boto3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        "service_status": {}
    }


def load_input(payload_path: str) -> Dict[str, Any]:
    """
    Load upstream payload from S3 when ECS handoff variables are present.
    Fall back to local file input for controlled local testing.
    """
    if INPUT_S3_BUCKET and INPUT_S3_KEY:
        logger.info(
            "Loading fraud detection input payload from s3://%s/%s",
            INPUT_S3_BUCKET,
            INPUT_S3_KEY
        )
        response = s3.get_object(Bucket=INPUT_S3_BUCKET, Key=INPUT_S3_KEY)
        return json.loads(response["Body"].read().decode("utf-8"))

    if not payload_path or not os.path.exists(payload_path):
        logger.info("No payload provided. Using placeholder input.")
        return empty_payload()

    with open(payload_path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_output(result: Dict[str, Any], output_path: str) -> None:
    """
    Write full enriched payload to S3 when ECS handoff variables are present.
    Fall back to local file output for controlled local testing.
    """
    if OUTPUT_S3_BUCKET and OUTPUT_S3_KEY:
        logger.info(
            "Writing fraud detection output payload to s3://%s/%s",
            OUTPUT_S3_BUCKET,
            OUTPUT_S3_KEY
        )
        s3.put_object(
            Bucket=OUTPUT_S3_BUCKET,
            Key=OUTPUT_S3_KEY,
            Body=json.dumps(result, indent=2).encode("utf-8"),
            ContentType="application/json"
        )
        return

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def run_fraud_checks_for_page(page: Dict[str, Any], seen_texts: Set[str]) -> List[Dict[str, Any]]:
    """
    First controlled real fraud detection increment using text heuristics only.
    """
    page_number = page.get("page_number", 1)
    text = page.get("extracted_text", "") or ""
    norm_text = normalize_text(text)

    flags: List[Dict[str, Any]] = []

    if not norm_text:
        flags.append({
            "flag_type": "blank_page_text",
            "severity": "medium",
            "confidence_score": 0.9,
            "description": "No OCR text detected for this page.",
            "evidence": {"page_number": page_number}
        })
    elif len(norm_text) < 10:
        flags.append({
            "flag_type": "very_low_text_volume",
            "severity": "low",
            "confidence_score": 0.7,
            "description": "Very little OCR text detected for this page.",
            "evidence": {"page_number": page_number, "text_length": len(norm_text)}
        })

    if re.search(r"(.)\1{5,}", text):
        flags.append({
            "flag_type": "repeated_character_pattern",
            "severity": "medium",
            "confidence_score": 0.75,
            "description": "Suspicious repeated character sequence detected.",
            "evidence": {"page_number": page_number}
        })

    if norm_text and norm_text in seen_texts:
        flags.append({
            "flag_type": "duplicate_page_text",
            "severity": "medium",
            "confidence_score": 0.85,
            "description": "Page text duplicates text seen on another page in the same document.",
            "evidence": {"page_number": page_number}
        })

    if norm_text:
        seen_texts.add(norm_text)

    logger.info("Fraud detection increment processed page_number=%s flags=%s", page_number, len(flags))
    return flags


def build_pages(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    pages = payload.get("pages", [])
    output_pages: List[Dict[str, Any]] = []
    seen_texts: Set[str] = set()

    for index, page in enumerate(pages, start=1):
        if not isinstance(page, dict):
            page = {"page_number": index}

        page_flags = run_fraud_checks_for_page(page, seen_texts)

        enriched_page = dict(page)
        enriched_page["page_number"] = page.get("page_number", index)

        metadata = dict(page.get("metadata", {})) if isinstance(page.get("metadata", {}), dict) else {}
        metadata.update({
            "fraud_flags": page_flags,
            "fraud_detection_stage": "completed_real_increment"
        })
        enriched_page["metadata"] = metadata

        output_pages.append(enriched_page)

    return output_pages


def build_manifest_update(payload: Dict[str, Any]) -> Dict[str, Any]:
    now = utc_now_iso()
    manifest_update = dict(payload.get("manifest_update", {}))
    pipeline_history = list(manifest_update.get("pipeline_history", []))
    service_status = dict(payload.get("service_status", manifest_update.get("service_status", {})))

    service_status["fraud_detection"] = "completed"

    pipeline_history.append({
        "stage": "fraud_detection",
        "status": "completed_real_increment",
        "timestamp": now,
        "engine_name": "fraud_detection_worker",
        "engine_version": "v0.2",
        "notes": "Text-based fraud heuristics executed."
    })

    manifest_update.update({
        "manifest_id": payload.get("manifest_id", manifest_update.get("manifest_id", "UNKNOWN")),
        "pipeline_status": "processing",
        "last_updated": now,
        "partial_execution_flags": manifest_update.get("partial_execution_flags", {}),
        "service_status": service_status,
        "pipeline_history": pipeline_history
    })

    return manifest_update


def build_execution_state(payload: Dict[str, Any]) -> Dict[str, Any]:
    execution_state = dict(payload.get("execution_state", {}))
    completed_stages = list(execution_state.get("completed_stages", []))

    if "fraud_detection" not in completed_stages:
        completed_stages.append("fraud_detection")

    return {
        "current_stage": "fraud_detection",
        "completed_stages": completed_stages,
        "failed_stages": list(execution_state.get("failed_stages", [])),
        "skipped_stages": list(execution_state.get("skipped_stages", []))
    }


def build_output(payload: Dict[str, Any]) -> Dict[str, Any]:
    output_pages = build_pages(payload)

    total_flags = sum(
        len(page.get("metadata", {}).get("fraud_flags", []))
        for page in output_pages
        if isinstance(page, dict) and isinstance(page.get("metadata", {}), dict)
    )

    manifest_update = build_manifest_update(payload)
    execution_state = build_execution_state(payload)

    return {
        "manifest_id": payload.get("manifest_id", "UNKNOWN"),
        "document_id": payload.get("document_id", "UNKNOWN"),
        "source_uri": payload.get("source_uri", "UNKNOWN"),
        "source_bucket": payload.get("source_bucket", "UNKNOWN"),
        "source_batch_uri": payload.get("source_batch_uri", payload.get("source_uri", "UNKNOWN")),
        "document_type": payload.get("document_type", "UNKNOWN"),
        "expected_document_type": payload.get("expected_document_type", "UNKNOWN"),
        "ingestion_timestamp": payload.get("ingestion_timestamp", utc_now_iso()),
        "creation_timestamp": payload.get("creation_timestamp", utc_now_iso()),
        "processing_parameters": payload.get("processing_parameters", {}),
        "requested_services": payload.get("requested_services", {}),
        "service_status": manifest_update.get("service_status", payload.get("service_status", {})),
        "execution_state": execution_state,
        "documents": payload.get("documents", []),
        "pages": output_pages,
        "metadata": {
            "stage": "fraud_detection",
            "partial_execution": False,
            "notes": "Initial real fraud detection increment using text heuristics.",
            "fraud_flags_detected": total_flags
        },
        "manifest_update": manifest_update
    }


def main():
    payload_path = os.environ.get("FRAUD_INPUT", "")
    output_path = os.environ.get("FRAUD_OUTPUT", "/tmp/fraud_output.json")

    payload = load_input(payload_path)
    result = build_output(payload)
    write_output(result, output_path)

    if OUTPUT_S3_BUCKET and OUTPUT_S3_KEY:
        logger.info(
            "Fraud detection worker completed. Output written to s3://%s/%s",
            OUTPUT_S3_BUCKET,
            OUTPUT_S3_KEY
        )
    else:
        logger.info("Fraud detection worker completed. Output written to %s", output_path)


if __name__ == "__main__":
    main()
