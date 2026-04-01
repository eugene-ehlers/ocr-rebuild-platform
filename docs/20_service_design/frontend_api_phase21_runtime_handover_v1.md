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
