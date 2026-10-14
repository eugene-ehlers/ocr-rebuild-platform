"""Client-scoped, consent-gated upload path for I-DIP.

Writes first to the OCR internal audit store under mandatory linkage metadata,
then returns only a client-safe payload that I-DIP may place in its vault.

No direct access to the internal store is ever granted to I-DIP or the client.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_document_id() -> str:
    return f"doc_{uuid.uuid4().hex[:12]}"


def _new_request_id() -> str:
    return f"req_{uuid.uuid4().hex[:12]}"


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

    # In a real implementation this writes file_bytes + linkage
    # to the OCR internal store under a client-scoped key and
    # records an audit event. The internal store is never exposed.
    _write_to_ocr_internal_store(
        linkage=linkage,
        filename=filename,
        content_type=content_type,
        file_bytes=file_bytes,
    )

    # Client-safe payload returned to I-DIP for its vault.
    # Contains no credentials, no internal paths, no raw OCR text.
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
    """Placeholder for the secure write to the OCR audit store.

    Real implementation must:
    - use a service role that only the OCR platform holds
    - store under a key derived from client_id + document_id
    - attach the full linkage metadata
    - emit an audit log entry
    - never return a presigned URL or credential to the caller
    """
    # Intentionally empty in this stub. The contract is defined;
    # storage wiring is a later deployment step.
    _ = (linkage, filename, content_type, file_bytes)
