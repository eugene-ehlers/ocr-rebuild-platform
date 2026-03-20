from __future__ import annotations

from importlib import import_module
from typing import Any, Dict
import inspect


SERVICE_MODULES = {
    "financial_management": "infrastructure.ecs.financial_management.task",
    "fica": "infrastructure.ecs.fica_compliance.task",
    "credit_decision": "infrastructure.ecs.credit_decision.task",
}


def _invoke_callable(fn, payload: Dict[str, Any]) -> Dict[str, Any]:
    signature = inspect.signature(fn)
    params = list(signature.parameters.values())

    if len(params) == 0:
        result = fn()
        return {
            "invocation_style": "no_args",
            "result": result if isinstance(result, dict) else {"raw_result": result},
        }

    result = fn(payload)
    return {
        "invocation_style": "payload_arg",
        "result": result if isinstance(result, dict) else {"raw_result": result},
    }


def _invoke_task_module(module_path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    module = import_module(module_path)

    candidate_names = [
        "run_task",
        "handle",
        "handler",
        "main",
        "execute",
    ]

    for name in candidate_names:
        fn = getattr(module, name, None)
        if callable(fn):
            invocation = _invoke_callable(fn, payload)
            return {
                "execution_mode": "service_stub",
                "module": module_path,
                "callable": name,
                "invocation": invocation,
            }

    return {
        "execution_mode": "service_stub_unresolved",
        "module": module_path,
        "result": {
            "status": "no_supported_callable_found",
        },
    }


def execute_service_family(service_family: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    if service_family not in SERVICE_MODULES:
        raise ValueError(f"Unsupported service family: {service_family}")

    module_path = SERVICE_MODULES[service_family]
    execution = _invoke_task_module(module_path, payload)

    return {
        "service_family": service_family,
        "downstream_status": "executed",
        "summary": f"{service_family} execution invoked via decision engine.",
        "execution": execution,
    }
