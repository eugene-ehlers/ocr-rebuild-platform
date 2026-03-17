# Pipeline Execution Contract
## 1. Purpose

Define the authoritative runtime contract for the OCR Rebuild pipeline.

This document is the single source of truth for:

- orchestration payload passed between pipeline stages
- mandatory and optional service execution semantics
- stage input and output expectations
- manifest update semantics
- aggregation semantics for completed, skipped, failed, and unrequested services
This contract exists to prevent drift between:

- Step Functions orchestration
- Lambda and ECS worker implementations
- manifest lifecycle behavior
- canonical output assembly
- project documentation
- deployed AWS runtime behavior
## 2. Scope

This contract applies to:

- manifest generation
- preprocessing
- OCR
- table extraction
- logo/template recognition
- fraud detection
- aggregation

It governs both:

- state passed between stages
- service-specific enrichment behavior

Local temp files, container-local artifacts, and internal worker implementation details are not the authoritative inter-stage contract.
## 3. Core Principles

### 3.1 Contract-first orchestration
All stages must consume and return a structured orchestration payload.

### 3.2 Stateless workers
Workers must not rely on durable local state between stages.

### 3.3 Manifest-centric control
Manifest state remains the durable execution control record.

### 3.4 Mandatory core, optional enrichments
The pipeline consists of:

- mandatory core path:
  - manifest generation
  - preprocessing
  - OCR
- optional enrichment path:
  - table extraction
  - logo/template recognition
  - fraud detection
- mandatory finalization:
  - aggregation

### 3.5 Append and enrich, do not destructively replace
Stages must preserve required prior payload fields and add their own outputs without removing required upstream state.
## 4. Authoritative Top-Level Execution Payload

The pipeline execution payload must support the following top-level structure.

```json
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
  "manifest_update": {}
}
## 5. Required Top-Level Fields

The following fields are the minimum controlled execution contract.

### 5.1 Required identifiers
- `manifest_id`
- `document_id`

### 5.2 Required source tracking
- `source_uri`

### 5.3 Required service selection
- `requested_services`

### 5.4 Required service lifecycle tracking
- `service_status`

### 5.5 Required page payload
- `pages`

### 5.6 Required manifest update payload
- `manifest_update`
## 6. Requested Services Semantics

### 6.1 Service categories

#### Mandatory
- `ocr`

#### Optional
- `table_extraction`
- `logo_recognition`
- `fraud_detection`

### 6.2 Defaults
If omitted by the caller:

- `ocr` defaults to `true`
- all optional services default to `false`

### 6.3 Allowed values
Each requested service flag must be boolean.

### 6.4 Execution rule
A service may only execute if:
- it is mandatory, or
- it is explicitly requested
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
The service was requested but intentionally not executed due to rule, routing, or controlled skip logic.

#### `processing`
The service is in progress.

#### `completed`
The service finished successfully.

#### `failed`
The service was attempted but failed.

#### `partial`
The service completed only partially and produced partial output.
## 8. Stage-by-Stage Contract

## 8.1 GenerateManifest

### Input
May accept either:
- a single-document request, or
- a batch-style request

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

### Rules
- must not leave execution payload fragmented across unrelated wrapper objects
- must normalize input into the authoritative contract shape
## 8.2 Preprocessing

### Input
Must consume:
- top-level execution payload
- `source_bucket`
- `pages` or sufficient source information to derive pages

### Output
Must preserve:
- identifiers
- requested services
- service status
- execution state
- manifest update

Must enrich `pages` with:
- `page_number`
- `rotation_angle`
- `orientation`
- `preprocessing_params`
- processed page location metadata

### Rules
- preprocessing must not remove or reset requested service selections
- preprocessing completion must update execution and manifest state
## 8.3 OCR

### Input
Must consume:
- normalized execution payload
- preprocessed page references in `pages`

### Output
Must preserve upstream payload and enrich `pages` with:
- `extracted_text`
- `line_block_word_confidence`
- `engine_name`
- `engine_version`

### Rules
- OCR is mandatory unless explicitly governed otherwise in a future approved design change
- OCR completion must set `service_status.ocr = completed` on success
## 8.4 Table Extraction

### Input
Must consume:
- normalized execution payload
- OCR-enriched `pages`

### Output
Must preserve upstream payload and enrich pages with:
- `tables`

### Rules
- if `requested_services.table_extraction = false`, the stage must not be treated as expected output
- absence due to not requested is not an error
## 8.5 Logo / Template Recognition

### Input
Must consume:
- normalized execution payload
- OCR-enriched `pages`

### Output
Must preserve upstream payload and enrich page metadata with:
- detected logos / template findings

### Rules
- if `requested_services.logo_recognition = false`, absence is not an error
## 8.6 Fraud Detection

### Input
Must consume:
- normalized execution payload
- OCR-enriched `pages`

### Output
Must preserve upstream payload and enrich page metadata with:
- fraud flags
- fraud-related findings

### Rules
- if `requested_services.fraud_detection = false`, absence is not an error
## 8.7 Aggregation

### Input
Must consume:
- normalized execution payload
- all prior mandatory outputs
- any optional enrichment outputs that were requested and completed or partially completed

### Output
Must produce:
- `canonical_document`
- final `manifest_update`
- final aggregation metadata

### Rules
Aggregation must:
- treat OCR as mandatory
- treat optional enrichments as optional
- distinguish:
  - `not_requested`
  - `skipped`
  - `failed`
  - `partial`
  - `completed`
- produce semantically correct canonical output even when optional enrichments are absent
## 9. Manifest Update Contract

The `manifest_update` section is the authoritative inter-stage manifest mutation payload.

It must support at minimum:

```json
{
  "manifest_id": "string",
  "documents": [],
  "processing_parameters": {},
  "pipeline_status": "pending|processing|completed|failed|partial|UNKNOWN",
  "retry_count": 0,
  "last_updated": "ISO-8601 string",
  "partial_execution_flags": {},
  "client_notification": {
    "required": false,
    "status": "not_required",
    "message": ""
  },
  "service_status": {
    "ocr": "requested",
    "table_extraction": "not_requested",
    "logo_recognition": "not_requested",
    "fraud_detection": "not_requested"
  },
  "pipeline_history": []
}
### 9.1 Required manifest semantics
Manifest updates must explicitly record:
- requested services
- executed services
- skipped services
- failed services
- partial services

