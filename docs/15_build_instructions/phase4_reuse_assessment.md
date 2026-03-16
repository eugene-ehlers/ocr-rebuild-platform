# Phase 4 Reuse Assessment

## 1. Purpose

Assess the existing OCR application against the approved OCR Rebuild target state to determine what can be reused, reused with modification, replaced, or is missing.

## 2. Scope

This assessment covers the live existing OCR application in AWS and local CloudShell source/workspace evidence for:

- OCR page-processing code
- preprocessing logic
- table extraction logic
- fraud / anomaly checks
- logo / template recognition logic
- document manifest handling
- canonical output generation
- upload / page splitting / document decomposition logic
- retry / error handling logic
- logging / monitoring hooks
- existing AWS resource definitions
- existing Lambda handlers / containers / task scripts
- existing naming conventions
- existing config / env vars / bucket usage
- existing test harnesses or sample documents

## 3. Existing system inspected

### 3.1 Live deployed OCR components verified

- `OcrIngestStub-dev` Lambda
- `OcrIngestContainer-dev` Lambda (image-based, ECR-backed)
- `OcrQuickWorker-dev` Lambda
- `OcrDetailedWorker-dev` Lambda
- `OcrGetResult-dev` Lambda
- `agentic-parser` Lambda
- S3 buckets:
  - `ocrsvc-dev-uploads`
  - `ocrsvc-dev-results`
  - `ocrsvc-dev-logs`
  - `ocrsvc-dev-artifacts`
- SQS queues:
  - `OcrQuickQueue-dev`
  - `OcrDetailedQueue-dev`
  - `OcrAgenticQueue-dev`
  - `QuickResultReadyQueue-dev`
  - `DetailedResultReadyQueue-dev`
- ECR repository:
  - `ocr-engine-dev:v10`
- Database table:
  - `public.document_run`

### 3.2 Governing / target-state documents read

- `working_method_and_change_control.md`
- `evaluation_framework.md`
- `phase2_logical_architecture.md`
- `phase2_hybrid_workflow.mmd`
- `phase3_pipeline_docs.md`
- `canonical_document_schema.json`
- `document_manifest_schema.json`
- `phase3_schema_audit.log`
- `phase4_implementation_design.md`

## 4. Reuse assessment summary

The current OCR application contains real reusable assets for:

- upload-triggered ingestion
- OCR execution
- results path construction
- quality scoring and routing
- queue-based quick vs detailed branching
- document-type contract registry
- detailed AI extraction wrapper
- result retrieval / aggregation API pattern
- basic CloudWatch logging and SQS-trigger wiring
- sample result artifacts and packaged source backups

The current OCR application does **not** contain approved-target reusable implementations for:

- preprocessing pipeline
- table extraction pipeline
- fraud pipeline
- logo/template recognition pipeline
- rebuild target manifest schema
- rebuild target canonical schema
- Step Functions orchestration
- ECS task architecture
- target naming convention alignment
- partial processing architecture at rebuild target level
- page/batch/streaming hybrid orchestration at rebuild target level

## 5. Component-by-component reuse table

