# Pipeline Execution Contract

## 1. Purpose

Define the authoritative runtime contract for the OCR Rebuild platform as a hybrid, modular, continuously improving document intelligence system.

This document is the single source of truth for:
- orchestration payload passed between pipeline stages
- mandatory and optional capability execution semantics
- embedded execution plan semantics
- internal and external provider substitution rules
- fallback and escalation semantics
- manifest update semantics
- canonical output assembly semantics
- evaluation and routing traceability requirements

This contract exists to prevent drift between:
- Step Functions orchestration
- Lambda and ECS worker implementations
- internal capability modules
- external API-backed capability adapters
- manifest lifecycle behavior
- canonical output assembly
- project documentation
- deployed AWS runtime behavior

## 2. Scope

This contract applies to:
- manifest generation
- normalization
- preprocessing
- OCR
- structured extraction modules
- enrichment modules
- fallback / escalation routing
- aggregation
- evaluation and traceability metadata

It governs both:
- state passed between stages
- capability-specific enrichment behavior
- routing and provider-selection behavior
- execution plan preservation and update behavior

Local temp files, container-local artifacts, and internal worker implementation details are not the authoritative inter-stage contract.

## 3. Core Principles

### 3.1 Contract-first orchestration
All stages must consume and return a structured orchestration payload.

### 3.2 Stateless workers
Workers must not rely on durable local state between stages.

### 3.3 Manifest-centric control
Manifest state remains the durable execution control record.

### 3.4 Capability-modular execution
The pipeline consists of modular capability domains that may be:
- internal
- open-source based
- external API-backed
- placeholder-backed for future implementation

### 3.5 Client outcome first
Routing and provider selection must prioritize client outcome over engine purity.

### 3.6 Append and enrich, do not destructively replace
Stages must preserve required prior payload fields and add their own outputs without removing required upstream state.

### 3.7 Substitution without redesign
External providers and internal modules must be interchangeable through stable contract fields and routing semantics.

### 3.8 Embedded execution plan baseline
For the current governed baseline, the execution plan is embedded directly in the runtime payload and must be preserved through all stages.

## 4. Authoritative Top-Level Execution Payload

The pipeline execution payload must support the following top-level structure:

    {
      "manifest_id": "string",
      "document_id": "string",
      "source_uri": "string",
      "source_bucket": "string",
      "source_batch_uri": "string",
      "document_type": "string",
      "expected_document_type": "string",
      "ingestion_timestamp": "ISO-8601 string",
      "creation_timestamp": "ISO-8601 string",
      "processing_parameters": {},
      "requested_services": {
        "ocr": true,
        "table_extraction": false,
        "logo_recognition": false,
        "fraud_detection": false
      },
      "service_status": {
        "ocr": "requested",
        "table_extraction": "not_requested",
        "logo_recognition": "not_requested",
        "fraud_detection": "not_requested"
      },
      "execution_state": {
        "current_stage": "string",
        "completed_stages": [],
        "failed_stages": [],
        "skipped_stages": []
      },
      "documents": [],
      "pages": [],
      "execution_plan": {},
      "routing_decision": {},
      "evaluation": {},
      "manifest_update": {}
    }

## 5. Required Top-Level Fields

The following fields are the minimum controlled execution contract.

### 5.1 Required identifiers
- `manifest_id`
- `document_id`

### 5.2 Required source tracking
- `source_uri`

### 5.3 Required document scope tracking
- `documents`

### 5.4 Required service selection
- `requested_services`

### 5.5 Required service lifecycle tracking
- `service_status`

### 5.6 Required page payload
- `pages`

### 5.7 Required execution intent
- `execution_plan`

### 5.8 Required routing traceability
- `routing_decision`

### 5.9 Required evaluation traceability
- `evaluation`

### 5.10 Required manifest update payload
- `manifest_update`

## 6. Requested Services Semantics

### 6.1 Service categories

#### Mandatory baseline
- `ocr`

#### Optional current baseline
- `table_extraction`
- `logo_recognition`
- `fraud_detection`

#### Future governed capability domains
The contract must remain extensible for future requested service selection such as:
- handwriting
- key_value_extraction
- signature_detection
- checkbox_detection
- barcode_extraction
- language_detection
- layout_analysis
- font_analysis
- image_region_extraction
- formula_extraction
- authenticity_scoring
- tamper_detection
- clause_extraction
- question_answer_support

### 6.2 Defaults
If omitted by the caller:
- `ocr` defaults to `true`
- currently optional baseline services default to `false`

### 6.3 Allowed values
Each requested service flag must be boolean unless a future governed extension introduces richer selection semantics.

### 6.4 Execution rule
A service or capability domain may only execute if:
- it is mandatory, or
- it is explicitly requested, or
- governed routing rules require it for fallback or client outcome protection, or
- it is required by the embedded execution plan to fulfill the selected service

## 7. Service Status Semantics

The `service_status` object is authoritative for service execution interpretation.

Allowed normalized states:
- `requested`
- `not_requested`
- `skipped`
- `processing`
- `completed`
- `failed`
- `partial`

