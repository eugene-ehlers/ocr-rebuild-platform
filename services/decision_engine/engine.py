from __future__ import annotations

import inspect
import json
import os
from datetime import date, datetime
from importlib import import_module
from typing import Any, Dict

EXECUTION_MODE = os.getenv("EXECUTION_MODE", "local")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

SERVICE_MODULES = {
    "financial_management": "infrastructure.ecs.financial_management.task",
    "fica": "infrastructure.ecs.fica_compliance.task",
    "credit_decision": "infrastructure.ecs.credit_decision.task",
}

AWS_TARGETS = {
    "financial_management": {
        "invoke_type": "ecs",
        "cluster": "ocr-rebuild-cluster",
        "task_definition": "financial-management-worker-task-prod",
        "container_name": "financial_management",
        "subnets": [
            "subnet-08bb8a5fb305fb74a",
            "subnet-075eb014db65f8d57",
        ],
        "security_groups": [
            "sg-0ad48d96d00af793f",
        ],
        "assign_public_ip": "ENABLED",
    },
    "fica": {
        "invoke_type": "ecs",
        "cluster": "ocr-rebuild-cluster",
        "task_definition": "fica-compliance-worker-task-prod",
        "container_name": "fica_compliance",
        "subnets": [
            "subnet-08bb8a5fb305fb74a",
            "subnet-075eb014db65f8d57",
        ],
        "security_groups": [
            "sg-0ad48d96d00af793f",
        ],
        "assign_public_ip": "ENABLED",
    },
    "credit_decision": {
        "invoke_type": "ecs",
        "cluster": "ocr-rebuild-cluster",
        "task_definition": "credit-decision-worker-task-prod",
        "container_name": "credit_decision",
        "subnets": [
            "subnet-08bb8a5fb305fb74a",
            "subnet-075eb014db65f8d57",
        ],
        "security_groups": [
            "sg-0ad48d96d00af793f",
        ],
        "assign_public_ip": "ENABLED",
    },
}


def _make_json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): _make_json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_make_json_safe(v) for v in value]
    if isinstance(value, tuple):
        return [_make_json_safe(v) for v in value]
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return value


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

    candidate_names = ["run_task", "handle", "handler", "main", "execute"]

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

    try:
        import boto3  # type: ignore
    except Exception as e:
        return {
            "execution_mode": "aws_fallback",
            "error": f"boto3_import_failed: {e}",
            "fallback": _invoke_local(service_family, payload),
        }

    try:
        ecs = boto3.client("ecs", region_name=AWS_DEFAULT_REGION)
        response = ecs.run_task(
            cluster=target["cluster"],
            launchType="FARGATE",
            taskDefinition=target["task_definition"],
            overrides={
                "containerOverrides": [
                    {
                        "name": target["container_name"],
                        "environment": [
                            {"name": "PAYLOAD", "value": json.dumps(payload)},
                        ],
                    }
                ]
            },
            networkConfiguration={
                "awsvpcConfiguration": {
                    "subnets": target["subnets"],
                    "securityGroups": target["security_groups"],
                    "assignPublicIp": target["assign_public_ip"],
                }
            },
        )

        return {
            "execution_mode": "aws_live",
            "invoke_type": target["invoke_type"],
            "target_name": service_family,
            "task_count": len(response.get("tasks", [])),
            "failure_count": len(response.get("failures", [])),
            "response_excerpt": _make_json_safe({
                "tasks": response.get("tasks", [])[:1],
                "failures": response.get("failures", [])[:3],
            }),
        }

    except Exception as e:
        return {
            "execution_mode": "aws_fallback",
            "error": f"aws_ecs_invocation_failed: {e}",
            "fallback": _invoke_local(service_family, payload),
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
        if execution["execution_mode"] == "aws_live":
            downstream_status = "aws_attempted"
            summary = f"{service_family} execution routed through live AWS bridge."
        else:
            downstream_status = "aws_fallback"
            summary = f"{service_family} execution attempted via AWS bridge and fell back safely."
    else:
        raise ValueError(f"Unsupported EXECUTION_MODE: {EXECUTION_MODE}")

    return {
        "service_family": service_family,
        "downstream_status": downstream_status,
        "summary": summary,
        "execution": execution,
    }
