# OCR Rebuild — Phase 2 Logical Architecture (Hybrid Document Intelligence Baseline)

## 1. Overview
Scope: document ingestion, normalization, OCR, structured extraction, enrichment, evaluation, intelligent routing, and canonical output assembly.

The platform is not a single-engine OCR tool.
It is a modular document intelligence system designed to deliver:

- best achievable client outcome
- lowest sustainable processing cost
- measurable and continuously improving accuracy
- governed fallback to managed services where open-source or internal capability is insufficient

The solution must support:

- single-page image uploads
- multi-page documents
- page-by-page assembled documents
- multi-document project uploads
- hybrid processing and routing
- continuous measurement, evaluation, and improvement

The initial implementation is intentionally API-driven where this provides:
- faster delivery
- stronger early accuracy
- lower implementation risk
- immediate market-relevant capability coverage

This is a deliberate operating model, not an architectural shortcut.

Out of scope for this phase:
- front-end UI/dashboard implementation
- downstream business decisioning beyond document intelligence
- final enterprise operating model and commercial packaging

## 2. Core Strategic Principle

The platform must be built as an internal orchestration, decisioning, and intelligence framework that can use both:

- externally provided capability services via API
- internally implemented capability modules

The initial implementation is intentionally API-driven where this provides:
- faster delivery
- stronger early accuracy
- lower implementation risk
- immediate market-relevant capability coverage

This is a deliberate operating model, not a temporary shortcut.

The long-term strategy is to progressively replace expensive external capabilities with internal modules where internal performance is sufficient on:
- accuracy
- confidence quality
- latency
- operating cost
- maintainability

Managed-service or third-party capabilities must remain valid fallback options where they materially outperform internal capability for client-critical outcomes.

Therefore:
- the architecture must own orchestration internally
- capability providers must be modular and replaceable
- external services must be integrated as API-backed modules behind governed contracts
- replacing an external provider with an internal module must be a controlled substitution, not a redesign

The platform must use intelligent decisioning to determine:
- what capability is needed
- which engine or module should perform it
- when internal capability is sufficient
- when managed-service fallback is required
- how performance, cost, and accuracy are measured over time

## 3. Solution Boundaries

Layer | Included (In-Scope) | Excluded (Out-of-Scope)
----- | ------------------ | -----------------------
Document Intake | Upload API, single/multi-page upload, project upload, metadata capture | Front-end UI/dashboard, user auth beyond AWS/IAM boundary
Normalization | Source-type detection, grouping, page derivation, page ordering, OCR-eligible routing | Full structured-digital parsing implementation in this phase
Preprocessing | PDF/image normalization, image enhancement, page preparation | Advanced image science beyond governed increments
OCR | Primary OCR engine, fallback OCR path, OCR quality scoring | Final production benchmark winner pre-decided without evidence
Structured Extraction | Tables, forms/key-values, selection marks, signatures, handwriting, barcodes, layout roles, language, font/style, images/figures, stamps/logos via modular services | Full best-in-class implementation of every module in Phase 5
Decisioning | Rule-based routing, fallback selection, confidence/completeness-based escalation, future ML routing support | Opaque or untraceable routing logic
Evaluation | Metrics, benchmark outputs, correction capture hooks, drift/change analysis, champion-challenger support | Fully mature MLOps stack in this phase
Aggregation | Canonical document outputs, project/document attribution, lineage and decision traceability | Downstream BI/reporting productization
AWS Infrastructure | S3, Lambda, ECS/Fargate, Step Functions, DynamoDB/RDS, SQS/SNS, CloudWatch | Final enterprise observability estate beyond current governed scope

## 4. Capability Model

The system must be designed around pluggable capability modules.

### 4.1 Core processing modules
- input normalization
- preprocessing
- printed text OCR
- OCR quality assessment
- OCR routing / fallback decisioning
- aggregation

### 4.2 Structured intelligence modules
- table extraction
- key-value / form extraction
- layout analysis
- selection mark / checkbox detection
- signature detection
- barcode / QR extraction
- document classification
- document splitting / grouping

### 4.3 Extended intelligence modules
- handwriting recognition
- language / script detection
- logo / stamp / seal detection
- image / figure region extraction
- font / style analysis
- formula / math extraction
- derived-field inference
- future redaction / PII / semantic post-processing

These modules may begin as:
- implemented
- heuristic
- placeholder
- managed-service backed

But they must exist in the architecture as governed capability domains.

## 5. Hybrid Processing Principle

The platform must support hybrid execution paths.

### 5.1 Hybrid engine strategy
A document or page may be processed by:
- primary internal or open-source capability
- external API-backed capability
- managed-service fallback
- future specialized engine/module

