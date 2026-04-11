"""create integration and lineage tables

Revision ID: 0009_integration_lineage_layer
Revises: 0008_support_admin_layer
Create Date: 2026-04-11
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0009_integration_lineage_layer"
down_revision = "0008_support_admin_layer"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "integration_correlations",
        sa.Column("correlation_id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("request_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("manifest_id", sa.Text(), nullable=True),
        sa.Column("execution_id", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.tenant_id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["request_id"], ["requests.request_id"], ondelete="RESTRICT"),
    )
    op.create_table(
        "processing_configuration_lineage",
        sa.Column("lineage_id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("request_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.tenant_id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["request_id"], ["requests.request_id"], ondelete="RESTRICT"),
    )


def downgrade() -> None:
    op.drop_table("processing_configuration_lineage")
    op.drop_table("integration_correlations")
