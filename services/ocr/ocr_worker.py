import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import boto3

from services.ocr.providers.base_provider import OCRProviderAdapter
from services.ocr.providers.provider_registry import (
    PROVIDER_ADAPTERS,
    SUPPORTED_PROVIDERS,
    get_runtime_enabled_providers,
    get_supported_provider_config,
)


s3 = boto3.client("s3")
RESULT_BUCKET = os.environ.get("RESULT_BUCKET", "UNKNOWN")
PROCESSED_BUCKET = os.environ.get("PROCESSED_BUCKET", "UNKNOWN")
OCR_INPUT = os.environ.get("OCR_INPUT", "/tmp/ocr_input.json")
OCR_OUTPUT = os.environ.get("OCR_OUTPUT", "/tmp/ocr_output.json")
INPUT_S3_BUCKET = os.environ.get("INPUT_S3_BUCKET", "")
INPUT_S3_KEY = os.environ.get("INPUT_S3_KEY", "")
OUTPUT_S3_BUCKET = os.environ.get("OUTPUT_S3_BUCKET", "")
OUTPUT_S3_KEY = os.environ.get("OUTPUT_S3_KEY", "")

REQUIRED_TEXT_OCR_FIELDS = [
    "provider",
    "provider_type",
    "execution_mode",
    "fallback_allowed",
    "decision_reason",
]

class OCRInstructionValidationError(ValueError):
    pass


class OCRProviderExecutionError(RuntimeError):
    pass


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
        "service_status": {},
        "execution_plan": {},
        "routing_decision": {},
        "evaluation": {},
    }


def load_input(payload_path: str) -> Dict[str, Any]:
    if INPUT_S3_BUCKET and INPUT_S3_KEY:
        response = s3.get_object(Bucket=INPUT_S3_BUCKET, Key=INPUT_S3_KEY)
        return json.loads(response["Body"].read().decode("utf-8"))

    if not payload_path or not os.path.exists(payload_path):
        return empty_payload()

    with open(payload_path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_output(result: Dict[str, Any], output_path: str) -> None:
    if OUTPUT_S3_BUCKET and OUTPUT_S3_KEY:
        s3.put_object(
            Bucket=OUTPUT_S3_BUCKET,
            Key=OUTPUT_S3_KEY,
            Body=json.dumps(result, indent=2).encode("utf-8"),
            ContentType="application/json",
        )
        return

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)


