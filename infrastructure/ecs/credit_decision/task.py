from __future__ import annotations

import json
from typing import Any, Dict

from services.credit_decision.service_runner import run


def run_task(payload: Dict[str, Any]) -> Dict[str, Any]:
    print(f"Running credit_decision ECS task with payload: {json.dumps(payload, sort_keys=True)}")
    return run(payload)