### 5.2 Routing objective
Routing must optimize for:
- client outcome first
- cost second
- latency third

while remaining measurable and explainable.

### 5.3 Routing examples
- internal OCR succeeds with acceptable quality → keep internal result
- internal OCR quality insufficient → escalate to Textract
- structured-digital source identified → route to future structured parser path
- handwriting-heavy page detected → route to handwriting-capable module or managed fallback
- forms/signatures/checkbox-heavy document → route to structured extraction capability set

## 6. Evaluation and Continuous Improvement Layer

The platform must not be static.

Every execution must generate signals that enable:
- quality measurement
- cost analysis
- routing analysis
- fallback analysis
- future model/rule improvement

### 6.1 Required evaluation outputs
At minimum the architecture must support:
- engine used
- fallback used or not
- fallback reason
- confidence and quality signals
- required field completeness
- document/page outcome status
- structured extraction success indicators
- processing cost attribution where possible

### 6.2 Improvement loop
The system must support:
1. measure
2. store
3. analyze
4. tune rules
5. compare engines/modules
6. improve cost/accuracy mix over time

## 7. Processing Scopes

### 7.1 Manifest / project scope
A manifest is a controlled execution scope and may represent:
- one logical document
- multiple logical documents
- a project/bundle upload

### 7.2 Document scope
A document is the logical business unit for canonical output and interpretation.

### 7.3 Page scope
A page is the smallest OCR-processing unit for OCR-eligible content and must support deterministic ordering and lineage.

## 8. High-Level Execution Flow

[Upload / Intake]
    |
[Normalization + Source Routing]
    |
[Classification / Grouping / Splitting]
    |
[Preprocessing]
    |
[Primary OCR / Primary Extraction]
    |
[Quality Assessment + Completeness Assessment]
    |
  +----------------------------------+
  | acceptable                       | → continue
  | not acceptable                   | → fallback / escalation
  +----------------------------------+
    |
[Intelligence Modules]
    |
[Aggregation]
    |
[Evaluation + Traceability + Metrics]

## 9. Capability Placeholder Requirement

The architecture must explicitly cater for future or immature capabilities, even where first-round implementation is limited.

Examples:
- handwriting
- multilingual/script-aware OCR
- signatures
- selection marks
- barcodes
- key-value extraction
- font/style
- formulas
- image/figure extraction

A capability may start as a placeholder or minimal implementation, but:
- the module boundary must exist
- the contract boundary must exist
- telemetry and routing hooks must exist

## 10. AWS Reference Architecture

Component | Role
--------- | ----
S3 | Raw inputs, normalized artifacts, processed artifacts, result payloads, benchmark/evaluation artifacts
Lambda | Lightweight normalization / preprocessing / orchestration-adjacent services
ECS/Fargate | Heavier OCR and enrichment modules, binary/model-dependent services
Step Functions | Workflow orchestration and routing control
DynamoDB/RDS | Manifest, execution state, document metadata, future evaluation metadata
SQS/SNS | Async tasking, notifications, future human-review/eventing hooks
CloudWatch/X-Ray | Logs, metrics, operational traceability
Future analytics layer | Benchmarking, fallback analysis, drift and cost reporting

## 11. Key Architectural Requirements

- modular service boundaries
- explicit engine and module replaceability
- explainable routing decisions
- document/page/project lineage
- fallback-aware execution design
- continuous improvement readiness
- schema and telemetry support for future benchmarking
- client outcome prioritized over engine purity

## 11.1 Capability substitution requirement

All capability modules must be integrated through stable internal contracts so that:
- an external API-backed provider can be used initially
- an internal implementation can later replace it
- fallback between internal and external providers can remain available
- substitution does not require workflow redesign or schema redesign

## 12. Current Phase 5 Reality

Current implementation is an early governed baseline, not the final capability target.

Current state includes:
- preprocessing baseline
- Tesseract-based OCR baseline
- heuristic enrichment modules
- aggregation baseline
- governed contracts evolving toward multi-document and hybrid routing support

This must be treated as:
- a controlled starting point
- not the final platform definition

## 13. Strategic North Star

The solution must evolve toward a market-competitive document intelligence platform that delivers:

- broad capability coverage
- optimal engine selection by use case
- fast initial delivery through API-backed external capability where needed
- progressive internalization of capability over time
- controlled fallback to managed services where internal capability is not yet sufficient
- measurable, defensible accuracy
- cost-optimized execution
- continuous improvement over time

The platform is therefore defined as:
- internally owned in orchestration, contracts, routing, telemetry, and aggregation
- hybrid in capability sourcing
- externally augmented where this gives better immediate market performance
- progressively internalized where this improves unit economics without compromising client outcome

The platform is therefore a hybrid, intelligent, and continuously improving document processing system.
