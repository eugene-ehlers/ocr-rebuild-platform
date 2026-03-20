from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

STORE_PATH = Path("runtime_data/request_store.json")


def _ensure_store() -> None:
    STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not STORE_PATH.exists():
        STORE_PATH.write_text(json.dumps({"requests": {}, "consents": {}}, indent=2))


def _read_store() -> Dict[str, Any]:
    _ensure_store()
    data = json.loads(STORE_PATH.read_text())
    if "requests" not in data:
        data["requests"] = {}
    if "consents" not in data:
        data["consents"] = {}
    return data


def _write_store(data: Dict[str, Any]) -> None:
    _ensure_store()
    STORE_PATH.write_text(json.dumps(data, indent=2, sort_keys=True))


def save_request(record: Dict[str, Any]) -> None:
    store = _read_store()
    request_id = record["request"]["request_id"]
    store["requests"][request_id] = record
    _write_store(store)


def get_request(request_id: str) -> Optional[Dict[str, Any]]:
    store = _read_store()
    return store["requests"].get(request_id)


def update_request(request_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    store = _read_store()
    existing = store["requests"].get(request_id)
    if not existing:
        return None

    existing.update(updates)
    store["requests"][request_id] = existing
    _write_store(store)
    return existing


def save_consent_record(customer_id: str, record: Dict[str, Any]) -> None:
    store = _read_store()
    customer_consents = store["consents"].setdefault(customer_id, [])
    customer_consents.append(record)
    _write_store(store)


def get_customer_consent_records(customer_id: str) -> List[Dict[str, Any]]:
    store = _read_store()
    return list(store["consents"].get(customer_id, []))


def revoke_customer_consent(consent_id: str, revoked_at: str) -> bool:
    store = _read_store()
    for customer_id, records in store["consents"].items():
        for record in records:
            if record.get("consent_id") == consent_id:
                record["revoked"] = True
                record["revoked_at"] = revoked_at
                _write_store(store)
                return True
    return False