### 7.1 Required meaning of each state

#### `requested`
The service was selected for execution but has not yet completed.

#### `not_requested`
The service was not selected and must not be treated as expected output.

#### `skipped`
The service was requested but intentionally not executed due to rule, routing, substitution logic, bundled output reuse, or controlled skip logic.

#### `processing`
The service is in progress.

#### `completed`
The service finished successfully.

#### `failed`
The service was attempted but failed.

#### `partial`
The service completed only partially and produced partial output.

## 8. Embedded Execution Plan Semantics

The `execution_plan` object is the authoritative embedded execution instruction set for the current runtime payload.

It carries:
- service intent
- required and optional capabilities
- provider/module selection by capability
- bundled provider reuse semantics
- fallback policy
- document and page overrides
- decision gate history
- plan lifecycle status

### 8.1 Runtime rule
All stages must preserve the embedded `execution_plan`.

### 8.2 Stage limitation rule
Stages may read and update the plan only in controlled ways relevant to their responsibility.

### 8.3 Material change rule
Any material change to provider assignment, fallback path, reroute, or capability activation must be:
- reflected in `execution_plan`
- captured in decision/gate history
- summarised in `routing_decision`
- supported by evidence in `evaluation`

## 9. Stage-by-Stage Contract

## 9.1 GenerateManifest

### Input
May accept either:
- a single-document request, or
- a batch-style request, or
- a project-style request

Minimum expected input:
- `manifest_id`
- `document_id`
- `source_uri`

### Output
Must produce:
- normalized execution payload
- initialized `requested_services`
- initialized `service_status`
- initialized `execution_state`
- initialized `manifest_update`
- `documents`
- normalized top-level identifiers
- initial `execution_plan`
- initial `routing_decision`
- initial `evaluation`

### Rules
- must not leave execution payload fragmented across unrelated wrapper objects
- must normalize input into the authoritative contract shape
- if Gate 0 or equivalent upstream composition has already created an execution plan, it must be carried forward, not discarded

## 9.2 Preprocessing

### Input
Must consume:
- top-level execution payload
- `source_bucket`
- `source_uri`
- `documents`
- `pages` or sufficient source information to derive pages
- relevant instructions from `execution_plan`

### Output
Must preserve:
- identifiers
- document scope
- requested services
- service status
- execution state
- execution plan
- routing traceability
- evaluation traceability
- manifest update

Must normalize or enrich `pages` with:
- `document_id`
- `page_number`
- source page location metadata
- processed page location metadata
- `rotation_angle`
- `orientation`
- `preprocessing_params`

### Rules
- preprocessing is responsible for controlled source normalization for OCR-eligible inputs when governed page records do not already exist
- preprocessing must support deterministic page ordering
- preprocessing must not remove or reset requested service selections
- preprocessing must preserve the embedded execution plan
- preprocessing completion must update execution and manifest state
- preprocessing must not route structured-digital source classes into raster OCR-first processing unless explicitly governed
- preprocessing may add normalization evidence useful to later gates

## 9.2.1 Input normalization semantics

### Manifest scope
A single execution payload may represent:
- one logical document, or
- multiple logical documents in one manifest/project scope

### Document scope
`documents[]` is the authoritative list of logical documents in execution scope.

Each logical document must support:
- `document_id`
- `source_uri` or equivalent source lineage
- `expected_document_type` where available

### Page scope
`pages[]` is the authoritative OCR-processing page list.

Each page record must belong to a logical document and support deterministic page ordering.

### OCR-eligible source classes
The following classes normalize into page records for preprocessing and OCR:
- single-image documents
- multi-page PDFs
- multi-page TIFF where supported
- page-by-page assembled image documents

### Structured-digital source classes
The following classes are not OCR-first by default:
- CSV
- XLSX
- DOCX
- text-native PDFs
- machine-readable structured files

Until a governed structured extraction path exists, these must be rejected, marked unsupported for the OCR path, or handled only under an explicitly approved temporary rule.

### Grouping rules
Where multiple uploaded objects are present, normalization must distinguish between:
- many pages of one logical document
- many separate logical documents
- one project containing multiple logical documents

This distinction must come from:
- explicit caller metadata, or
- approved deterministic grouping rules

Workers must not make uncontrolled grouping guesses.

## 9.3 OCR

### Input
Must consume:
- normalized execution payload
- preprocessed page references in `pages`
- `execution_plan.capability_plan.TEXT_OCR` or equivalent governed OCR instruction

### Output
Must preserve upstream payload and enrich `pages` with:
- `extracted_text`
- `line_block_word_confidence`
- `engine_name`
- `engine_version`

### Rules
- OCR is mandatory unless explicitly governed otherwise in a future approved design change
- OCR completion must set `service_status.ocr = completed` on success
- OCR stages must emit enough metadata for quality-based acceptance or fallback escalation
- OCR must preserve the embedded execution plan
- OCR must not invent provider logic outside the plan unless a gate-driven adjustment has occurred

## 9.3.1 Canonical output semantics

### Logical document rule
Canonical output is defined per logical document, not per manifest as a whole.

