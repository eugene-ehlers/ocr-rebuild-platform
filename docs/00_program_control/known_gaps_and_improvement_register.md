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
| GAP-029 | OCR provider interface contract enforcement | OCR provider abstraction control is now documented, but explicit plan-carried OCR instruction validation, normalized provider adapter enforcement, and governed fallback-chain execution required end-to-end runtime proof. | OCR worker now enforces explicit TEXT_OCR instruction presence, validates required OCR instruction fields, rejects missing or unsupported provider instructions safely, normalizes provider output structure, records governed execution metadata, the manifest generator now emits a governed TEXT_OCR instruction block aligned to the provider-interface contract, OCR payloads now record attempted provider-chain and fallback traceability, a governed AWS Textract adapter baseline now exists behind the provider registry, fallback-chain iteration now safely continues to later governed providers when an earlier provider is invalid, not runtime-enabled, or execution-fails, Gate 2 truth propagation now preserves execution truth correctly, and live AWS governed fallback execution is proven end to end with controlled primary failure followed by successful Textract fallback. attempted_provider_chain, fallback_used, and fallback_provider are now correct through final payload completion for the baseline OCR governed fallback path. | Hidden provider defaults, unsupported-provider drift, and downstream continuation after failed OCR quality gate are materially reduced for the baseline OCR governed fallback path. Future providers still require independent proof. | Medium | Use governed TEXT_OCR instruction blocks emitted by manifest generation and treat current runtime support as Tesseract-primary with Textract adapter available when explicitly runtime-enabled under governed execution control. | Extend provider adapters under the normalized contract and require independent live proof for each future governed provider path. | CLOSED (baseline OCR governed fallback path proven) |
---
| GAP-030 | Service rule table governance | Service rule table completion introduced identifier collisions and misplaced end-of-document markers in capability-to-provider mappings during controlled table expansion. | Financial Management, FICA, and Credit service rule tables are now structurally completed for the current design scope; duplicate/incorrect capability-provider identifiers and misplaced end markers were corrected and sequential numbering was restored. Controlled vocabulary persistence outside these table artifacts remains incomplete. | Medium | Medium | Use the corrected governed markdown tables in docs/20_service_design as the only current design truth and validate identifiers before future table expansion. | Maintain identifier validation and controlled-vocabulary registry alignment during future table changes; add automated duplicate-ID and end-marker checks to governed document validation. | PARTIAL |

| GAP-031 | Runtime-to-contract alignment | Governed affordability runtime executes successfully through execution, transformation, and validation, but the resulting transformed payload still does not satisfy authoritative CREDIT-OTC-002 contract requirements. Missing required outputs include affordability_status, manual_review, affordability_score, affordability_risk_flags, affordability_metrics, affordability_summary, next_step_guidance, and overall_confidence; missing required data dependencies include parsed_transactions, classified_transactions, cash_flow_summary, and debt_positions. | Transformation Layer v1 and Validation Runtime v1 now expose this mismatch explicitly and produce a governed fail correctly, without inference or fabricated values. Current investigation indicates this gap is not isolated and reflects broader shared dependency incompleteness in a reusable financial-analysis substrate affecting multiple service families. Candidate execution-plan work (v2) demonstrates structural substrate insertion direction only and does not yet constitute full semantic remediation. | Service outcome cannot yet pass governed validation even though runtime execution is functioning correctly. | High | Use the governed fail artifacts, transformation notes, validation runtime notes, system audit summary, and candidate execution-plan v2 review note as the authoritative interpretation of current behaviour. | Introduce a controlled remediation path: either extend governed execution outputs, add an approved governed decision component that produces the missing contract fields, formalize and integrate a shared execution-layer financial-analysis substrate, or formally revise the service contract if business requirements change. | OPEN |

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


---

## Phase Closure Alignment — Multi-Period Substrate

- The multi-period financial-analysis substrate contract is now **defined and implemented as part of the governed baseline**.
- Authoritative definition: `docs/20_service_design/financial_management_payloads_v1.md` (Section 9).

Interpretation constraints:

