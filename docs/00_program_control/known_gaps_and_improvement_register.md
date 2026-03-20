# Known Gaps and Improvement Register

## Purpose

Maintain an explicit governed register of:
- known gaps
- limitations
- deferred controls
- improvement opportunities
- interpretation risks

This register exists to prevent:
- silent assumptions
- undocumented omissions
- ambiguous handovers
- incorrect future interpretation of missing behaviour

---

## Status Values

- `OPEN` — known gap not yet addressed
- `PARTIAL` — partially addressed but still incomplete
- `CLOSED` — addressed and no longer a live gap
- `SUPERSEDED` — replaced by a later design decision

---

## Register

| Gap ID | Area | Description | Current State | Impact | Interpretation Risk | Current Workaround | Target / Next Step | Status |
|---|---|---|---|---|---|---|---|---|
| GAP-001 | Runtime validation | CloudShell local `python3` is 3.9, while governed runtime baseline is Python 3.11. | Python 3.11 container validation adopted and used to validate AWS-mode `create_request(...)` persistence successfully. | Local validation can still be misleading if run with system python. | High | Validate runtime-sensitive behaviour in Python 3.11 container. | Keep all runtime validation aligned to Python 3.11 or governed AWS runtime until host environment is upgraded. | PARTIAL |
| GAP-002 | Telemetry module scaffold | Phase 1 originally omitted `components` and `pages` under telemetry module. | Fixed during Phase 10. | Replay from bad scaffold can fail. | Medium | Corrected scaffold script exists. | Ensure scaffold baseline script remains the source of truth. | CLOSED |
| GAP-003 | Downstream execution | Real AWS ECS/Lambda invocation was previously unavailable and execution used only local service stubs. | Dual-mode execution active from Phase 20. Worker packaging/import issues are now resolved. ECR images exist, ECS task definitions are aligned, live Fargate execution is validated for financial management, fica compliance, and credit decision, decision-engine AWS routing plus SQLite persistence are validated under Python 3.11 runtime, and a full controlled OCR pipeline Step Functions execution has now succeeded in AWS for a governed image input through preprocessing, OCR, gate evaluation, aggregation, and final validation. | AWS ECS/Lambda execution path is operational for the currently wired service families and the current OCR pipeline baseline, though broader production hardening remains pending. | Low | Use Python 3.11 container or governed AWS runtime for validation. | Continue with next governed implementation phase; retain Python 3.11 validation discipline and expand governed runtime validation coverage carefully. | PARTIAL |
| GAP-004 | Persistence | Request and consent persistence previously used local JSON-file storage and lacked structured persistence semantics. | SQLite persistence active from Phase 19. | Stronger structured persistence now exists, but still not a cloud-managed production datastore. | Low | Use SQLite as governed local persistence layer. | Replace with governed production datastore when AWS persistence phase begins. | PARTIAL |
| GAP-005 | Consent enforcement mode | Consent checks previously allowed failed requests to proceed under soft enforcement. | Hard enforcement active from Phase 18. | Consent failures now block execution. | Low | Block and persist remediation state. | Monitor and refine enforcement edge cases. | CLOSED |
| GAP-006 | Document enforcement mode | Document readiness checks previously allowed failed requests to proceed under soft enforcement. | Hard enforcement active from Phase 18. | Failed document readiness now blocks execution. | Low | Block and persist remediation state. | Monitor and refine readiness thresholds and edge cases. | CLOSED |
| GAP-007 | Document classification | Document type inference is heuristic from document ID strings, not OCR/content-backed. | Heuristic inference active. | Misclassification possible. | High | Use naming convention heuristics and surface readiness failures. | OCR/content-backed classification phase. | OPEN |
| GAP-008 | Document completeness | Completeness is not truly validated; currently inferred / assumed from simple rules. | Placeholder completeness. | Missing pages or incomplete documents may be undetected. | High | Use expected-type checks and remediation prompts. | Real completeness validation phase. | OPEN |
| GAP-009 | Document freshness | Freshness is not truly validated; currently marked `unknown`. | No real freshness logic. | Expired/stale documents may not be detected. | High | Persist freshness as unknown. | Add real freshness rules and evidence-based validation. | OPEN |
| GAP-010 | Document quality | Quality scoring is not OCR/image based; still placeholder-level. | No true quality scoring. | Poor quality inputs may pass into execution. | Medium | Surface only basic readiness outcomes. | Introduce real quality scoring / preprocessing checks. | OPEN |
| GAP-011 | Consent evidence validation | Consent evidence is checked only for presence of evidence reference, not authenticity/signature/legal proof. | Evidence metadata persisted. | False positives for “valid” evidence possible. | High | Treat evidence reference as dev placeholder only. | Signed/legal evidence validation phase. | OPEN |
| GAP-012 | Standing consent expiry testing | Lifecycle model supports expiry fields, but expiry has not been verified via time-shifted scenario tests. | Expiry fields implemented. | Expiry logic may be unproven in practice. | Medium | Persist expiry fields and evaluate current timestamps. | Add explicit expiry test scenarios. | OPEN |
| GAP-013 | Revoked consent surfaced state | After revocation, later request correctly fails but newly evaluated consent may surface as unavailable/missing rather than explicitly revoked. | Operationally correct, semantically improvable. | Revocation semantics may be under-expressed. | Medium | Note behaviour in program-state docs. | Refine surfaced-state handling for revoked consent. | OPEN |
| GAP-014 | Consent registry scope | Consent registry is local and request-store based, not cross-system or enterprise-governed. | Local JSON-based registry active. | Cannot support multi-channel or external system consent reuse. | High | Use local registry only for dev/testing. | Introduce centralised consent service / datastore. | OPEN |
| GAP-015 | Orchestration persistence model | Request lifecycle persistence is not event-driven and lacks audit-grade immutability. | Mutable JSON store. | Loss of audit trail fidelity and replay capability. | High | Store latest state only. | Introduce append-only/event-sourced persistence. | OPEN |
| GAP-016 | Idempotency | Request creation and execution are not idempotent; duplicate submissions may create duplicate executions. | No idempotency keys. | Duplicate processing and inconsistent state possible. | High | None. | Introduce idempotency keys and request deduplication. | OPEN |
| GAP-017 | Error handling model | No structured error taxonomy or failure classification across orchestration and services. | Generic success/failure only. | Poor diagnosability and inconsistent handling. | Medium | Basic status fields. | Introduce error model (codes, categories, retry flags). | OPEN |
| GAP-018 | Retry / resilience | No retry strategy, backoff, or failure recovery logic implemented. | Single-pass execution. | Transient failures will cause hard failures. | High | Manual rerun endpoint only. | Introduce controlled retry and resilience policies. | OPEN |
| GAP-019 | Observability | No metrics, tracing, or structured logging aligned to runtime stages. | Basic print/log outputs. | Limited visibility into system behaviour. | High | Manual inspection. | Add CloudWatch metrics, structured logs, tracing. | OPEN |
| GAP-020 | Security / access control | No authentication, authorization, or request-level security enforcement. | Open internal execution model. | Unauthorized access risk. | High | None (dev mode). | Introduce authN/authZ layer and request validation. | OPEN |
| GAP-021 | Data validation | Input payload validation is minimal and not schema-enforced. | Basic field checks only. | Invalid payloads may propagate downstream. | Medium | Manual validation in code. | Introduce schema validation (e.g. JSON schema). | OPEN |
| GAP-022 | API contract governance | API responses are not versioned or contract-governed. | Implicit contract via code. | Breaking changes risk for consumers. | Medium | None. | Introduce versioned API contract and schema governance. | OPEN |
| GAP-023 | Service routing governance | Service routing is code-based and static, not externally governed/configurable. | Hardcoded mapping. | Reduced flexibility and control. | Medium | Code updates. | Externalise routing configuration. | OPEN |
| GAP-024 | Execution plan integration | Execution plan is not yet fully enforced as authoritative runtime instruction object. | Execution Plan v1 is now enforced for the frontend/API orchestration path and the three frontend service-family workers. Frontend orchestration builds and persists the execution plan, propagates it downstream, workers acknowledge and validate it strictly, invalid payloads are rejected safely, and stage results plus finalization reasons are persisted. Broader pipeline-wide execution-plan enforcement remains incomplete. | Drift risk is materially reduced for the frontend/API orchestration path and its governed workers, but still exists outside that scope. | Medium | Use persisted execution plans, stage results, worker validation outputs, and finalization reasons as the runtime truth for frontend/API orchestration. | Extend governed execution-plan enforcement to the wider OCR pipeline and related runtime stages. | PARTIAL |
| GAP-025 | Decision engine AWS response shape | AWS bridge responses originally included boto3-native `datetime` objects that were not JSON-safe for persistence. | JSON-safe normalization added in `services/decision_engine/engine.py`. | Persistence blocking defect resolved for current path, but future AWS response expansions must preserve JSON-safe serialization. | Medium | Normalize AWS response excerpts before persistence. | Maintain JSON-safe response discipline for all persisted orchestration payloads. | PARTIAL |
| GAP-026 | Finalization outcome classification | Downstream worker rejection and fallback-success cases were previously not classified distinctly in finalization. | Frontend finalization now distinguishes blocked, available, rejected, and execution_failed outcomes, and persists/surfaces `finalization_reason`. | Frontend/API orchestration classification risk is materially reduced, but equivalent classification discipline is not yet enforced across the wider pipeline. | Medium | Use `finalization_reason` together with `result_status` as the governed interpretation of runtime outcome. | Extend equivalent outcome-classification governance to broader runtime flows where applicable. | PARTIAL |

