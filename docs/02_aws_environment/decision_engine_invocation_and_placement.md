# OCR Rebuild — Decision Engine Invocation and Placement

Status: DRAFT - PIPELINE INVOCATION BASELINE

## 1. Purpose

Define where each decision engine is invoked in the runtime pipeline, what it reads, what it writes, and how it fits into the current AWS implementation pattern.

This document is authoritative for:
- invocation points for Decision Engine 0 to 4
- gate placement relative to Step Functions and runtime stages
- read/write payload responsibilities at each gate
- initial implementation pattern for decision engines
- future separation of decision engines into dedicated services without redesign

This document exists to prevent:
- decision logic being embedded ad hoc in workers
- ambiguity about where gate decisions happen
- mismatches between architecture and Step Functions implementation
- loss of execution-plan discipline during implementation

## 2. Core Principle

The decision ecosystem uses fixed standard gates, but not every gate needs to be a separate physical service in the first implementation.

For the controlled baseline:
- logical gate boundaries must exist
- invocation points must be explicit
- input/output responsibility must be explicit
- future extraction into dedicated services must be possible without redesign

## 3. Standard Gate Set

The fixed gate model is:

- Gate 0 — Request Interpretation and Service Assembly (Decision Engine 0)
- Gate 1 — Document Understanding and Initial Execution Planning (Decision Engine 1)
- Gate 2 — Extraction Quality and Fallback Decision (Decision Engine 2)
- Gate 3 — Service Sufficiency and Enrichment Decision (Decision Engine 3)
- Gate 4 — Final Validation and Delivery Decision (Decision Engine 4)

## 4. Pipeline Placement Overview

The intended high-level placement is:

- before manifest generation: Gate 0
- after early document understanding / before major execution: Gate 1
- after OCR / primary extraction: Gate 2
- after enrichment / before final assembly: Gate 3
- after aggregation / before final delivery state: Gate 4

## 5. Invocation Model by Gate

## 5.1 Gate 0 — Request Interpretation and Service Assembly (Decision Engine 0)

### Placement
Before the runtime pipeline begins, or at the very start of orchestration before GenerateManifest.

### Trigger
- client submits request
- upstream system initiates service execution
- service request is transformed into execution scope

### Reads
- client request
- service request metadata
- explicit client constraints
- client-selected service if provided
- default service composition rules

### Writes
- service selection
- required capabilities
- optional capabilities
- minimum output requirements
- relevant gates
- initial execution plan seed

### Output target
Embedded into the pipeline payload before or during GenerateManifest.

### Initial implementation pattern
May initially be implemented as:
- orchestration-adjacent service composition logic
- request interpretation Lambda
- lightweight rule block at the start of orchestration

### Long-term implementation pattern
Can become a dedicated service composition / request interpretation engine.

## 5.2 Gate 1 — Document Understanding and Initial Execution Planning (Decision Engine 1)

### Placement
After initial request interpretation and early document understanding, before heavy extraction stages execute.

### Trigger
- manifest exists
- source metadata available
- lightweight document characteristics available
- initial normalization/classification evidence available

### Reads
- embedded execution plan seed
- service requirements from Gate 0
- file type / source type
- document count
- page count where known
- lightweight document understanding evidence
- early classification signals

### Writes
- initial execution plan
- capability-to-provider mapping
- bundled provider usage plan
- initial fallback policy
- document/page override placeholders where needed
- routing_decision summary

### Output target
Embedded execution plan inside the runtime payload.

### Initial implementation pattern
May initially be implemented as:
- planning Lambda
- orchestration-adjacent rule module
- controlled logic invoked just before primary execution path

### Long-term implementation pattern
Dedicated execution planning engine.

## 5.3 Gate 2 — Extraction Quality and Fallback Decision (Decision Engine 2)

### Placement
After OCR and other primary extraction results become available.

### Trigger
- OCR or primary extraction completed
- quality and completeness evidence produced
- page/document outputs available for evaluation

### Reads
- current execution plan
- OCR outputs
- extraction quality evidence
- completeness indicators
- page-level confidence
- expected outputs from the current plan

### Writes
- adjusted execution plan if required
- fallback decisions
- page-level reroute decisions
- document-level reroute decisions
- updated routing_decision
- evaluation evidence and quality conclusions
- decision_gate_history entry

### Output target
Embedded execution plan plus routing/evaluation sections in the runtime payload.

### Initial implementation pattern
May initially be implemented as:
- rule-based evaluation Lambda
- controlled post-OCR evaluation block
- orchestration branch point using an evaluation task

### Long-term implementation pattern
Dedicated quality evaluation and fallback engine.

## 5.4 Gate 3 — Service Sufficiency and Enrichment Decision (Decision Engine 3)

### Placement
After enrichment stages or when enough outputs exist to assess whether the service objective has been met.

### Trigger
- OCR completed
- one or more enrichment capabilities completed
- service-level outputs can be compared to minimum output requirements

