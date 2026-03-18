# OCR Rebuild — Decision Ecosystem and Gate Specification

Status: DRAFT - DECISION ORCHESTRATION BASELINE

## 1. Purpose

Define the governed decision ecosystem for OCR Rebuild so that:

- client requests are translated into executable service plans
- execution plans are refined as new evidence becomes available
- provider and capability choices can change at controlled gates
- fallback, reprocessing, escalation, and completion decisions are made consistently
- future optimisation, champion-challenger testing, and advanced decision engines can be added without redesign

This document is authoritative for:
- fixed gate structure
- decision engine responsibilities
- execution plan evolution
- gate inputs and outputs
- re-decision rules
- staged optimisation readiness

## 2. Core Principle

The platform must not operate as a single linear pipeline with one routing decision at the start.

Instead, it must operate as a staged decision ecosystem in which:
- each phase produces new information
- each gate evaluates whether decisions remain valid
- plans may be accepted, refined, partially rerouted, escalated, or looped back
- services are fulfilled through capability composition, not fixed product-specific pipelines

## 3. Decision Ecosystem Overview

The platform uses fixed standard gates.

Not every service uses every gate with the same intensity, but the gate framework remains standard.

The standard decision sequence is:

- Gate 0 — Request Interpretation and Service Assembly (Decision Engine 0)
- Gate 1 — Document Understanding and Initial Execution Planning (Decision Engine 1)
- Gate 2 — Extraction Quality and Fallback Decision (Decision Engine 2)
- Gate 3 — Service Sufficiency and Enrichment Decision (Decision Engine 3)
- Gate 4 — Final Validation and Delivery Decision (Decision Engine 4)

## 4. Decision Ecosystem Layers

The decision ecosystem sits between service composition and runtime execution.

The layers are:

### 4.1 Service composition layer
Determines:
- what service is being requested
- what client outcome is required
- what capabilities are required

### 4.2 Decision ecosystem layer
Determines:
- which gates are relevant
- how execution plans are assembled and revised
- which providers/modules fulfill required capabilities
- whether to reprocess, enrich, escalate, or stop

### 4.3 Runtime execution layer
Carries out the plan through:
- Step Functions
- Lambda
- ECS workers
- internal modules
- external providers

## 5. Fixed Gate Model

## 5.1 Gate 0 — Request Interpretation and Service Assembly (Decision Engine 0)

### Purpose
Interpret the client request and convert it into a structured service requirement set.

### Inputs
- client request
- requested service(s)
- client metadata
- SLA/cost sensitivity where available
- explicit client constraints where available

### Outputs
- selected service definition
- required sub-services
- required capabilities
- optional capabilities
- minimum output requirements
- relevant gate set
- initial service-level constraints

### Typical decisions
- what service is being requested
- whether the request maps to one or multiple services
- what minimum capability set is required
- whether the request is supported, partially supported, or unsupported

### Typical decision states
- ACCEPT_REQUEST
- ACCEPT_WITH_LIMITATIONS
- REQUIRE_CLARIFICATION
- REJECT_UNSUPPORTED

### Notes
This gate does not choose providers.
It defines what must be delivered.

## 5.2 Gate 1 — Document Understanding and Initial Execution Planning (Decision Engine 1)

### Purpose
Refine the request using early document evidence and produce the initial execution plan.

### Inputs
- Gate 0 output
- source metadata
- file type
- page count
- lightweight document analysis
- initial classification signals
- initial layout or quality signals where available

### Outputs
- initial execution plan
- required providers/modules by capability
- initial route per document and page where needed
- bundled capability reuse opportunities
- gate-specific thresholds
- initial fallback allowances

### Typical decisions
- which capabilities are actually needed after inspecting document characteristics
- whether to split by document/page
- whether a bundled provider is advantageous
- whether some capabilities can be deferred until later gates
- whether some capabilities should go directly to external providers

### Typical decision states
- PLAN_ACCEPTED
- PLAN_ACCEPTED_WITH_MONITORING
- PLAN_REQUIRES_HIGH_RISK_FLAG
- PLAN_REQUIRES_CLIENT_CONSTRAINT_EXCEPTION

