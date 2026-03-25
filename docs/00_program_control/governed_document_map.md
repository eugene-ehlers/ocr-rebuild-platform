# Governed Document Map

## Purpose

Define the controlled document classes for this project, the purpose of each class, the authoritative files currently used, and the storage expectation for each class.

This map exists to ensure that:
- all contributors use the same document stack
- design authority is not confused with runtime state
- progress is recorded in governed locations only
- unnecessary artifacts do not become pseudo-documentation

---

## Document Classes

### 1. Design Authority

Defines what must be built and how it must be built.

Current governed files include:
- `docs/00_program_control/document_intelligence_operating_baseline.md`
- `docs/00_program_control/known_gaps_and_improvement_register.md`
- approved architecture, data model, AWS environment, and SOP documents under `docs/`

Storage expectation:
- GitHub: required
- S3: required governed backup/reference copy

---

### 2. Decision Register

Defines why material design and governance decisions were made.

Current governed files include:
- `docs/00_program_control/decision_register.md`

Storage expectation:
- GitHub: required
- S3: required governed backup/reference copy

---

### 3. Runtime State

Defines what currently exists, what is currently enforced, and what safe boundaries currently apply.

Current governed files include:
- `docs/20_service_design/frontend_api_phase21_runtime_handover_v1.md`

Storage expectation:
- GitHub: required
- S3: required governed backup/reference copy

---

### 4. Implementation

Defines the executable system and deployable implementation.

Current governed locations include:
- `services/`
- `api/`
- `infrastructure/`

Storage expectation:
- GitHub: required
- S3: not required as a parallel governed document store unless specifically needed for deployment or release packaging

---

## Progress Recording Rules

Further progress must be saved only in governed locations:

- design changes -> Design Authority documents
- rationale for material choices -> Decision Register
- current implemented state and safe boundaries -> Runtime State
- executable changes -> Implementation

Progress must not be recorded through:
- ad hoc notes
- generated artifacts
- build outputs
- backup files
- temporary files

---

## Storage Rules

### Governed documents
The following document classes must be retained in both:
- GitHub
- S3

Required classes:
- Design Authority
- Decision Register
- Runtime State

### Code
Implementation code must be retained in:
- GitHub

Additional storage beyond GitHub is optional unless required by deployment, release, or operational packaging needs.

---

## Minimal Retention Rule

The project does not retain documentation or artifacts purely to show activity volume or historical busyness.

Only the following are governed and worth retaining:
- what must be built
- why key decisions were made
- what currently exists
- the executable implementation
- required rollback or recovery material

Everything else must be ignored or removed in a controlled manner.

---

## Change Management Rule

Any material project change must update the relevant governed class at the time the change is made:

- Design Authority if the target state or rules changed
- Decision Register if a material option was selected
- Runtime State if the safe current-state interpretation changed
- Implementation if executable behavior changed

No material change is complete until the relevant governed documentation is aligned.

---

## Phase Closure Alignment — Multi-Period Substrate Authority

The following document and section are now **authoritative Design Authority sources** for the financial-management multi-period substrate:

- `docs/20_service_design/financial_management_payloads_v1.md` — Section 9

This section is the governed authority for:

- `prior_statement_history`
- `period_groupings`
- `trend_metrics`
- `missing_period_flags`
- `exclusion_flags`
- `multi_period_requirement_signal`

Interpretation constraints:

- These constructs are **baseline-defined and implemented**.
- No interpretation may treat them as optional, missing, or future-state.
- All service rule tables and runtime behaviour must align to this contract.

## Phase Closure Alignment — FM-OTC-002 Controlled Exposure Authority

The following governed files now jointly define the approved documentation baseline for current FM-OTC-002 exposure under Option A:

- `docs/00_program_control/decision_register.md`
- `docs/20_service_design/frontend_api_phase21_runtime_handover_v1.md`
- `docs/20_service_design/financial_management_input_to_outcome_rule_table_v1.md`

Interpretation constraints:

- current controlled request selector is `analysis_type`
- `analysis_type=explain_document` selects FM-OTC-001
- `analysis_type=cash_flow_multi_period` selects FM-OTC-002
- omitted `analysis_type` defaults to FM-OTC-001
- runtime selection must remain mutually exclusive
- exactly one outward governed Financial Management outcome may be emitted
- insufficient multi-period basis for FM-OTC-002 must fail closed

