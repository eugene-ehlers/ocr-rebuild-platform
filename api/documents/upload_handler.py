"""Client-scoped, consent-gated upload path for I-DIP.

Writes first to the OCR internal audit store under mandatory linkage metadata,
then returns only a client-safe payload that I-DIP may place in its vault.

No direct access to the internal store is ever granted to I-DIP or the client.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List
import json
import os
import uuid

import boto3
from botocore.exceptions import ClientError


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_document_id() -> str:
    return f"doc_{uuid.uuid4().hex[:12]}"


def _new_request_id() -> str:
    return f"req_{uuid.uuid4().hex[:12]}"


def _s3_client():
    return boto3.client("s3", region_name=os.environ.get("AWS_REGION", "us-east-1"))


def _internal_bucket() -> str:
    bucket = os.environ.get("OCR_INTERNAL_BUCKET", "").strip()
    if not bucket:
        raise RuntimeError("OCR_INTERNAL_BUCKET environment variable is required")
    return bucket


def upload_from_idip(
    *,
    client_id: str,
    source_app: str,
    file_bytes: bytes,
    filename: str,
    content_type: str,
    processing_consent_valid: bool,
    consent_record_ids: List[str],
    disclosure_consent_status: str = "not_required",
) -> Dict[str, Any]:
    """Accept an authenticated I-DIP upload.

    Preconditions (enforced by caller):
    - session belongs to client_id
    - processing_consent_valid is True
    - source_app is "idip" or "passport"

    Returns a client-safe payload only.
    """
    if source_app not in ("idip", "passport"):
        raise ValueError("source_app must be idip or passport")
    if not client_id:
        raise ValueError("client_id is required")
    if not processing_consent_valid:
        raise ValueError("valid processing consent is required")
    if not consent_record_ids:
        raise ValueError("consent_record_ids must be supplied")

    document_id = _new_document_id()
    request_id = _new_request_id()
    timestamp = _utc_now()

    linkage = {
        "request_id": request_id,
        "document_id": document_id,
        "client_id": client_id,
        "source_app": source_app,
        "timestamp": timestamp,
        "consent_record_ids": list(consent_record_ids),
        "processing_consent_status": "valid",
        "disclosure_consent_status": disclosure_consent_status,
    }

    _write_to_ocr_internal_store(
        linkage=linkage,
        filename=filename,
        content_type=content_type,
        file_bytes=file_bytes,
    )

    return {
        "success": True,
        "document_id": document_id,
        "request_id": request_id,
        "status": "accepted",
        "message": "Document accepted under client scope. Processing may be requested separately.",
        "client_safe": {
            "document_id": document_id,
            "request_id": request_id,
            "filename": filename,
            "uploaded_at": timestamp,
        },
    }


def _write_to_ocr_internal_store(
    *,
    linkage: Dict[str, Any],
    filename: str,
    content_type: str,
    file_bytes: bytes,
) -> None:
    """Write the original file and linkage metadata to the private OCR internal bucket.

    Key layout (client-scoped, not listable by I-DIP):
      clients/{client_id}/documents/{document_id}/original/{filename}
      clients/{client_id}/documents/{document_id}/linkage.json

    The service role that runs this code is the only principal allowed to write.
    No presigned URL is generated or returned.
    """
    bucket = _internal_bucket()
    s3 = _s3_client()

    client_id = linkage["client_id"]
    document_id = linkage["document_id"]
    safe_name = filename.replace("/", "_").replace("\\", "_") or "upload.bin"

    original_key = f"clients/{client_id}/documents/{document_id}/original/{safe_name}"
    linkage_key = f"clients/{client_id}/documents/{document_id}/linkage.json"

    try:
        s3.put_object(
            Bucket=bucket,
            Key=original_key,
            Body=file_bytes,
            ContentType=content_type,
            ServerSideEncryption="AES256",
            Metadata={
                "request-id": linkage["request_id"],
                "document-id": document_id,
                "client-id": client_id,
                "source-app": linkage["source_app"],
            },
        )
        s3.put_object(
            Bucket=bucket,
            Key=linkage_key,
            Body=json.dumps(linkage, indent=2).encode("utf-8"),
            ContentType="application/json",
            ServerSideEncryption="AES256",
        )
    except ClientError as exc:
        raise RuntimeError(f"OCR internal store write failed: {exc}") from exc
