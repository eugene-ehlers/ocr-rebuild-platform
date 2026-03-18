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
                "engine_version": "contract_v2",
                "notes": "Manifest scaffold generated and normalized into pipeline execution contract with execution-plan, routing, and evaluation placeholders."
            }
        ]
    }


def build_execution_plan(event: Dict[str, Any], requested_services: Dict[str, bool]) -> Dict[str, Any]:
    required_capabilities = ["TEXT_OCR"]
    optional_capabilities = []

    if requested_services.get("table_extraction", False):
        optional_capabilities.append("TABLE_STRUCTURE")
    if requested_services.get("logo_recognition", False):
        optional_capabilities.append("LOGO_RECOGNITION")
    if requested_services.get("fraud_detection", False):
        optional_capabilities.append("AUTHENTICITY_SCORING")

    return {
        "plan_id": event.get("manifest_id", "UNKNOWN"),
        "manifest_id": event.get("manifest_id", "UNKNOWN"),
        "service_id": event.get("service_id", "OCR_BASELINE"),
        "service_name": event.get("service_name", "OCR Baseline"),
        "service_objective": event.get("service_objective", "Extract document content through governed OCR pipeline."),
        "required_capabilities": required_capabilities,
        "optional_capabilities": optional_capabilities,
        "minimum_output_requirements": {
            "text_required": True
        },
        "capability_plan": {
            "TEXT_OCR": {
                "provider": "tesseract",
                "provider_type": "open_source",
                "execution_mode": "primary",
                "fallback_allowed": True,
                "fallback_provider": "aws_textract_detect_document_text",
                "decision_reason": "default_text_ocr_plan_v1"
            }
        },
        "bundled_provider_usage": {},
        "fallback_policy": {
            "page_level_reroute_allowed": True,
            "document_level_reroute_allowed": True,
            "external_escalation_allowed": True,
            "max_quality_loops": 1,
            "max_enrichment_loops": 1,
            "partial_acceptance_allowed": True
        },
        "document_overrides": [],
        "page_overrides": [],
        "relevant_gates": [0, 1, 2, 3, 4],
        "decision_gate_history": [
            {
                "gate_id": "0",
                "gate_name": "Request Interpretation and Service Assembly",
                "decision_engine_id": "0",
                "decision_state": "ACCEPT_REQUEST",
                "decision_reason": "default_service_mapping_v1",
                "plan_change_summary": "Initialized baseline execution plan at manifest generation.",
                "timestamp": utc_now_iso()
            }
        ],
        "plan_status": "planned"
    }


def build_routing_decision() -> Dict[str, Any]:
    return {
        "selected_strategy": "baseline_v1",
        "primary_provider_summary": "tesseract",
        "fallback_used": False,
        "fallback_provider": "aws_textract_detect_document_text",
        "selected_capability_path": "TEXT_OCR",
        "decision_basis": "default_text_ocr_plan_v1",
        "current_route_state": "manifest_generated",
        "last_gate_applied": "0"
    }


def build_evaluation() -> Dict[str, Any]:
    return {
        "quality_score": 0.0,
        "completeness_score": 0.0,
        "required_fields_present": False,
        "routing_acceptance_reason": "manifest_initialized_v1"
    }


def build_execution_payload(
    event: Dict[str, Any],
    manifest: Dict[str, Any],
    requested_services: Dict[str, bool],
    service_status: Dict[str, str],
) -> Dict[str, Any]:
    execution_plan = build_execution_plan(event, requested_services)

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
        "execution_plan": execution_plan,
        "routing_decision": build_routing_decision(),
        "evaluation": build_evaluation(),
        "manifest_update": manifest
    }


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    logger.info("Manifest generation invoked.")
    safe_event = event or {}

    requested_services = build_requested_services(safe_event)
    service_status = build_service_status(requested_services)
    manifest = build_manifest(safe_event, requested_services, service_status)
    save_manifest(manifest)

    return build_execution_payload(safe_event, manifest, requested_services, service_status)
