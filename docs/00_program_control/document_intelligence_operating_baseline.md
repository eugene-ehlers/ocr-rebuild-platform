# OCR Rebuild — Document Intelligence Operating Baseline

Status: CONTROL DOCUMENT — AUTHORITATIVE BASELINE

## 1. Purpose

This document defines the authoritative operating model for the OCR Rebuild platform.

It is the required entry point for:
- all developers
- all future chats
- all architectural or implementation decisions

It exists to ensure:
- the platform is built as a **document intelligence system**, not a linear OCR pipeline
- all components align to a single model
- no uncontrolled implementation drift occurs
- future optimisation, substitution, and expansion are enabled from the start

---

## 2. What We Are Building

The platform is:

> A modular, decision-driven document intelligence system that composes services from atomic capabilities and dynamically selects execution paths using a staged decision ecosystem.

It is NOT:
- a fixed OCR pipeline
- a single-model solution
- a static product implementation

---

## 3. Core Operating Principles

### 3.1 Service composition, not fixed products
- Clients request outcomes
- Services are assembled dynamically
- Services are decomposed into capabilities

### 3.2 Capability-driven architecture
- All functionality is built from atomic capabilities
- Capabilities are reusable
- Capabilities are provider-agnostic

### 3.3 Decision-driven execution
- Execution is controlled by decision engines
- Decisions occur at defined gates
- Decisions can change as new evidence emerges

### 3.4 Hybrid provider strategy
- External services are used first for speed and quality
- Internal modules replace them over time
- All providers are accessed via API-compatible interfaces

### 3.5 Execution plan as control object
- The execution_plan is the authoritative runtime instruction
- All routing, fallback, and provider selection must be recorded there
- No hidden decisions outside the plan are allowed

### 3.5A OCR provider abstraction control
- OCR is a provider-agnostic capability, not a hard-coded product implementation
- OCR provider selection must occur through governed abstraction boundaries
- Bootstrap OCR implementations may exist for controlled runtime validation, but they must not become design truth
- No stage may hard-code provider-specific behavior as permanent architecture

### 3.6 Full traceability
- routing_decision must summarise execution path
- evaluation must capture quality and completeness
- manifest_update must capture lifecycle and history

---

## 4. Authoritative Document Set (Read Order)


### OCR provider abstraction control
`docs/05_ocr_engines/ocr_provider_abstraction_control.md`

Defines:
- provider abstraction boundary
- bootstrap-vs-design distinction
- control rules for OCR provider selection and fallback

---


All developers must read and adhere to the following in order:

### 1. Service Composition
`docs/01_architecture/service_composition_model.md`

Defines:
- how services are constructed
- how client requests map to capabilities

---

### 2. Capability Registry
`docs/01_architecture/capability_registry_provider_map.md`

Defines:
- atomic capabilities
- provider options
- bundling considerations
- internalisation roadmap

---

### 3. Decision Ecosystem
`docs/01_architecture/decision_ecosystem_and_gate_specification.md`

Defines:
- Gate 0–4 structure
- decision responsibilities
- re-decision model

---

### 4. Execution Plan Contract
`docs/03_data_model/execution_plan_contract.md`

Defines:
- execution_plan structure
- capability_plan
- fallback rules
- gate history

---

### 5. Pipeline Integration
`docs/03_data_model/execution_plan_pipeline_integration_spec.md`

Defines:
- how execution_plan is embedded in runtime payload
- how stages must behave
- preservation rules

---

### 6. Responsibility Mapping
`docs/02_aws_environment/decision_and_runtime_responsibility_mapping.md`

Defines:
- who does what
- separation between decisioning and execution
- AWS component responsibilities

---

### 7. Decision Invocation Placement
`docs/02_aws_environment/decision_engine_invocation_and_placement.md`

Defines:
- where each gate runs
- when each decision engine is invoked
- how Step Functions must call them

---

### 8. Decision Rules (v1)
`docs/02_aws_environment/decision_engine_rule_placeholders_v1.md`

Defines:
- initial rule logic
- placeholder scorecards
- minimum decision outputs

---

## 5. End-to-End Flow (Authoritative Model)

1. Client request received  
2. Gate 0 → service composition  
3. Gate 1 → execution plan creation  
4. Runtime execution begins  
5. OCR / extraction performed  
6. Gate 2 → quality + fallback decisions  
7. Enrichment executed  
8. Gate 3 → service sufficiency decision  
9. Aggregation  
10. Gate 4 → final validation  
11. Delivery + traceability preserved  

---

## 6. What Must NEVER Happen

The following are strictly prohibited:

### 6.1 No logic in workers
Workers must:
- execute capabilities
- NOT make routing decisions

---

### 6.2 No hidden provider decisions
All provider choices must:
- be defined in execution_plan
- be traceable

---

### 6.3 No linear pipeline shortcuts
The system must:
- respect decision gates
- allow re-routing and loops

---

### 6.4 No breaking the payload contract
All stages must preserve:
- execution_plan
- routing_decision
- evaluation
- manifest_update

---

### 6.5 No fixed product pipelines
Services must:
- be composed dynamically
- not hard-coded end-to-end

---

## 7. Current Implementation State (Baseline)

The platform currently operates with:

- rule-based decision engines (v1)
- limited provider set (Tesseract, Textract, placeholders)
- simple thresholds
- partial capability coverage

This is intentional.

The structure is designed for:
- future optimisation
- provider substitution
- model upgrades
- cost vs accuracy trade-offs

