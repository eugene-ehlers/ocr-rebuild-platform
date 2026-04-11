"""create reporting snapshot table

Revision ID: 0011_reporting_layer
Revises: 0010_event_store
Create Date: 2026-04-11
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0011_reporting_layer"
down_revision = "0010_event_store"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "reporting_snapshots",
        sa.Column("snapshot_id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("snapshot_date", sa.Date(), nullable=False),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.tenant_id"], ondelete="RESTRICT"),
    )


def downgrade() -> None:
    op.drop_table("reporting_snapshots")
