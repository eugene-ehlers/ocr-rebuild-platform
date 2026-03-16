import boto3
import os

s3 = boto3.client("s3")

PROCESSED_BUCKET = os.environ.get("PROCESSED_BUCKET")

def lambda_handler(event, context):
    pages = event.get("pages", [])
    processed_pages = []

    for page in pages:
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
            "processed_key": processed_key
        })

    return {
        "document_id": event["document_id"],
        "processed_pages": processed_pages
    }