- No new gap is introduced for the multi-period substrate.
- GAP-031 MUST be interpreted as:
  - a **contract-to-capability alignment gap (CREDIT-OTC-002)**,
  - NOT a missing substrate capability gap.
- The following governed constructs are **present and baseline-complete** and must not be treated as missing:
  - `prior_statement_history`
  - `period_groupings`
  - `trend_metrics`
  - `missing_period_flags`
  - `exclusion_flags`
  - `multi_period_requirement_signal`


### Frontend UX Misalignment (DOI)

**Description**  
The current frontend operates as a Developer / Operational Interface (DOI) and is not aligned with the approved frontend customer experience design baseline.

**Impact**  
High — leads to:
- user confusion  
- incorrect input handling  
- inability to execute realistic user journeys  
- inability to perform valid end-to-end testing  

**Reference**  
docs/00_program_control/evidence/FE_GAP_ANALYSIS_20260401_step02_dimension_evidence.txt

**Priority**  
Critical

| GAP-frontend-release-promotion-origin | Frontend release promotion origin alignment | Governed frontend safety model now requires immutable releases and `current/` promotion, but CloudFront still serves bucket root rather than `current/`. | Current live sites remain stable, S3 versioning is enabled, and governed docs now prohibit destructive live-root deployment. | Until origin/path is aligned to `current/`, the full immutable promotion model is documented but not yet active at runtime. | High | Partial | Implement controlled CloudFront origin/path alignment to `current/` without breaking restored live sites; add release metadata exposure and controlled promotion procedure. | OPEN |


| GAP-035 | Builder payload handoff | Builder output was not being handed to downstream execution correctly | Builder output is now created before _execute(...) and used consistently for downstream handoff with manifest_id and document continuity | Frontend/API path aligned to runtime truth | Low | Builder output is authoritative downstream handoff payload | Extend consistency checks across broader pipeline | CLOSED |


---

### GAP — STRUCTURED BANK STATEMENT RECONSTRUCTION SERVICE

**Gap ID:** GAP-NEW-FIN-STRUCT-RECON  
**Category:** Functional Capability Gap  
**Service Domain:** Financial Services  

**Description:**
There is currently no evidenced service that converts OCR-extracted bank statement data into a structured electronic financial representation (e.g. transactions, balances, statement periods).

**Required Capability:**
A governed sub-service under financial services that:
- consumes OCR output (`pages`, `extracted_text`)
- reconstructs:
  - transactions
  - statement period (start/end)
  - balances
  - structured financial signals
- outputs standardized structured bank statement substrate

**Explicit Boundary:**
- NOT part of `serviceCode: "ocr"`
- MUST exist as separate service (e.g. financial_management or new sub-service)

**Current Runtime Evidence:**
- OCR produces only:
  - pages
  - extracted_text
- No structured financial parsing present in OCR worker
- Credit decision expects structured financial inputs but relies on downstream logic

**Impact:**
- Frontend must not assume structured financial outputs from OCR
- Credit decision may reject due to missing structured data
- Limits end-to-end financial decision capability

**Required Outcome:**
Introduce governed structured extraction service aligned to architecture and workflow model.

Resolution:
This gap has been resolved with the implementation of FM-OTC-007 under financial_management (analysis_type = reconstruct_bank_statement).

**Status:** CLOSED

---

## Model lineage persistence — Delivered

Status:
Delivered in current runtime development state

Details:
- Decision Engine stamps selected lineage for reconstruction, classification, and scoring
- Runtime execution derives executed lineage from downstream outputs
- OCR is recorded as executed metadata only
- Single JSON structure used for lineage persistence

Remaining gaps:
- broader multi-model continuity fallback scenarios still need runtime hardening and wider validation

## Structured bank statement reconstruction subservice — Delivered

Status:
Delivered in current runtime development state

Details:
- financial_management now supports analysis_type = reconstruct_bank_statement
- governed outcome = FM-OTC-007
- returns structured_bank_statement with:
  - transactions
  - transaction_count
  - statement_period_start
  - statement_period_end

Disposition:
Available through governed Decision Engine orchestration as a financial-management subservice.