### Notes
This is the first provider-aware decision point.

## 5.3 Gate 2 — Extraction Quality and Fallback Decision (Decision Engine 2)

### Purpose
Evaluate primary extraction results and decide whether they are sufficient or whether partial/full rerouting is required.

### Inputs
- OCR results
- extraction confidence
- completeness indicators
- detected capability outputs
- page-level and document-level quality signals
- expected outputs from Gate 1 plan

### Outputs
- accepted outputs
- adjusted execution plan
- fallback decisions
- page-level reroute decisions
- provider escalation decisions
- retry or reprocessing decisions

### Typical decisions
- accept primary OCR result
- rerun specific pages
- escalate specific capabilities to external provider
- continue without reroute
- mark some outputs partial
- stop if quality is fundamentally insufficient

### Typical decision states
- ACCEPT_PRIMARY_RESULT
- REPROCESS_INTERNAL
- ESCALATE_EXTERNAL
- PARTIAL_ACCEPT
- FAIL_QUALITY_GATE

### Notes
This is the most critical quality-control gate.

## 5.4 Gate 3 — Service Sufficiency and Enrichment Decision (Decision Engine 3)

### Purpose
Determine whether the available outputs are sufficient to fulfill the requested service outcome, or whether additional enrichment is required.

### Inputs
- accepted extraction outputs
- enrichment outputs already available
- minimum output requirements from Gate 0
- capability completion status
- service-specific rules

### Outputs
- sufficiency decision
- additional enrichment plan
- service-level missing requirements
- optional escalation or client interaction indicators
- updated execution plan

### Typical decisions
- service is already sufficient
- additional capability required
- external validation required
- downstream QA support can proceed
- service can only be returned partially

### Typical decision states
- SERVICE_READY
- ENRICHMENT_REQUIRED
- EXTERNAL_VALIDATION_REQUIRED
- PARTIAL_SERVICE_ONLY
- FAIL_SERVICE_SUFFICIENCY

### Notes
This gate is outcome-oriented, not extraction-oriented.

## 5.5 Gate 4 — Final Validation and Delivery Decision (Decision Engine 4)

### Purpose
Make the final decision about whether the service output can be delivered, must be qualified, or must be escalated.

### Inputs
- final assembled outputs
- confidence and completeness summaries
- service sufficiency result
- authenticity/fraud summaries where relevant
- client constraints
- delivery rules

### Outputs
- final accepted output package
- delivery qualification metadata
- final service status
- escalation markers
- evaluation summary
- closed execution plan

### Typical decisions
- deliver as complete
- deliver as partial
- hold for escalation
- mark unsupported
- return with qualification note

### Typical decision states
- FINAL_ACCEPT
- FINAL_ACCEPT_PARTIAL
- FINAL_ACCEPT_WITH_QUALIFICATION
- ESCALATE
- FINAL_REJECT

### Notes
This gate produces the final governed delivery state.

## 6. Execution Plan Evolution

Execution planning is not static.

The plan evolves through the gates as follows:

- service requirement set
- initial execution plan
- refined execution plan
- adjusted execution plan
- final execution plan

### 6.1 Service requirement set
Produced at Gate 0.
Defines what must be delivered.

### 6.2 Initial execution plan
Produced at Gate 1.
Defines initial provider/module choices.

### 6.3 Refined execution plan
Produced when Gate 2 or Gate 3 changes capability/provider choices.

### 6.4 Adjusted execution plan
Used when page-level or capability-level rerouting occurs.

### 6.5 Final execution plan
Recorded at Gate 4 as the accepted path used for delivery.

## 7. Re-decision Rules

A gate may only trigger re-decision if materially new information exists.

Examples of valid re-decision triggers:
- low OCR quality
- missing structured fields
- unexpected handwriting
- unexpected table density
- authenticity risk
- failure of a selected provider/module
- bundled provider output making another call unnecessary

