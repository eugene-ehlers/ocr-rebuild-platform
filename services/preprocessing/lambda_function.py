import boto3
import io
import os
from datetime import datetime, timezone
from typing import Any, Dict, List

from PIL import Image, ImageFilter, ImageOps


s3 = boto3.client("s3")

PROCESSED_BUCKET = os.environ.get("PROCESSED_BUCKET", "UNKNOWN")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


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


def build_processed_pages(event: Dict[str, Any]) -> List[Dict[str, Any]]:
    pages = event.get("pages", [])
    processed_pages: List[Dict[str, Any]] = []

    for index, page in enumerate(pages, start=1):
        key = page["s3_key"]
        processed_key = key.replace("uploads/", "processed/")

        source_obj = s3.get_object(
            Bucket=event["source_bucket"],
            Key=key
        )
        source_bytes = source_obj["Body"].read()

        processed_bytes, recipe_metadata = preprocess_image_bytes(source_bytes)

        s3.put_object(
            Bucket=PROCESSED_BUCKET,
            Key=processed_key,
            Body=processed_bytes,
            ContentType="image/png"
        )

        processed_pages.append({
            "page_number": page.get("page_number", index),
            "processed_key": processed_key,
            "rotation_angle": 0,
            "orientation": "UNKNOWN",
            "preprocessing_params": {
                "status": "completed_real_increment",
                "recipe": "grayscale_autocontrast_median3",
                **recipe_metadata
            },
            "metadata": {
                "stage": "preprocessing",
                "source_key": key,
                "processed_bucket": PROCESSED_BUCKET
            }
        })

    return processed_pages


def build_manifest_update(event: Dict[str, Any]) -> Dict[str, Any]:
    now = utc_now_iso()
    manifest_update = dict(event.get("manifest_update", {}))
    pipeline_history = list(manifest_update.get("pipeline_history", []))

    pipeline_history.append({
        "stage": "preprocessing",
        "status": "completed_real_increment",
        "timestamp": now,
        "engine_name": "preprocessing_lambda",
        "engine_version": "v0.2",
        "notes": "Applied grayscale, autocontrast, and median filter preprocessing."
    })

    manifest_update.update({
        "manifest_id": event.get("manifest_id", manifest_update.get("manifest_id", "UNKNOWN")),
        "pipeline_status": "processing",
        "last_updated": now,
        "partial_execution_flags": manifest_update.get("partial_execution_flags", {}),
        "service_status": event.get("service_status", manifest_update.get("service_status", {})),
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


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    processed_pages = build_processed_pages(event)
    manifest_update = build_manifest_update(event)
    execution_state = build_execution_state(event)

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
        "service_status": event.get("service_status", {}),
        "execution_state": execution_state,
        "documents": event.get("documents", []),
        "pages": processed_pages,
        "manifest_update": manifest_update
    }
