"""Post OCR extraction results back to I-DIP.

Called by the OCR worker (or a thin wrapper) when text and fields are ready.
I-DIP stores the raw text so the document never needs to be re-read, and
pre-fills the matching form for user review.
"""

from __future__ import annotations

from typing import Any, Dict, Optional
import json
import os
import urllib.request
import urllib.error


def _endpoint(document_id: str) -> str:
    base = os.environ.get("IDIP_RESULTS_BASE_URL", "").strip().rstrip("/")
    if not base:
        raise RuntimeError("IDIP_RESULTS_BASE_URL is not configured")
    return f"{base}/my/passport/documents/ocr-result/{document_id}"


def post_results(
    *,
    document_id: str,
    raw_ocr_text: str,
    fields: Optional[Dict[str, Any]] = None,
    auth_cookie: Optional[str] = None,
) -> Dict[str, Any]:
    """POST raw text and extracted fields to I-DIP.

    auth_cookie: optional session cookie if the endpoint requires the user session.
    For service-to-service, prefer a shared secret header later.
    """
    url = _endpoint(document_id)
    payload = {
        "raw_ocr_text": raw_ocr_text or "",
        "fields": fields or {},
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    if auth_cookie:
        req.add_header("Cookie", auth_cookie)

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read().decode("utf-8")
            return {"ok": True, "status": resp.status, "body": body}
    except urllib.error.HTTPError as exc:
        return {"ok": False, "status": exc.code, "body": exc.read().decode("utf-8", errors="replace")}
    except Exception as exc:
        return {"ok": False, "status": 0, "body": str(exc)}
