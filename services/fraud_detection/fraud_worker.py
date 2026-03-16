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
    Load upstream payload.

    In production this will come from Step Functions / S3 / ECS task input.
    """
    if not payload_path or not os.path.exists(payload_path):
        logger.info("No payload provided. Using placeholder input.")
        return {
            "document_id": "UNKNOWN",
            "manifest_id": "UNKNOWN",
            "source_uri": "UNKNOWN",
            "pages": []
        }

    with open(payload_path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_fraud_checks_for_page(page: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Placeholder page-level fraud detection logic.
    """
    page_number = page.get("page_number", 1)
    logger.info("Fraud detection placeholder invoked for page_number=%s", page_number)

    return []


def build_pages(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    pages = payload.get("pages", [])
    output_pages: List[Dict[str, Any]] = []

    for index, page in enumerate(pages, start=1):
        if not isinstance(page, dict):
            page = {"page_number": index}

        page_flags = run_fraud_checks_for_page(page)

        enriched_page = dict(page)
        enriched_page["page_number"] = page.get("page_number", index)

        metadata = dict(page.get("metadata", {})) if isinstance(page.get("metadata", {}), dict) else {}
        metadata.update({
            "fraud_flags": page_flags,
            "fraud_detection_stage": "completed_placeholder"
        })
        enriched_page["metadata"] = metadata

        output_pages.append(enriched_page)

    return output_pages


def build_output(payload: Dict[str, Any]) -> Dict[str, Any]:
    output_pages = build_pages(payload)

    total_flags = sum(
        len(page.get("metadata", {}).get("fraud_flags", []))
        for page in output_pages
        if isinstance(page, dict) and isinstance(page.get("metadata", {}), dict)
    )

    return {
        "document_id": payload.get("document_id", "UNKNOWN"),
        "manifest_id": payload.get("manifest_id", "UNKNOWN"),
        "source_uri": payload.get("source_uri", "UNKNOWN"),
        "pages": output_pages,
        "metadata": {
            "stage": "fraud_detection",
            "partial_execution": False,
            "notes": "Placeholder fraud detection output mapped to controlled schema.",
            "fraud_flags_detected": total_flags
        },
        "manifest_update": {
            "pipeline_status": "processing",
            "last_updated": utc_now_iso(),
            "partial_execution_flags": {},
            "pipeline_history": [
                {
                    "stage": "fraud_detection",
                    "status": "completed_placeholder",
                    "timestamp": utc_now_iso(),
                    "engine_name": "fraud_detection_worker",
                    "engine_version": "skeleton_v1",
                    "notes": "Fraud detection placeholder results generated."
                }
            ]
        }
    }


def main():
    payload_path = os.environ.get("FRAUD_INPUT", "")
    output_path = os.environ.get("FRAUD_OUTPUT", "/tmp/fraud_output.json")

    payload = load_input(payload_path)
    result = build_output(payload)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    logger.info("Fraud detection skeleton completed")


if __name__ == "__main__":
    main()
