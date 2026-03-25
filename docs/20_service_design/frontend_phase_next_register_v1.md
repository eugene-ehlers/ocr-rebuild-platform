# Front-End Phase-Next Register v1

Status: WORKING DESIGN REGISTER  
Purpose: Preserve higher-order front-end capabilities, innovations, and deferred design ideas that are not part of the current Phase 1 build baseline, so they are not lost during implementation hardening.

## 1. Scope

This register captures:
- deferred advanced UX capabilities
- adaptive/intelligent front-end features
- richer API/workspace/result capabilities not yet available in current backend/runtime baseline
- candidate future services/models for build-vs-buy evaluation

This register does **not** replace:
- governed decision register
- governed gap register
- current Phase 1 contract baseline

It complements them.

---

## 2. Phase 2 Candidate Items

### FE-PN-001 — Logical Document Workspace Persistence
**Summary:** Persist full logical document structure across sessions, including document -> file -> page hierarchy, grouping, ordering, and linking.  
**Why deferred:** Current backend does not yet expose durable workspace persistence contract.  
**Value:** Enables richer document preparation and session continuity.

### FE-PN-002 — Missing Page Detection
**Summary:** Detect likely incomplete statements / page gaps before submission.  
**Why deferred:** Capability not yet implemented or formally contracted.  
**Value:** Reduces failed or misleading processing outcomes.

### FE-PN-003 — Pre-Processing Quality Feedback
**Summary:** Provide page/image quality scoring and actionable re-upload guidance before processing.  
**Why deferred:** Requires additional quality evaluation capability at front-end boundary.  
**Value:** Improves OCR success and reduces retry volume.

### FE-PN-004 — Explanation Generation Layer
**Summary:** Explain extracted outputs, warnings, and confidence to the user in plain language.  
**Why deferred:** Requires explanation service/model strategy and result normalization.  
**Value:** Improves trust and usability.

### FE-PN-005 — Partial Success Recovery
**Summary:** Allow retry and recovery for failed subset/sections while preserving successful outputs.  
**Why deferred:** Current backend contract does not yet prove subset retry semantics.  
**Value:** Reduces full reruns and improves user control.

### FE-PN-006 — Audit Trail Visibility
**Summary:** Show user-visible audit events for submission, consent, processing, and result access.  
**Why deferred:** User-facing audit model not yet defined.  
**Value:** Supports compliance, transparency, and trust.

### FE-PN-007 — Adaptive Guidance Engine
**Summary:** Dynamically guide users based on behaviour, friction, and confidence signals.  
**Why deferred:** Requires telemetry event model and decisioning layer.  
**Value:** Reduces abandonment and improves completion.

### FE-PN-008 — Behavioural Telemetry Model
**Summary:** Capture structured front-end telemetry across upload, workspace, validation, and error recovery.  
**Why deferred:** Telemetry routes exist structurally but client and event model remain placeholder.  
**Value:** Enables optimisation and future adaptive UX.

### FE-PN-009 — Trust and Consent Enrichment
**Summary:** Extend trust UI beyond submission confirmation into richer evidence visibility, consent history, expiry awareness, and revocation handling.  
**Why deferred:** Current consent evidence exists, but front-end trust model is not yet fully surfaced.  
**Value:** Strengthens compliance experience.

### FE-PN-010 — Multilingual UX Support
**Summary:** Support multilingual UI, explanations, and guided flows.  
**Why deferred:** No selected translation/support strategy yet.  
**Value:** Expands usability across user segments.

---

## 3. Phase 3 Candidate Items

### FE-PN-011 — Real-Time Adaptive UI Modes
**Summary:** Adjust flow complexity and guidance dynamically for novice vs advanced users.  
**Why deferred:** Requires mature telemetry + decision engine integration.  
**Value:** Personalised, lower-friction journey.

### FE-PN-012 — Conversational Assistance Layer
**Summary:** Embedded AI assistant for workspace guidance, validation help, and result interpretation.  
**Why deferred:** Requires model selection, guardrails, and interaction architecture.  
**Value:** Future advisory and support differentiation.

### FE-PN-013 — Advanced Recommendation Engine
**Summary:** Suggest next steps, document groupings, corrections, or service follow-ons based on user context and evidence.  
**Why deferred:** Requires behavioural modelling and recommendation logic.  
**Value:** Higher completion and more intelligent service use.

### FE-PN-014 — Champion / Challenger UX
**Summary:** Support controlled testing of different layouts, guidance styles, and flows.  
**Why deferred:** Requires telemetry maturity and experiment framework.  
**Value:** Continuous measurable optimisation.

### FE-PN-015 — Suspicious Session / Behaviour Risk Layer
**Summary:** Detect suspicious interaction patterns and trigger additional safeguards.  
**Why deferred:** Requires security telemetry, policy design, and risk decisioning.  
**Value:** Abuse resistance and stronger platform trust.

### FE-PN-016 — Cross-Session Document Intelligence
**Summary:** Reuse, compare, merge, and analyse previous document sets over time.  
**Why deferred:** Requires historical document model, persistence, and stronger result normalization.  
**Value:** Powerful continuity for financial/document intelligence workflows.

---

## 4. Current Back-End Constraint Notes

The following remain current hard constraints from verified project state:

- frontend request flow is request-based, not full workspace/job abstraction
- document routes are scaffolded placeholders
- document workspace hook is scaffolded placeholder
- status/result retrieval exists through request orchestration
- current backend truth centers on:
  - requestId
  - requestStatus
  - resultStatus
  - finalizationReason
  - consentRecords
  - downstream_execution
- richer abstractions such as:
  - workspaceId
  - logicalDocumentId
  - fileAssetId
  - validationRunId
  - processingJobId
  are not yet verified as implemented runtime truth

This means Phase 2/3 items must be aligned later to actual backend evolution.

---

## 5. Operating Rule

When a future capability is:
- valuable
- intentionally deferred
- not safe for current implementation
- or not yet supported by backend/runtime truth

it must be added here rather than lost.

This register should be reviewed:
- before each new front-end design phase
- before major API contract changes
- before promoting innovation items into governed gaps or decisions
