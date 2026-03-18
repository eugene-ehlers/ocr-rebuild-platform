# OCR Rebuild — Phase 5 Input Normalization and Routing Design

Status: DRAFT - HYBRID DOCUMENT INTELLIGENCE BASELINE

## 1. Purpose

Define the governed input normalization and routing model for OCR Rebuild so that uploaded source objects are converted into the correct execution model before preprocessing, OCR, structured extraction, and downstream intelligence routing.

This document closes the design gap between:
- raw uploaded source objects
- logical document scope
- page-level processing requirements
- OCR-eligible vs structured-digital routing
- internal vs external capability routing
- multi-document project handling
- future modular intelligence capability expansion

This document is authoritative for:
- source input classes
- normalization rules
- document/page semantics
- routing rules into internal or external capability paths
- canonical expectations for single-document and multi-document requests
- future capability substitution readiness

## 2. Core Design Principle

The platform must not assume that raw uploaded source objects already exist as governed document or page records.

A controlled normalization step must convert uploaded source material into:
- manifest / project scope
- one or more logical documents
- governed page records for OCR-eligible content
- routing classification for structured-digital content
- capability-routing decisions for downstream modules

Normalization is therefore not just file preparation.
It is the first intelligence and orchestration control point.

## 3. Strategic Routing Principle

The routing model must support both:
- external API-backed capability providers
- internal capability modules

The initial operating model is intentionally API-capable so the platform can deliver:
- fast time to market
- broad capability coverage
- strong early quality
- reduced implementation risk

Over time, internal capability should replace expensive external capability where internal performance is sufficient.

Therefore routing must be designed so that:
- external capability can be used immediately
- internal capability can be introduced progressively
- substitution does not require redesign of workflow or contracts
- fallback remains available when client outcome requires it

## 4. Processing Scopes

### 4.1 Manifest / project scope
A manifest represents a single controlled execution scope.

A manifest may contain:
- one logical document
- multiple logical documents in one upload batch
- a multi-document project/bundle

Examples:
- one payslip PDF
- one bank statement uploaded page by page
- one project containing payslip + bank statement + CV + ID document

### 4.2 Document scope
A document is the logical unit for canonical output, classification, interpretation, routing, and downstream extraction.

Each logical document must have:
- `document_id`
- source lineage
- `expected_document_type` where available
- source-type classification where available

A manifest may contain multiple documents.

### 4.3 Page scope
A page is the OCR-processing unit for OCR-eligible content.

Pages must:
- belong to a logical document
- support deterministic ordering
- support lineage from raw source to normalized artifact to processed artifact
- support future module-level enrichment

## 5. Supported Input Classes

## 5.1 OCR-eligible source classes
These source types normalize into governed page images and proceed through preprocessing and OCR-capable paths.

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

## 5.2 Structured-digital source classes
These source types are not OCR-first by default.

Examples:
- CSV
- XLSX
- DOCX
- text-native PDF
- machine-readable JSON
- XML

Default rule:
- these must route to structured parsing or document extraction paths, not raster OCR-first processing, unless a governed hybrid rule explicitly applies

## 5.3 Hybrid source classes
Some source types may contain mixed characteristics.

Examples:
- PDF containing both selectable text and scanned pages
- DOCX containing embedded scans
- spreadsheet with screenshots or scanned inserts
- image-plus-text compound submissions

Default rule:
- hybrid handling must be governed explicitly
- workers must not improvise mixed-mode routing without approved decision rules

## 6. Normalization Rules

## 6.1 Required normalization outcome
Normalization must produce:
- manifest/project scope
- documents array
- page records for OCR-eligible documents
- deterministic page ordering
- page artifact lineage
- source-type routing classification
- capability-routing metadata sufficient for downstream decisioning

## 6.2 Required OCR normalization output
For OCR-eligible documents, normalization must produce page records with at least:
- document linkage
- page ordering
- source artifact location
- normalized artifact location
- processed artifact location once preprocessing completes
- metadata sufficient for OCR, fallback, and enrichment routing

## 6.3 Deterministic ordering
Page order must be deterministic.

Allowed sources of order:
1. explicit caller-provided page order
2. source file natural page order
3. governed filename ordering rule when explicit order is absent

## 6.4 Caller intent vs inferred grouping
Where a request contains multiple uploaded objects, normalization must distinguish between:
- many pages of one document
- many separate documents
- one project containing multiple logical documents

This distinction must come from:
- explicit caller metadata where provided
- approved deterministic grouping rules
- future classification support where governed

Workers must not make uncontrolled grouping guesses.

## 6.5 Normalization lineage rule
Normalization must preserve lineage from:
- original uploaded object
- normalized page artifact
- processed page artifact
- downstream OCR/extraction result

This is required so that:
- fallback decisions are traceable
- reprocessing is controlled
- benchmarking remains possible
- substitution of engines/providers does not destroy lineage

