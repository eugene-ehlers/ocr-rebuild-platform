# OCR Rebuild — Phase 5 Controlled Implementation Scope

Status: GOVERNED IMPLEMENTATION BASELINE

---

## 1. Purpose

Define the controlled subset of the OCR platform that will be implemented in Phase 5, while preserving alignment to the full target architecture.

This document prevents:
- uncontrolled shortcuts
- silent scope creep
- rework caused by partial implementations becoming permanent

---

## 2. Core Principle

The system must be built in controlled increments, but designed for the full architecture from day one.

No implementation may:
- contradict governed contracts
- bypass normalization rules
- introduce alternative data models
- perform uncontrolled routing or inference

---

## 3. Phase 5 — Allowed Scope (Build Now)

### 3.1 Input normalization (limited)

Supported:
- single-image documents (PNG, JPG, JPEG)
- multi-page PDFs (basic deterministic splitting)
- optional: TIFF (only if trivial and stable)

---

### 3.2 Preprocessing

- must operate on normalized page records only
- must not perform source normalization beyond governed rules
- current image enhancement pipeline remains valid

---

### 3.3 OCR

- single OCR engine implementation
- page-level extraction only
- must enrich page schema (text, confidence, engine metadata)

---

### 3.4 Aggregation

- canonical output per logical document
- multi-document manifests allowed, but:
  - aggregation remains per document
  - no project-level aggregation yet

---

## 4. Explicitly Out of Scope (Do NOT Implement Yet)

### 4.1 Structured-digital formats

Includes:
- DOCX
- XLSX
- CSV
- text-native PDFs
- JSON/XML structured inputs

Rules:
- must NOT be routed through OCR
- must NOT be temporarily supported via OCR
- must be rejected or marked as `unsupported`

---

### 4.2 Hybrid documents

Includes:
- mixed scanned + text PDFs
- embedded images in DOCX/XLSX

Rules:
- no heuristic detection
- no partial handling
- no implicit routing decisions

---

### 4.3 Page-by-page document assembly

- no uncontrolled grouping logic
- no inference based on filenames beyond simple deterministic ordering
- no merging without explicit metadata

---

### 4.4 Multi-document aggregation

- no combined canonical output across documents
- no cross-document merging
- no project-level summary logic

---

### 4.5 Advanced preprocessing

- no layout analysis
- no advanced rotation detection (beyond current simple handling)
- no DPI normalization strategies
- no ML-based enhancement

---

## 5. Mandatory Future Backlog (Must Be Implemented)

### 5.1 Full input normalization engine

- robust PDF splitting
- TIFF support
- page-by-page ingestion with explicit grouping
- deterministic grouping rules
- page lineage tracking

---

### 5.2 Structured extraction pipeline

- DOCX parsing
- XLSX parsing
- CSV ingestion
- text-native PDF handling

---

### 5.3 Hybrid routing engine

- detect scanned vs digital content
- route between OCR and structured pipelines
- support mixed-mode processing per document

---

### 5.4 Multi-document orchestration

- manifest-level aggregation
- project-level outputs
- document grouping semantics

---

### 5.5 Multi-engine OCR

- pluggable OCR engines
- fallback strategies
- confidence reconciliation

---

### 5.6 Advanced preprocessing

- rotation detection
- skew correction
- DPI normalization
- noise reduction strategies

---

### 5.7 Production hardening

- manifest ID enforcement
- retries and DLQs
- idempotency guarantees
- observability (metrics, logs, tracing)
- alerting and failure handling

---

## 6. Non-Negotiable Rules for Developers

- Do NOT introduce logic outside governed contracts
- Do NOT infer document grouping
- Do NOT bypass normalization
- Do NOT extend schemas ad hoc
- Do NOT “temporarily support” out-of-scope formats

All extensions must:
- be documented
- be approved
- align with target architecture

---

## 7. Success Criteria for Phase 5

Success is defined by correctness and alignment, not completeness.

The system must:
- successfully process:
  - single-image documents
  - multi-page PDFs
- produce valid normalized page structures
- maintain strict document-to-page linkage
- comply with execution contract and schemas
- produce stable, repeatable canonical outputs

---

## 8. Architectural Integrity Rule

This phase is intentionally limited in implementation scope.

However:
- the full architecture defined in Phase 2 and Phase 3 remains the governing target state
- all implementations must remain forward-compatible with that architecture

No shortcuts may compromise future extensibility.

