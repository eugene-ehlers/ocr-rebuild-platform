# Decision Register

## OCR-First Controlled Exposure Decisions

### Decision: FICA OCR-First Controlled Exposure Authority
- decision_id: DR-FICA-OCR-FIRST-001
- status: approved
- scope: fica
- approved_scope_boundary: ocr_first_only
- excluded_scope: bureau|pep|pip|home_affairs|external_compliance_enrichment
- controlled_selector_expectation: selector_must_lock_exactly_one_governed_fica_outcome
- outward_outcome_rule: exactly_one_fica_outcome_may_be_emitted
- fail_closed_rule: insufficient_basis_for_selected_fica_outcome_must_fail_closed
- approved_outcome_codes: FICA-OTC-001|FICA-OTC-002|FICA-OTC-003|FICA-OTC-004|FICA-OTC-005|FICA-OTC-006
- notes: extraction_and_analytical_fica_otcs_must_remain_distinct

### Decision: Credit OCR-First Controlled Exposure Authority
- decision_id: DR-CREDIT-OCR-FIRST-001
- status: approved
- scope: credit_decision
- approved_scope_boundary: ocr_first_only
- excluded_scope: bureau|pep|pip|home_affairs|pricing|offer_generation
- controlled_selector_expectation: selector_must_lock_exactly_one_governed_credit_outcome
- outward_outcome_rule: exactly_one_credit_outcome_may_be_emitted
- fail_closed_rule: insufficient_basis_for_selected_credit_outcome_must_fail_closed
- approved_outcome_codes: Credit-OTC-001|Credit-OTC-002|Credit-OTC-003|Credit-OTC-004|Credit-OTC-005|Credit-OTC-006|Credit-OTC-007|Credit-OTC-008|Credit-OTC-009
- notes: extraction_and_analytical_credit_otcs_must_remain_distinct

---

## End of Document

### Frontend Redesign Alignment to Design Baseline

**Decision**  
The frontend will be incrementally redesigned to align with the approved frontend customer experience design baseline (Steps 1–7).

**Rationale**  
The current frontend is a Developer / Operational Interface (DOI) and not suitable for customer-facing usage.

**Approach**  
- Layered implementation  
- Non-breaking transition  
- Replace DOI behaviour with governed UX model

## DR-frontend-deployment-safety-immutable-releases

### Decision
Frontend deployments for S3 + CloudFront hosted sites must move from mutable live-root overwrite to an immutable release-folder model with controlled promotion.

### Reason
A destructive root deployment pattern caused a production incident affecting company and pilot sites. Root-level overwrite with destructive sync and no versioning or retained releases made rollback difficult and increased blast radius.

### Rule
- live root is logically read-only for deployment
- deployment writes go only to `releases/<release-id>/`
- promotion updates `current/`
- promotion must not use `sync --delete`
- runtime release metadata is required
- CloudFront serving `current/` is the governed target state

### Status
Approved

---

## DR-E2E-LIGHTWEIGHT-INTEGRATION-001

### Decision
A lightweight, additive end-to-end integration approach was approved to validate system wiring without modifying protected backend components.

### Key Elements
- Async ECS launch treated as initial success
- request_id embedded into manifest
- manifest_id propagated through execution payload
- OCR → decision adapter introduced
- S3 result persistence implemented
- poller-based ingestion used
- frontend polling and rendering enabled

### Rationale
- Preserve governed backend design
- Avoid large-scale redesign during validation phase
- Enable working E2E flow for validation and UAT

### Constraint
This is NOT the target architecture and must not be treated as design authority.

### Status
Approved (interim)

## Decision: External API moved to Phase 2

Status: Approved

Decision:
External third-party API integration is moved to Phase 2.

Reason:
The current backend is integration-ready for the controlled frontend, but is not yet external-partner ready because the codebase does not yet provide a hardened external API layer with authentication, versioned OpenAPI contract, standardized error model, idempotency rules, or explicit async integration semantics.

Implications:
- Controlled frontend integration may proceed now.
- Third-party onboarding is blocked until the external API hardening workstream is complete.
- Current request orchestration contract remains internal.

Phase 1 complete items relevant to this decision:
- request_execution_payload_v1 implemented
- builder invoked before _execute(...)
- governed payload handoff corrected
- runtime payload builder defect resolved under governed change control

Phase 2 required:
- HTTP API layer
- authentication/authorization
- versioned OpenAPI specification
- partner-safe error contract
- idempotency and retry semantics
- explicit async processing model
- partner-facing integration documentation

### DR-PHASE1-BUILDER-PAYLOAD-AUTHORITY

Decision:

For the Phase 1 frontend/backend integration path, the output of request_execution_payload_v1 is the authoritative downstream handoff payload.

This payload:

- is created before downstream execution
- is passed into _execute(...)
- is used for downstream execution

Status: ACTIVE

## Decision: Decision Engine is the sole frontend orchestration entrypoint

Status: Approved

Decision:
All frontend requests must go through the Decision Engine. The Decision Engine determines required processing, builds the governed execution plan, orchestrates required services and models, applies governance, and returns the final result.

Clarification:
OCR is not treated as a direct frontend-to-service bypass. OCR is executed through the governed backend flow and recorded as executed lineage when used.

Implications:
- Frontend never calls backend capability modules directly
- Reconstruction, classification, scoring, and decisioning are orchestrated by the Decision Engine
- Model lineage is persisted as a single JSON object rather than schema-expanding columns

## Decision: Financial Management subservice for structured bank statement reconstruction

Status: Approved

Decision:
A new governed financial-management subservice is implemented for structured bank statement reconstruction.

Implemented shape:
- service family remains: financial_management
- analysis_type: reconstruct_bank_statement
- governed outcome: FM-OTC-007
- outcome_intent: reconstruct_bank_statement

Purpose:
Return a structured electronic bank statement from OCR-derived transaction substrate without invoking broader financial analysis or credit decision logic.

Implications:
- frontend can request structured bank statement reconstruction through the Decision Engine
- no new top-level service family or direct frontend-to-service bypass is introduced
- output is suitable for electronic-copy use cases and downstream reuse