### Multi-document manifest rule
If a manifest contains multiple logical documents:
- each document must remain attributable to its own `document_id`
- aggregation must support one canonical document per logical document
- a future project-level summary may exist, but it must not replace document-level canonical outputs

### Current implementation rule
The current implementation may continue to assemble one canonical document for a single-document manifest without redesign.
Multi-document canonical bundle behavior may be added as a controlled extension.

## 9.4 Table Extraction

### Input
Must consume:
- upstream execution payload
- OCR-enriched pages or other governed extraction-ready page structures
- relevant capability entries from `execution_plan.capability_plan`

### Output
Must preserve upstream payload and enrich the appropriate page/document structures with table results.

### Rules
- may be internal, heuristic, or external-provider backed
- substitution of implementation must not break page/document contract shape
- must preserve bundled provider reuse semantics where relevant
- must avoid duplicate extraction if bundled outputs already satisfy required coverage
- must preserve the embedded execution plan

## 9.5 Logo / Template Recognition

### Input
Must consume:
- upstream execution payload
- page/document structures sufficient for template or logo detection
- relevant capability or service instruction from the embedded plan

### Output
Must preserve upstream payload and enrich page/document metadata with logo/template results.

### Rules
- may be heuristic initially
- future replacements may be model-based or provider-backed without contract redesign
- must preserve the embedded execution plan

## 9.6 Fraud Detection / Authenticity / Related Trust Signals

### Input
Must consume:
- upstream execution payload
- OCR and/or structured extraction outputs as required
- relevant capability entries from the embedded plan

### Output
Must preserve upstream payload and enrich page/document metadata with fraud, authenticity, or anomaly signals.

### Rules
- may begin as heuristic
- future replacements may be more advanced without breaking contract structure
- must preserve the embedded execution plan
- should write supporting evidence into `evaluation`

## 9.7 Future Intelligence Modules

The contract must remain forward-compatible with future modules such as:
- handwriting recognition
- key-value extraction
- signature detection
- checkbox detection
- barcode extraction
- language detection
- layout analysis
- font analysis
- image/figure extraction
- formula extraction
- clause extraction
- question-answer support

Each such module must:
- preserve upstream payload
- enrich controlled output fields
- update `service_status` where governed
- read the relevant capability entries from `execution_plan`
- update `routing_decision` where provider or path choice matters
- update `evaluation` where quality/completeness signals are produced

## 9.8 Aggregation

### Input
Must consume:
- full enriched execution payload after prior capability execution
- final state of the embedded `execution_plan`

### Output
Must produce:
- document-level canonical outputs
- updated manifest state
- preserved routing lineage
- preserved evaluation metadata suitable for later analysis
- preserved final execution plan

### Rules
- aggregation must not erase provider-selection lineage
- aggregation must preserve explainability of accepted/fallback paths
- aggregation must support current single-document implementation and future multi-document expansion
- aggregation is where the final executed path becomes durable lineage

## 10. Routing Decision Contract

The `routing_decision` object is authoritative for the summarised runtime view of how the platform chose and adjusted capability paths.

It should support fields such as:
- selected_strategy
- primary_provider_summary
- fallback_used
- fallback_provider
- fallback_reason
- selected_capability_path
- decision_basis
- document_route
- page_route_overrides
- current_route_state
- last_gate_applied

The exact implementation may evolve, but routing traceability must exist from the first governed hybrid baseline.

The `routing_decision` object must remain consistent with, but may be simpler than, the richer embedded `execution_plan`.

## 11. Evaluation Contract

The `evaluation` object is authoritative for execution quality and improvement signals.

It should support fields such as:
- quality_score
- completeness_score
- confidence_summary
- required_fields_present
- required_fields_missing
- routing_acceptance_reason
- benchmark_tags
- capability_evidence
- future correction / review metadata

The exact implementation may evolve, but evaluation traceability must exist from the first governed hybrid baseline.

The `evaluation` object is the evidence base for:
- fallback activation
- reroute decisions
- partial acceptance
- final acceptance or rejection

## 12. Manifest Update Semantics

The `manifest_update` object remains the durable execution control update.

It must continue to support:
- manifest identifiers
- pipeline status
- retry state
- service status
- client notification state
- pipeline history

It must also remain extensible for:
- multi-document semantics
- routing traceability pointers
- evaluation summary pointers
- controlled future provider-substitution metadata

## 13. Preservation Rules

Stages must preserve the following unless there is an approved contract revision:
- `manifest_id`
- `document_id`
- `source_uri`
- `requested_services`
- `service_status`
- `documents`
- `pages`
- `execution_plan`
- `routing_decision`
- `evaluation`
- `manifest_update`

No stage may silently remove required upstream fields.

## 14. Current Baseline Decision

Effective immediately:
- OCR Rebuild must treat the execution payload as a hybrid capability orchestration contract
- the embedded execution plan is the authoritative runtime instruction object
- preprocessing must no longer be assumed to receive pre-built pages for all requests
- provider substitution and fallback must be supported without redesign
- execution traceability must be preserved for future cost/quality optimization
