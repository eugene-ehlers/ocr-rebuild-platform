# Phase 4 Build Plan

## 1. Purpose

Define the controlled developer build sequence for Phase 4 using the approved design and the completed reuse assessment.

This document tells developers exactly:

- what existing code can be carried forward
- what must be adapted
- what must be rebuilt
- what order to build and test in
- what must not be reused as final target implementation

## 2. Governing Inputs

This build plan is based on:

- `docs/00_program_control/working_method_and_change_control.md`
- `docs/11_benchmarks/evaluation_framework.md`
- `docs/01_architecture/phase2_logical_architecture.md`
- `docs/01_architecture/phase3_pipeline_docs.md`
- `docs/03_data_model/canonical_document_schema.json`
- `docs/03_data_model/document_manifest_schema.json`
- `docs/19_chat_execution_logs/phase3_schema_audit.log`
- `docs/02_aws_environment/phase4_implementation_design.md`
- `docs/15_build_instructions/phase4_reuse_assessment.md`

## 3. Mandatory Build Rules

Developers must follow these rules:

- no guesses
- no assumptions
- retrieve live state before changing anything
- smallest safe step only
- one controlled change at a time
- verify each step before the next
- if evidence is missing, mark `UNKNOWN`
- do not reuse old code if it breaks approved architecture, schema, modularity, extensibility, or evaluation criteria

## 4. Approved Reuse Position

## 4.1 Reuse as adaptation base

The following existing components may be reused **with modification**:

1. OCR engine code from `ocr-engine-dev:v10`
2. intake / routing logic from `OcrIngestStub-dev`
3. quick/detailed SQS worker patterns
4. contract registry and service gating pattern
5. `agentic-parser` structured extraction wrapper
6. result retrieval / aggregation pattern from `OcrGetResult-dev`
7. existing sample artifacts for seed testing

## 4.2 Do not reuse as final implementation

The following must **not** be treated as target-final implementation:

1. current OCR output schema
2. current detailed result schema
3. current `document_run` structure as final manifest model
4. current dev naming conventions
5. placeholder shell scripts:
   - `run_ocr_pipeline.sh`
   - `run_table_extraction.sh`
   - `run_logo_template_recognition.sh`
   - `run_fraud_detection.sh`

## 4.3 Build from scratch

The following approved-target components must be built new:

1. preprocessing pipeline
2. table extraction pipeline
3. fraud detection pipeline
4. logo/template recognition pipeline
5. canonical aggregation layer
6. manifest implementation
7. Step Functions orchestration
8. ECS/Fargate path where required by target design
9. target observability / alarms / retry controls

## 5. Target Build Sequence

## Step 1 — Freeze reusable source components

Objective:

Capture the reusable current components into controlled build source locations before refactoring begins.

Components to extract:

- OCR engine source from `ocr-engine-dev:v10`
- intake logic from `OcrIngestStub-dev`
- quick worker source
- detailed worker source
- contract registry
- agentic-parser source
- get-result source

Required outcome:

- version-controlled source copies exist in the rebuild codebase
- each extracted component is tagged as:
  - `reuse_candidate`
  - `reference_only`
  - `do_not_reuse`

## Step 2 — Define adapter mappings

Objective:

Map current outputs and state structures to the approved target structures.

Required mappings:

1. current OCR artifact -> target canonical page fields
2. current detailed artifact -> target canonical enrichment fields
3. current `document_run` fields -> target manifest fields
4. current queue/stage names -> target orchestration states

Required outcome:

- explicit field mapping document or code-level mapping spec
- unknowns marked `UNKNOWN`
- no field silently dropped without decision

## Step 3 — Build target manifest implementation

Objective:

Implement the approved manifest model before pipeline refactoring expands.

Must support:

- `manifest_id`
- `creation_timestamp`
- `source_batch_uri`
- document entries
- `pipeline_status`
- `retry_count`
- `last_updated`
- `partial_execution_flags`
- `client_notification`
- `pipeline_history`