def build_controlled_error(
    code: str,
    message: str,
    details: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    return {
        "error_code": code,
        "error_message": message,
        "error_details": details or {},
    }


def get_text_ocr_plan(event: Dict[str, Any]) -> Dict[str, Any]:
    execution_plan = dict(event.get("execution_plan", {}))
    capability_plan = dict(execution_plan.get("capability_plan", {}))
    text_ocr_plan = capability_plan.get("TEXT_OCR")

    if not isinstance(text_ocr_plan, dict):
        raise OCRInstructionValidationError(
            "Missing governed TEXT_OCR instruction block in execution plan."
        )

    missing_fields = [
        field for field in REQUIRED_TEXT_OCR_FIELDS if field not in text_ocr_plan
    ]
    if missing_fields:
        raise OCRInstructionValidationError(
            f"TEXT_OCR instruction block missing required fields: {', '.join(missing_fields)}"
        )

    if not isinstance(text_ocr_plan.get("fallback_allowed"), bool):
        raise OCRInstructionValidationError(
            "TEXT_OCR field 'fallback_allowed' must be boolean."
        )

    provider = str(text_ocr_plan.get("provider", "")).strip()
    provider_type = str(text_ocr_plan.get("provider_type", "")).strip()
    execution_mode = str(text_ocr_plan.get("execution_mode", "")).strip()
    decision_reason = str(text_ocr_plan.get("decision_reason", "")).strip()

    if not provider:
        raise OCRInstructionValidationError("TEXT_OCR field 'provider' must be non-empty.")
    if not provider_type:
        raise OCRInstructionValidationError(
            "TEXT_OCR field 'provider_type' must be non-empty."
        )
    if not execution_mode:
        raise OCRInstructionValidationError(
            "TEXT_OCR field 'execution_mode' must be non-empty."
        )
    if not decision_reason:
        raise OCRInstructionValidationError(
            "TEXT_OCR field 'decision_reason' must be non-empty."
        )

    fallback_chain = text_ocr_plan.get("fallback_chain", [])
    if fallback_chain is None:
        fallback_chain = []

    if not isinstance(fallback_chain, list):
        raise OCRInstructionValidationError("TEXT_OCR field 'fallback_chain' must be a list.")

    for index, fallback_item in enumerate(fallback_chain, start=1):
        if not isinstance(fallback_item, dict):
            raise OCRInstructionValidationError(
                f"TEXT_OCR fallback_chain item {index} must be an object."
            )
        for field in ["provider", "provider_type", "execution_mode"]:
            if not str(fallback_item.get(field, "")).strip():
                raise OCRInstructionValidationError(
                    f"TEXT_OCR fallback_chain item {index} missing required field '{field}'."
                )

    if execution_mode not in {"primary", "fallback", "recovery"}:
        raise OCRInstructionValidationError(
            f"Unsupported TEXT_OCR execution_mode '{execution_mode}'."
        )

    return dict(text_ocr_plan)


def validate_provider_support(
    provider_instruction: Dict[str, Any],
    *,
    require_runtime_enabled: bool,
) -> None:
    provider = provider_instruction["provider"]
    provider_type = provider_instruction["provider_type"]
    execution_mode = provider_instruction["execution_mode"]

    supported = get_supported_provider_config(provider)

    if not supported:
        raise OCRInstructionValidationError(
            f"OCR provider '{provider}' is not supported by governed provider registry."
        )

    if provider_type != supported["provider_type"]:
        raise OCRInstructionValidationError(
            f"OCR provider '{provider}' requires provider_type '{supported['provider_type']}', got '{provider_type}'."
        )

    if execution_mode not in supported["execution_modes"]:
        raise OCRInstructionValidationError(
            f"OCR provider '{provider}' does not support execution_mode '{execution_mode}'."
        )

    if require_runtime_enabled and not bool(supported.get("runtime_enabled", False)):
        enabled = ", ".join(get_runtime_enabled_providers()) or "none"
        raise OCRInstructionValidationError(
            f"OCR provider '{provider}' is governed but not runtime-enabled in current baseline. "
            f"Runtime-enabled providers: {enabled}."
        )


def get_provider_adapter(provider_name: str) -> OCRProviderAdapter:
    adapter = PROVIDER_ADAPTERS.get(provider_name)
    if adapter is None:
        raise OCRProviderExecutionError(
            f"OCR provider '{provider_name}' reached execution unexpectedly without adapter support."
        )
    return adapter


def execute_provider(
    image_bytes: bytes,
    provider_instruction: Dict[str, Any],
) -> Dict[str, Any]:
    provider = provider_instruction["provider"]
    adapter = get_provider_adapter(provider)
    return adapter.execute(image_bytes, provider_instruction)


def attempt_provider_chain(
    image_bytes: bytes,
    text_ocr_plan: Dict[str, Any],
) -> Dict[str, Any]:
    attempted_providers: List[Dict[str, Any]] = []
    primary_instruction = {
        "provider": text_ocr_plan["provider"],
        "provider_type": text_ocr_plan["provider_type"],
        "execution_mode": text_ocr_plan["execution_mode"],
        "decision_reason": text_ocr_plan["decision_reason"],
    }

    provider_candidates = [primary_instruction]

    if text_ocr_plan.get("fallback_allowed"):
        provider_candidates.extend(list(text_ocr_plan.get("fallback_chain", [])))

    last_error: Optional[Dict[str, Any]] = None

    for index, provider_instruction in enumerate(provider_candidates):
        fallback_used = index > 0

        try:
            validate_provider_support(
                provider_instruction,
                require_runtime_enabled=True,
            )
        except Exception as exc:
            attempted_providers.append(
                {
                    "provider": provider_instruction["provider"],
                    "provider_type": provider_instruction["provider_type"],
                    "execution_mode": provider_instruction["execution_mode"],
                    "status": "not_runtime_enabled_or_invalid",
                    "error_message": str(exc),
                }
            )
            last_error = build_controlled_error(
                code="OCR_PROVIDER_VALIDATION_FAILED",
                message=str(exc),
                details={
                    "provider_instruction": provider_instruction,
                    "attempted_providers": attempted_providers,
                },
            )
            if not text_ocr_plan.get("fallback_allowed"):
                break
            continue

        try:
            result = execute_provider(image_bytes, provider_instruction)
            result["attempted_providers"] = attempted_providers + [
                {
                    "provider": provider_instruction["provider"],
                    "provider_type": provider_instruction["provider_type"],
                    "execution_mode": provider_instruction["execution_mode"],
                    "status": "completed",
                }
            ]
            result["fallback_used"] = fallback_used
            return result
        except Exception as exc:
            attempted_providers.append(
                {
                    "provider": provider_instruction["provider"],
                    "provider_type": provider_instruction["provider_type"],
                    "execution_mode": provider_instruction["execution_mode"],
                    "status": "failed",
                    "error_message": str(exc),
                }
            )
            last_error = build_controlled_error(
                code="OCR_PROVIDER_EXECUTION_FAILED",
                message=str(exc),
                details={
                    "provider_instruction": provider_instruction,
                    "attempted_providers": attempted_providers,
                },
            )
            if not text_ocr_plan.get("fallback_allowed"):
                break

    raise OCRProviderExecutionError(
        json.dumps(
            last_error
            or build_controlled_error(
                code="OCR_PROVIDER_EXECUTION_FAILED",
                message="OCR provider execution failed without structured error.",
                details={"attempted_providers": attempted_providers},
            )
        )
    )


def process_page(page: Dict[str, Any], text_ocr_plan: Dict[str, Any]) -> Dict[str, Any]:
    processed_key = page.get("processed_key", "UNKNOWN")

    source_obj = s3.get_object(
        Bucket=PROCESSED_BUCKET,
        Key=processed_key,
    )
    image_bytes = source_obj["Body"].read()

    ocr_result = attempt_provider_chain(image_bytes, text_ocr_plan)

    page_evaluation = dict(page.get("evaluation", {}))
    page_evaluation.update(
        {
            "ocr_completed": True,
            "ocr_provider": ocr_result["provider"],
            "ocr_quality_score": ocr_result["confidence"],
            "required_fields_present": bool(ocr_result["text"]),
            "ocr_execution_mode": ocr_result["provider_metadata"]["execution_mode"],
            "ocr_decision_reason": ocr_result["provider_metadata"]["decision_reason"],
            "ocr_attempted_providers": list(ocr_result.get("attempted_providers", [])),
            "ocr_fallback_used": bool(ocr_result.get("fallback_used", False)),
        }
    )

    page_routing = dict(page.get("routing_decision", {}))
    page_routing.update(
        {
            "selected_capability_path": "TEXT_OCR",
            "primary_provider_summary": text_ocr_plan["provider"],
            "selected_provider_summary": ocr_result["provider"],
            "executed_provider": ocr_result["provider"],
            "fallback_used": ocr_result["fallback_used"],
            "current_route_state": "ocr_completed",
            "decision_basis": ocr_result["provider_metadata"]["decision_reason"],
            "execution_mode": ocr_result["provider_metadata"]["execution_mode"],
        }
    )

    enriched_page = dict(page)
    enriched_page.update(
        {
            "page_number": page.get("page_number", 1),
            "extracted_text": ocr_result["text"],
            "line_block_word_confidence": {
                "page_confidence": ocr_result["confidence"]
            },
            "engine_name": ocr_result["engine_name"],
            "engine_version": ocr_result["engine_version"],
            "provider": ocr_result["provider"],
            "routing_decision": page_routing,
            "evaluation": page_evaluation,
        }
    )

    metadata = (
        dict(page.get("metadata", {}))
        if isinstance(page.get("metadata", {}), dict)
        else {}
    )
    metadata.update(
        {
            "stage": "ocr",
            "result_bucket": RESULT_BUCKET,
            "source_processed_key": processed_key,
            "provider_type": ocr_result["provider_type"],
            "execution_mode": ocr_result["provider_metadata"]["execution_mode"],
            "decision_reason": ocr_result["provider_metadata"]["decision_reason"],
            "attempted_providers": ocr_result.get("attempted_providers", []),
            "attempted_provider_chain": ocr_result.get("attempted_providers", []),
            "fallback_used": bool(ocr_result.get("fallback_used", False)),
        }
    )
    enriched_page["metadata"] = metadata

    return enriched_page


def build_manifest_update(event: Dict[str, Any], text_ocr_plan: Dict[str, Any],
    ocr_pages: List[Dict[str, Any]]) -> Dict[str, Any]:
    now = utc_now_iso()
    manifest_update = dict(event.get("manifest_update", {}))
    pipeline_history = list(manifest_update.get("pipeline_history", []))
    service_status = dict(event.get("service_status", manifest_update.get("service_status", {})))

    service_status["ocr"] = "completed"

    fallback_used = any(
        bool(page.get("metadata", {}).get("fallback_used", False))
        for page in ocr_pages
        if isinstance(page, dict)
    )

    attempted_provider_chain = []
    for page in ocr_pages:
        metadata = page.get("metadata", {})
        if not isinstance(metadata, dict):
            continue
        for attempt in metadata.get("attempted_provider_chain", []):
            if attempt not in attempted_provider_chain:
                attempted_provider_chain.append(attempt)

    pipeline_history.append(
        {
            "stage": "ocr",
            "status": "completed_with_governed_provider_instruction",
            "timestamp": now,
            "engine_name": text_ocr_plan["provider"],
            "engine_version": "provider_contract_v1",
            "provider": text_ocr_plan["provider"],
            "provider_type": text_ocr_plan["provider_type"],
            "execution_mode": text_ocr_plan["execution_mode"],
            "notes": "OCR executed with explicit execution-plan-carried provider instruction validation.",
        }
    )

    manifest_update.update(
        {
            "manifest_id": event.get("manifest_id", manifest_update.get("manifest_id", "UNKNOWN")),
            "pipeline_status": "processing",
            "last_updated": now,
            "partial_execution_flags": manifest_update.get("partial_execution_flags", {}),
            "service_status": service_status,
            "pipeline_history": pipeline_history,
        }
    )

    return manifest_update


def build_execution_state(event: Dict[str, Any]) -> Dict[str, Any]:
    execution_state = dict(event.get("execution_state", {}))
    completed_stages = list(execution_state.get("completed_stages", []))

    if "ocr" not in completed_stages:
        completed_stages.append("ocr")

    return {
        "current_stage": "ocr",
        "completed_stages": completed_stages,
        "failed_stages": list(execution_state.get("failed_stages", [])),
        "skipped_stages": list(execution_state.get("skipped_stages", [])),
    }


def build_routing_decision(
    event: Dict[str, Any],
    text_ocr_plan: Dict[str, Any],
    ocr_pages: List[Dict[str, Any]],
) -> Dict[str, Any]:
    routing_decision = dict(event.get("routing_decision", {}))
    fallback_used = any(
        page.get("routing_decision", {}).get("fallback_used", False)
        for page in ocr_pages
        if isinstance(page, dict)
    )

    attempted_provider_chain: List[Dict[str, Any]] = []
    for page in ocr_pages:
        if not isinstance(page, dict):
            continue
        metadata = page.get("metadata", {})
        if not isinstance(metadata, dict):
            continue
        for attempt in metadata.get("attempted_provider_chain", []):
            if attempt not in attempted_provider_chain:
                attempted_provider_chain.append(attempt)

    routing_decision.update(
        {
            "selected_strategy": routing_decision.get("selected_strategy", "baseline_v1"),
            "primary_provider_summary": text_ocr_plan["provider"],
            "fallback_used": fallback_used,
            "selected_capability_path": "TEXT_OCR",
            "decision_basis": text_ocr_plan["decision_reason"],
            "attempted_provider_chain": attempted_provider_chain,
            "current_route_state": "ocr_completed",
            "last_gate_applied": routing_decision.get("last_gate_applied", "2"),
            "ocr_pages_processed": len(ocr_pages),
            "ocr_execution_mode": text_ocr_plan["execution_mode"],
        }
    )
    return routing_decision


def build_evaluation(event: Dict[str, Any], ocr_pages: List[Dict[str, Any]]) -> Dict[str, Any]:
    evaluation = dict(event.get("evaluation", {}))
    page_confidences = [
        page.get("line_block_word_confidence", {}).get("page_confidence", 0.0)
        for page in ocr_pages
        if isinstance(page, dict)
    ]
    non_empty_pages = sum(
        1 for page in ocr_pages if (page.get("extracted_text", "") or "").strip()
    )
    total_pages = len(ocr_pages)
    quality_score = sum(page_confidences) / len(page_confidences) if page_confidences else 0.0

    evaluation.update(
        {
            "ocr_completed": True,
            "quality_score": quality_score,
            "completeness_score": (non_empty_pages / total_pages) if total_pages else 0.0,
            "required_fields_present": non_empty_pages > 0,
            "confidence_summary": {
                "page_confidences": page_confidences,
                "average_page_confidence": quality_score,
            },
            "routing_acceptance_reason": evaluation.get(
                "routing_acceptance_reason",
                "ocr_completed_under_governed_provider_instruction_v1",
            ),
        }
    )
    return evaluation


def build_failure_result(event: Dict[str, Any], error: Dict[str, Any]) -> Dict[str, Any]:
    execution_state = dict(event.get("execution_state", {}))
    failed_stages = list(execution_state.get("failed_stages", []))
    if "ocr" not in failed_stages:
        failed_stages.append("ocr")

    service_status = dict(event.get("service_status", {}))
    service_status["ocr"] = "failed"

    manifest_update = dict(event.get("manifest_update", {}))
    pipeline_history = list(manifest_update.get("pipeline_history", []))
    pipeline_history.append(
        {
            "stage": "ocr",
            "status": "rejected_before_provider_execution",
            "timestamp": utc_now_iso(),
            "engine_name": "ocr_worker",
            "engine_version": "provider_contract_v1",
            "notes": error["error_message"],
        }
    )
    manifest_update.update(
        {
            "manifest_id": event.get("manifest_id", manifest_update.get("manifest_id", "UNKNOWN")),
            "pipeline_status": "failed",
            "last_updated": utc_now_iso(),
            "partial_execution_flags": manifest_update.get("partial_execution_flags", {}),
            "service_status": service_status,
            "pipeline_history": pipeline_history,
        }
    )

    routing_decision = dict(event.get("routing_decision", {}))
    routing_decision.update(
        {
            "selected_capability_path": "TEXT_OCR",
            "current_route_state": "ocr_rejected",
            "decision_basis": error["error_message"],
            "fallback_used": False,
        }
    )

    evaluation = dict(event.get("evaluation", {}))
    evaluation.update(
        {
            "ocr_completed": False,
            "required_fields_present": False,
            "routing_acceptance_reason": error["error_message"],
        }
    )

    return {
        "manifest_id": event.get("manifest_id", "UNKNOWN"),
        "document_id": event.get("document_id", "UNKNOWN"),
        "source_uri": event.get("source_uri", "UNKNOWN"),
        "source_bucket": event.get("source_bucket", "UNKNOWN"),
        "source_batch_uri": event.get("source_batch_uri", event.get("source_uri", "UNKNOWN")),
        "document_type": event.get("document_type", "UNKNOWN"),
        "expected_document_type": event.get("expected_document_type", "UNKNOWN"),
        "ingestion_timestamp": event.get("ingestion_timestamp", utc_now_iso()),
        "creation_timestamp": event.get("creation_timestamp", utc_now_iso()),
        "processing_parameters": event.get("processing_parameters", {}),
        "requested_services": event.get("requested_services", {}),
        "service_status": service_status,
        "execution_state": {
            "current_stage": "ocr",
            "completed_stages": list(execution_state.get("completed_stages", [])),
            "failed_stages": failed_stages,
            "skipped_stages": list(execution_state.get("skipped_stages", [])),
        },
        "documents": event.get("documents", []),
        "pages": [],
        "execution_plan": dict(event.get("execution_plan", {})),
        "routing_decision": routing_decision,
        "evaluation": evaluation,
        "metadata": {
            "stage": "ocr",
            "engine_name": "ocr_worker",
            "engine_version": "provider_contract_v1",
            "partial_execution": False,
            "notes": "OCR execution rejected due to invalid governed provider instruction.",
        },
        "manifest_update": manifest_update,
        "error": error,
    }


def run(event: Dict[str, Any]) -> Dict[str, Any]:
    try:
        text_ocr_plan = get_text_ocr_plan(event)
        validate_provider_support(
            {
                "provider": text_ocr_plan["provider"],
                "provider_type": text_ocr_plan["provider_type"],
                "execution_mode": text_ocr_plan["execution_mode"],
                "decision_reason": text_ocr_plan["decision_reason"],
            }
        )
    except OCRInstructionValidationError as exc:
        return build_failure_result(
            event,
            build_controlled_error(
                code="OCR_INSTRUCTION_VALIDATION_FAILED",
                message=str(exc),
            ),
        )

    pages = event.get("pages", [])
    ocr_pages: List[Dict[str, Any]] = []

    for index, page in enumerate(pages, start=1):
        if not isinstance(page, dict):
            page = {"page_number": index}
        ocr_pages.append(process_page(page, text_ocr_plan))

    manifest_update = build_manifest_update(event, text_ocr_plan, ocr_pages)
    execution_state = build_execution_state(event)
    routing_decision = build_routing_decision(event, text_ocr_plan, ocr_pages)
    evaluation = build_evaluation(event, ocr_pages)

    return {
        "manifest_id": event.get("manifest_id", "UNKNOWN"),
        "document_id": event.get("document_id", "UNKNOWN"),
        "source_uri": event.get("source_uri", "UNKNOWN"),
        "source_bucket": event.get("source_bucket", "UNKNOWN"),
        "source_batch_uri": event.get("source_batch_uri", event.get("source_uri", "UNKNOWN")),
        "document_type": event.get("document_type", "UNKNOWN"),
        "expected_document_type": event.get("expected_document_type", "UNKNOWN"),
        "ingestion_timestamp": event.get("ingestion_timestamp", utc_now_iso()),
        "creation_timestamp": event.get("creation_timestamp", utc_now_iso()),
        "processing_parameters": event.get("processing_parameters", {}),
        "requested_services": event.get("requested_services", {}),
        "service_status": manifest_update.get("service_status", event.get("service_status", {})),
        "execution_state": execution_state,
        "documents": event.get("documents", []),
        "pages": ocr_pages,
        "execution_plan": dict(event.get("execution_plan", {})),
        "routing_decision": routing_decision,
        "evaluation": evaluation,
        "metadata": {
            "stage": "ocr",
            "engine_name": text_ocr_plan["provider"],
            "engine_version": "provider_contract_v1",
            "partial_execution": False,
            "notes": "OCR executed with governed provider instruction validation and normalized provider output contract.",
        },
        "manifest_update": manifest_update,
    }


def main() -> None:
    payload = load_input(OCR_INPUT)
    result = run(payload)
    write_output(result, OCR_OUTPUT)

    if OUTPUT_S3_BUCKET and OUTPUT_S3_KEY:
        print(
            json.dumps(
                {
                    "status": "OCR worker completed",
                    "output_s3_bucket": OUTPUT_S3_BUCKET,
                    "output_s3_key": OUTPUT_S3_KEY,
                }
            )
        )
    else:
        print(json.dumps({"status": "OCR worker completed", "output_path": OCR_OUTPUT}))


if __name__ == "__main__":
    main()
