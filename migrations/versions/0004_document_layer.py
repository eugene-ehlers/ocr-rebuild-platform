"""create document layer tables

Revision ID: 0004_document_layer
Revises: 0003_request_structure
Create Date: 2026-04-11
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0004_document_layer"
down_revision = "0003_request_structure"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "request_documents",
        sa.Column("document_id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("request_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("document_uri", sa.Text(), nullable=False),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.tenant_id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["request_id"], ["requests.request_id"], ondelete="RESTRICT"),
    )
    op.create_table(
        "document_bundles",
        sa.Column("bundle_id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("request_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", sa.Text(), nullable=True),
        sa.Column("bundle_metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.tenant_id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["request_id"], ["requests.request_id"], ondelete="RESTRICT"),
    )


def downgrade() -> None:
    op.drop_table("document_bundles")
    op.drop_table("request_documents")