Required outcome:

- manifest model exists in approved target structure
- manifest updates can be called by all pipelines
- current `document_run` may be used only as transitional source/reference if needed

## Step 4 — Refactor intake into target entrypoint

Objective:

Adapt existing ingest logic into the approved target intake design.

Reuse from current app:

- upload-trigger pattern
- result path derivation
- quality/routing helper concepts where still valid

Must add or change:

- target bucket names
- target naming conventions
- manifest creation/update
- approved document/page/batch context
- removal of non-target hard-coded assumptions
- compatibility with future Step Functions orchestration

Required outcome:

- upload intake works under target naming and manifest control
- no direct dependence on legacy dev structure as final design

## Step 5 — Separate preprocessing from OCR

Objective:

Create the preprocessing pipeline as its own approved component.

Important:

Current OCR engine contains PDF page splitting and document handling logic, but preprocessing is not a deployed modular pipeline today.

Reuse allowed:

- page decomposition logic from OCR engine where appropriate

Must build new:

- preprocessing stage boundaries
- preprocessing metadata output
- preprocessing manifest updates
- page-level preprocessing outputs for downstream OCR/table/logo/fraud pipelines

Required outcome:

- preprocessing is independently callable
- preprocessing writes required canonical/manifest fields
- preprocessing is not embedded as an undocumented side effect only

## Step 6 — Refactor OCR engine into target OCR component

Objective:

Adapt the current OCR engine into a target-compliant OCR module.

Reuse from current app:

- PDF-to-image conversion
- image OCR execution
- DOC/DOCX text extraction path
- deterministic results path logic where still appropriate

Must add or change:

- target canonical field writing
- page-level metadata
- confidence structures
- engine traceability fields
- preprocessing integration
- partial execution support
- manifest updates
- target error handling

Required outcome:

- OCR output aligns to approved canonical expectations
- OCR no longer writes only the legacy thin schema

## Step 7 — Build table extraction pipeline

Objective:

Implement table extraction as an independent modular pipeline.

Current status:

- no live reusable deployed implementation found

Must produce:

- page-level table outputs
- table IDs
- rows/cells structure
- confidence where supported
- manifest updates
- partial-failure handling

Required outcome:

- table extraction is independent and target-compliant

## Step 8 — Build logo/template recognition pipeline

Objective:

Implement logo/template recognition as an independent modular pipeline.

Current status:

- no live reusable deployed implementation found

Must produce:

- logo detections
- template matches
- confidence and engine metadata
- manifest updates
- partial-failure handling

Required outcome:

- logo/template recognition is independent and target-compliant

## Step 9 — Build fraud/anomaly pipeline

Objective:

Implement fraud detection as an independent modular pipeline.

Current status:

- no live reusable deployed implementation found

Must produce:

- fraud flags
- confidence/risk outputs
- manifest updates
- partial-failure handling
- traceable error handling

Required outcome:

- fraud pipeline is independent and target-compliant

## Step 10 — Refactor detailed extraction wrapper

Objective:

Retain useful contract-driven extraction, but move it into the approved modular architecture.

Reuse from current app:

- contract registry pattern
- service enablement filtering
- structured extraction wrapper pattern
- document-type modularity pattern

Must add or change:

- target output mapping
- target pipeline boundaries
- target secrets/config handling
- target stage and manifest updates
- removal of broken DB-status dependency path
- separation from responsibilities that belong to table/logo/fraud pipelines

Required outcome:

- AI enrichment is one clean modular component, not the whole architecture

## Step 11 — Build canonical aggregation layer

Objective:

Create the target canonical aggregator that merges outputs from:

- preprocessing
- OCR
- table extraction
- logo/template recognition
- fraud detection
- AI enrichment where applicable

Important:

Do not use current OCR or detailed artifacts as final canonical output.

