# FRONTEND API RUNTIME — WHAT IS (AUTHORITATIVE)

## 1. RUNTIME ARCHITECTURE

Single orchestrator with internal workflow control.

Location:
services/decision_engine/frontend_request_orchestrator.py

---

## 2. ENTRYPOINT

create_request(payload)

---

## 3. EXECUTION MODEL

create_request
→ _run_workflow
    → _run_gating_sequence
    → _run_downstream_sequence
    → _run_finalization_sequence
→ _persist_workflow_record
→ _build_workflow_response

---

## 4. WORKFLOW PHASES

### GATING
- context
- execution plan
- consent
- document
- enforcement

### DOWNSTREAM
- service execution

### FINALIZATION
- request_status
- result_status
- finalization_reason

---

## 5. ORCHESTRATION RECORD

request
execution_plan
stage_results
consent_check
document_check
enforcement
downstream_execution
finalization
routing
last_updated

---

## 6. PERSISTENCE

Full orchestration_record persisted without transformation.

---

## 7. RESPONSE

Derived from finalization.

---

## 8. CHARACTERISTICS

- single runtime authority
- internal workflow structure
- deterministic execution
- contract-preserving

---

## 9. IMPORTANT

This is CURRENT RUNTIME STATE.

Not modular architecture.

---


## Phase 1 runtime handover update

Current state:
- Frontend integration may proceed against the controlled backend orchestration interface.
- The execution payload builder defect has been corrected.
- request_execution_payload_v1 now executes before downstream handoff.
- Payload boundary evidence is captured at the downstream_execution handoff.

Important boundary:
This interface is approved for controlled frontend integration only.
It is not yet the external third-party API contract.

Deferred to Phase 2:
- external API surface
- auth
- OpenAPI
- standardized external error contract
- idempotency / retry model
- async partner integration semantics

---

## 11. Phase 1 runtime handover update (APPENDED - GOVERNED)

### Phase 1 request contract actually used

Current controlled frontend/backend request for the credit decision runtime path includes:

- serviceCode = credit_decision
- analysis_type = bank_statement_ocr_extraction
- documentIds contains ONLY bank statement documents
- processingConsent and disclosureConsent must be true

### Document rule (Phase 1)

For this analysis type:

- ONLY bank_statement documents are valid
- Adding identity_document is not part of this controlled flow and may fail enforcement

### Runtime payload authority

Proven runtime behaviour:

- request_execution_payload_v1 runs before downstream execution
- Builder output is the authoritative downstream handoff payload
- downstream execution receives the transformed payload
- transformed payload retains:
  - manifest_id
  - document

### Lifecycle truth (Phase 1)

Valid runtime states:

- blocked
- processing
- completed / available
- completed / rejected

IMPORTANT:

- completed / rejected is a VALID governed outcome
- It is NOT a system failure

### Proven runtime outcome

Observed:

- request_status = completed
- result_status = rejected
- finalization_reason = downstream_worker_rejected_payload

This reflects correct fail-closed downstream behaviour.

- No change to enforcement model

## Runtime orchestration clarification (actual state)

Current actual runtime behavior:
- Frontend submits requests only to the Decision Engine
- Decision Engine builds execution_plan and enforces validation before downstream execution
- Decision Engine invokes required backend stages based on request context and governed runtime lock
- OCR, reconstruction, classification, scoring, and decision logic are backend-orchestrated capabilities
- OCR-only behavior, where used, still executes through the Decision Engine rather than by direct frontend service invocation

## Model lineage (actual state)

A single JSON lineage object is now used to persist selected and executed model/service metadata.

Current implemented lineage identifiers:
- reconstruction: bank_reconstruction_champion_v1_13Apr2026
- classification: txn_classifier_baseline_v1_13Apr2026
- scoring: credit_score_baseline_v1_13Apr2026

Runtime rule:
- Decision Engine stamps selected lineage
- downstream execution contributes executed lineage
- OCR is observed/executed lineage, not selected lineage

## Financial Management subservice: structured bank statement reconstruction (actual state)

Implemented subservice:
- service family: financial_management
- analysis_type: reconstruct_bank_statement
- governed outcome: FM-OTC-007
- outcome_intent: reconstruct_bank_statement

Runtime behavior:
- frontend request goes to Decision Engine
- Decision Engine selects financial_management with analysis_type = reconstruct_bank_statement
- OCR-derived transaction substrate is reconstructed into a structured electronic bank statement
- result is returned as governed FM-OTC-007 output

Current output shape:
- fm_otc_007.outcome_intent
- fm_otc_007.structured_bank_statement.transactions
- fm_otc_007.structured_bank_statement.transaction_count
- fm_otc_007.structured_bank_statement.statement_period_start
- fm_otc_007.structured_bank_statement.statement_period_end
- fm_otc_007.summary

Boundary:
- this is a financial-management subservice
- not a new top-level service
- still orchestrated only through the Decision Engine
