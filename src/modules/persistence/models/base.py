"""Shared SQLAlchemy model helpers for System B persistence."""

from __future__ import annotations

import uuid

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.modules.persistence.db import Base


class TimestampMixin:
    created_at: Mapped[object] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


class UpdatedAtMixin:
    updated_at: Mapped[object | None] = mapped_column(DateTime(timezone=True), nullable=True)


class TenantScopedMixin:
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.tenant_id", ondelete="RESTRICT"), nullable=False
    )


class Tenant(Base, TimestampMixin):
    __tablename__ = "tenants"

    tenant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_json: Mapped[dict | None] = mapped_column("metadata", JSONB, nullable=True)


class User(Base, TimestampMixin, UpdatedAtMixin, TenantScopedMixin):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("tenant_id", "email", name="uq_users_tenant_email"),)

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(Text, nullable=False)
    profile_metadata: Mapped[dict | None] = mapped_column(JSONB, nullable=True)


class Membership(Base, TimestampMixin, UpdatedAtMixin, TenantScopedMixin):
    __tablename__ = "memberships"

    membership_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="RESTRICT"), nullable=False
    )
    role: Mapped[str] = mapped_column(Text, nullable=False)


class ServiceDefinition(Base, TimestampMixin):
    __tablename__ = "service_definitions"

    service_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_code: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    service_name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)


class ServiceConfigurationVersion(Base, TimestampMixin):
    __tablename__ = "service_configuration_versions"

    config_version_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("service_definitions.service_id", ondelete="RESTRICT"), nullable=False
    )
    version_label: Mapped[str] = mapped_column(Text, nullable=False)
    config_payload: Mapped[dict] = mapped_column(JSONB, nullable=False)


class RuleVersion(Base, TimestampMixin):
    __tablename__ = "rule_versions"

    rule_version_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rule_code: Mapped[str] = mapped_column(Text, nullable=False)
    version_label: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)


class Request(Base, TimestampMixin, UpdatedAtMixin, TenantScopedMixin):
    __tablename__ = "requests"

    request_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="RESTRICT"), nullable=False
    )
    service_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("service_definitions.service_id", ondelete="RESTRICT"), nullable=False
    )
    config_version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("service_configuration_versions.config_version_id", ondelete="RESTRICT"),
        nullable=False,
    )
    current_snapshot_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("request_snapshots.snapshot_id", ondelete="RESTRICT"),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(Text, nullable=False)
    request_metadata: Mapped[dict | None] = mapped_column(JSONB, nullable=True)


class RequestSnapshot(Base, TimestampMixin, TenantScopedMixin):
    __tablename__ = "request_snapshots"
    __table_args__ = (UniqueConstraint("request_id", "version", name="uq_request_snapshots_request_version"),)

    snapshot_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("requests.request_id", ondelete="RESTRICT"), nullable=False
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    snapshot_data: Mapped[dict] = mapped_column(JSONB, nullable=False)


class RequestedServiceItem(Base, TimestampMixin, UpdatedAtMixin, TenantScopedMixin):
    __tablename__ = "requested_service_items"

    item_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("requests.request_id", ondelete="RESTRICT"), nullable=False
    )
    item_code: Mapped[str] = mapped_column(Text, nullable=False)
    parameters: Mapped[dict | None] = mapped_column(JSONB, nullable=True)


class RequestParty(Base, TimestampMixin, UpdatedAtMixin, TenantScopedMixin):
    __tablename__ = "request_parties"

    party_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("requests.request_id", ondelete="RESTRICT"), nullable=False
    )
    party_type: Mapped[str] = mapped_column(Text, nullable=False)
    party_payload: Mapped[dict | None] = mapped_column(JSONB, nullable=True)


class RequestDocument(Base, TimestampMixin, UpdatedAtMixin, TenantScopedMixin):
    __tablename__ = "request_documents"

    document_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("requests.request_id", ondelete="RESTRICT"), nullable=False
    )
    document_uri: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_json: Mapped[dict | None] = mapped_column("metadata", JSONB, nullable=True)


class DocumentBundle(Base, TimestampMixin, UpdatedAtMixin, TenantScopedMixin):
    __tablename__ = "document_bundles"

    bundle_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("requests.request_id", ondelete="RESTRICT"), nullable=False
    )
    status: Mapped[str | None] = mapped_column(Text, nullable=True)
    bundle_metadata: Mapped[dict | None] = mapped_column(JSONB, nullable=True)


class JourneyInstance(Base, TimestampMixin, UpdatedAtMixin, TenantScopedMixin):
    __tablename__ = "journey_instances"

    journey_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("requests.request_id", ondelete="RESTRICT"), nullable=False
    )
    status: Mapped[str | None] = mapped_column(Text, nullable=True)


