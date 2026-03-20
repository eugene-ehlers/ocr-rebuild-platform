import logging
import os
import sys
import uuid
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


def build_source_uri(event: Dict[str, Any]) -> str:
    source_uri = event.get("source_uri")
    if source_uri:
        return source_uri

    source_bucket = event.get("source_bucket", "")
    source_key = event.get("source_key", "")
    if source_bucket and source_key:
        return f"s3://{source_bucket}/{source_key}"

    return "UNKNOWN"


def build_manifest_id(event: Dict[str, Any]) -> str:
    manifest_id = event.get("manifest_id")
    if manifest_id:
        return manifest_id
    return f"manifest-{uuid.uuid4().hex}"


def build_document_id(event: Dict[str, Any]) -> str:
    document_id = event.get("document_id")
    if document_id:
        return document_id
    return f"doc-{uuid.uuid4().hex}"


def build_document_entries(
    event: Dict[str, Any],
    document_id: str,
    source_uri: str
) -> List[Dict[str, Any]]:
    documents = event.get("documents", [])
    if isinstance(documents, list) and documents:
        entries = []
        for doc in documents:
            if isinstance(doc, dict):
                entries.append({
                    "document_id": doc.get("document_id", document_id),
                    "source_uri": doc.get("source_uri", source_uri),
                    "expected_document_type": doc.get(
                        "expected_document_type",
                        event.get("expected_document_type", "UNKNOWN")
                    )
                })
        if entries:
            return entries

    return [
        {
            "document_id": document_id,
            "source_uri": source_uri,
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


def build_manifest(
    event: Dict[str, Any],
    requested_services: Dict[str, bool],
    service_status: Dict[str, str],
    manifest_id: str,
    document_id: str,
    source_uri: str
) -> Dict[str, Any]:
    now = utc_now_iso()
    return {
        "manifest_id": manifest_id,
        "creation_timestamp": event.get("creation_timestamp", now),
        "source_batch_uri": event.get("source_batch_uri", source_uri),
        "documents": build_document_entries(event, document_id, source_uri),
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
                "engine_version": "contract_v2",
                "notes": "Manifest scaffold generated and normalized into pipeline execution contract."
            }
        ]
    }


def build_execution_plan(event: Dict[str, Any], requested_services: Dict[str, bool], manifest_id: str) -> Dict[str, Any]:
    return {
        "plan_id": manifest_id,
        "manifest_id": manifest_id,
        "service_id": "OCR_BASELINE",
        "service_name": "OCR Baseline",
        "required_capabilities": ["TEXT_OCR"],
        "optional_capabilities": [],
        "minimum_output_requirements": {"text_required": True},
        "capability_plan": {
            "TEXT_OCR": {
                "provider": "tesseract",
                "fallback_provider": "aws_textract_detect_document_text"
            }
        },
        "plan_status": "planned"
    }


def build_execution_payload(
    event: Dict[str, Any],
    manifest: Dict[str, Any],
    requested_services: Dict[str, bool],
    service_status: Dict[str, str],
    manifest_id: str,
    document_id: str,
    source_uri: str,
) -> Dict[str, Any]:
    execution_plan = build_execution_plan(event, requested_services, manifest_id)

    return {
        "manifest_id": manifest_id,
        "document_id": document_id,
        "source_uri": source_uri,
        "source_bucket": event.get("source_bucket", "UNKNOWN"),
        "source_batch_uri": source_uri,
        "document_type": event.get("document_type", "UNKNOWN"),
        "expected_document_type": event.get("expected_document_type", "UNKNOWN"),
        "ingestion_timestamp": event.get("ingestion_timestamp", utc_now_iso()),
        "creation_timestamp": manifest.get("creation_timestamp", utc_now_iso()),
        "processing_parameters": {},
        "requested_services": requested_services,
        "service_status": service_status,
        "execution_state": {
            "current_stage": "manifest_generation",
            "completed_stages": ["manifest_generation"],
            "failed_stages": [],
            "skipped_stages": []
        },
        "documents": manifest.get("documents", []),
        "pages": [],
        "execution_plan": execution_plan,
        "routing_decision": {},
        "evaluation": {},
        "manifest_update": manifest
    }


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    logger.info("Manifest generation invoked.")
    safe_event = event or {}

    manifest_id = build_manifest_id(safe_event)
    document_id = build_document_id(safe_event)
    source_uri = build_source_uri(safe_event)

    requested_services = build_requested_services(safe_event)
    service_status = build_service_status(requested_services)

    manifest = build_manifest(
        safe_event,
        requested_services,
        service_status,
        manifest_id,
        document_id,
        source_uri
    )

    save_manifest(manifest)

    return build_execution_payload(
        safe_event,
        manifest,
        requested_services,
        service_status,
        manifest_id,
        document_id,
        source_uri
    )
