# OCR Rebuild — Phase 5 Controlled Implementation Scope

Status: ACTIVE - CONTROLLED HYBRID IMPLEMENTATION BASELINE

## 1. Purpose

Define the governed implementation scope for the current Phase 5 delivery so that development can proceed quickly without losing alignment to the broader hybrid document intelligence strategy.

This document exists to make clear:

- what is intentionally being implemented now
- what is intentionally placeholder-backed or externally backed
- what is not yet fully implemented but must remain architecturally visible
- what must be measured and improved over time
- how external capability will be progressively internalized without redesign

This document must be read together with:
- Phase 2 Logical Architecture
- Phase 3 Pipeline Workflow
- Phase 5 Input Normalization and Routing Design
- governed execution/data contracts

## 2. Core Delivery Principle

The current delivery is not the final platform.
It is the first governed implementation increment of a broader hybrid document intelligence system.

The implementation approach is intentionally:

- fast to deliver
- API-capable
- modular
- substitution-ready
- measurable

This means the platform may use:
- internal modules
- open-source components
- external API-backed capability
- managed-service fallback

from the start.

The architecture must therefore be judged by:
- correctness of module boundaries
- routing and decisioning readiness
- telemetry and traceability readiness
- substitution readiness
- client outcome protection

and not only by how many capabilities are already internally implemented.

## 3. Controlled Current-Scope Objective

The current implementation objective is to establish a governed operational baseline that proves:

- end-to-end orchestration works
- normalization and page/document semantics are governed
- primary OCR and enrichment flow is functioning
- aggregation works against hardened contracts
- future internal/external substitution is possible without redesign

## 4. Current In-Scope Delivery Baseline

The current governed implementation baseline includes:

### 4.1 Core workflow baseline
- intake
- normalization baseline
- preprocessing baseline
- OCR baseline
- enrichment stage baselines
- aggregation baseline

### 4.2 Current implemented capability baseline
- PDF/image normalization baseline
- Tesseract-based printed OCR baseline
- heuristic table extraction baseline
- heuristic logo/template baseline
- heuristic fraud baseline
- canonical aggregation baseline

### 4.3 Architecture-ready but not fully implemented capability domains
The following capability domains must be treated as architecturally in-scope even where implementation is partial, placeholder-based, or deferred:

- handwriting recognition
- language / script detection
- layout analysis
- key-value / forms extraction
- signatures
- selection marks / checkboxes
- barcode / QR extraction
- document classification
- document splitting / grouping
- font / style analysis
- image / figure extraction
- formula extraction
- structured-digital parsing
- hybrid OCR/structured execution
- intelligent fallback routing
- evaluation / benchmark telemetry

## 5. External Capability Operating Model

The platform is intentionally designed to allow external capability use from the beginning.

This is not a design compromise.
It is a deliberate strategy to:
- accelerate delivery
- achieve higher early quality
- reduce time-to-market risk
- support broader client-required capability coverage

External providers must be treated as:
- API-backed capability modules
- replaceable adapters behind governed contracts
- valid controlled fallback options

They must not be treated as the platform itself.

## 6. Internalization Strategy

The competitive strategy is not to avoid external capability at all costs.

It is to:
- use external capability where this materially improves client outcome or delivery speed
- measure quality, cost, and fallback behavior
- progressively replace expensive external capability with internal capability where justified
- preserve managed-service fallback where internal capability is still insufficient

Internalization must therefore happen through controlled substitution, not redesign.

## 7. What Is Intentionally Restricted in the Current Round

The current implementation round is intentionally restricted to avoid uncontrolled expansion while governed foundations are still being established.

Current restrictions include:
- limited current source-type routing implementation
- limited current capability-routing logic
- limited current fallback-decision telemetry
- limited current module depth in non-core capability domains
- no final benchmark-proven OCR engine decision yet
- no full structured-digital parsing path yet
- no final production intelligence-routing dashboard yet

These restrictions are accepted only because:
- the architecture is being shaped to support them properly
- they are documented explicitly
- they are not being mistaken for final platform scope

## 8. What Must Not Be Forgotten

The following must remain visible and active in all future implementation decisions:

- this is a hybrid document intelligence platform, not a narrow OCR engine build
- capability breadth matters as much as OCR text extraction
- external capability usage is acceptable when client outcome requires it
- internal replacement must remain a standing objective
- telemetry and evaluation are mandatory for future improvement
- placeholders are acceptable only where module boundaries and contracts are already established

## 9. Required Measurement Readiness

Even in restricted implementation, the platform must remain ready to measure:

- engine used
- provider used
- fallback used
- fallback reason
- quality indicators
- completeness indicators
- module execution coverage
- cost attribution where possible
- document/page/project routing path

Without this, improvement and internalization will stall later.

## 10. Required Substitution Readiness

All implementation choices in the current round must preserve the ability to replace:

- external OCR with internal OCR
- external forms with internal forms extraction
- external handwriting with internal handwriting module
- external structured extraction with internal structured parsers
- heuristic modules with improved or model-based modules

This replacement must be possible through stable contracts and routing logic, not through re-architecture.

## 11. Controlled Next-Wave Priorities

After the current governed baseline, the next-wave priorities remain:

1. strengthen normalization and routing
2. add routing/evaluation metadata to contracts
3. improve OCR quality measurement
4. introduce hybrid internal/external fallback routing
5. expand capability modules beyond current heuristics
6. establish benchmark and decision analytics
7. internalize high-cost external capability where justified
8. production hardening and operational controls

## 12. Success Standard for the Current Round

The current round is successful if it establishes:
- a working governed baseline
- stable contracts
- normalization and routing direction
- substitution-ready architecture
- explicit visibility of future capability domains
- no false assumption that current capability breadth equals final platform breadth

## 13. Strategic Interpretation

This implementation scope must always be interpreted as:

- a controlled first operating baseline
- externally augmentable from day one
- internally improvable over time
- measurable by design
- intentionally broader than the currently implemented module depth

The purpose of the current round is not to finish the platform.

The purpose is to establish the correct architecture, contracts, routing, and operating model so the platform can expand, improve, and internalize capability without repeated redesign.