## 7. Routing Layers

Routing must happen at multiple levels.

### 7.1 Source-type routing
Determine whether input is:
- OCR-eligible
- structured-digital
- hybrid
- unsupported

### 7.2 Document-type routing
Determine whether document likely requires:
- generic OCR
- structured extraction
- handwriting handling
- forms / key-values
- signatures / checkboxes
- barcode / QR
- specialized downstream modules

### 7.3 Capability routing
Determine whether the platform should use:
- internal capability
- open-source capability
- external API-backed capability
- managed-service fallback
- placeholder or deferred path

### 7.4 Quality-based routing
Determine whether primary result is sufficient or must escalate.

Examples:
- internal OCR accepted
- internal OCR escalated to Textract
- internal extraction accepted
- external form extraction required
- handwriting escalated to specialist path

## 8. Initial Routing Philosophy

The routing design must support a deliberate commercial and technical model:

- deliver quickly using external API-backed capability where needed
- own orchestration, contracts, routing, telemetry, and aggregation internally
- progressively replace expensive external capability with internal modules where performance is sufficient
- preserve fallback for client-critical cases

This means:
- external providers are capability adapters, not the platform itself
- internal modules are strategic replacements, not forced first choices
- routing must remain explainable and measurable

## 9. Capability Domains the Routing Model Must Cater For

The routing design must explicitly support present or future capability selection for:

- printed OCR
- handwriting recognition
- language / script detection
- layout analysis
- table extraction
- key-value / form extraction
- selection mark / checkbox detection
- signature detection
- barcode / QR extraction
- document classification
- document splitting
- logo / stamp / seal detection
- font / style analysis
- image / figure extraction
- formula extraction
- fraud / anomaly analysis
- future structured-digital parsing

A capability may begin as:
- implemented
- heuristic
- external-service-backed
- placeholder

But it must exist as a routing-aware capability domain.

## 10. Routing Outputs Required for Downstream Stages

Normalization and routing must produce enough metadata for downstream stages to know:

- what the source type is
- what the logical document boundaries are
- what pages belong to which document
- which capability families are required
- whether initial execution should prefer internal or external capability
- whether fallback is permitted or required
- what decision basis was used

## 11. Canonical Model Implications

### 11.1 Manifest
A manifest may contain multiple documents and must remain the controlled execution scope.

### 11.2 Canonical output
Canonical output is produced per logical document.

For multi-document manifests, aggregation must support:
- one canonical document per logical document
- future project-level summary outputs
- document-level lineage and routing traceability

### 11.3 Page linkage
Page records must remain attributable to logical documents and to source lineage.

## 12. Required Contract Enhancements

The contracts must explicitly support:
- document-to-page linkage
- normalization semantics
- source-type routing classification
- capability-routing metadata
- lineage fields
- fallback and provider-selection traceability
- evaluation signals over time

Likely required fields include:
- `document_id` on pages
- `page_id`
- source artifact location fields
- normalized artifact location fields
- processed artifact location fields
- source type
- routing decision metadata
- fallback reason metadata
- provider/engine selection metadata

## 13. Current Implementation Gap

Current implementation has moved forward, but remains below intended architecture.

Current limitations include:
- partial OCR-eligible normalization implementation only
- no full structured-digital routing path
- no full capability-routing decision model
- no full fallback-decision telemetry
- no comprehensive hybrid source handling
- limited current module selection logic

This must be treated as:
- a controlled starting increment
- not the final routing architecture

## 14. Controlled Implementation Sequence

### Step 1
Update governed contracts to support explicit normalization semantics, lineage, routing metadata, and future provider substitution.

### Step 2
Implement normalization for core OCR-eligible source classes:
- single-image documents
- multi-page PDFs
- multi-page TIFF where feasible

### Step 3
Support page-by-page assembled document ingestion with deterministic grouping and ordering rules.

### Step 4
Define structured-digital routing paths for:
- DOCX
- XLSX
- CSV
- text-native PDFs
- machine-readable structured content

### Step 5
Introduce capability-routing metadata and first controlled routing decisions for:
- internal vs external OCR
- forms / tables / signatures / handwriting placeholders
- future fallback reason capture

### Step 6
Only after routing and normalization are governed should the platform continue with:
- expanded fallback orchestration
- benchmark-driven OCR engine optimization
- internal capability replacement planning
- production hardening
- decision analytics and dashboards

## 15. Strategic Outcome

This design is successful when the platform can:
- normalize any governed input into controlled execution scope
- distinguish documents from pages from projects
- route inputs toward the correct capability families
- support both external API-backed and internal capability execution
- preserve substitution readiness for future internalization
- avoid workflow redesign when engines/providers change
- prepare the platform for continuous improvement rather than one-off implementation
