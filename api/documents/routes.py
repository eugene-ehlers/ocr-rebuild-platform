from .handlers import placeholder_response
from .upload_handler import upload_from_idip


def upload_registration():
    """Legacy placeholder retained for scaffold compatibility."""
    return placeholder_response("documents", "upload_registration")


def upload_from_idip_route(payload: dict):
    """Authenticated I-DIP upload entry point.

    Expected payload keys:
    - client_id
    - source_app
    - filename
    - content_type
    - file_b64 (base64-encoded bytes) or file_bytes
    - processing_consent_valid
    - consent_record_ids
    - disclosure_consent_status (optional)
    """
    import base64

    file_bytes = payload.get("file_bytes")
    if file_bytes is None and payload.get("file_b64"):
        file_bytes = base64.b64decode(payload["file_b64"])
    if not isinstance(file_bytes, (bytes, bytearray)):
        raise ValueError("file content is required")

    return upload_from_idip(
        client_id=str(payload.get("client_id", "")),
        source_app=str(payload.get("source_app", "")),
        file_bytes=bytes(file_bytes),
        filename=str(payload.get("filename", "upload.bin")),
        content_type=str(payload.get("content_type", "application/octet-stream")),
        processing_consent_valid=bool(payload.get("processing_consent_valid", False)),
        consent_record_ids=list(payload.get("consent_record_ids") or []),
        disclosure_consent_status=str(payload.get("disclosure_consent_status", "not_required")),
    )


def retrieve():
    return placeholder_response("documents", "retrieve")


def replace():
    return placeholder_response("documents", "replace")


def append():
    return placeholder_response("documents", "append")


def reorder():
    return placeholder_response("documents", "reorder")


def merge():
    return placeholder_response("documents", "merge")


def split():
    return placeholder_response("documents", "split")


def validate_completeness():
    return placeholder_response("documents", "validate_completeness")


def validate_freshness():
    return placeholder_response("documents", "validate_freshness")