### 9.2 Pipeline history rules
`pipeline_history` must be append-only.

Each history item should include:
- `stage`
- `status`
- `timestamp`

And may include:
- `engine_name`
- `engine_version`
- `notes`
## 10. Execution State Contract

`execution_state` is the orchestration-facing transient control state.

Expected structure:

```json
{
  "current_stage": "string",
  "completed_stages": [],
  "failed_stages": [],
  "skipped_stages": []
}
## 11. Aggregation Semantics

Aggregation must interpret optional services according to the following rules:

| Service state | Aggregation expectation | Error condition |
| --- | --- | --- |
| `not_requested` | Do not expect output | No |
| `skipped` | Do not expect output, but record skip semantics | No |
| `completed` | Include output if present | Yes, if expected output is missing without explanation |
| `partial` | Include partial output with explicit partial semantics | No, unless contract-required fields are missing |
| `failed` | Do not fabricate output; record failure semantics | No, unless failure handling contract is violated |
## 12. Preservation Rules

Stages must preserve the following unless there is an approved contract revision:

- `manifest_id`
- `document_id`
- `source_uri`
- `requested_services`
- `service_status`
- `pages`
- `manifest_update`

No stage may silently remove required upstream fields.

## 13. Error, Retry, and Partial Execution Rules

### 13.1 Failure
A stage failure must:
- update `service_status` appropriately
- update `manifest_update.pipeline_status` appropriately
- append pipeline history

### 13.2 Retry
Retries must:
- increment retry semantics in manifest where applicable
- not corrupt prior successful outputs
- preserve idempotent behavior as far as practical

### 13.3 Partial execution
Partial execution must be explicitly represented in:
- `service_status`
- `partial_execution_flags`
- `pipeline_history`

## 14. Implementation Rules

### 14.1 Preferred worker model
Preferred model:
- direct structured payload consumption and emission

### 14.2 Allowed local file usage
Local files may be used:
- as internal worker implementation detail
- for temporary artifact handling

Local files must not be the authoritative inter-stage contract.

### 14.3 Orchestration model
Preferred orchestration model:
- mandatory core path
- conditional optional service execution
- mandatory aggregation/finalization

## 15. Document Authority and Change Control

This document is authoritative for pipeline runtime contract behavior.

No changes to:
- stage payload shape
- requested service semantics
- service status semantics
- manifest inter-stage semantics
- aggregation absence/failure semantics

may be implemented unless this contract is updated first or in the same controlled change set.

## 16. Current Gap Summary

At the time of creation of this document, the platform has the following known alignment gaps:

- deployed Step Functions skeleton exists
- worker input/output contracts are not yet fully normalized to this contract
- optional service selection is not yet fully implemented in orchestration
- manifest schema does not yet explicitly encode all service-status semantics defined here

These gaps must be resolved in controlled follow-on implementation steps.
