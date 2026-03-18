# OCR Rebuild — Phase 5 Input Normalization and Routing Design

Status: DRAFT - CONTROLLED DESIGN BASELINE

## 1. Purpose

Define the governed input normalization and routing model for OCR Rebuild so that uploaded source objects are converted into the correct execution model before preprocessing and OCR.

This document closes the current design gap between:
- raw uploaded source objects
- logical document scope
- page-level processing requirements
- OCR-eligible vs structured-digital routing decisions
- multi-document project handling

This document is authoritative for:
- source input classes
- normalization rules
- document/page semantics
- routing rules into OCR or non-OCR extraction paths
- canonical expectations for multi-page and multi-document requests

## 2. Core Design Principle

The OCR pipeline must not assume that raw uploaded source objects already exist as governed page records.

A controlled normalization step must convert uploaded source material into:
- manifest/project scope
- one or more logical documents
- governed page records for OCR-eligible document types
- routing decisions for non-OCR-native document types

## 3. Processing Scopes

### 3.1 Manifest / project scope
A manifest represents a single controlled execution scope.

A manifest may contain:
- one logical document
- multiple logical documents in one project or upload batch

Examples:
- one payslip PDF
- one bank statement uploaded page by page
- one project containing payslip + bank statement + CV

### 3.2 Document scope
A document is the logical unit for canonical output and document-type interpretation.

Each logical document must have:
- `document_id`
- `source_uri` or source component lineage
- `expected_document_type` where available

A manifest may contain multiple documents.

### 3.3 Page scope
A page is the OCR-processing unit for OCR-eligible documents.

Pages must belong to a logical document and must support deterministic ordering.

## 4. Supported Input Classes

## 4.1 OCR-eligible source classes
These source types normalize into page images and proceed through preprocessing + OCR.

### Single-image document
Examples:
- PNG
- JPG
- JPEG
- single-page TIFF

Normalization result:
- one logical document
- one page record

### Multi-page file document
Examples:
- PDF
- multi-page TIFF

Normalization result:
- one logical document
- one page record per page in source order

### Page-by-page assembled document
Examples:
- multiple uploaded images representing one logical document

Normalization result:
- one logical document
- multiple page records in governed caller-supplied or deterministically inferred order

### Multi-document project / batch
Examples:
- payslip + bank statement + CV
- KYC document pack
- onboarding evidence bundle

Normalization result:
- one manifest
- multiple logical documents
- page records grouped by document

## 4.2 Structured-digital source classes
These source types are not OCR-first by default.

Examples:
- CSV
- XLSX
- DOCX
- text-native PDF
- machine-readable JSON/XML

Default rule:
- these must route to structured extraction or document parsing paths, not raster OCR-first processing, unless a future approved design explicitly requires hybrid OCR handling.

## 4.3 Hybrid source classes
Some source types may require mixed handling.

Examples:
- PDF containing both selectable text and scanned pages
- DOCX containing embedded scanned images
- spreadsheet with embedded screenshots/scans

Default rule:
- hybrid routing is a future controlled extension and must not be inferred ad hoc by workers.

## 5. Normalization Rules

## 5.1 Normalization outcome
Normalization must produce:
- manifest/project scope
- documents array
- page records for OCR-eligible documents
- page ordering
- page artifact lineage
- source-type routing decision

## 5.2 Required OCR normalization output
For OCR-eligible documents, normalization must produce page records with at least:
- `document_id`
- `page_number`
- source artifact location
- processed artifact location when preprocessing completes
- page-level metadata sufficient for downstream OCR and enrichment stages

## 5.3 Deterministic ordering
Page order must be deterministic.

Allowed sources of order:
1. explicit caller-provided page order
2. source file natural page order (e.g. PDF/TIFF)
3. governed filename ordering rule if uploaded page-by-page and explicit order is absent

## 5.4 Caller intent vs inferred grouping
Where a request contains multiple uploaded objects, normalization must distinguish between:
- many pages of one document
- many separate documents

This distinction must come from:
- explicit caller metadata where provided, or
- approved deterministic grouping rules

Workers must not make uncontrolled guesses about grouping.

## 6. Routing Rules

## 6.1 OCR-eligible route
If source type is OCR-eligible, route to:
- normalization
- preprocessing
- OCR
- optional enrichments
- aggregation

## 6.2 Structured-digital route
If source type is structured-digital, route to:
- future structured extraction path
- not the raster OCR path by default

## 6.3 Temporary implementation rule
Until structured extraction exists, structured-digital types must be:
- rejected with controlled status, or
- marked unsupported for the OCR path,
unless an approved temporary handling rule is documented.

## 7. Canonical Model Implications

## 7.1 Manifest
A manifest may contain multiple documents.

## 7.2 Canonical output
Canonical output should be produced per logical document.

For multi-document manifests, aggregation must support:
- one canonical document per document_id
- optional future project-level aggregation summary

## 7.3 Page linkage
Page records must be attributable to a logical document.
The page contract must support explicit document-to-page linkage.

## 8. Required Contract Enhancements

The current execution/page contracts require enhancement to explicitly support:
- document-to-page linkage
- page artifact lineage
- normalization semantics
- routing classification

Likely required fields include:
- `document_id` on page records
- source page location fields
- processed page location fields
- optional normalized `page_id`

Final field decisions must be implemented through controlled contract updates after this design is approved.

## 9. Current Implementation Gap

Current preprocessing implementation only transforms `event.pages[]` if pages already exist.

It does not yet:
- derive pages from source documents
- split PDFs into pages
- create single-page records from raw image uploads
- group uploaded page images into logical documents
- route structured-digital files away from OCR-first flow

Therefore the current code is below the intended architecture and must be brought into alignment.

## 10. Controlled Implementation Sequence

### Step 1
Update governed contracts to support explicit document/page normalization semantics.

### Step 2
Implement normalization for OCR-eligible source classes:
- single-image documents
- multi-page PDFs
- multi-page TIFF where feasible

### Step 3
Support page-by-page assembled document ingestion with deterministic grouping/order rules.

### Step 4
Define structured-digital routing path for:
- DOCX
- XLSX
- CSV
- text-native PDFs

### Step 5
Only after normalization is working, continue with:
- manifest ID enforcement
- Step Functions final output alignment
- CI/CD buildspec implementation
- production hardening

## 11. Current Baseline Decision

Effective immediately:
- OCR Rebuild must treat input normalization as a first-class controlled design concern
- preprocessing must no longer be assumed to receive pre-built pages for all requests
- OCR usefulness is not considered complete until normalization produces real page records and OCR processes them successfully
