from __future__ import annotations

import inspect
import os
from importlib import import_module
from typing import Any, Dict

EXECUTION_MODE = os.getenv("EXECUTION_MODE", "local")

SERVICE_MODULES = {
    "financial_management": "infrastructure.ecs.financial_management.task",
    "fica": "infrastructure.ecs.fica_compliance.task",
    "credit_decision": "infrastructure.ecs.credit_decision.task",
}

AWS_TARGETS = {
    "financial_management": {
        "invoke_type": "ecs",
        "target_name": "financial_management",
    },
    "fica": {
        "invoke_type": "ecs",
        "target_name": "fica_compliance",
    },
    "credit_decision": {
        "invoke_type": "ecs",
        "target_name": "credit_decision",
    },
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


def _invoke_local(service_family: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    module_path = SERVICE_MODULES[service_family]
    return _invoke_task_module(module_path, payload)


def _invoke_aws(service_family: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    target = AWS_TARGETS[service_family]

    return {
        "execution_mode": "aws_bridge",
        "bridge_status": "stubbed",
        "invoke_type": target["invoke_type"],
        "target_name": target["target_name"],
        "aws_request_payload": payload,
        "aws_response": {
            "status": "aws_bridge_not_yet_connected",
            "message": "AWS bridge path selected, but live ECS/Lambda invocation is not yet wired in this phase.",
        },
    }


def execute_service_family(service_family: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    if service_family not in SERVICE_MODULES:
        raise ValueError(f"Unsupported service family: {service_family}")

    mode = EXECUTION_MODE.strip().lower()

    if mode == "local":
        execution = _invoke_local(service_family, payload)
        downstream_status = "executed"
        summary = f"{service_family} execution invoked via local decision-engine path."
    elif mode == "aws":
        execution = _invoke_aws(service_family, payload)
        downstream_status = "aws_bridge_stubbed"
        summary = f"{service_family} execution routed through AWS bridge stub."
    else:
        raise ValueError(f"Unsupported EXECUTION_MODE: {EXECUTION_MODE}")

    return {
        "service_family": service_family,
        "downstream_status": downstream_status,
        "summary": summary,
        "execution": execution,
    }