class AttemptRecord(Base, TimestampMixin, UpdatedAtMixin, TenantScopedMixin):
    __tablename__ = "attempt_records"

    attempt_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("requests.request_id", ondelete="RESTRICT"), nullable=False
    )
    attempt_type: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str | None] = mapped_column(Text, nullable=True)


class RetryEscalationRecord(Base, TimestampMixin, UpdatedAtMixin, TenantScopedMixin):
    __tablename__ = "retry_escalation_records"

    retry_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("requests.request_id", ondelete="RESTRICT"), nullable=False
    )
    status: Mapped[str | None] = mapped_column(Text, nullable=True)
    details: Mapped[dict | None] = mapped_column(JSONB, nullable=True)


class ResumeRestartDecision(Base, TimestampMixin, TenantScopedMixin):
    __tablename__ = "resume_restart_decisions"

    decision_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("requests.request_id", ondelete="RESTRICT"), nullable=False
    )
    decision_type: Mapped[str] = mapped_column(Text, nullable=False)
    details: Mapped[dict | None] = mapped_column(JSONB, nullable=True)


class Consent(Base, TimestampMixin, TenantScopedMixin):
    __tablename__ = "consents"

    consent_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("requests.request_id", ondelete="RESTRICT"), nullable=False
    )
    payload: Mapped[dict | None] = mapped_column(JSONB, nullable=True)


class Declaration(Base, TimestampMixin, TenantScopedMixin):
    __tablename__ = "declarations"

    declaration_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("requests.request_id", ondelete="RESTRICT"), nullable=False
    )
    declaration_text: Mapped[str | None] = mapped_column(Text, nullable=True)


class AuthorizationTrace(Base, TimestampMixin, TenantScopedMixin):
    __tablename__ = "authorization_traces"

    auth_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("requests.request_id", ondelete="RESTRICT"), nullable=False
    )
    payload: Mapped[dict | None] = mapped_column(JSONB, nullable=True)


class ResultPackage(Base, TimestampMixin, UpdatedAtMixin, TenantScopedMixin):
    __tablename__ = "result_packages"

    result_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("requests.request_id", ondelete="RESTRICT"), nullable=False
    )
    result_uri: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str | None] = mapped_column(Text, nullable=True)


class Notification(Base, TimestampMixin, UpdatedAtMixin, TenantScopedMixin):
    __tablename__ = "notifications"

    notification_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("requests.request_id", ondelete="RESTRICT"), nullable=False
    )
    status: Mapped[str | None] = mapped_column(Text, nullable=True)
    payload: Mapped[dict | None] = mapped_column(JSONB, nullable=True)


class SupportCase(Base, TimestampMixin, UpdatedAtMixin, TenantScopedMixin):
    __tablename__ = "support_cases"

    case_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("requests.request_id", ondelete="RESTRICT"), nullable=False
    )
    status: Mapped[str | None] = mapped_column(Text, nullable=True)
    priority: Mapped[str | None] = mapped_column(Text, nullable=True)


class AdminAction(Base, TimestampMixin, TenantScopedMixin):
    __tablename__ = "admin_actions"

    action_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("requests.request_id", ondelete="RESTRICT"), nullable=False
    )
    action_type: Mapped[str | None] = mapped_column(Text, nullable=True)
    payload: Mapped[dict | None] = mapped_column(JSONB, nullable=True)


class IntegrationCorrelation(Base, TimestampMixin, TenantScopedMixin):
    __tablename__ = "integration_correlations"

    correlation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("requests.request_id", ondelete="RESTRICT"), nullable=False
    )
    manifest_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    execution_id: Mapped[str | None] = mapped_column(Text, nullable=True)


class ProcessingConfigurationLineage(Base, TimestampMixin, TenantScopedMixin):
    __tablename__ = "processing_configuration_lineage"

    lineage_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("requests.request_id", ondelete="RESTRICT"), nullable=False
    )
    payload: Mapped[dict | None] = mapped_column(JSONB, nullable=True)


class EventStore(Base):
    __tablename__ = "event_store"
    __table_args__ = (UniqueConstraint("aggregate_id", "event_sequence", name="uq_event_store_aggregate_sequence"),)

    event_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    aggregate_type: Mapped[str] = mapped_column(Text, nullable=False)
    aggregate_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    event_type: Mapped[str] = mapped_column(Text, nullable=False)
    event_sequence: Mapped[int] = mapped_column(Integer, nullable=False)
    event_timestamp: Mapped[object] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.tenant_id", ondelete="RESTRICT"), nullable=False
    )
    actor_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="RESTRICT"), nullable=True
    )
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False)


class ReportingSnapshot(Base, TimestampMixin, TenantScopedMixin):
    __tablename__ = "reporting_snapshots"

    snapshot_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    snapshot_date: Mapped[object] = mapped_column(Date, nullable=False)
    payload: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
