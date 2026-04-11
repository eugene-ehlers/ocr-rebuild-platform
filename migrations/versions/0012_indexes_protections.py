"""create indexes and immutability protections

Revision ID: 0012_indexes_protections
Revises: 0011_reporting_layer
Create Date: 2026-04-11
"""

from alembic import op

revision = "0012_indexes_protections"
down_revision = "0011_reporting_layer"
branch_labels = None
depends_on = None


IMMUTABLE_TABLES = [
    "request_snapshots",
    "resume_restart_decisions",
    "consents",
    "declarations",
    "authorization_traces",
    "admin_actions",
]


def _create_read_only_trigger(table_name: str) -> None:
    op.execute(
        f"""
        CREATE OR REPLACE FUNCTION {table_name}_readonly_guard()
        RETURNS trigger AS $$
        BEGIN
            RAISE EXCEPTION '{table_name} is immutable';
        END;
        $$ LANGUAGE plpgsql;
        """
    )
    op.execute(
        f"""
        CREATE TRIGGER trg_{table_name}_readonly_update
        BEFORE UPDATE ON {table_name}
        FOR EACH ROW EXECUTE FUNCTION {table_name}_readonly_guard();
        """
    )
    op.execute(
        f"""
        CREATE TRIGGER trg_{table_name}_readonly_delete
        BEFORE DELETE ON {table_name}
        FOR EACH ROW EXECUTE FUNCTION {table_name}_readonly_guard();
        """
    )


def upgrade() -> None:
    op.create_index("ix_requests_tenant_status", "requests", ["tenant_id", "status"], unique=False)
    op.create_index("ix_requests_user_id", "requests", ["user_id"], unique=False)
    op.create_index("ix_request_documents_request_id", "request_documents", ["request_id"], unique=False)
    op.create_index("ix_result_packages_request_id", "result_packages", ["request_id"], unique=False)
    op.create_index("ix_support_cases_status_tenant", "support_cases", ["status", "tenant_id"], unique=False)
    op.create_index(
        "ix_reporting_snapshots_tenant_snapshot_date",
        "reporting_snapshots",
        ["tenant_id", "snapshot_date"],
        unique=False,
    )
    op.create_index(
        "ix_event_store_aggregate_sequence",
        "event_store",
        ["aggregate_id", "event_sequence"],
        unique=False,
    )
    op.create_index("ix_event_store_event_type", "event_store", ["event_type"], unique=False)
    op.create_index("ix_event_store_tenant_id", "event_store", ["tenant_id"], unique=False)
    op.create_index(
        "ix_event_store_actor_timestamp",
        "event_store",
        ["actor_id", "event_timestamp"],
        unique=False,
    )

    op.execute(
        """
        CREATE OR REPLACE FUNCTION event_store_append_only_guard()
        RETURNS trigger AS $$
        BEGIN
            RAISE EXCEPTION 'event_store is append-only';
        END;
        $$ LANGUAGE plpgsql;
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_event_store_no_update
        BEFORE UPDATE ON event_store
        FOR EACH ROW EXECUTE FUNCTION event_store_append_only_guard();
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_event_store_no_delete
        BEFORE DELETE ON event_store
        FOR EACH ROW EXECUTE FUNCTION event_store_append_only_guard();
        """
    )

    for table_name in IMMUTABLE_TABLES:
        _create_read_only_trigger(table_name)


def downgrade() -> None:
    for table_name in IMMUTABLE_TABLES:
        op.execute(f"DROP TRIGGER IF EXISTS trg_{table_name}_readonly_delete ON {table_name};")
        op.execute(f"DROP TRIGGER IF EXISTS trg_{table_name}_readonly_update ON {table_name};")
        op.execute(f"DROP FUNCTION IF EXISTS {table_name}_readonly_guard();")

    op.execute("DROP TRIGGER IF EXISTS trg_event_store_no_delete ON event_store;")
    op.execute("DROP TRIGGER IF EXISTS trg_event_store_no_update ON event_store;")
    op.execute("DROP FUNCTION IF EXISTS event_store_append_only_guard();")

    op.drop_index("ix_event_store_actor_timestamp", table_name="event_store")
    op.drop_index("ix_event_store_tenant_id", table_name="event_store")
    op.drop_index("ix_event_store_event_type", table_name="event_store")
    op.drop_index("ix_event_store_aggregate_sequence", table_name="event_store")
    op.drop_index("ix_reporting_snapshots_tenant_snapshot_date", table_name="reporting_snapshots")
    op.drop_index("ix_support_cases_status_tenant", table_name="support_cases")
    op.drop_index("ix_result_packages_request_id", table_name="result_packages")
    op.drop_index("ix_request_documents_request_id", table_name="request_documents")
    op.drop_index("ix_requests_user_id", table_name="requests")
    op.drop_index("ix_requests_tenant_status", table_name="requests")
