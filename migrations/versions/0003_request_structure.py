"""create request structure tables

Revision ID: 0003_request_structure
Revises: 0002_request_core
Create Date: 2026-04-11
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0003_request_structure"
down_revision = "0002_request_core"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "request_snapshots",
        sa.Column("snapshot_id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("request_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("snapshot_data", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.tenant_id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["request_id"], ["requests.request_id"], ondelete="RESTRICT"),
        sa.UniqueConstraint("request_id", "version", name="uq_request_snapshots_request_version"),
    )
    op.create_table(
        "requested_service_items",
        sa.Column("item_id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("request_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("item_code", sa.Text(), nullable=False),
        sa.Column("parameters", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.tenant_id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["request_id"], ["requests.request_id"], ondelete="RESTRICT"),
    )
    op.create_table(
        "request_parties",
        sa.Column("party_id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("request_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("party_type", sa.Text(), nullable=False),
        sa.Column("party_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.tenant_id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["request_id"], ["requests.request_id"], ondelete="RESTRICT"),
    )
    op.create_foreign_key(
        "fk_requests_current_snapshot_id",
        "requests",
        "request_snapshots",
        ["current_snapshot_id"],
        ["snapshot_id"],
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    op.drop_constraint("fk_requests_current_snapshot_id", "requests", type_="foreignkey")
    op.drop_table("request_parties")
    op.drop_table("requested_service_items")
    op.drop_table("request_snapshots")
