# OCR Rebuild — Decision and Runtime Responsibility Mapping

Status: DRAFT - IMPLEMENTATION RESPONSIBILITY BASELINE

## 1. Purpose

Define which runtime component owns which responsibility in the OCR Rebuild platform.

This document is authoritative for:
- responsibility boundaries between architecture layers and runtime components
- which component creates, reads, updates, and preserves the execution plan
- which component performs decisioning versus execution
- which component owns evidence production, fallback activation, and final lineage
- how current AWS components align to the staged decision ecosystem

This document exists to prevent:
- worker-level decision sprawl
- hidden provider logic inside runtime modules
- orchestration drift
- ambiguity about who owns plan creation, plan refinement, and plan preservation

## 2. Core Principle

The platform must separate:

- service composition
- decisioning
- execution
- aggregation
- durable state tracking

No runtime worker should become an uncontrolled product builder or general routing engine.

Each component must have a bounded responsibility.

## 3. Runtime Component Set

The current controlled baseline recognises the following runtime components:

- Service Composition / request interpretation logic
- Decision Engine 0
- Decision Engine 1
- Decision Engine 2
- Decision Engine 3
- Decision Engine 4
- Step Functions state machine
- GenerateManifest component
- Preprocessing Lambda
- OCR worker
- Table extraction worker
- Logo/template worker
- Fraud/authenticity worker
- Aggregation worker
- Manifest store / durable manifest update logic
- Future external provider adapters

## 4. Responsibility Layers

## 4.1 Service composition responsibility
Owns:
- interpretation of client service request
- selection of service definition
- decomposition into sub-services and capabilities
- minimum output requirements
- relevant gate set

Does not own:
- provider selection
- OCR quality decisions
- runtime fallback execution

## 4.2 Decision responsibility
Owns:
- execution plan creation
- execution plan refinement
- capability-to-provider mapping
- fallback and reroute decisions
- service sufficiency decisions
- final delivery acceptance decisions

Does not own:
- actual OCR execution
- actual extraction execution
- final payload storage mechanics

## 4.3 Runtime execution responsibility
Owns:
- carrying out assigned capability work
- preserving runtime payload
- producing outputs and evidence
- reporting results and quality metrics

Does not own:
- redefining service intent
- inventing new products
- uncontrolled provider substitution

## 4.4 Aggregation responsibility
Owns:
- final assembly of output payloads
- preservation of final plan lineage
- final manifest update assembly
- production of canonical document outputs

Does not own:
- retroactive redesign of the execution plan
- hidden fallback decisions outside gate semantics

## 5. Gate-to-Component Ownership

## 5.1 Gate 0 — Request Interpretation and Service Assembly (Decision Engine 0)

### Primary owner
- Service Composition logic / Decision Engine 0

### Responsibilities
- interpret client request
- select service definition
- determine required capabilities
- determine minimum outputs
- determine relevant gates
- initialize service-level constraints

### Outputs owned
- service selection
- required capabilities
- initial service requirement set
- initial execution plan seed

### Current implementation note
May initially be implemented as lightweight orchestration-adjacent logic rather than a separate deployed engine, provided the responsibility boundary remains clear.

## 5.2 Gate 1 — Document Understanding and Initial Execution Planning (Decision Engine 1)

### Primary owner
- Decision Engine 1

### Responsibilities
- read service requirement set
- inspect early document evidence
- build initial execution plan
- assign providers/modules by capability
- identify bundled provider reuse opportunities
- define initial fallback allowances
- determine document/page override need

### Outputs owned
- initial execution plan
- initial routing summary
- initial gate thresholds

### Current implementation note
This may initially live in orchestration planning logic or an early planning Lambda, but it must remain a distinct responsibility.

## 5.3 Gate 2 — Extraction Quality and Fallback Decision (Decision Engine 2)

### Primary owner
- Decision Engine 2

### Responsibilities
- evaluate OCR and extraction quality
- determine whether results are acceptable
- decide on page-level reroute
- decide on document-level reroute
- activate fallback where allowed
- update execution plan if material changes occur

### Outputs owned
- adjusted execution plan
- fallback decisions
- quality acceptance or rejection
- updated routing summary
- quality evidence

### Current implementation note
This may initially be implemented through rule logic adjacent to OCR/extraction evaluation, but must remain distinct from the OCR worker itself.

## 5.4 Gate 3 — Service Sufficiency and Enrichment Decision (Decision Engine 3)

### Primary owner
- Decision Engine 3

### Responsibilities
- determine whether the requested service outcome has been met
- identify missing required capabilities or outputs
- decide on further enrichment
- trigger external validation where governed
- decide partial vs complete service readiness

### Outputs owned
- service sufficiency result
- enrichment requirement decisions
- adjusted execution plan where required
- service-level completeness evidence

### Current implementation note
This may initially be implemented near aggregation-prep logic, but must remain distinct from aggregation itself.

## 5.5 Gate 4 — Final Validation and Delivery Decision (Decision Engine 4)

### Primary owner
- Decision Engine 4

### Responsibilities
- make final accept / partial / qualified / escalate decision
- confirm service delivery state
- close plan lifecycle
- finalize delivery qualification metadata

### Outputs owned
- final delivery state
- final acceptance decision
- final route interpretation
- final evaluation summary

### Current implementation note
This may initially sit adjacent to final aggregation/delivery logic, but must remain a distinct decision responsibility.

## 6. Component-by-Component Runtime Responsibilities

## 6.1 Step Functions state machine

### Owns
- orchestration order
- task invocation sequencing
- payload handoff between stages
- controlled branching
- retry / catch behavior
- preservation of top-level runtime payload

