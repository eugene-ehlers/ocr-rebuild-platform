from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

DB_PATH = Path("runtime_data/request_store.db")


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _init_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS requests (
                request_id TEXT PRIMARY KEY,
                customer_id TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS consents (
                consent_id TEXT PRIMARY KEY,
                customer_id TEXT NOT NULL,
                consent_type TEXT NOT NULL,
                record_json TEXT NOT NULL,
                captured_at TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_requests_customer_id ON requests(customer_id)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_consents_customer_id ON consents(customer_id)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_consents_type ON consents(consent_type)"
        )
        conn.commit()


_init_db()


def save_request(record: Dict[str, Any]) -> None:
    request_id = record["request"]["request_id"]
    customer_id = record["request"]["customer_id"]
    payload_json = json.dumps(record, sort_keys=True)

    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO requests (request_id, customer_id, payload_json)
            VALUES (?, ?, ?)
            ON CONFLICT(request_id) DO UPDATE SET
                customer_id=excluded.customer_id,
                payload_json=excluded.payload_json
            """,
            (request_id, customer_id, payload_json),
        )
        conn.commit()


def get_request(request_id: str) -> Optional[Dict[str, Any]]:
    with _connect() as conn:
        row = conn.execute(
            "SELECT payload_json FROM requests WHERE request_id = ?",
            (request_id,),
        ).fetchone()

    if not row:
        return None
    return json.loads(row["payload_json"])


def update_request(request_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    existing = get_request(request_id)
    if not existing:
        return None

    existing.update(updates)
    save_request(existing)
    return existing


def save_consent_record(customer_id: str, record: Dict[str, Any]) -> None:
    consent_id = record["consent_id"]
    consent_type = record["consent_type"]
    record_json = json.dumps(record, sort_keys=True)
    captured_at = record.get("captured_at")

    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO consents (consent_id, customer_id, consent_type, record_json, captured_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(consent_id) DO UPDATE SET
                customer_id=excluded.customer_id,
                consent_type=excluded.consent_type,
                record_json=excluded.record_json,
                captured_at=excluded.captured_at
            """,
            (consent_id, customer_id, consent_type, record_json, captured_at),
        )
        conn.commit()


def get_customer_consent_records(customer_id: str) -> List[Dict[str, Any]]:
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT record_json
            FROM consents
            WHERE customer_id = ?
            ORDER BY COALESCE(captured_at, created_at) DESC
            """,
            (customer_id,),
        ).fetchall()

    return [json.loads(row["record_json"]) for row in rows]


def revoke_customer_consent(consent_id: str, revoked_at: str) -> bool:
    with _connect() as conn:
        row = conn.execute(
            "SELECT record_json FROM consents WHERE consent_id = ?",
            (consent_id,),
        ).fetchone()

        if not row:
            return False

        record = json.loads(row["record_json"])
        record["revoked"] = True
        record["revoked_at"] = revoked_at

        conn.execute(
            "UPDATE consents SET record_json = ? WHERE consent_id = ?",
            (json.dumps(record, sort_keys=True), consent_id),
        )
        conn.commit()

    return True


def get_persistence_health() -> Dict[str, Any]:
    with _connect() as conn:
        request_count = conn.execute("SELECT COUNT(*) AS c FROM requests").fetchone()["c"]
        consent_count = conn.execute("SELECT COUNT(*) AS c FROM consents").fetchone()["c"]

    return {
        "backend": "sqlite",
        "db_path": str(DB_PATH),
        "requests": request_count,
        "consents": consent_count,
    }
