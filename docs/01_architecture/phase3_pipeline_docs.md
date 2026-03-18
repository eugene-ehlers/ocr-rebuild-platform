# Phase 3 OCR Pipeline Workflow (Hybrid Document Intelligence Flow)

## 1. Purpose

This document defines the operational Phase 3 workflow for the OCR Rebuild platform as a hybrid, API-capable, continuously improving document intelligence pipeline.

The workflow is not limited to a single OCR engine or a single static extraction path.

It exists to support:
- fast initial delivery using external API-backed services where needed
- progressive internalization of capability over time
- intelligent routing between internal and external capabilities
- modular extraction and enrichment
- measurable quality, cost, and fallback behavior

## 2. Strategic Processing Model

The Phase 3 workflow must be interpreted as a capability orchestration flow, not a single-engine OCR sequence.

The platform must support:
- internal/open-source first-pass processing where appropriate
- managed-service or external API fallback where client outcome requires it
- modular capability execution by document, page, or project scope
- telemetry and traceability sufficient for continuous improvement

## 3. High-Level Workflow

The operational workflow is:

1. intake and upload capture
2. normalization and routing
3. classification / grouping / splitting
4. preprocessing
5. primary OCR / primary extraction
6. quality and completeness evaluation
7. fallback / escalation if required
8. intelligence module execution
9. aggregation into canonical outputs
10. evaluation, traceability, and improvement signals

## 4. Controlled Processing Stages

### 4.1 Intake
Capture:
- source object(s)
- source metadata
- upload grouping metadata where provided
- expected document type where known
- requested service selections

### 4.2 Normalization
Convert raw uploaded content into governed execution scope:
- manifest / project scope
- logical document scope
- page scope for OCR-eligible inputs
- routing classification for structured-digital or unsupported content

### 4.3 Classification / Grouping / Splitting
Determine:
- document grouping
- page ordering
- document type classification where possible
- whether document splitting is required
- whether downstream routing requires document-specific capability selection

### 4.4 Preprocessing
Prepare OCR-eligible content for downstream OCR and extraction:
- page rendering from PDF where applicable
- image normalization
- grayscale / contrast / filtering
- controlled processed artifact creation
- page lineage preservation

### 4.5 Primary OCR / Primary Extraction
Run the first-pass capability set using the selected primary engine.

Examples:
- internal Tesseract-based OCR
- future internal handwriting module
- future internal form/key-value extraction
- future structured parser for digital-native inputs

Primary execution does not imply final acceptance.

### 4.6 Quality and Completeness Evaluation
Evaluate the primary result for:
- confidence quality
- text completeness
- required field completeness
- structural extraction sufficiency
- document-type-specific adequacy
- fallback need

### 4.7 Fallback / Escalation
If internal or open-source capability is insufficient, escalate selectively to:
- managed-service OCR
- managed-service form extraction
- managed-service table extraction
- future specialist external providers

Fallback must be:
- explainable
- traceable
- measurable
- attributable to a reason code

### 4.8 Intelligence Module Execution
Execute modular capabilities as required by document type and routing logic.

Examples:
- table extraction
- key-value extraction
- handwriting
- signatures
- checkboxes / selection marks
- barcodes / QR
- language detection
- layout analysis
- logo / stamp / seal detection
- fraud heuristics
- font/style analysis
- image / figure extraction
- formula extraction

Modules may be:
- internal
- heuristic
- external API-backed
- placeholder for controlled future implementation

### 4.9 Aggregation
Assemble:
- page-level outputs
- document-level canonical outputs
- manifest/project-level updates
- routing lineage
- evaluation metadata
- module execution summaries

### 4.10 Evaluation and Improvement
Every run must generate signals for:
- quality analysis
- cost analysis
- fallback analysis
- engine comparison
- improvement opportunities
- future benchmarking

## 5. Execution Philosophy

### 5.1 Client outcome first
The platform must prefer the route that best protects client outcome.

### 5.2 Internalize where justified
If internal capability is good enough, prefer it to reduce cost and improve unit economics.

### 5.3 Fallback where necessary
If internal capability is not yet sufficient, use external capability rather than knowingly degrade client outcome.

### 5.4 Replace by substitution
External capabilities must sit behind stable contracts so that future internal replacement is a controlled substitution rather than a redesign.

## 6. Workflow Interpretation Rules

### 6.1 The pipeline is modular
A document does not need to use every module.

### 6.2 The pipeline is conditional
Routing and module invocation depend on:
- source type
- document type
- quality
- confidence
- required outcomes
- cost/accuracy tradeoff rules

### 6.3 The pipeline is hybrid
Different pages or documents in the same manifest may use different capability paths.

### 6.4 The pipeline is measurable
All major routing and module decisions must be attributable and reportable.

## 7. Required Routing Signals

The workflow must support routing based on signals such as:
- OCR confidence
- text density
- required field presence
- page quality
- document type
- handwriting detection
- structured layout need
- duplicate / suspicious content
- language/script
- cost or fallback thresholds

These may begin as rule-based signals and later evolve into learned decisioning.

## 8. Required Traceability

The workflow must support recording:
- primary engine used
- fallback used
- fallback provider
- fallback reason
- modules executed
- modules skipped
- quality score(s)
- completeness score(s)
- document and page lineage
- final accepted path

## 9. Controlled Current-State Interpretation

At present, the implemented workflow is an early baseline:
- preprocessing baseline exists
- internal Tesseract OCR baseline exists
- heuristic enrichment modules exist
- aggregation baseline exists

This current implementation must be interpreted as:
- the first governed operating increment
- not the final capability model
- compatible with future internal and external module substitution

## 10. Diagram Reference

The Phase 3 workflow diagram remains a useful visual reference, but it must now be interpreted through the hybrid document intelligence model defined in this document and the updated logical architecture.

Image reference:
`phase3_pipeline_workflow.png`

S3 reference:
`s3://ocr-rebuild-program/docs/01_architecture/phase3_pipeline_workflow.png`

## 11. Strategic Outcome

Phase 3 is successful when the workflow supports:
- modular capability execution
- explainable routing
- external API-backed capability where needed
- progressive internalization over time
- measurable quality and cost outcomes
- no dependence on a single engine or provider as the platform definition
