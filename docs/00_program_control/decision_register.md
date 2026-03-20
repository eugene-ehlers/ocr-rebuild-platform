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