| Current Component | Current Location | Current Purpose | Target Component | Reuse Decision | Evidence | Required Changes | Risks | Notes |
|---|---|---|---|---|---|---|---|---|
| Upload-triggered ingestion Lambda | `OcrIngestStub-dev`, local `~/OcrIngestStub-src/index.js` | Intake from S3 upload, DB lookup, invoke OCR, wait for OCR, quality score, queue route | Intake/orchestration entrypoint | REUSE_WITH_MODIFICATION | Live config shows S3 upload trigger to `OcrIngestStub-dev`; source shows DB lookup, OCR invoke, wait loop, quality scoring, queue routing | Rename to target convention, remove hard-coded current bucket/DB assumptions, refactor to target manifest updates, align to Phase 2/4 orchestration model | Current design is single-flow and DB-centric, not target manifest-centric; synchronous wait can timeout on large docs | Strong reuse candidate for intake/routing logic only |
| OCR engine container | `OcrIngestContainer-dev`, ECR `ocr-engine-dev:v10`, `/var/task/app.py` | OCR on images/PDF/DOCX/DOC using Tesseract, pdftoppm, antiword; writes `ocr_result.json` | OCR engine | REUSE_WITH_MODIFICATION | Live image inspected; `app.py` performs PDF→images→Tesseract, DOC/DOCX extraction, writes OCR JSON to results bucket | Wrap or adapt output to target canonical schema; add page metadata, confidence structures, engine metadata, preprocessing hooks, manifest updates | Output schema is too thin; no target confidence granularity; no preprocessing stage separation; no partial pipeline reporting | This is the strongest candidate for direct code reuse in page-by-page OCR |
| OCR output structure | Sample `ocr_result.json` in `ocrsvc-dev-results` | Current OCR artifact persisted to S3 | Canonical page output | REPLACE | Sample shows fields `engine_version`, `pages[].text`, `confidence`, `full_text`, `statement_summary`, `transactions`, `error` | Redesign output mapping to approved canonical schema | Current artifact does not match Phase 3 schema audit requirements | Can be used only as source input, not target output |
| OCR quality scoring and routing logic | `~/OcrIngestStub-src/index.js` | Compute QC scores and decide quick vs deep route | Routing / benchmark / evaluation support | REUSE_WITH_MODIFICATION | Source shows `computeQualityScores`, acceptable/not-acceptable gating, `routing_mode` selection | Externalize thresholds/config, align doc types, integrate with manifest/status model, target naming | Current logic is embedded in ingest Lambda and tied to current DB schema | Useful operational logic, not target-complete architecture |
| Quick worker | Live package `/tmp/ocr_live_packages/quick_worker/index.js` | Wait for OCR readiness, write `quick_result.json`, update DB stage | Quick-path pipeline component | REUSE_WITH_MODIFICATION | Live code inspected from Lambda package | Align to target canonical/manifest schemas, determine whether quick path remains valid in approved design, add proper manifest tracking | Current quick result is placeholder-style with empty fields and DB coupling | Reusable wrapper pattern, not reusable as target output model |
| Detailed worker | Live package `/tmp/ocr_live_packages/detailed_worker/index.js` | Validate contract/doc type, filter services, enqueue agentic-parser, update stage, error artifact writing | Detailed pipeline orchestrator | REUSE_WITH_MODIFICATION | Live code inspected; SQS event mapping exists; writes detailed error artifacts and stages | Rename to target convention, remove current DB assumptions, integrate manifest updates, align service routing with approved modular pipeline design | No target manifest logic; no Step Functions; no table/fraud/logo branches | Good reusable wrapper/orchestration pattern for deep analysis branch |
| Contract registry / service gating | Live package `detailed_worker/shared/contractsRegistry.mjs` | Document-type service registry and enablement rules | Modular document-type contract layer | REUSE_WITH_MODIFICATION | Contract registry inspected; doc types include bank statements, payslips, IDs, proof of address, tax certificates, financial statements, etc. | Convert to rebuild-owned contract/config layer, align names and supported services to target architecture, separate unsupported target pipelines | Current contracts assume Tesseract/agentic flow and some services marked false; not tied to target schemas | Strong reuse candidate for modularity/extensibility foundation |
| Agentic parser | `agentic-parser` Lambda, local `~/agentic-parser-src/lambda_function.py` | Contract-driven AI extraction from OCR JSON, writes `detailed_result.json` | Detailed extraction / classification / ratios / risk wrapper | REUSE_WITH_MODIFICATION | Live code and logs inspected; SQS triggered; writes structured JSON | Remove direct OpenAI key dependency from env, harden DB/status updates, align output to target canonical schema, separate fraud/logo/table from generic AI result | Logs show DB stage update failure (`No module named 'pg8000.legacy'`); output not target canonical schema | Reusable for contract-based structured extraction only |
| Detailed result structure | Sample `detailed_result.json` in `ocrsvc-dev-results` | Current detailed AI artifact | Canonical aggregated output | REUSE_WITH_MODIFICATION | Sample shows useful structured extraction, classification, ratios, risk score | Map into target canonical model and manifest update flow; preserve useful structured fields as enrichment only | Not aligned to approved canonical schema; lacks page/table/logo/fraud canonical nesting | Useful as intermediate enrichment artifact |
| Result retrieval Lambda | Live package `/tmp/ocr_live_packages/get_result/index.js` | Return combined OCR/quick/detailed results to caller | Aggregation / retrieval API | REUSE_WITH_MODIFICATION | Live code inspected; combines DB + S3, returns 202 when not ready, derives fields | Adapt to rebuild result model, manifest-based status, target naming, and target API contracts | Current logic tied to current DB and current artifact names | Good reusable retrieval/aggregation pattern |
| Upload/document decomposition path scheme | `OcrIngestStub-src/index.js`, OCR engine `app.py`, sample S3 paths | Derive result paths from upload key and UUID | Document decomposition / storage layout | REUSE_WITH_MODIFICATION | Live code shows UUID extraction from filename and deterministic result paths | Align to target bucket names and manifest structure | Current pathing tied to `ocrsvc-dev-*` and current run-based storage pattern | Reusable path derivation approach |
| Document run tracking table | PostgreSQL `public.document_run` | Track upload, OCR keys, stage, quality, routing, errors, requested services | Manifest / status tracking | REUSE_WITH_MODIFICATION | Table structure inspected; sample rows queried | Map useful columns to target manifest design or transitional adapter; do not treat as target final schema | Not the approved manifest schema; no `retry_count`, `partial_execution_flags`, `pipeline_history` as required by Phase 3/4 | This is manifest-like tracking, but not target-compliant |
| Manifest implementation | AWS + DB inspection | Target manifest/state tracking | Document manifest schema | REPLACE | No manifest table found; only `document_run` table exists; result bucket contains OCR/detailed files only | Build approved manifest model in target design | Current implementation is not the approved manifest schema | Current state tracking can only inform migration mapping |
| Canonical schema implementation | AWS + sample artifacts | Approved canonical document schema | Canonical schema | REPLACE | Sample OCR and detailed outputs do not match target schema or Phase 3 audit fields | Build new canonical aggregation/output layer | Existing schema too thin and inconsistent with target | Existing outputs are inputs/reference only |
| Preprocessing pipeline | Live Lambda/SQS/ECR search | Preprocess pages before OCR | Preprocessing pipeline | MISSING | No live preprocessing Lambda, queue, or ECR repo found; only placeholder shell/docs exist | Build from scratch or extract later if hidden elsewhere | None from current live OCR app because no evidence found | Placeholder scripts are not implementation evidence |
| Table extraction pipeline | Live Lambda/SQS/ECR search; local `run_table_extraction.sh` | Extract tables | Table extraction pipeline | MISSING | No live deployed table component found; local shell script is simulated placeholder output only | Build from scratch or wrap future engine | Local script is not production code | No reusable live implementation found |
| Fraud/anomaly pipeline | Live Lambda/SQS/ECR search; local `run_fraud_detection.sh` | Fraud detection | Fraud pipeline | MISSING | No live deployed fraud component found; local shell script is simulated placeholder output only | Build from scratch or wrap future engine | Local script is not production code | No reusable live implementation found |
| Logo/template recognition pipeline | Live Lambda/SQS/ECR search; local `run_logo_template_recognition.sh` | Logo/template detection | Logo/template pipeline | MISSING | No live deployed logo/template component found; local shell script is simulated placeholder output only | Build from scratch or wrap future engine | Local script is not production code | No reusable live implementation found |
| Current retry/error handling | `OcrQuickWorker-dev`, `OcrDetailedWorker-dev`, logs | Throw-on-not-ready, SQS retries, stage updates, error artifact write | Retry / fault isolation / recovery | REUSE_WITH_MODIFICATION | Quick worker throws to allow retry; detailed worker writes error artifact and deletes message; logs show timeouts and failure cases | Formalize retry counts and partial execution in target manifest and Step Functions/SQS control | Current retry tracking not aligned to target schema; no target-level retry counters | Reusable patterns, not complete target control model |
| Logging / monitoring hooks | CloudWatch log groups and logs | Runtime logging for OCR flow | Logging / observability | REUSE_WITH_MODIFICATION | Log groups verified; logs show stage progress, timeouts, queue activity, agentic failures | Align naming to target conventions, add target alarms/metrics/X-Ray/Step Functions observability | Logging is basic text logs only; no target observability model | Useful baseline only |
| Existing AWS naming patterns | Live resources | Existing OCR dev environment naming | Target prod naming convention | REPLACE | Current names: `OcrIngestStub-dev`, `ocrsvc-dev-results`, `OcrQuickQueue-dev`, etc. | Rename to target convention in Phase 4 docs | Current naming conflicts with target `<pipeline>-lambda-<function>-prod`, bucket naming, queue/topic naming | Reuse logic, not names |
| Existing Step Functions orchestration | AWS inspection | Workflow orchestration | Step Functions-based orchestration | MISSING | `aws stepfunctions list-state-machines` returned none | Build from scratch | No live reusable implementation | Direct gap against Phase 2/4 target |
| Existing ECS tasks/services | AWS inspection | Heavy pipeline execution | ECS/Fargate target execution | MISSING | No ECS clusters, task definitions, or services found | Build from scratch if target requires ECS | No live reusable implementation | Direct gap against Phase 4 target |
| Existing tests / sample artifacts | Local files and S3 sample outputs | Test and demonstration artifacts | Test harness / validation assets | REUSE_WITH_MODIFICATION | Sample outputs, local zips, `ocr_result.json`, `unified_result.json`, test JSON files, results bucket artifacts found | Curate and classify into controlled rebuild test set | Unknown provenance/coverage; many files are ad hoc | Useful for seed test corpus only |
| Local placeholder pipeline scripts | `run_ocr_pipeline.sh`, `run_table_extraction.sh`, `run_logo_template_recognition.sh`, `run_fraud_detection.sh` | Demonstration scripts for project docs | Production rebuild components | REPLACE | Scripts inspected; each simulates outputs using `jq` placeholders | None; do not reuse as implementation | Misleading if treated as real implementation | Documentation/demo aids only |
| Current quick/detailed queue topology | Live SQS queues and Lambda mappings | Async branching across OCR flow | Queue/task topology | REUSE_WITH_MODIFICATION | Queues and mappings verified | Rename, refactor to target pipeline topology, formalize result-ready/notification behavior | No target partial-processing or Step Functions control | Good basis for async branch patterns |
| Current page splitting / PDF decomposition inside OCR engine | ECR image `/var/task/app.py` | Convert PDF pages to images and OCR each page | Page decomposition | REUSE_WITH_MODIFICATION | `pdftoppm` + per-page Tesseract loop verified in live image | Separate into target preprocessing/OCR stages and add page metadata | Currently bundled inside OCR engine rather than modular preprocessing path | Reusable algorithmic code path |

