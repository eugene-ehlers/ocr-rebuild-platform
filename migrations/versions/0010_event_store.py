"""create append-only event store table

Revision ID: 0010_event_store
Revises: 0009_integration_lineage_layer
Create Date: 2026-04-11
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0010_event_store"
down_revision = "0009_integration_lineage_layer"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "event_store",
        sa.Column("event_id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("aggregate_type", sa.Text(), nullable=False),
        sa.Column("aggregate_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("event_type", sa.Text(), nullable=False),
        sa.Column("event_sequence", sa.Integer(), nullable=False),
        sa.Column("event_timestamp", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("actor_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.tenant_id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["actor_id"], ["users.user_id"], ondelete="RESTRICT"),
        sa.UniqueConstraint("aggregate_id", "event_sequence", name="uq_event_store_aggregate_sequence"),
    )


def downgrade() -> None:
    op.drop_table("event_store")
