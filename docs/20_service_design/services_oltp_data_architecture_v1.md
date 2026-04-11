# Services OLTP Data Architecture v1

## 1. Purpose

This document defines the governed OLTP data architecture for the Services Application (System B).

It exists to provide design authority for future backend and data work related to:
- service application persistence
- user journey persistence
- request lifecycle persistence
- audit-grade history preservation
- support/admin operational queryability
- reference-based integration with the OCR Platform (System A)

This document is limited to System B and its integration boundary with System A. It does not govern the OCR runtime data architecture itself.

---

## 2. System Context

### System B — Services Application

System B is the client-facing and service-orchestration application layer. It includes:
- frontend user journeys
- backend service orchestration
- request intake and lifecycle handling
- resumable user interactions
- support, reporting, and admin operational capabilities
- service-level results handling

System B is the operational system of record for the business service interaction model.

### System A — OCR Platform

System A is the OCR/core execution platform. It includes:
- payload-driven pipeline execution
- manifest-based execution control
- execution planning and routing
- OCR and enrichment runtime processing
- runtime artifacts and traceability

System A is the system of record for OCR execution and runtime processing truth.

### Boundary

System B owns:
- request/application lifecycle
- user and tenant context
- journey continuity and resumability
- support/admin operational history
- service-level results state
- audit-grade service interaction history

System A owns:
- execution plan
- manifest
- OCR runtime payloads
- runtime execution state
- OCR and enrichment artifacts
- engine-level routing/evaluation traceability

System B and System A interact through references and correlation identifiers, not by duplicating ownership of execution/runtime artifacts.

---

## 3. Design Drivers (WHY)

The Services Application OLTP architecture must satisfy the following design drivers.

### Auditability

The service application must support audit-grade persistence of user and operational activity. History must not depend on overwrite-only mutable state.

### Reconstructability

The architecture must support reconstruction of:
- a user journey
- request evolution
- state transitions
- rule decisions
- operational interventions
- service-configuration lineage

at any point in time.

### Flexible Service Evolution

The service offering is modular and evolving. New services, new fields, new rules, and new operational patterns must be supported without destructive redesign.

### Resumable Journeys

Users may:
- interrupt a journey
- return later
- continue from the correct state
- update prior information when rules permit
- be forced to restart when governed rules require it

The architecture must support this operationally and historically.

### Rule / Version Lineage

The architecture must preserve:
- which rule version applied
- which service configuration applied
- which operational decision was taken
- why continuation, expiry, retry, or blocking occurred

### Operational Support Requirements

Support/admin users must be able to query the system efficiently for:
- request status
- journey history
- exception state
- notifications
- support interventions
- audit evidence

### Evidence Basis

The design basis includes explicit governance signals that:
- traceability and auditability are mandatory :contentReference[oaicite:0]{index=0}
- lifecycle and history must be captured :contentReference[oaicite:1]{index=1}
- current request persistence is not yet event-driven and lacks audit-grade immutability (GAP-015) :contentReference[oaicite:2]{index=2}

These constraints require an OLTP architecture that preserves append-only history while still supporting operational queryability.

---

## 4. Architecture Options Considered

### Option A — Relational-Only

This option was considered because relational OLTP supports strong operational querying and is a natural fit for structured business entities such as users, requests, documents, and support records.

It was rejected as the primary pattern because:
- append-only history becomes a secondary design concern rather than a first-class one
- reconstruction requires multiple bespoke history/version tables
- rule lineage and journey replay become harder to model cleanly
- evolving service metadata becomes more cumbersome without a flexible attribute strategy

### Option B — DynamoDB-Only

This option was considered because append-only events, flexible attributes, and versioned item models are possible in a NoSQL-first pattern.

It was rejected because:
- operational querying for support/admin use cases becomes significantly harder
- the service application has a rich relationship model that is not naturally query-friendly in a single DynamoDB-first design
- debugging and operational investigation are more complex
- the pattern creates high design sensitivity around access patterns and partitioning

### Option C — Event-Sourcing-First

This option was considered because event sourcing is naturally aligned to:
- append-only history
- reconstruction
- replay
- immutable decision lineage

It was rejected as the primary architecture because:
- it introduces high architectural and development complexity
- it makes ordinary OLTP workflows and support queries projection-dependent from the start
- it is higher risk than required for the current governed scope

### Option D — Hybrid OLTP Architecture

This option combines:
- a structured relational core for operational system-of-record data and queryability
- a dedicated append-only event/history store for immutable history
- flexible attribute handling for evolving service definitions and metadata

This option was selected because it best satisfies the full set of design drivers without forcing either relational-only compromises or event-sourcing-first complexity.

---

## 5. Selected Architecture (WHAT)

## Selected Pattern

The selected pattern is:

**Hybrid OLTP Architecture**

This architecture is the governed design authority for System B.

### Relational Core

The relational core exists to store structured, operationally queryable business data for the Services Application.

Its purpose is to support:
- users, tenants, roles, and access context
- requests/applications
- document submission metadata
- service definitions and service configuration references
- support/admin operational records
- current-state projections where required for OLTP use

The relational core is the primary operational query surface for support, admin, and service workflows.

### Event / History Store

The event/history store exists to preserve append-only historical truth for service application behavior.