### Reads
- current execution plan
- service requirements from Gate 0
- current capability outputs
- evaluation evidence
- service completeness indicators
- authenticity / fraud / signature / structured extraction outputs where relevant

### Writes
- service sufficiency decision
- further enrichment plan if required
- external validation requirement if governed
- partial completion markers if relevant
- updated execution plan
- updated routing_decision
- evaluation evidence and completeness conclusions
- decision_gate_history entry

### Output target
Embedded execution plan plus routing/evaluation sections in the runtime payload.

### Initial implementation pattern
May initially be implemented as:
- sufficiency-evaluation Lambda
- aggregation-adjacent rule module before final acceptance
- orchestration branch point using a service sufficiency evaluator

### Long-term implementation pattern
Dedicated service sufficiency / enrichment decision engine.

## 5.5 Gate 4 — Final Validation and Delivery Decision (Decision Engine 4)

### Placement
After aggregation has assembled final outputs, just before final delivery state is confirmed.

### Trigger
- aggregation completed
- final outputs and summaries available
- route and evaluation history available

### Reads
- final assembled outputs
- current execution plan
- routing_decision summary
- evaluation summary
- service sufficiency status
- delivery rules

### Writes
- final accept / partial / qualified / escalate state
- final execution plan status
- final routing summary
- final evaluation summary
- final delivery qualification metadata
- decision_gate_history entry

### Output target
Final payload plus final manifest update and final execution plan state.

### Initial implementation pattern
May initially be implemented as:
- final validation Lambda
- aggregation-adjacent rule block
- final Step Functions decision point after aggregation

### Long-term implementation pattern
Dedicated final validation / delivery decision engine.

## 6. Current Controlled Baseline Placement

For the initial implementation, the following placement is acceptable.

### 6.1 Gate 0
Implemented before or at GenerateManifest entry.

### 6.2 Gate 1
Implemented after manifest initialization and early document understanding, before major extraction routing is finalised.

### 6.3 Gate 2
Implemented after OCR output is available and before enrichment reroute decisions are finalised.

### 6.4 Gate 3
Implemented after enrichment outputs are available and before final output acceptance is decided.

### 6.5 Gate 4
Implemented after aggregation and before final success state is declared.

## 7. Invocation Ownership by Runtime Component

## 7.1 Step Functions
Owns:
- orchestration placement of gate invocations
- passing payload between gates and workers
- branching based on gate outputs
- loop control where governed

Must not:
- replace decision engines with uncontrolled inline logic

## 7.2 Decision Lambdas / Rule Modules
Own:
- gate-specific evaluation
- gate-specific output object creation
- controlled updates to execution_plan, routing_decision, and evaluation

Must not:
- perform unrelated worker responsibilities
- bypass gate history recording

## 7.3 Workers
Own:
- execution of capabilities assigned by the plan

Must not:
- invoke themselves as substitute decision engines
- independently rewrite provider strategy outside gate semantics

## 8. Read/Write Payload Contract by Gate

## 8.1 Gate read rule
Each gate reads:
- the current embedded execution plan
- relevant evidence produced so far
- relevant outputs for its phase
- service requirements where needed

## 8.2 Gate write rule
Each gate writes only:
- gate-specific decision results
- controlled plan adjustments
- routing summary updates
- evaluation evidence summaries
- decision history entry

## 8.3 Preservation rule
Each gate invocation must preserve all unrelated payload sections.

## 9. Loop and Re-entry Placement

## 9.1 Gate 2 loop placement
If OCR quality is insufficient:
- Gate 2 may trigger reroute or fallback
- Step Functions may re-enter the relevant execution branch
- execution plan must record the adjustment

## 9.2 Gate 3 loop placement
If service sufficiency is not met:
- Gate 3 may trigger additional enrichment
- Step Functions may invoke the missing capability path
- execution plan must record the adjustment

## 9.3 Loop limits
Looping must obey `execution_plan.fallback_policy` or equivalent governed bounded-loop settings.

## 10. First-Pass Implementation Rule

The initial system may implement decision engines as:
- simple rule-based Lambdas
- coarse scorecards
- limited thresholds
- pass-through logic where appropriate

This is acceptable only if:
- each gate still exists logically
- each invocation point is explicit
- each gate still reads/writes the correct parts of the payload
- future replacement with more advanced engines does not require redesign

## 11. Future Evolution Path

The design must support future progression from:
- inline or Lambda-based rule modules

to:
- dedicated decision services
- optimisation solvers
- champion/challenger decision engines
- learned routing models

This evolution must happen by replacing gate implementations, not by redesigning the gate model or payload structure.

## 12. Strategic Outcome

This specification is successful when:
- every developer knows where each gate runs
- gate logic is not hidden inside unrelated workers
- Step Functions can invoke decision logic in a governed order
- execution plan updates happen at controlled points
- future decision-engine sophistication can be added without changing the overall architecture