Required outcome:

- canonical output is produced only by the target aggregator
- canonical output conforms to approved schema direction and Phase 3 audit requirements

## Step 12 — Build target orchestration

Objective:

Implement approved orchestration using target AWS services and naming.

Must support:

- page-level flow
- batch-level flow
- future streaming/very-large-document path
- modular pipeline selection
- partial reprocessing
- retries
- failure isolation
- multi-document/multi-user workflow isolation

Current status:

- no live Step Functions
- no live ECS services/tasks

Required outcome:

- orchestration matches Phase 2 and Phase 4 target design
- legacy queue flow may inform implementation, but is not the final architecture by itself

## Step 13 — Build target observability and controls

Objective:

Add target logging, monitoring, and operational controls.

Must include:

- CloudWatch logs aligned to target names
- queue alarms
- workflow alarms
- retry visibility
- partial-failure visibility
- manifest consistency checks
- operational traces where required

Required outcome:

- production supportability is aligned with target design

## Step 14 — Build result retrieval/output interface

Objective:

Adapt the current result retrieval pattern into target-compliant output retrieval.

Reuse from current app:

- not-ready vs ready response behavior
- multi-artifact aggregation pattern

Must add or change:

- canonical-output-first response behavior
- target manifest-aware status reporting
- partial processing status exposure
- target naming and paths

Required outcome:

- retrieval path exposes target outputs, not legacy internal artifact structures

## Step 15 — Controlled testing

Objective:

Validate reused and rebuilt components against the evaluation framework.

Test categories required:

- single-page upload
- small multi-page document
- large document
- partial reprocessing
- OCR-only
- OCR + tables
- OCR + fraud
- OCR + logos/templates
- full pipeline
- failure injection / retry
- manifest integrity
- canonical schema integrity

Seed inputs may include:

- existing results bucket sample cases
- existing local OCR sample artifacts
- controlled new test documents

Required outcome:

- evaluation framework evidence exists before production approval

## 6. Developer Work Packaging

Recommended implementation work packages:

### Work Package A — Reuse extraction
- extract reusable source components
- classify each as reuse/adapt/reference-only

### Work Package B — Target manifest and state model
- implement manifest
- define field mappings from current state

### Work Package C — Intake + preprocessing + OCR
- refactor intake
- build preprocessing
- adapt OCR engine

### Work Package D — New modular pipelines
- table extraction
- logo/template recognition
- fraud detection

### Work Package E — AI enrichment + aggregation
- adapt contract registry / agentic parser
- build canonical aggregator
- adapt result retrieval

### Work Package F — Orchestration and observability
- Step Functions
- ECS where required
- alarms/logging/controls

### Work Package G — Test and benchmark
- scenario tests
- performance tests
- schema validation
- failure/retry tests

## 7. Build Stop Conditions

Development must stop and be diagnosed if any of the following occur:

- reused component cannot be evidenced from source/live inspection
- reused code conflicts with approved schema
- reused code conflicts with approved architecture
- reused code prevents modularity/extensibility
- reused code breaks partial processing requirements
- reused code introduces undocumented hard-coded behavior
- manifest/state changes are proposed without evidence
- pipeline implementation proceeds without verification

## 8. Definition of Done

Phase 4 build work is only complete when:

- reusable components have been extracted and controlled
- all required new target pipelines have been implemented
- canonical output aligns to approved target model
- manifest/state tracking aligns to approved target model
- orchestration aligns to approved target design
- partial processing and retries are supported
- old code carried forward is explicit and justified
- evaluation framework tests have been completed
- developers can identify exactly which legacy code was retained and why

## 9. Developer Interpretation Rule

Developers must interpret the reuse assessment and this build plan together.

The reuse assessment answers:

- what exists
- what can be reused
- what cannot be reused
- where the risks are

This build plan answers:

- what order to build in
- what to extract first
- what to refactor
- what must be built new