---

## 8. Next Implementation Priorities

### Priority 1 — Enforce execution_plan in runtime
- OCR worker must read from capability_plan
- no hardcoded provider logic

### Priority 2 — Implement Gate 2 (quality loop)
- OCR evaluation
- fallback trigger

### Priority 3 — Implement Gate 3 (service sufficiency)
- enforce minimum_output_requirements

### Priority 4 — Populate evaluation and routing_decision
- even if simple
- must always exist

### Priority 5 — Enable loop control
- page-level reroute
- bounded retry logic

---

## 9. How This Evolves

This system is designed to evolve by:

- replacing rule logic with models
- adding optimisation layers
- introducing champion/challenger strategies
- refining scorecards
- expanding capability coverage

WITHOUT:
- redesigning the architecture
- breaking contracts
- rewriting pipelines

---

## 10. Success Criteria

This baseline is successful when:

- services are composed, not hardcoded
- execution paths are dynamic and traceable
- decisions are made at gates, not inside workers
- execution_plan controls runtime behaviour
- new providers can be added without redesign
- optimisation can be introduced without refactoring core architecture

---

## 11. Final Instruction

All future work must align with this document.

If any implementation conflicts with:
- execution_plan
- decision gates
- capability model

Then:
- the implementation is incorrect
- the document must be consulted before proceeding


---

## System Governance — Source of Truth & Artifact Control

This system operates under strict documentation and artifact governance to ensure consistency, prevent drift, and enable coordinated development across multiple developers and environments.

---

### 1. System Layers (Authoritative Separation)

The system is governed by four strictly separated layers:

#### 1.1 Design Authority (CONTROL)

Defines what must be built and how it must be built.

Includes:
- architecture
- execution model (including execution plan design)
- service boundaries
- SOPs
- allowed technology stack
- governance rules
- gap register

This is the highest authority in the system.

---

#### 1.2 Decision Register (RATIONALE)

Captures why specific design decisions were made at a given point in time.

Includes:
- selected option
- brief rationale
- relevant constraints

Purpose:
- prevent rework
- prevent re-debate of resolved decisions
- preserve intent behind design choices

Decision records support Design Authority but do not override it.

---

#### 1.3 Runtime State (CURRENT TRUTH)

Describes what currently exists in the system.

Includes:
- what is implemented
- what is not implemented
- current enforcement scope
- current safe operational boundaries

Runtime State is descriptive only and must not introduce or redefine design.

---

#### 1.4 Implementation (EXECUTION)

Represents the executable system.

Includes:
- application code
- infrastructure definitions (including Step Functions, ECS, Lambda, etc.)
- deployment configurations
- required runtime artifacts

Implementation must strictly conform to Design Authority.

---

### 2. Hard Separation Rules (Non-Negotiable)

The following rules are strictly enforced:

- Design Authority must not describe temporary runtime behavior.
- Runtime State must not introduce or redefine design.
- Implementation must not introduce behavior not defined in Design Authority.
- Decision Register must not be used to bypass or override Design Authority.

---

### 3. Critical Rule — Design Authority Enforcement

Any behavior not explicitly defined in Design Authority is invalid and must not be implemented.

This applies to:
- new features
- modifications
- interpretations of existing behavior

No implicit or assumed behavior is permitted.

---

### 4. Artifact Classification (Strict Control)

Only the following artifacts are considered valid and governed:

#### Allowed (Authoritative or Required)

- Design documents under docs/
- Runtime state documents
- Decision register entries
- Production code under:
  - services/
  - api/
  - infrastructure/
- Required deployment and runtime artifacts

---

#### Non-Authoritative (Must Not Be Used for Design or Interpretation)

The following are strictly classified as supporting artifacts only:

- build/ directory contents
- __pycache__/
- compiled files (*.pyc)
- backup files:
  - *.bak
  - *.pre_contract_preservation
  - timestamped backup files
- generated packaging artifacts
- temporary or local output files

These may be used for:
- debugging
- controlled investigation

They must NOT be used for:
- design decisions
- runtime interpretation
- defining system behavior

---

### 5. Artifact Retention Policy (Minimalist Enforcement)

The system follows a strict minimal-retention model:

- Only artifacts required for:
  - execution
  - deployment
  - reproducibility
  are retained.

- All non-required artifacts must be:
  - ignored, or
  - removed in a controlled manner.

- Historical clutter, duplicate artifacts, and unused outputs are not permitted.

---

### 6. Operational Enforcement

All developers, systems, and automated processes must:

- verify behavior against Design Authority before any change
- ignore non-authoritative artifacts during analysis
- avoid deriving behavior from generated or cached files
- maintain strict alignment between design, runtime state, and implementation

---

### 7. Conflict Resolution

In any conflict:

1. Design Authority is the source of truth
2. Runtime State reflects current system condition only
3. Implementation must be corrected to align with Design Authority
4. Supporting artifacts must be ignored for decision-making

---

### 8. Governance Intent

This structure exists to:

- eliminate ambiguity
- prevent architectural drift
- ensure consistent development across contributors
- maintain a clean, controlled, and scalable system

Deviation from these rules is not permitted.

## Governed Document Stack

The project operates with the following controlled document classes:

- Design Authority
- Decision Register
- Runtime State
- Implementation

The governed file-to-class mapping is maintained in:

- `docs/00_program_control/governed_document_map.md`

This mapping is mandatory and must be kept aligned as the document stack evolves.

