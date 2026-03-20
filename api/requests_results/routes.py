from typing import Any, Dict

from .handlers import placeholder_response
from services.decision_engine.frontend_request_orchestrator import (
    create_request,
    get_catalog,
    get_remediation,
    get_result,
    get_status,
    rerun_request,
)


def catalog() -> Dict[str, Any]:
    return get_catalog()


def create(payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
    if payload is None:
        return placeholder_response("requests_results", "create_missing_payload")
    return create_request(payload)


def status(request_id: str = "placeholder_request_id") -> Dict[str, Any]:
    return get_status(request_id)


def remediation(request_id: str = "placeholder_request_id") -> Dict[str, Any]:
    return get_remediation(request_id)


def result(request_id: str = "placeholder_request_id") -> Dict[str, Any]:
    return get_result(request_id)


def rerun(request_id: str = "placeholder_request_id") -> Dict[str, Any]:
    return rerun_request(request_id)
