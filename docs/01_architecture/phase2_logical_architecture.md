# OCR Rebuild — Phase 2 Logical Architecture (Final Draft, Solution Boundaries)

## 1. Overview
Scope: OCR and information extraction solution from document upload → preprocessing → OCR/table/logo/fraud pipelines → canonical output.
Handles single-page, multi-page, and multi-document uploads, with hybrid page/batch/streaming paths and multi-user concurrency.

Out of scope: Front-end UI, downstream business logic, storage/archiving policies, advanced AI post-processing beyond extraction.

## 2. Solution Boundaries

Layer | Included (In-Scope) | Excluded (Out-of-Scope)
----- | ------------------ | -----------------------
Document Intake | Upload API, single/multi-page, folder upload, metadata capture | Front-end UI/dashboard, authentication beyond AWS IAM
Preprocessing | Page splitting, rotation, DPI normalization, optional batching | Advanced image enhancement
OCR Engine | Text extraction, confidence scoring, multi-engine support | NLP/semantic analysis
Table Extraction | Detect tables, convert to JSON | Advanced table interpretation
Logo/Template Recognition | Identify logos/templates for metadata/fraud | Brand analysis
Fraud Detection | Anomaly detection using pipeline outputs | Business rules beyond detection
Orchestration | Page/batch/streaming flows, pipeline selection, multi-user workflow isolation | Workflows outside OCR solution
Canonical Schema | Unified JSON output | Downstream analytics/storage policies
Progress Tracking | Stage, confidence, batch/page status, retries, client notifications | Front-end visualization beyond metadata
AWS Infrastructure | S3, Lambda, Step Functions, DynamoDB/RDS, SQS/SNS, CloudWatch/X-Ray | Cross-account security/integration beyond IAM

## 3. Hybrid Processing Paths

- Page-level: Small documents, full parallelism
- Batch-level: Medium/large documents, reduces orchestration overhead
- Streaming: Very large documents, sequential batches to manage memory/Lambda limits

Workflow Decision Logic:

[Document Upload]
    |
[Determine Doc Size & Type]
    |
  +----------------+
  | Small          | → Page-level parallel pipelines
  | Medium/Large   | → Batch-level parallel pipelines
  | Very Large     | → Streaming/sequential batch pipelines
  +----------------+
    |
[Pipeline Execution] → Canonical Output

**Client Upload Modes**
- Continuous full document upload
- Page-by-page incremental upload
- Partial reprocessing supported (pipeline-specific)

## 4. Pipeline Components

Pipeline | Function | Input | Output | Notes
-------- | ------- | ----- | ------ | -----
Preprocessing | Normalize, split, batch | Raw pages/images | Preprocessed pages/batches | Optional batching for large docs
OCR Engine | Text extraction | Preprocessed pages/batches | Text + confidence | Modular interface
Table Extraction | Structured tables | Preprocessed pages/batches | JSON | Independent pipeline
Logo/Template Recognition | Metadata for classification/fraud | Preprocessed pages/batches | Logo/template info | Independent
Fraud Detection | Risk/anomaly detection | Text, tables, logos | Risk/confidence scores | Independent
Aggregation | Merge outputs | All pipeline outputs | Canonical JSON | Schema compliance

**Performance / Benchmark Placeholders**
- Time per page: UNKNOWN
- Time per batch: UNKNOWN
- Throughput (pages/sec): UNKNOWN
- Expected confidence metrics (OCR, tables, fraud, logos): UNKNOWN

**Client Failure Handling**
- If a pipeline fails: notify client immediately
- Provide actionable next steps (rerun pipeline, re-upload page/document)
- Log errors with root cause for traceability

## 5. Page/Batch-Level Orchestration

- Metadata tracking per page/batch: pipeline stage/status, timestamps, confidence/risk, errors
- Partial reprocessing and retries supported
- Multi-user workflow isolation via Step Functions/SQS

## 6. Multi-User & Multi-Document Handling

- Each document/folder upload is independent workflow
- Folder uploads processed per document, hybrid processing per document size
- Real-time workflow metadata enables progress tracking and feedback

## 7. Canonical Schema Compliance

- Unified JSON containing:
  - Document ID, page/batch IDs, timestamps
  - Text blocks + confidence
  - Tables in JSON format
  - Logos/templates metadata
  - Risk/confidence scores

## 8. AWS Reference Architecture

Component | Role
--------- | ----
S3 | Store raw, preprocessed, canonical outputs
Lambda | Page/batch orchestration, pipeline triggers
Step Functions | Workflow control, retries, multi-path orchestration
DynamoDB/RDS | Metadata tracking
SQS/SNS | Async task management, notifications
CloudWatch/X-Ray | Logging, monitoring, metrics
Optional ECS/Fargate | Heavy/long-running pipelines

## 9. Key Considerations

- Hybrid paths ensure optimal treatment for any document size
- Multi-user concurrency supported
- Partial reprocessing at page or batch level
- Canonical outputs allow downstream integration
- Solution boundaries explicitly defined (in-scope vs out-of-scope)
- Performance placeholders included for later benchmarking
- Client communication and failure handling explicitly defined
- Upload flexibility documented (continuous vs page-by-page)
