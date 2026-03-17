import logging
import os
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)

from manifest_store import save_manifest


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_document_entries(event: Dict[str, Any]) -> List[Dict[str, Any]]:
    documents = event.get("documents", [])
    if isinstance(documents, list) and documents:
        entries = []
        for doc in documents:
            if isinstance(doc, dict):
                entries.append({
                    "document_id": doc.get("document_id", event.get("document_id", "UNKNOWN")),
                    "source_uri": doc.get("source_uri", event.get("source_uri", "UNKNOWN")),
                    "expected_document_type": doc.get(
                        "expected_document_type",
                        event.get("expected_document_type", "UNKNOWN")
                    )
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


def build_requested_services(event: Dict[str, Any]) -> Dict[str, bool]:
    requested = event.get("requested_services", {})
    if not isinstance(requested, dict):
        requested = {}

    return {
        "ocr": bool(requested.get("ocr", True)),
        "table_extraction": bool(requested.get("table_extraction", False)),
        "logo_recognition": bool(requested.get("logo_recognition", False)),
        "fraud_detection": bool(requested.get("fraud_detection", False))
    }


def build_service_status(requested_services: Dict[str, bool]) -> Dict[str, str]:
    return {
        "ocr": "requested" if requested_services.get("ocr", True) else "not_requested",
        "table_extraction": "requested" if requested_services.get("table_extraction", False) else "not_requested",
        "logo_recognition": "requested" if requested_services.get("logo_recognition", False) else "not_requested",
        "fraud_detection": "requested" if requested_services.get("fraud_detection", False) else "not_requested"
    }


def build_manifest(event: Dict[str, Any], requested_services: Dict[str, bool], service_status: Dict[str, str]) -> Dict[str, Any]:
    now = utc_now_iso()
    return {
        "manifest_id": event.get("manifest_id", "UNKNOWN"),
        "creation_timestamp": event.get("creation_timestamp", now),
        "source_batch_uri": event.get("source_batch_uri", event.get("source_uri", "UNKNOWN")),
        "documents": build_document_entries(event),
        "processing_parameters": event.get("processing_parameters", {}),
        "requested_services": requested_services,
        "pipeline_status": "pending",
        "retry_count": 0,
        "last_updated": now,
        "partial_execution_flags": {},
        "service_status": service_status,
        "client_notification": {
            "required": False,
            "status": "not_required",
            "message": ""
        },
        "pipeline_history": [
            {
                "stage": "manifest_generation",
                "status": "completed_realigned_contract",
                "timestamp": now,
                "engine_name": "manifest_generator",
                "engine_version": "contract_v1",
                "notes": "Manifest scaffold generated and normalized into pipeline execution contract."
            }
        ]
    }


def build_execution_payload(
    event: Dict[str, Any],
    manifest: Dict[str, Any],
    requested_services: Dict[str, bool],
    service_status: Dict[str, str],
) -> Dict[str, Any]:
    return {
        "manifest_id": manifest.get("manifest_id", "UNKNOWN"),
        "document_id": event.get("document_id", "UNKNOWN"),
        "source_uri": event.get("source_uri", "UNKNOWN"),
        "source_bucket": event.get("source_bucket", "UNKNOWN"),
        "source_batch_uri": manifest.get("source_batch_uri", event.get("source_uri", "UNKNOWN")),
        "document_type": event.get("document_type", "UNKNOWN"),
        "expected_document_type": event.get("expected_document_type", "UNKNOWN"),
        "ingestion_timestamp": event.get("ingestion_timestamp", utc_now_iso()),
        "creation_timestamp": manifest.get("creation_timestamp", utc_now_iso()),
        "processing_parameters": manifest.get("processing_parameters", {}),
        "requested_services": requested_services,
        "service_status": service_status,
        "execution_state": {
            "current_stage": "manifest_generation",
            "completed_stages": ["manifest_generation"],
            "failed_stages": [],
            "skipped_stages": []
        },
        "documents": manifest.get("documents", []),
        "pages": event.get("pages", []),
        "manifest_update": manifest,
    }


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    logger.info("Manifest generation invoked.")
    safe_event = event or {}

    requested_services = build_requested_services(safe_event)
    service_status = build_service_status(requested_services)
    manifest = build_manifest(safe_event, requested_services, service_status)
    save_manifest(manifest)

    return build_execution_payload(safe_event, manifest, requested_services, service_status)
