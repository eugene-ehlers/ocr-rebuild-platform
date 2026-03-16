import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_document_entries(event: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Build minimal manifest document entries.

    Placeholder behavior:
    - accepts event["documents"] if supplied
    - falls back to a single-document entry if only document_id/source_uri are present
    """
    documents = event.get("documents", [])
    if isinstance(documents, list) and documents:
        entries = []
        for doc in documents:
            if isinstance(doc, dict):
                entries.append({
                    "document_id": doc.get("document_id", "UNKNOWN"),
                    "source_uri": doc.get("source_uri", "UNKNOWN"),
                    "expected_document_type": doc.get("expected_document_type", "UNKNOWN")
                })
        if entries:
            return entries

    return [
        {
            "document_id": event.get("document_id", "UNKNOWN"),
            "source_uri": event.get("source_uri", "UNKNOWN"),
            "expected_document_type": event.get("expected_document_type", "UNKNOWN")
        }
    ]


def build_manifest(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Controlled baseline manifest aligned to docs/03_data_model/document_manifest_schema.json.
    This is a scaffold, not final production manifest lifecycle logic.
    """
    return {
        "manifest_id": event.get("manifest_id", "UNKNOWN"),
        "creation_timestamp": event.get("creation_timestamp", utc_now_iso()),
        "source_batch_uri": event.get("source_batch_uri", event.get("source_uri", "UNKNOWN")),
        "documents": build_document_entries(event),
        "processing_parameters": event.get("processing_parameters", {}),
        "pipeline_status": "pending",
        "retry_count": 0,
        "last_updated": utc_now_iso(),
        "partial_execution_flags": {},
        "client_notification": {
            "required": False,
            "status": "not_required",
            "message": ""
        },
        "pipeline_history": [
            {
                "stage": "manifest_generation",
                "status": "completed_placeholder",
                "timestamp": utc_now_iso(),
                "engine_name": "manifest_generator",
                "engine_version": "skeleton_v1",
                "notes": "Initial controlled manifest scaffold generated."
            }
        ]
    }


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    logger.info("Manifest generation invoked.")
    manifest = build_manifest(event or {})

    return {
        "statusCode": 200,
        "manifest": manifest
    }
