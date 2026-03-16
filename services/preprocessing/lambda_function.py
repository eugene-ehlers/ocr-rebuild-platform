import boto3
import os
from datetime import datetime, timezone

s3 = boto3.client("s3")

PROCESSED_BUCKET = os.environ.get("PROCESSED_BUCKET", "UNKNOWN")


def utc_now_iso():
    return datetime.now(timezone.utc).isoformat()


def lambda_handler(event, context):
    pages = event.get("pages", [])
    processed_pages = []

    for index, page in enumerate(pages, start=1):
        key = page["s3_key"]
        processed_key = key.replace("uploads/", "processed/")

        s3.copy_object(
            Bucket=PROCESSED_BUCKET,
            CopySource={
                "Bucket": event["source_bucket"],
                "Key": key
            },
            Key=processed_key
        )

        processed_pages.append({
            "page_number": page.get("page_number", index),
            "processed_key": processed_key,
            "rotation_angle": 0,
            "orientation": "UNKNOWN",
            "preprocessing_params": {
                "status": "placeholder_complete"
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
                    "status": "completed_placeholder",
                    "timestamp": utc_now_iso(),
                    "engine_name": "preprocessing_lambda",
                    "engine_version": "skeleton_v1",
                    "notes": "S3 copy and preprocessing placeholder metadata generated."
                }
            ]
        }
    }