Its purpose is to store immutable history for:
- journey events
- workflow transitions
- audit events
- rule evaluations
- retry/escalation activity
- request changes and key checkpoints
- operational interventions

This store follows the append-only principle. Historical events must not be overwritten.

### Flexible Attribute Strategy

The architecture must support limited flexible attributes for evolving service behavior and metadata.

Flexible attributes are used for:
- service-specific request metadata
- evolving service parameters
- rule evaluation inputs/outputs
- configuration lineage details
- operational metadata that is not stable enough to justify rigid structure from the outset

Flexible attributes must not replace disciplined core entity structure.

### Integration Layer

System B integrates with System A using references and correlation identifiers.

Examples include:
- manifest identifiers
- execution/job correlation identifiers
- result artifact references
- runtime trace pointers

System B must reference System A cleanly without duplicating System A ownership.

---

## 6. Core Design Principles (NON-NEGOTIABLE)

The following principles are mandatory and govern all future System B data design:

1. **Append-only history is mandatory**
   - Journey events, audit events, rule evaluations, and workflow transitions must be preserved as append-only records.

2. **Versioned entities are mandatory**
   - Request/application state, service configuration, and rules/policies must support version lineage.

3. **Reconstructability is mandatory**
   - The architecture must support reconstruction of the full user and operational journey at any point in time.

4. **Flexible evolution is mandatory**
   - The system must support evolving services and changing metadata without destructive redesign.

5. **OLTP-first operation is mandatory**
   - The service application must operate independently of analytics or a future lakehouse.

6. **Operational queryability is mandatory**
   - Support/admin workflows must remain efficient and practical.

7. **Clean system boundaries are mandatory**
   - System B must not duplicate System A runtime ownership.

These principles are enforced standards, not optional guidance.

---

## 7. Data Responsibility Model

### System B owns

System B is the system of record for:
- requests/applications
- users/tenants/access context
- journey history
- request lifecycle state
- service-level results state
- notifications
- support/admin operational records
- audit-grade service interaction history
- rule evaluation history at service-application level
- resumability and continuity decisions

### System A owns

System A is the system of record for:
- execution plan
- manifest
- OCR runtime payloads
- execution routing and evaluation inside the OCR platform
- OCR and enrichment artifacts
- runtime processing lineage

### External systems own

External systems are the system of record for:
- authentication credentials
- external identity verification
- external authority/verification systems
- any future third-party verification domains

---

## 8. High-Level Data Architecture

This section is conceptual only.

### Core OLTP Store

A structured relational OLTP core stores:
- master business entities
- transactional service entities
- support/admin operational entities
- current-state projections

### Event / History Store

A dedicated append-only history layer stores:
- immutable journey events
- immutable audit events
- rule/version application history
- workflow transitions
- retry and escalation events
- change checkpoints and lineage

### Projections / Current State

Operational current-state views may be maintained for:
- request status
- active draft/request state
- latest allowed next action
- support-facing current status

These projections do not replace durable history.

### Integration References

System B stores references to System A and external systems using:
- correlation identifiers
- integration references
- external subject identifiers
- manifest and execution references

---

## 9. Risks and Mitigations

### Risk 1 — Dual-Store Complexity

Using a relational core plus append-only history increases architectural complexity.

**Mitigation:**
- strict separation between operational state and immutable history
- clear design rules for where each class of data belongs
- request-centric aggregate boundaries

### Risk 2 — Consistency Model Complexity

The architecture introduces consistency concerns between state and history.

**Mitigation:**
- define disciplined write patterns in the next package
- define authoritative order of writes and projection updates
- prevent ambiguous ownership between state and event records

### Risk 3 — Developer Misuse of Overwrite Semantics

Developers may attempt to overwrite or summarize history.

**Mitigation:**
- append-only principle is mandatory
- overwrite of historical records is non-compliant by design
- projections must be treated separately from history

### Risk 4 — Query Duplication / Read Model Confusion

Operational users may query the wrong store or duplicate read logic.

**Mitigation:**
- relational core remains the primary operational query surface
- history store remains the primary historical truth surface
- next design phase must define read-model responsibilities clearly

---

## 10. What This Enables

This architecture enables:

### Agile System Evolution
The service application can add new services, change rules, and extend operational metadata without destructive redesign.

### Future Analytics Readiness
The OLTP design preserves durable operational truth that can later feed lakehouse/analytics patterns without making analytics a runtime dependency.

### Support Tooling
Support and admin operations can query structured current-state data efficiently while still accessing detailed historical lineage when needed.

### Audit / Compliance
The system can reconstruct user and operational journeys in a way suitable for audit, review, and governance.

### Continuous Improvement
The application can preserve the configuration and decision lineage needed to evaluate service evolution and support a modular, improving service model over time.

---

## 11. What Is Explicitly Out of Scope

This document does not define:
- schema design
- table design
- indexing design
- physical DDL
- implementation details
- deployment details
- final concrete database product selection

This document governs architecture pattern and data responsibility only.

---

## 12. Next Design Steps

The next package must define:

### Immediate next step
**Logical-to-physical mapping**

This must map:
- which System B entities belong in the relational core
- which belong in the append-only history layer
- which are projections
- which are references only

### Follow-on design steps
After logical-to-physical mapping:
1. schema design
2. indexing strategy
3. write model
4. projection/update model
5. integration contract refinement where needed

This document is the design authority input for those next steps.