## 6. Schema alignment implications

### 6.1 Canonical schema alignment

Current live outputs do **not** meet the approved canonical document schema or the enhanced Phase 3 audit expectations.

Observed gaps include:

- no `document_id` in the current OCR artifact sample
- page objects use `text` instead of `extracted_text`
- no `rotation_angle`
- no `orientation`
- no `language_code`
- no `preprocessing_params`
- no `line_block_word_confidence`
- no canonical table structure
- no canonical `pages.metadata` structure matching target
- no `previous_version_id`
- no `multi_layer_text`
- no page-level `engine_name` / `engine_version` in target form

Implication:

- existing OCR and detailed artifacts can be reused as **source/intermediate artifacts only**
- a new target canonical aggregation layer is required

### 6.2 Manifest schema alignment

Current `document_run` is only a **manifest-like** operational table.

Observed gaps against target manifest requirements:

- no `manifest_id`
- no `creation_timestamp` in target manifest form
- no `source_batch_uri`
- no `documents[]` manifest structure
- no explicit target `retry_count`
- no explicit target `partial_execution_flags`
- no target `pipeline_history`
- no target `client_notification`
- no rebuild target `processing_parameters` structure

Implication:

- current `document_run` can inform migration mapping
- it cannot be reused as the approved manifest implementation as-is

