"""Persistence-layer immutability notes and helpers.

Database-level protections are authoritative and will be created by Alembic
for immutable tables and append-only event_store behavior.
"""

IMMUTABLE_TABLES = {
    "request_snapshots",
    "resume_restart_decisions",
    "consents",
    "declarations",
    "authorization_traces",
    "admin_actions",
}

APPEND_ONLY_TABLES = {"event_store"}