Examples of invalid re-decision triggers:
- arbitrary plan change without new information
- provider preference change without measurable reason
- ad hoc duplication of already obtained bundled outputs

## 8. Looping and Re-entry

The platform must support controlled loops.

### 8.1 Gate 2 loop
Example:
- OCR result insufficient
- reroute selected pages
- re-enter extraction
- return to Gate 2

### 8.2 Gate 3 loop
Example:
- service still missing required outputs
- run additional enrichment capability
- return to Gate 3

### 8.3 Escalation path
Example:
- service still insufficient after allowed loops
- mark for external validation or future client/human escalation

Looping must be:
- bounded
- traceable
- capability-specific where possible
- not a full restart unless required

## 9. Decision Engine Responsibilities

## 9.1 Decision Engine 0
Responsible for:
- request interpretation
- service selection
- capability requirement definition

Does not:
- choose providers
- run quality evaluation

## 9.2 Decision Engine 1
Responsible for:
- initial provider-aware planning
- bundled capability awareness
- route definition

Does not:
- decide final quality acceptance

## 9.3 Decision Engine 2
Responsible for:
- extraction quality evaluation
- fallback and reroute decisions
- internal vs external escalation

## 9.4 Decision Engine 3
Responsible for:
- service sufficiency evaluation
- enrichment requirement decisions
- service-level completion checks

## 9.5 Decision Engine 4
Responsible for:
- final acceptance
- qualified delivery
- final escalation status

## 10. Scorecards and Rule Sets

Each decision engine must have its own scorecards/rules.

These may begin as placeholders or simple rule sets, but the structure must exist from day one.

Each gate should support:
- scorecards
- thresholds
- rule outcomes
- decision reasons
- future champion/challenger variants

## 10.1 Placeholder scorecards
Initially, some scorecards may:
- treat all providers equally
- use coarse thresholds
- act as pass-through logic

This is acceptable if:
- the gate exists
- the input/output structure exists
- the decision record exists

## 10.2 Future scorecard evolution
Future evolution may include:
- weighted scorecards
- solver-backed optimisation
- learned decision models
- champion/challenger testing
- client-specific decision policies

## 11. Champion-Challenger Readiness

The decision ecosystem must support future champion-challenger behaviour.

This means the design must allow:
- multiple candidate strategies at a gate
- alternative plans being recorded
- controlled sampling of challenger strategies
- comparison of outcomes across strategies

This does not require full implementation now, but the model must support it.

## 12. Standard Decision Record

Each gate should produce a decision record containing at minimum:
- gate_id
- gate_name
- decision_engine_id
- input_summary
- selected_decision
- decision_reason
- scorecard_or_rule_reference
- plan_before
- plan_after
- timestamp

## 13. Standard Execution Plan Structure

The execution plan should support:
- service_id
- required_capabilities
- optional_capabilities
- capability_plan
- bundled_provider_usage
- fallback_policy
- page_overrides
- document_overrides
- decision_gate_history
- final_status

The detailed execution plan contract may be specified separately.

## 14. Service-to-Gate Usage Rule

All services use the fixed gate framework, but not all gates carry equal weight.

Examples:
- Basic OCR may rely mainly on Gates 0, 1, 2, and 4
- Will validation may rely heavily on all five gates
- Fraud document packs may use Gate 3 more intensively because service sufficiency depends on multiple evidence types

## 15. Runtime Mapping Principle

The decision ecosystem must map cleanly into runtime components.

Illustrative mapping:
- Gate 0 may be implemented in service composition logic
- Gate 1 may be implemented in orchestration planning logic
- Gate 2 may be implemented after OCR/extraction quality analysis
- Gate 3 may be implemented after enrichment aggregation
- Gate 4 may be implemented in final aggregation/delivery validation

This runtime mapping may evolve without changing the gate model.

## 16. Strategic Outcome

This specification is successful when:
- the platform no longer behaves as a single static pipeline
- service composition and execution planning are separated
- provider selection can change as evidence increases
- capability rerouting is possible without redesign
- optimisation can be introduced progressively
- every future developer can build toward the same staged decision ecosystem