## 7. Orchestration alignment implications

### 7.1 Alignment found

Current live OCR application already demonstrates:

- S3 upload-triggered ingestion
- OCR invocation from ingest
- quick vs deep queue routing
- SQS-triggered worker processing
- asynchronous result production
- result retrieval with not-ready responses

### 7.2 Alignment gaps

Current live OCR application does **not** demonstrate:

- Step Functions orchestration
- page-level vs batch-level vs streaming target control
- partial reprocessing architecture at target level
- target manifest-driven retries
- target pipeline modular separation for preprocessing/table/logo/fraud
- ECS/Fargate execution path required by target design

Implication:

- existing orchestration patterns are reusable at code-pattern level
- target orchestration still requires major rebuild work

## 8. Required modifications for reusable components

### 8.1 Ingest / OCR / routing chain

Reusable chain:

- `OcrIngestStub-dev`
- `OcrIngestContainer-dev`
- `OcrQuickWorker-dev`
- `OcrDetailedWorker-dev`
- `OcrGetResult-dev`

Required modifications:

- align names to target convention
- separate preprocessing from OCR where target requires it
- remove dependence on current `document_run` as final state model
- emit target manifest updates
- emit target canonical-compliant output
- externalize routing and quality thresholds
- support target partial reprocessing and modular pipeline selection
- remove long synchronous waiting where it conflicts with target orchestration

