from __future__ import annotations

import json
import os

from services.financial_management.service_runner import run


def main() -> None:
    raw_payload = os.environ.get("PAYLOAD", "{}")
    payload = json.loads(raw_payload)
    result = run(payload)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
