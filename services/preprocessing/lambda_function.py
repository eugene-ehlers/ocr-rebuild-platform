import boto3
import io
import os
from datetime import datetime, timezone

from PIL import Image, ImageFilter, ImageOps


s3 = boto3.client("s3")

PROCESSED_BUCKET = os.environ.get("PROCESSED_BUCKET", "UNKNOWN")


def utc_now_iso():
    return datetime.now(timezone.utc).isoformat()


def preprocess_image_bytes(image_bytes):
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


def lambda_handler(event, context):
    pages = event.get("pages", [])
    processed_pages = []

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

    return {
        "document_id": event.get("document_id", "UNKNOWN"),
        "source_uri": event.get("source_uri", "UNKNOWN"),
        "pages": processed_pages,
        "manifest_update": {
            "pipeline_status": "processing",
            "last_updated": utc_now_iso(),
            "partial_execution_flags": {},
            "pipeline_history": [
                {
                    "stage": "preprocessing",
                    "status": "completed_real_increment",
                    "timestamp": utc_now_iso(),
                    "engine_name": "preprocessing_lambda",
                    "engine_version": "v0.2",
                    "notes": "Applied grayscale, autocontrast, and median filter preprocessing."
                }
            ]
        }
    }
