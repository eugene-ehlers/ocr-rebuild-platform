import json
import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, List


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_input(payload_path: str) -> Dict[str, Any]:
    """
    Load upstream payload from file if present.

    Placeholder only:
    future production input may come from Step Functions, S3, or ECS task input.
    """
    if not payload_path or not os.path.exists(payload_path):
        logger.info("No payload supplied. Using placeholder aggregation input.")
        return {
            "document_id": "UNKNOWN",
            "manifest_id": "UNKNOWN",
            "source_uri": "UNKNOWN",
            "document_type": "UNKNOWN",
            "ingestion_timestamp": utc_now_iso(),
            "pages": []
        }

    with open(payload_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_pages(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Preserve enriched page structures coming from upstream pipeline stages.

    This controlled skeleton does not perform deep merge logic across multiple
    independent stage payloads yet. It assumes the upstream payload already
    carries the latest page-level view.
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


def build_canonical_document(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build canonical document aligned to docs/03_data_model/canonical_document_schema.json
    and the hardened page-level contract.
    """
    canonical_pages = build_pages(payload)

    return {
        "document_id": payload.get("document_id", "UNKNOWN"),
        "source_uri": payload.get("source_uri", "UNKNOWN"),
        "document_type": payload.get("document_type", "UNKNOWN"),
        "ingestion_timestamp": payload.get("ingestion_timestamp", utc_now_iso()),
        "pages": canonical_pages,
        "metadata": {
            "aggregation_status": "completed_placeholder",
            "aggregation_note": "Canonical document assembled from current unified page payload.",
            "page_count": len(canonical_pages)
        }
    }


def build_manifest_update(payload: Dict[str, Any], canonical_document: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build manifest update aligned to docs/03_data_model/document_manifest_schema.json.
    """
    return {
        "manifest_id": payload.get("manifest_id", "UNKNOWN"),
        "documents": [
            {
                "document_id": canonical_document.get("document_id", "UNKNOWN"),
                "source_uri": canonical_document.get("source_uri", "UNKNOWN"),
                "expected_document_type": canonical_document.get("document_type", "UNKNOWN")
            }
        ],
        "processing_parameters": {
            "aggregation_status": "completed_placeholder"
        },
        "pipeline_status": "completed",
        "retry_count": payload.get("retry_count", 0),
        "last_updated": utc_now_iso(),
        "partial_execution_flags": payload.get("partial_execution_flags", {}),
        "client_notification": {
            "required": False,
            "status": "not_required",
            "message": ""
        },
        "pipeline_history": [
            {
                "stage": "aggregation",
                "status": "completed_placeholder",
                "timestamp": utc_now_iso(),
                "engine_name": "aggregation_worker",
                "engine_version": "skeleton_v2",
                "notes": "Canonical document and manifest update assembled from unified page payload."
            }
        ]
    }


def build_output(payload: Dict[str, Any]) -> Dict[str, Any]:
    canonical_document = build_canonical_document(payload)
    manifest_update = build_manifest_update(payload, canonical_document)

    return {
        "metadata": {
            "stage": "aggregation",
            "partial_execution": False,
            "notes": "Placeholder aggregation output mapped to hardened canonical and manifest schemas."
        },
        "canonical_document": canonical_document,
        "manifest_update": manifest_update
    }


def main() -> None:
    payload_path = os.environ.get("AGGREGATION_INPUT", "")
    output_path = os.environ.get("AGGREGATION_OUTPUT", "/tmp/aggregation_output.json")

    payload = load_input(payload_path)
    result = build_output(payload)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    logger.info("Aggregation skeleton completed. Output written to %s", output_path)


if __name__ == "__main__":
    main()
