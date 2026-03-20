import boto3
import fitz
import io
import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple
from urllib.parse import urlparse

from PIL import Image, ImageFilter, ImageOps


s3 = boto3.client("s3")

PROCESSED_BUCKET = os.environ.get("PROCESSED_BUCKET", "UNKNOWN")
OUTPUT_S3_BUCKET = os.environ.get("OUTPUT_S3_BUCKET", "")
OUTPUT_S3_KEY = os.environ.get("OUTPUT_S3_KEY", "")

SUPPORTED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tif", ".tiff"}
SUPPORTED_PDF_EXTENSIONS = {".pdf"}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_s3_uri(uri: str) -> Tuple[str, str]:
    parsed = urlparse(uri)
    if parsed.scheme != "s3" or not parsed.netloc or not parsed.path:
        raise ValueError(f"Unsupported or invalid S3 URI: {uri}")
    return parsed.netloc, parsed.path.lstrip("/")


def get_extension_from_key(key: str) -> str:
    key_lower = key.lower()
    dot_index = key_lower.rfind(".")
    return key_lower[dot_index:] if dot_index != -1 else ""


def build_normalized_source_key(manifest_id: str, document_id: str, page_number: int) -> str:
    return f"normalized/{manifest_id}/{document_id}/pages/page_{page_number:04d}.png"


def build_processed_key(manifest_id: str, document_id: str, page_number: int) -> str:
    return f"processed/{manifest_id}/{document_id}/pages/page_{page_number:04d}.png"


def preprocess_image_bytes(image_bytes: bytes) -> tuple[bytes, Dict[str, Any]]:
    """
    First controlled real preprocessing increment:
    - load image
    - convert to grayscale
    - autocontrast
    - light median filtering
    - return processed bytes and metadata
    """
    with Image.open(io.BytesIO(image_bytes)) as img:
        original_mode = img.mode
        original_size = img.size

        processed = ImageOps.grayscale(img)
        processed = ImageOps.autocontrast(processed)
        processed = processed.filter(ImageFilter.MedianFilter(size=3))

        output = io.BytesIO()
        processed.save(output, format="PNG")
        output.seek(0)

        metadata = {
            "original_mode": original_mode,
            "original_width": original_size[0],
            "original_height": original_size[1],
            "output_format": "PNG",
            "grayscale": True,
            "autocontrast": True,
            "median_filter": 3
        }

        return output.read(), metadata


def normalize_existing_pages(event: Dict[str, Any]) -> List[Dict[str, Any]]:
    pages = event.get("pages", [])
    normalized_pages: List[Dict[str, Any]] = []

    source_bucket = event.get("source_bucket", "UNKNOWN")
    default_document_id = event.get("document_id", "UNKNOWN")

    for index, page in enumerate(pages, start=1):
        normalized_pages.append({
            "document_id": page.get("document_id", default_document_id),
            "page_number": page.get("page_number", index),
            "source_bucket": page.get("source_bucket", source_bucket),
            "source_key": page.get("source_key") or page.get("s3_key", ""),
            "page_id": page.get("page_id"),
            "rotation_angle": page.get("rotation_angle", 0),
            "orientation": page.get("orientation", "UNKNOWN"),
            "preprocessing_params": dict(page.get("preprocessing_params", {})),
            "routing_decision": dict(page.get("routing_decision", {})),
            "evaluation": dict(page.get("evaluation", {})),
            "metadata": dict(page.get("metadata", {}))
        })

    return normalized_pages


def normalize_single_image_document(
    event: Dict[str, Any],
    source_bucket: str,
    source_key: str
) -> List[Dict[str, Any]]:
    manifest_id = event.get("manifest_id", "UNKNOWN")
    document_id = event.get("document_id", "UNKNOWN")

    source_obj = s3.get_object(Bucket=source_bucket, Key=source_key)
    source_bytes = source_obj["Body"].read()

    with Image.open(io.BytesIO(source_bytes)) as img:
        output = io.BytesIO()
        img.save(output, format="PNG")
        output.seek(0)
        normalized_bytes = output.read()

    normalized_key = build_normalized_source_key(manifest_id, document_id, 1)

    s3.put_object(
        Bucket=PROCESSED_BUCKET,
        Key=normalized_key,
        Body=normalized_bytes,
        ContentType="image/png"
    )

    return [{
        "document_id": document_id,
        "page_id": f"{document_id}-page-1",
        "page_number": 1,
        "source_bucket": PROCESSED_BUCKET,
        "source_key": normalized_key,
        "rotation_angle": 0,
        "orientation": "UNKNOWN",
        "preprocessing_params": {},
        "routing_decision": {},
        "evaluation": {},
        "metadata": {
            "stage": "normalization",
            "normalization_source_type": "single_image",
            "original_source_bucket": source_bucket,
            "original_source_key": source_key
        }
    }]


