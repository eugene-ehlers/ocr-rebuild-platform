import json
import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, List

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
        "document_type": "UNKNOWN",
        "ingestion_timestamp": utc_now_iso(),
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
            "Loading aggregation input payload from s3://%s/%s",
            INPUT_S3_BUCKET,
            INPUT_S3_KEY
        )
        response = s3.get_object(Bucket=INPUT_S3_BUCKET, Key=INPUT_S3_KEY)
        return json.loads(response["Body"].read().decode("utf-8"))

    if not payload_path or not os.path.exists(payload_path):
        logger.info("No payload supplied. Using placeholder aggregation input.")
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
            "Writing aggregation output payload to s3://%s/%s",
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


def build_pages(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Preserve enriched page structures coming from upstream pipeline stages.
    """
    pages = payload.get("pages", [])
    if not isinstance(pages, list):
        return []

    output_pages: List[Dict[str, Any]] = []

    for index, page in enumerate(pages, start=1):
        if isinstance(page, dict):
            enriched_page = dict(page)
            enriched_page["page_number"] = page.get("page_number", index)
            output_pages.append(enriched_page)
        else:
            output_pages.append({
                "page_number": index,
                "extracted_text": "UNKNOWN",
                "metadata": {
                    "aggregation_note": "Non-dict page payload replaced with controlled placeholder."
                }
            })

    return output_pages


def summarize_pages(pages: List[Dict[str, Any]]) -> Dict[str, Any]:
    table_count = 0
    logo_count = 0
    fraud_flag_count = 0
    non_empty_pages = 0
    total_extracted_characters = 0

    for page in pages:
        if not isinstance(page, dict):
            continue

        extracted_text = page.get("extracted_text", "") or ""
        if extracted_text.strip():
            non_empty_pages += 1
            total_extracted_characters += len(extracted_text)

        table_count += len(page.get("tables", []) or [])

        metadata = page.get("metadata", {})
        if isinstance(metadata, dict):
            logo_count += len(metadata.get("logos", []) or [])
            fraud_flag_count += len(metadata.get("fraud_flags", []) or [])

    return {
        "page_count": len(pages),
        "non_empty_pages": non_empty_pages,
        "total_extracted_characters": total_extracted_characters,
        "tables_detected": table_count,
        "logos_detected": logo_count,
        "fraud_flags_detected": fraud_flag_count
    }


def build_canonical_document(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build canonical document aligned to docs/03_data_model/canonical_document_schema.json
    and the hardened page-level contract.
    """
    canonical_pages = build_pages(payload)
    summary = summarize_pages(canonical_pages)

    return {
        "document_id": payload.get("document_id", "UNKNOWN"),
        "source_uri": payload.get("source_uri", "UNKNOWN"),
        "document_type": payload.get("document_type", "UNKNOWN"),
        "ingestion_timestamp": payload.get("ingestion_timestamp", utc_now_iso()),
        "pages": canonical_pages,
        "metadata": {
            "aggregation_status": "completed_real_increment",
            "aggregation_note": "Canonical document assembled from unified page payload with document-level summary metadata.",
            "requested_services": payload.get("requested_services", {}),
            "service_status": payload.get("service_status", {}),
            **summary
        }
    }


def build_manifest_update(payload: Dict[str, Any], canonical_document: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build manifest update aligned to docs/03_data_model/document_manifest_schema.json.
    """
    now = utc_now_iso()
    manifest_update = dict(payload.get("manifest_update", {}))
    pipeline_history = list(manifest_update.get("pipeline_history", []))
    service_status = dict(payload.get("service_status", manifest_update.get("service_status", {})))

    pipeline_history.append({
        "stage": "aggregation",
        "status": "completed_real_increment",
        "timestamp": now,
        "engine_name": "aggregation_worker",
        "engine_version": "v0.3",
        "notes": "Canonical document and manifest update assembled with document-level summary metadata."
    })

    manifest_update.update({
        "manifest_id": payload.get("manifest_id", manifest_update.get("manifest_id", "UNKNOWN")),
        "documents": [
            {
                "document_id": canonical_document.get("document_id", "UNKNOWN"),
                "source_uri": canonical_document.get("source_uri", "UNKNOWN"),
                "expected_document_type": canonical_document.get("document_type", "UNKNOWN")
            }
        ],
        "processing_parameters": {
            **dict(payload.get("processing_parameters", {})),
            "aggregation_status": "completed_real_increment"
        },
        "pipeline_status": "completed",
        "retry_count": payload.get("retry_count", manifest_update.get("retry_count", 0)),
        "last_updated": now,
        "partial_execution_flags": manifest_update.get("partial_execution_flags", {}),
        "service_status": service_status,
        "client_notification": manifest_update.get("client_notification", {
            "required": False,
            "status": "not_required",
            "message": ""
        }),
        "pipeline_history": pipeline_history
    })

    return manifest_update


def build_execution_state(payload: Dict[str, Any]) -> Dict[str, Any]:
    execution_state = dict(payload.get("execution_state", {}))
    completed_stages = list(execution_state.get("completed_stages", []))

    if "aggregation" not in completed_stages:
        completed_stages.append("aggregation")

    return {
        "current_stage": "aggregation",
        "completed_stages": completed_stages,
        "failed_stages": list(execution_state.get("failed_stages", [])),
        "skipped_stages": list(execution_state.get("skipped_stages", []))
    }


def build_output(payload: Dict[str, Any]) -> Dict[str, Any]:
    canonical_document = build_canonical_document(payload)
    manifest_update = build_manifest_update(payload, canonical_document)
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
        "pages": payload.get("pages", []),
        "metadata": {
            "stage": "aggregation",
            "partial_execution": False,
            "notes": "Aggregation output mapped to hardened canonical and manifest schemas with summary metadata."
        },
        "canonical_document": canonical_document,
        "manifest_update": manifest_update
    }


def main() -> None:
    payload_path = os.environ.get("AGGREGATION_INPUT", "")
    output_path = os.environ.get("AGGREGATION_OUTPUT", "/tmp/aggregation_output.json")

    payload = load_input(payload_path)
    result = build_output(payload)
    write_output(result, output_path)

    if OUTPUT_S3_BUCKET and OUTPUT_S3_KEY:
        logger.info(
            "Aggregation worker completed. Output written to s3://%s/%s",
            OUTPUT_S3_BUCKET,
            OUTPUT_S3_KEY
        )
    else:
        logger.info("Aggregation worker completed. Output written to %s", output_path)


if __name__ == "__main__":
    main()
