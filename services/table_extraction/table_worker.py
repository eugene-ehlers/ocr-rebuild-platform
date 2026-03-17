import json
import logging
import os
import re
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
            "Loading table extraction input payload from s3://%s/%s",
            INPUT_S3_BUCKET,
            INPUT_S3_KEY
        )
        response = s3.get_object(Bucket=INPUT_S3_BUCKET, Key=INPUT_S3_KEY)
        return json.loads(response["Body"].read().decode("utf-8"))

    if not payload_path or not os.path.exists(payload_path):
        logger.info("No payload file supplied. Using placeholder input.")
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
            "Writing table extraction output payload to s3://%s/%s",
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


def split_table_line(line: str) -> List[str]:
    """
    First controlled real increment:
    split likely table rows on pipes, tabs, or repeated spaces.
    """
    if "|" in line:
        parts = [p.strip() for p in line.split("|")]
    elif "\t" in line:
        parts = [p.strip() for p in line.split("\t")]
    else:
        parts = [p.strip() for p in re.split(r"\s{2,}", line)]

    return [p for p in parts if p]


def extract_tables_for_page(page: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    First controlled real table extraction increment using text heuristics only.
    Detects simple table-like consecutive lines with multiple columns.
    """
    page_number = page.get("page_number", 1)
    text = page.get("extracted_text", "") or ""
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    candidate_rows: List[List[str]] = []
    for line in lines:
        columns = split_table_line(line)
        if len(columns) >= 2:
            candidate_rows.append(columns)

    if len(candidate_rows) < 2:
        logger.info("No table-like text detected for page_number=%s", page_number)
        return []

    max_cols = max(len(row) for row in candidate_rows)
    table_rows = []

    for row_index, row in enumerate(candidate_rows):
        cells = []
        for col_index in range(max_cols):
            column_name = f"column_{col_index + 1}"
            cell_text = row[col_index] if col_index < len(row) else ""
            cells.append({
                "column_name": column_name,
                "cell_text": cell_text,
                "confidence_score": None
            })

        table_rows.append({
            "row_index": row_index,
            "cells": cells
        })

    logger.info("Detected heuristic table for page_number=%s with %s rows", page_number, len(table_rows))

    return [
        {
            "table_id": f"page_{page_number}_table_1",
            "table_name": "heuristic_text_table",
            "page_number": page_number,
            "rows": table_rows
        }
    ]


def build_pages(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    pages = payload.get("pages", [])
    output_pages: List[Dict[str, Any]] = []

    for index, page in enumerate(pages, start=1):
        if not isinstance(page, dict):
            page = {"page_number": index}

        page_tables = extract_tables_for_page(page)

        enriched_page = dict(page)
        enriched_page["page_number"] = page.get("page_number", index)
        enriched_page["tables"] = page_tables

        metadata = dict(page.get("metadata", {})) if isinstance(page.get("metadata", {}), dict) else {}
        metadata.update({
            "table_extraction_stage": "completed_real_increment"
        })
        enriched_page["metadata"] = metadata

        output_pages.append(enriched_page)

    return output_pages


def build_manifest_update(payload: Dict[str, Any]) -> Dict[str, Any]:
    now = utc_now_iso()
    manifest_update = dict(payload.get("manifest_update", {}))
    pipeline_history = list(manifest_update.get("pipeline_history", []))
    service_status = dict(payload.get("service_status", manifest_update.get("service_status", {})))

    service_status["table_extraction"] = "completed"

    pipeline_history.append({
        "stage": "table_extraction",
        "status": "completed_real_increment",
        "timestamp": now,
        "engine_name": "table_extraction_worker",
        "engine_version": "v0.2",
        "notes": "Heuristic table extraction from OCR text executed."
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

    if "table_extraction" not in completed_stages:
        completed_stages.append("table_extraction")

    return {
        "current_stage": "table_extraction",
        "completed_stages": completed_stages,
        "failed_stages": list(execution_state.get("failed_stages", [])),
        "skipped_stages": list(execution_state.get("skipped_stages", []))
    }


def build_output(payload: Dict[str, Any]) -> Dict[str, Any]:
    output_pages = build_pages(payload)
    total_tables = sum(len(page.get("tables", [])) for page in output_pages if isinstance(page, dict))
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
            "stage": "table_extraction",
            "partial_execution": False,
            "notes": "Initial real table extraction increment using text heuristics.",
            "tables_detected": total_tables
        },
        "manifest_update": manifest_update
    }


def main() -> None:
    payload_path = os.environ.get("TABLE_EXTRACTION_INPUT", "")
    output_path = os.environ.get("TABLE_EXTRACTION_OUTPUT", "/tmp/table_extraction_output.json")

    payload = load_input(payload_path)
    result = build_output(payload)
    write_output(result, output_path)

    if OUTPUT_S3_BUCKET and OUTPUT_S3_KEY:
        logger.info(
            "Table extraction worker completed. Output written to s3://%s/%s",
            OUTPUT_S3_BUCKET,
            OUTPUT_S3_KEY
        )
    else:
        logger.info("Table extraction worker completed. Output written to %s", output_path)


if __name__ == "__main__":
    main()