def normalize_pdf_document(
    event: Dict[str, Any],
    source_bucket: str,
    source_key: str
) -> List[Dict[str, Any]]:
    manifest_id = event.get("manifest_id", "UNKNOWN")
    document_id = event.get("document_id", "UNKNOWN")

    source_obj = s3.get_object(Bucket=source_bucket, Key=source_key)
    pdf_bytes = source_obj["Body"].read()

    pdf = fitz.open(stream=pdf_bytes, filetype="pdf")
    normalized_pages: List[Dict[str, Any]] = []

    for index in range(len(pdf)):
        page_number = index + 1
        page = pdf.load_page(index)
        pix = page.get_pixmap(dpi=200, alpha=False)
        normalized_bytes = pix.tobytes("png")

        normalized_key = build_normalized_source_key(manifest_id, document_id, page_number)

        s3.put_object(
            Bucket=PROCESSED_BUCKET,
            Key=normalized_key,
            Body=normalized_bytes,
            ContentType="image/png"
        )

        normalized_pages.append({
            "document_id": document_id,
            "page_id": f"{document_id}-page-{page_number}",
            "page_number": page_number,
            "source_bucket": PROCESSED_BUCKET,
            "source_key": normalized_key,
            "rotation_angle": 0,
            "orientation": "UNKNOWN",
            "preprocessing_params": {},
            "routing_decision": {},
            "evaluation": {},
            "metadata": {
                "stage": "normalization",
                "normalization_source_type": "pdf",
                "original_source_bucket": source_bucket,
                "original_source_key": source_key
            }
        })

    pdf.close()
    return normalized_pages


def normalize_pages_from_source(event: Dict[str, Any]) -> List[Dict[str, Any]]:
    existing_pages = event.get("pages", [])
    if existing_pages:
        return normalize_existing_pages(event)

    source_uri = event.get("source_uri", "")
    if not source_uri:
        return []

    source_bucket, source_key = parse_s3_uri(source_uri)
    extension = get_extension_from_key(source_key)

    if extension in SUPPORTED_IMAGE_EXTENSIONS:
        return normalize_single_image_document(event, source_bucket, source_key)

    if extension in SUPPORTED_PDF_EXTENSIONS:
        return normalize_pdf_document(event, source_bucket, source_key)

    raise ValueError(
        f"Unsupported OCR normalization source type for preprocessing: {source_key}"
    )


def build_processed_pages(event: Dict[str, Any]) -> List[Dict[str, Any]]:
    normalized_pages = normalize_pages_from_source(event)
    processed_pages: List[Dict[str, Any]] = []
    manifest_id = event.get("manifest_id", "UNKNOWN")

    for index, page in enumerate(normalized_pages, start=1):
        source_bucket = page["source_bucket"]
        source_key = page["source_key"]
        document_id = page.get("document_id", event.get("document_id", "UNKNOWN"))
        page_number = page.get("page_number", index)

        source_obj = s3.get_object(
            Bucket=source_bucket,
            Key=source_key
        )
        source_bytes = source_obj["Body"].read()

        processed_bytes, recipe_metadata = preprocess_image_bytes(source_bytes)
        processed_key = build_processed_key(manifest_id, document_id, page_number)

        s3.put_object(
            Bucket=PROCESSED_BUCKET,
            Key=processed_key,
            Body=processed_bytes,
            ContentType="image/png"
        )

        page_evaluation = dict(page.get("evaluation", {}))
        page_evaluation.update({
            "preprocessing_completed": True,
            "preprocessing_recipe": "grayscale_autocontrast_median3"
        })

        processed_pages.append({
            "document_id": document_id,
            "page_id": page.get("page_id", f"{document_id}-page-{page_number}"),
            "page_number": page_number,
            "source_bucket": source_bucket,
            "source_key": source_key,
            "processed_bucket": PROCESSED_BUCKET,
            "processed_key": processed_key,
            "rotation_angle": page.get("rotation_angle", 0),
            "orientation": page.get("orientation", "UNKNOWN"),
            "preprocessing_params": {
                "status": "completed_real_increment",
                "recipe": "grayscale_autocontrast_median3",
                **recipe_metadata
            },
            "routing_decision": dict(page.get("routing_decision", {})),
            "evaluation": page_evaluation,
            "metadata": {
                **dict(page.get("metadata", {})),
                "stage": "preprocessing"
            }
        })

    return processed_pages


