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

### 3.6 Full traceability
- routing_decision must summarise execution path
- evaluation must capture quality and completeness
- manifest_update must capture lifecycle and history

---

## 4. Authoritative Document Set (Read Order)

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

