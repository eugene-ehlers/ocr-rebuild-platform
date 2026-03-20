from __future__ import annotations

import json
from typing import Any, Dict


def run_task(payload: Dict[str, Any]) -> Dict[str, Any]:
    print(f"Running financial_management ECS task with payload: {json.dumps(payload, sort_keys=True)}")
    return {
        "service": "financial_management",
        "status": "executed",
        "received_payload": payload,
        "result": {
            "summary": "Financial management stub executed with real orchestration payload.",
            "capabilities": [
                "transaction_parsing",
                "category_classification",
                "cash_flow_classification",
                "debt_detection",
                "behavioural_analysis",
                "benchmarking",
                "reporting_explanation",
            ],
        },
    }
