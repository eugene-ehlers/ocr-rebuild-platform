import json
import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


KNOWN_TEMPLATE_MARKERS = {
    "invoice": ["invoice", "tax invoice", "invoice number"],
    "bank_statement": ["bank statement", "account number", "statement period"],
    "payslip": ["payslip", "employee number", "gross pay"],
    "id_document": ["identity number", "date of birth", "nationality"]
}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_input(payload_path: str) -> Dict[str, Any]:
    if not payload_path or not os.path.exists(payload_path):
        logger.info("No payload provided. Using placeholder.")
        return {
            "document_id": "UNKNOWN",
            "manifest_id": "UNKNOWN",
            "source_uri": "UNKNOWN",
            "pages": []
        }

    with open(payload_path, "r", encoding="utf-8") as f:
        return json.load(f)


def detect_logos_for_page(page: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    First controlled real increment:
    detect simple template/logo markers from extracted page text only.
    """
    page_number = page.get("page_number", 1)
    text = (page.get("extracted_text", "") or "").lower()

    findings: List[Dict[str, Any]] = []

    for label, markers in KNOWN_TEMPLATE_MARKERS.items():
        matched = [marker for marker in markers if marker in text]
        if matched:
            findings.append({
                "logo_id": f"{label}_{page_number}",
                "label": label,
                "confidence_score": 0.6,
                "matched_markers": matched
            })

    logger.info(
        "Logo recognition increment processed page_number=%s findings=%s",
        page_number,
        len(findings)
    )

    return findings


def build_pages(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    pages = payload.get("pages", [])
    output_pages: List[Dict[str, Any]] = []

    for index, page in enumerate(pages, start=1):
        if not isinstance(page, dict):
            page = {"page_number": index}

        page_logos = detect_logos_for_page(page)

        enriched_page = dict(page)
        enriched_page["page_number"] = page.get("page_number", index)

        metadata = dict(page.get("metadata", {})) if isinstance(page.get("metadata", {}), dict) else {}
        metadata.update({
            "logos": page_logos,
            "logo_recognition_stage": "completed_real_increment"
        })
        enriched_page["metadata"] = metadata

        output_pages.append(enriched_page)

    return output_pages


def build_output(payload: Dict[str, Any]) -> Dict[str, Any]:
    output_pages = build_pages(payload)

    total_logos = sum(
        len(page.get("metadata", {}).get("logos", []))
        for page in output_pages
        if isinstance(page, dict) and isinstance(page.get("metadata", {}), dict)
    )

    return {
        "document_id": payload.get("document_id", "UNKNOWN"),
        "manifest_id": payload.get("manifest_id", "UNKNOWN"),
        "source_uri": payload.get("source_uri", "UNKNOWN"),
        "pages": output_pages,
        "metadata": {
            "stage": "logo_recognition",
            "partial_execution": False,
            "notes": "Initial real logo recognition increment using text/template heuristics.",
            "logos_detected": total_logos
        },
        "manifest_update": {
            "pipeline_status": "processing",
            "last_updated": utc_now_iso(),
            "partial_execution_flags": {},
            "pipeline_history": [
                {
                    "stage": "logo_recognition",
                    "status": "completed_real_increment",
                    "timestamp": utc_now_iso(),
                    "engine_name": "logo_recognition_worker",
                    "engine_version": "v0.2",
                    "notes": "Template marker detection from OCR text executed."
                }
            ]
        }
    }


def main():
    payload_path = os.environ.get("LOGO_INPUT", "")
    output_path = os.environ.get("LOGO_OUTPUT", "/tmp/logo_output.json")

    payload = load_input(payload_path)
    result = build_output(payload)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    logger.info("Logo recognition worker completed")


if __name__ == "__main__":
    main()