### Must do
- pass `execution_plan` forward unchanged unless updated by a governed stage
- pass `routing_decision`, `evaluation`, and `manifest_update`
- preserve document and page outputs
- avoid destructive replacement of payload sections

### Must not do
- embed uncontrolled business logic
- hard-code provider choices that belong in decision engines
- silently drop execution plan sections

## 6.2 GenerateManifest component

### Owns
- initialization of normalized runtime payload
- initialization or carry-forward of embedded execution plan
- initialization of service status and execution state
- initialization of manifest update object

### Must do
- preserve upstream Gate 0 outputs if present
- create a valid payload shell
- normalize identifiers and documents list

### Must not do
- invent downstream provider logic
- discard service intent

## 6.3 Preprocessing Lambda

### Owns
- source normalization for OCR-eligible content
- page derivation where governed
- preprocessing artifact generation
- preprocessing evidence generation

### Must do
- read execution plan where relevant to normalization/preprocessing
- preserve execution plan
- emit normalization evidence for later gates
- preserve page/document lineage

### Must not do
- invent OCR provider decisions
- decide service sufficiency
- invent fallback paths outside governed rules

## 6.4 OCR worker

### Owns
- execution of TEXT_OCR capability according to plan
- OCR output production
- OCR evidence production
- OCR quality metrics

### Must do
- read `execution_plan.capability_plan.TEXT_OCR`
- honor page/document overrides where relevant
- emit quality evidence into evaluation
- preserve full payload

### Must not do
- decide new OCR providers on its own
- redefine service objective
- alter unrelated capability assignments

## 6.5 Table extraction worker

### Owns
- execution of table-related capabilities
- table output production
- table quality evidence

### Must do
- read relevant capability entries
- reuse bundled outputs where already available
- avoid unnecessary duplicate extraction
- preserve plan and payload

### Must not do
- choose duplicate table providers without governed reason
- redefine service sufficiency

## 6.6 Logo/template worker

### Owns
- logo/template-related enrichment outputs
- associated evidence

### Must do
- act only on relevant planned capability/service instruction
- preserve plan and payload

### Must not do
- redefine route for unrelated capabilities

## 6.7 Fraud/authenticity worker

### Owns
- authenticity and fraud signal generation
- anomaly and trust evidence
- capability outputs such as authenticity scoring, tamper signals, or consistency checks when implemented

### Must do
- read relevant capability entries
- emit evidence into evaluation
- preserve plan and payload

### Must not do
- decide final service acceptability on its own
- redefine product/service scope

## 6.8 Aggregation worker

### Owns
- final output assembly
- canonical document assembly
- preservation of final execution lineage
- final manifest update assembly

### Must do
- preserve final execution plan
- preserve routing and evaluation summaries
- produce outputs consistent with executed plan
- record final lineage and summaries

### Must not do
- erase gate history
- invent hidden reroutes
- override final acceptance semantics that belong to Decision Engine 4

## 6.9 Manifest store / durable control layer

### Owns
- durable control record persistence
- pipeline history persistence
- retry state persistence
- client notification state persistence

### Must do
- preserve manifest semantics
- remain aligned with runtime payload updates
- record pipeline history append-only

### Must not do
- become the source of ad hoc runtime decisions outside governed flow

## 7. Decision Engine Implementation Mapping

The initial implementation may not deploy five separate physical services immediately.

That is acceptable.

However, the logical responsibilities must still exist.

## 7.1 Allowed initial implementation pattern
Multiple logical decision engines may initially be implemented through:
- orchestration-adjacent rule modules
- dedicated planning/evaluation functions
- controlled rule blocks near specific runtime stages

provided that:
- the logical boundary remains explicit
- the outputs are recorded as gate decisions
- future extraction into dedicated services is possible without redesign

## 7.2 Disallowed implementation pattern
It is not acceptable to:
- bury all decisions inside individual workers
- let each worker independently choose providers
- mix service composition with low-level worker code
- bypass gate recording

## 8. Data Ownership by Component

## 8.1 execution_plan ownership
Primary owners:
- Decision Engine 0 to initialize intent
- Decision Engine 1 to build initial plan
- Decision Engine 2/3/4 to make controlled material updates

Runtime components may:
- read it
- append execution evidence
- update non-material execution metadata
- preserve it

Runtime components may not:
- replace it wholesale
- redefine it without gate semantics

## 8.2 routing_decision ownership
Primary owners:
- Decision Engines 1 to 4

Runtime components may:
- update factual route execution evidence only when a governed decision has actually been executed

## 8.3 evaluation ownership
Shared responsibility:
- runtime workers produce evidence
- decision engines interpret evidence
- aggregation preserves final summaries

## 8.4 manifest_update ownership
Shared responsibility:
- runtime stages append stage history and status
- aggregation produces final manifest update state

## 9. Responsibility Boundary Rules

### 9.1 Workers execute capabilities
They do not define products.

### 9.2 Decision engines decide route and sufficiency
They do not perform OCR/table/fraud extraction directly.

### 9.3 Orchestration coordinates flow
It does not become the business service layer.

### 9.4 Aggregation assembles results
It does not replace decision engines.

## 10. First-Pass Placeholder Readiness

The current baseline may use:
- placeholder decision rules
- coarse scorecards
- limited provider options
- simplified gate execution

This is acceptable only if:
- responsibilities remain correctly assigned
- plan and gate structures are preserved
- future refinement does not require redesign of ownership boundaries

## 11. Strategic Outcome

This responsibility mapping is successful when:
- every component has a bounded role
- decisioning remains separate from extraction
- execution plan ownership is clear
- workers do not become uncontrolled routers
- future developers can map architecture to AWS runtime without ambiguity