### 8.2 Agentic parser / contract registry

Reusable pieces:

- contract registry structure
- service enablement filtering
- contract-driven extraction approach
- structured output pattern

Required modifications:

- move to rebuild-controlled configuration layer
- support target pipeline outputs beyond current OCR/AI-only path
- align output to canonical schema
- fix DB/status write dependency issues
- remove direct secrets-in-env pattern
- separate generic AI enrichment from target fraud/logo/table responsibilities

### 8.3 Database-driven state tracking

Reusable idea:

- run-level operational state record

Required modifications:

- replace or wrap with approved manifest design
- add retry history, partial execution flags, pipeline history, notifications, timestamps aligned to target schema

## 9. Components that must be rebuilt

The following must be rebuilt to satisfy the approved design:

- preprocessing pipeline
- table extraction pipeline
- fraud detection pipeline
- logo/template recognition pipeline
- canonical aggregation/output layer
- manifest implementation
- Step Functions orchestration
- ECS/Fargate execution path
- target bucket/resource naming layer
- target observability/alarms model
- target partial processing controls
- target pipeline history and retry tracking

## 10. Missing capabilities

Based on live evidence, the current OCR app is missing these approved-target capabilities entirely:

- preprocessing as a deployed modular pipeline
- deployed table extraction component
- deployed fraud detection component
- deployed logo/template recognition component
- Step Functions state machines
- ECS task definitions and services
- approved manifest schema implementation
- approved canonical schema implementation
- target partial execution flags
- target pipeline history
- target client notification manifest fields
- target per-page/per-batch orchestration model

## 11. Estimated development time saved by reuse

### 11.1 Areas with meaningful reuse value

Estimated savings are directional only and based on confirmed live assets.