def build_manifest_update(event: Dict[str, Any], processed_pages: List[Dict[str, Any]]) -> Dict[str, Any]:
    now = utc_now_iso()
    manifest_update = dict(event.get("manifest_update", {}))
    pipeline_history = list(manifest_update.get("pipeline_history", []))

    pipeline_history.append({
        "stage": "preprocessing",
        "status": "completed_real_increment",
        "timestamp": now,
        "engine_name": "preprocessing_lambda",
        "engine_version": "v0.4",
        "notes": "Normalized OCR-eligible input into governed pages, preserved execution-plan context, and applied grayscale, autocontrast, and median filter preprocessing."
    })

    documents = []
    for doc in event.get("documents", []):
        doc_copy = dict(doc)
        doc_id = doc_copy.get("document_id", "UNKNOWN")
        doc_copy["page_count"] = sum(1 for p in processed_pages if p.get("document_id") == doc_id)
        documents.append(doc_copy)

    manifest_update.update({
        "manifest_id": event.get("manifest_id", manifest_update.get("manifest_id", "UNKNOWN")),
        "pipeline_status": "processing",
        "last_updated": now,
        "partial_execution_flags": manifest_update.get("partial_execution_flags", {}),
        "service_status": event.get("service_status", manifest_update.get("service_status", {})),
        "documents": documents if documents else manifest_update.get("documents", []),
        "pipeline_history": pipeline_history
    })

    return manifest_update


def build_execution_state(event: Dict[str, Any]) -> Dict[str, Any]:
    execution_state = dict(event.get("execution_state", {}))
    completed_stages = list(execution_state.get("completed_stages", []))

    if "preprocessing" not in completed_stages:
        completed_stages.append("preprocessing")

    return {
        "current_stage": "preprocessing",
        "completed_stages": completed_stages,
        "failed_stages": list(execution_state.get("failed_stages", [])),
        "skipped_stages": list(execution_state.get("skipped_stages", []))
    }


def build_routing_decision(event: Dict[str, Any], processed_pages: List[Dict[str, Any]]) -> Dict[str, Any]:
    routing_decision = dict(event.get("routing_decision", {}))
    routing_decision.update({
        "current_route_state": "preprocessing_completed",
        "last_gate_applied": routing_decision.get("last_gate_applied", "1"),
        "preprocessing_page_count": len(processed_pages),
        "preprocessing_source_types": sorted(list({
            p.get("metadata", {}).get("normalization_source_type", "existing_pages")
            for p in processed_pages
        }))
    })
    return routing_decision


def build_evaluation(event: Dict[str, Any], processed_pages: List[Dict[str, Any]]) -> Dict[str, Any]:
    evaluation = dict(event.get("evaluation", {}))
    evaluation.update({
        "preprocessing_completed": True,
        "preprocessing_page_count": len(processed_pages),
        "normalized_page_count": len(processed_pages),
        "routing_acceptance_reason": evaluation.get(
            "routing_acceptance_reason",
            "preprocessing_completed_v1"
        )
    })
    return evaluation


def resolve_output_s3_location(event: Dict[str, Any]) -> tuple[str, str]:
    output_bucket = event.get("output_s3_bucket", OUTPUT_S3_BUCKET)
    output_key = event.get("output_s3_key", OUTPUT_S3_KEY)
    return output_bucket, output_key


def write_output_to_s3(result: Dict[str, Any], event: Dict[str, Any]) -> None:
    output_bucket, output_key = resolve_output_s3_location(event)
    if output_bucket and output_key:
        s3.put_object(
            Bucket=output_bucket,
            Key=output_key,
            Body=json.dumps(result, indent=2).encode("utf-8"),
            ContentType="application/json"
        )


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    processed_pages = build_processed_pages(event)
    manifest_update = build_manifest_update(event, processed_pages)
    execution_state = build_execution_state(event)
    routing_decision = build_routing_decision(event, processed_pages)
    evaluation = build_evaluation(event, processed_pages)

    result = {
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
        "service_status": event.get("service_status", {}),
        "execution_state": execution_state,
        "documents": manifest_update.get("documents", event.get("documents", [])),
        "pages": processed_pages,
        "execution_plan": dict(event.get("execution_plan", {})),
        "routing_decision": routing_decision,
        "evaluation": evaluation,
        "manifest_update": manifest_update
    }

    write_output_to_s3(result, event)
    return result
