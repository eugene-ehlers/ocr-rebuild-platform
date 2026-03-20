# Decision Register

## Purpose

Maintain a concise governed record of why material design and governance decisions were made.

This register exists to:
- preserve decision rationale
- prevent repeated debate on resolved design choices
- avoid accidental reversal of intentional constraints
- support controlled continuity across developers and chats

This register is not an audit log and is not intended to record activity history.

---

## Record Format

Each decision record must capture:

- Decision ID
- Title
- Status
- Date
- Decision
- Rationale
- Consequences

---

## Status Values

- `ACTIVE` — current governing decision
- `SUPERSEDED` — replaced by a later decision
- `RETIRED` — no longer applicable

---

## Decisions

### DEC-001 — Strict Source-of-Truth and Artifact Control Model

- **Status:** ACTIVE
- **Date:** 2026-03-20

#### Decision

The system shall be governed by four strictly separated layers:

1. Design Authority
2. Decision Register
3. Runtime State
4. Implementation

The following hard rules apply:

- Design Authority defines what must be built and how it must be built.
- Runtime State describes current reality only and must not redefine design.
- Implementation must not introduce behavior not explicitly defined in Design Authority.
- Decision Register captures rationale and must not override Design Authority.
- Any behavior not explicitly defined in Design Authority is invalid and must not be implemented.

Artifact control is also strict:

- Only governed documents, runtime state documents, production code, and required deployment/runtime artifacts are authoritative or required.
- `build/`, `__pycache__/`, `*.pyc`, backup files, generated packaging artifacts, and temporary/local output files are non-authoritative supporting artifacts only.
- Non-required artifacts must be ignored or removed in a controlled manner under the minimalist retention policy.

#### Rationale

The project is being developed across multiple developers and chat sessions in a production-sensitive environment. Without strict source-of-truth separation and artifact control, generated artifacts, stale backups, and undocumented assumptions can be misread as authoritative system intent, causing drift, wasted effort, and architectural inconsistency.

#### Consequences

- Design, runtime, and code must be interpreted separately and must remain aligned.
- Generated artifacts and stale files must not be used as the basis for design or runtime interpretation.
- Future handovers and implementation work must verify against governed documentation first.
- Cleanup and retention decisions must be based on governed necessity, not convenience.

### DEC-002 — Runtime Validation Must Prefer Live AWS Baseline For Integrated Pipeline Proof

- **Status:** ACTIVE
- **Date:** 2026-03-20

#### Decision

Where integrated OCR pipeline behaviour is being validated, the preferred proof point is controlled live AWS execution against the deployed Step Functions, Lambda, ECS, and S3 runtime path.

Local inspection and static code review remain necessary, but they are not sufficient on their own to claim integrated runtime success.

#### Rationale

The pipeline includes cross-service orchestration, S3 payload handoff, Step Functions control flow, Lambda execution, ECS task execution, and persisted runtime payload transitions. These cannot be treated as fully proven through local code inspection alone.

#### Consequences

- Integrated pipeline claims must be backed by controlled live AWS execution evidence.
- Runtime handover documents must distinguish validated live behaviour from design intent.
- Static code review remains supporting analysis, not integrated execution proof.

### DEC-003 — OCR Must Be Provider-Abstraction Controlled, Not Provider-Owned

- **Status:** ACTIVE
- **Date:** 2026-03-20

#### Decision

The platform shall not be treated as owning a fixed OCR engine implementation.

OCR is a governed capability invoked through a provider abstraction boundary. Current Tesseract-backed OCR is permitted only as a controlled bootstrap execution provider for runtime validation and must not be interpreted as the permanent architecture.

Provider selection, fallback, and OCR routing must move under explicit governed execution-plan control and a normalized provider interface.

#### Rationale

The approved platform design is a modular document-intelligence orchestration system, not a single-engine OCR product. Without an explicit control decision, bootstrap OCR code can easily become mistaken for the target architecture, causing provider lock-in, hidden routing logic, and drift away from the intended decision-driven model.

#### Consequences

- Tesseract remains allowed only as a bootstrap/reference provider.
- OCR provider choice must become execution-plan-driven.
- Provider-specific logic must be isolated behind a governed abstraction boundary.
- Future OCR integrations must conform to a normalized interface before being treated as valid runtime providers.

### DEC-004 — OCR Provider Execution Must Be Governed By Explicit Plan-Carried Interface Control

- **Status:** ACTIVE
- **Date:** 2026-03-20

#### Decision

OCR execution must be controlled through an explicit execution-plan OCR instruction block and a normalized provider interface contract.

No OCR worker may silently infer provider choice, silently substitute providers, or expose provider-specific raw output as the governed runtime payload model.

Fallback is allowed only when explicitly permitted in the execution plan and only through a governed fallback chain.

#### Rationale

Provider abstraction control is not sufficient unless the runtime control object and provider execution interface are both explicitly governed. Without this, hidden defaults, silent substitutions, and provider-shaped payloads can reintroduce provider lock-in and architectural drift even when higher-level design documents prohibit it.

#### Consequences

- OCR workers must validate provider instruction completeness before execution.
- Unsupported or incomplete OCR instructions must be rejected safely.
- Fallback behavior must be explicit, traceable, and plan-driven.
- OCR provider adapters must normalize output into the governed page-level payload model.