| Reusable Area | Basis | Indicative Time Saving |
|---|---|---|
| OCR engine reuse/adaptation | Live ECR OCR engine exists and performs page OCR, PDF splitting, DOC/DOCX extraction | Medium |
| Ingest and routing wrapper reuse | Live ingest Lambda, quality scoring, queue routing, S3 path building already exist | Medium |
| Detailed extraction wrapper reuse | Live detailed worker, contract registry, agentic parser, get-result aggregator already exist | Medium |
| Test/sample seed reuse | Existing result artifacts and packaged source backups exist | Low to Medium |

### 11.2 Areas with little or no reuse value

| Area | Reason | Indicative Time Saving |
|---|---|---|
| Preprocessing | No live deployed implementation found | None |
| Table extraction | No live deployed implementation found | None |
| Fraud detection | No live deployed implementation found | None |
| Logo/template recognition | No live deployed implementation found | None |
| Step Functions | No live implementation | None |
| ECS path | No live implementation | None |
| Manifest schema | Current model not target-compliant | Low |
| Canonical schema | Current model not target-compliant | Low |

### 11.3 Overall assessment

Overall reuse can reduce effort materially for:

- OCR core execution
- upload intake
- queue-based asynchronous branching
- contract-driven AI enrichment
- result retrieval patterns

Overall reuse will **not** remove the need to build the approved modular architecture.

Estimated overall saving:
- **moderate**, not transformative

## 12. Risks and controls

| Risk | Impact | Control |
|---|---|---|
| Reusing current outputs as if they are target schema compliant | Breaks canonical/manifest alignment | Treat current outputs as intermediate only |
| Reusing current naming/resource layout | Conflicts with approved design | Rebuild names to target standard |
| Reusing DB-centric state tracking as final manifest model | Breaks Phase 3/4 schema requirements | Build approved manifest implementation |
| Carrying forward synchronous ingest wait behavior | Timeouts on large documents | Move long-running control to target orchestration |
| Reusing AI extraction without service boundary cleanup | Blurs fraud/logo/table responsibilities | Keep agentic parsing as one modular component only |
| Relying on undocumented/local placeholder scripts | False reuse assumption | Exclude placeholder shell scripts from implementation reuse |
| Reusing broken status update path in agentic-parser | Incomplete state tracking | Fix dependency/runtime packaging before reuse |
| Reusing current monolithic OCR engine without modular split | Violates preprocessing/OCR separation | Extract only proven code portions, rewrap cleanly |

## 13. Recommended reuse plan

### 13.1 Reuse as adaptation base

Carry forward and adapt:

1. OCR engine code from `ocr-engine-dev:v10`
2. ingest/routing logic from `OcrIngestStub-dev`
3. quick/detailed async worker patterns
4. contract registry and service gating pattern
5. agentic detailed extraction wrapper
6. get-result aggregation pattern
7. sample outputs and packaged backups as validation inputs

### 13.2 Do not reuse as final target implementation

Do not carry forward unchanged:

1. current output schemas
2. current `document_run` as final manifest model
3. current resource names
4. placeholder shell pipeline scripts
5. current orchestration topology as final target architecture

### 13.3 Build new around reused core logic

Build new target-owned layers for:

1. preprocessing
2. table extraction
3. fraud detection
4. logo/template recognition
5. canonical aggregation
6. manifest/state model
7. Step Functions/ECS architecture
8. target observability and retry controls

## 14. Next build sequence if reuse is approved

1. Extract and version the reusable OCR engine source from `ocr-engine-dev:v10`
2. Extract and version reusable intake/routing code from `OcrIngestStub-dev`
3. Extract and version reusable detailed worker, contract registry, and agentic-parser components
4. Define adapter mappings from current OCR/detailed outputs into target canonical schema
5. Define adapter mapping from current `document_run` fields into target manifest requirements
6. Build target preprocessing pipeline
7. Build target table extraction pipeline
8. Build target fraud pipeline
9. Build target logo/template pipeline
10. Build target canonical aggregation layer
11. Build target manifest implementation
12. Build Step Functions/ECS orchestration to approved Phase 4 design
13. Retest all reused components against evaluation framework and schema compliance