| GAP-027 | Source-of-truth governance | Generated artifacts, caches, backup files, and other non-governed outputs may be mistaken for live design or runtime truth. | System governance now defines strict source-of-truth separation and artifact control in the operating baseline, the decision register now records the governing rationale, the runtime handover now reinforces interpretation control, and the governed document map now defines the controlled document stack. Cleanup discipline is still to be operationalized. | Incorrect design interpretation, implementation drift, and wasted effort. | High | Prefer governed docs and live source manually; ignore generated artifacts during analysis. | Maintain explicit source-of-truth governance across the baseline, decision register, runtime handover, governed document map, and future cleanup rules. | PARTIAL |

| GAP-028 | OCR provider control | Current OCR runtime uses an embedded Tesseract implementation as bootstrap execution, but governed provider abstraction and full execution-plan-driven provider control are not yet enforced. | Live OCR pipeline runtime is validated, but current OCR stage remains implementation-bound rather than fully provider-abstraction-controlled. | Architectural drift, provider lock-in, and hidden OCR routing behavior. | High | Treat current Tesseract runtime as bootstrap provider only and prohibit interpreting it as design truth. | Design and implement governed OCR provider abstraction, normalized provider interface, and execution-plan-driven provider selection/fallback control. | OPEN |
| GAP-029 | OCR provider interface contract enforcement | OCR provider abstraction control is now documented, but explicit plan-carried OCR instruction validation, normalized provider adapter enforcement, and governed fallback-chain execution are not yet implemented end-to-end in runtime code. | OCR worker now enforces explicit TEXT_OCR instruction presence, validates required OCR instruction fields, rejects missing or unsupported provider instructions safely, normalizes provider output structure, records governed execution metadata, and the manifest generator now emits a governed TEXT_OCR instruction block aligned to the provider-interface contract. Broader runtime support for multiple providers and governed fallback-chain execution remains incomplete. | Hidden provider defaults and unsupported-provider drift are materially reduced, but full multi-provider and governed fallback execution is still incomplete. | Medium | Use governed TEXT_OCR instruction blocks emitted by manifest generation and treat current runtime support as Tesseract-only behind the controlled interface. | Extend runtime support to governed fallback-chain execution and additional provider adapters under the normalized contract. | PARTIAL |
---

## Governance Rule

This register is **mandatory maintenance**:

- Every phase MUST:
  - update existing gaps (status change if applicable)
  - add newly discovered gaps
- No gap may remain undocumented if identified
- No feature may be treated as "complete" if related gaps remain OPEN without explicit acceptance

---

## Usage in Handover

All future developer handovers MUST:
- reference this register
- not assume missing behaviour is intentional
- treat OPEN gaps as **known incomplete system areas**

---

