# OCR Rebuild — Evaluation Framework

## 1. Purpose
This document defines an independent evaluation tool for all proposed OCR rebuild designs.
All designs must be benchmarked against this framework before implementation.

## 2. Core Evaluation Categories

| Category | Description | Metrics / Criteria |
|----------|-------------|------------------|
| Processing Capability | Handle small and very large documents efficiently | Max pages per document, time per page, concurrency limits |
| Pipeline Completeness | Supports partial or full processing pipelines | OCR-only, OCR+fraud, OCR+tables, full processing |
| Accuracy & Quality | Quality of extracted data | OCR confidence, table correctness, fraud detection, logo/template accuracy |
| Performance / Speed | Latency and throughput | Time-to-first-result, end-to-end time, pages per second |
| User Communication | Transparency to client | Stage tracking per document/page, failure notifications, actionable guidance |
| Fault Isolation & Recovery | Handle failures without cascading | Fail fast, partial pipeline continuation, root cause logging |
| Resource Efficiency | Optimal use of compute, storage | CPU/memory per pipeline, Lambda/ECS usage, S3 access efficiency |
| Benchmark Comparisons | Engine and pipeline performance | Textract vs Azure vs Google AI, pipeline routing correctness |
| Operational Resilience | Reliability and auditability | Recovery time, audit logs, pipeline robustness |
| User-Friendliness / Feedback | Ease of understanding and acting on outputs | Confidence scores, risk indicators, clear messages |
| Modularity & Extensibility | Adding new document types or pipelines without rebuild | Document-type isolation, schema stability, conditional pipelines |

## 3. Flexibility / Upload Modes
- Continuous document upload (full PDF or multi-page)  
- Page-by-page upload (incremental submission)  
- Partial reprocessing (re-run specific pages or pipelines without full re-upload)  

## 4. Modularity & Extensibility
- New document types (e.g., insurance, invoices) can be added without affecting existing pipelines.  
- Each document type can have independent preprocessing, OCR, table extraction, fraud, or template rules.  
- Canonical schema supports extensions without breaking existing fields.  
- Pipeline steps remain independent and conditional per client request.  
- All new types must be evaluated with this framework.

## 5. Evaluation Process
1. Intake: describe pipelines, parallelism, failure handling, outputs.  
2. Benchmark against framework categories (performance, accuracy, resource use).  
3. Scenario analysis: single-page, small multi-page, large document, partial processing.  
4. Client communication assessment: stage reporting, error guidance.  
5. Pass/Fail: design accepted only if it meets critical evaluation criteria.  
6. Documentation: store evaluation results in S3 under `docs/11_benchmarks/evaluation_framework/`.

## 6. Key Notes
- Independent of implementation details.  
- Benchmarks must be applied before any coding.  
- Metrics, thresholds, and scoring can evolve; categories remain constant.  
- Ensures system is competitive: speed, accuracy, agility, user-friendliness.

