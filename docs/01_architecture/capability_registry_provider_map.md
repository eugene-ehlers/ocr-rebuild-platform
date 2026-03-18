# OCR Rebuild — Capability Registry and Provider Map

Status: DRAFT - EXECUTION DESIGN BASELINE

## 1. Purpose

Define the governed registry of atomic platform capabilities and the provider/module options available to fulfill them.

This document is authoritative for:
- atomic capability definitions
- provider capability coverage
- bundled provider overlap awareness
- capability-to-provider mapping
- future internalization planning
- execution decision ecosystem inputs

This document must support:
- service composition
- execution decisioning
- fallback design
- cost optimisation
- provider substitution over time

## 2. Core Principle

The platform must be built from atomic reusable capabilities.

A capability is the smallest governed functional unit that can be requested, fulfilled, measured, and improved independently.

Client-facing services are composed from capabilities.
Execution plans are built by selecting providers/modules that fulfill required capabilities.

## 3. Capability Registry Structure

Each capability should be understood through:
- capability_id
- capability_name
- capability_family
- description
- minimum expected outputs
- candidate providers/modules
- bundled overlap risk
- future internalization intent

## 4. Capability Families

The platform capability registry is grouped into the following families:

### 4.1 Core extraction
- TEXT_OCR
- TEXT_STRUCTURE
- HANDWRITING_EXTRACTION
- LANGUAGE_DETECTION

### 4.2 Structured extraction
- TABLE_DETECTION
- TABLE_STRUCTURE
- KEY_VALUE_EXTRACTION
- CHECKBOX_DETECTION
- BARCODE_QR_EXTRACTION

### 4.3 Document understanding
- DOCUMENT_CLASSIFICATION
- LAYOUT_ANALYSIS
- IMAGE_REGION_DETECTION
- FONT_ANALYSIS

### 4.4 Trust and authenticity
- AUTHENTICITY_SCORING
- TAMPER_DETECTION
- CONSISTENCY_CHECKING
- CROSS_DOCUMENT_MATCHING

### 4.5 Legal / human evidence
- SIGNATURE_DETECTION
- CLAUSE_EXTRACTION
- QUESTION_ANSWER_SUPPORT

## 5. Atomic Capability Definitions

## 5.1 TEXT_OCR

### Description
Extract machine-readable printed text from document pages.

### Minimum outputs
- extracted text
- page linkage
- confidence summary
- engine/provider metadata

### Candidate providers/modules
- Tesseract
- AWS Textract DetectDocumentText
- future internal OCR models

### Bundled overlap risk
May be included in broader providers that also return tables, forms, and selection marks.

### Future internalization
High priority

## 5.2 TEXT_STRUCTURE

### Description
Represent line, block, and reading-order structure of extracted text.

### Minimum outputs
- line/block segmentation
- positional or ordering metadata where available

### Candidate providers/modules
- Tesseract-derived structures
- Textract
- future layout-aware OCR modules

### Bundled overlap risk
Often bundled with OCR

## 5.3 HANDWRITING_EXTRACTION

### Description
Extract handwritten text.

### Minimum outputs
- extracted handwriting text
- confidence
- page linkage

### Candidate providers/modules
- external specialist provider
- Textract where appropriate
- future internal handwriting model

### Future internalization
Medium-term priority

## 5.4 LANGUAGE_DETECTION

### Description
Detect language or script present.

### Minimum outputs
- language code
- confidence if available

### Candidate providers/modules
- lightweight NLP libraries
- OCR engine metadata
- cloud NLP APIs

## 5.5 TABLE_DETECTION

### Description
Detect whether tables are present on a page/document.

### Minimum outputs
- table presence indicator
- page linkage
- table count where possible

### Candidate providers/modules
- OpenCV / internal heuristics
- Textract
- future dedicated table models

## 5.6 TABLE_STRUCTURE

### Description
Extract structured table rows, columns, and cells.

### Minimum outputs
- table objects
- rows/cells
- confidence where available

### Candidate providers/modules
- internal heuristic table worker
- Textract AnalyzeDocument
- future deep-learning table extractor

### Bundled overlap risk
Often bundled with OCR/forms/checkmarks in external providers

### Future internalization
High priority for cost optimisation

## 5.7 KEY_VALUE_EXTRACTION

### Description
Extract structured form-style key-value pairs.

### Minimum outputs
- key-value pairs
- confidence
- page/document linkage

### Candidate providers/modules
- placeholder/internal heuristic
- Textract AnalyzeDocument
- future transformer-based internal extraction

### Future internalization
Medium-to-high priority

## 5.8 CHECKBOX_DETECTION

### Description
Detect and interpret selection marks / checkboxes.

### Minimum outputs
- selection state
- location/page linkage
- confidence where available

### Candidate providers/modules
- Textract
- internal CV heuristic
- future internal checkbox module

## 5.9 BARCODE_QR_EXTRACTION

### Description
Detect and decode barcodes / QR codes.

### Minimum outputs
- decoded value
- barcode type
- page linkage

### Candidate providers/modules
- open-source barcode libraries
- CV-based decoding
- external provider if needed

## 5.10 DOCUMENT_CLASSIFICATION

### Description
Classify document type and subtype.

### Minimum outputs
- document type
- subtype where available
- confidence

### Candidate providers/modules
- internal keyword/layout heuristics
- future classifier model
- optional external classifier

### Future internalization
High priority because it drives routing

## 5.11 LAYOUT_ANALYSIS

### Description
Understand high-level page/document structural regions.

### Minimum outputs
- layout regions
- region types
- positional metadata

### Candidate providers/modules
- OpenCV/layout heuristics
- future layout models
- external APIs where justified

## 5.12 IMAGE_REGION_DETECTION

### Description
Detect meaningful embedded image regions.

### Minimum outputs
- region presence
- location metadata
- region classification where available

### Candidate providers/modules
- internal CV
- future object detection model

## 5.13 FONT_ANALYSIS

### Description
Detect font inconsistency or style-level anomalies relevant to authenticity.

### Minimum outputs
- font/style anomaly indicators
- location linkage where available

### Candidate providers/modules
- internal heuristics
- future CV/model support

## 5.14 AUTHENTICITY_SCORING

### Description
Assess trustworthiness of the document using available document evidence.

### Minimum outputs
- authenticity score
- signal summary
- confidence/explanation metadata

### Candidate providers/modules
- internal fraud/authenticity rules
- future ML authenticity model
- optional external fraud APIs

### Future internalization
Strategic differentiator

## 5.15 TAMPER_DETECTION

### Description
Detect likely tampering or manipulation signals.

### Minimum outputs
- tamper flags
- signal evidence
- severity/confidence

### Candidate providers/modules
- internal heuristics
- future authenticity/tamper models
- optional external specialist providers

## 5.16 CONSISTENCY_CHECKING

### Description
Check internal consistency within a document or set of extracted values.

### Minimum outputs
- inconsistency flags
- rule results
- evidence summary

### Candidate providers/modules
- internal rules engine
- future ML/rules hybrid

## 5.17 CROSS_DOCUMENT_MATCHING

### Description
Compare entities or facts across multiple documents.

### Minimum outputs
- matched entities
- contradiction flags
- linkage summary

### Candidate providers/modules
- internal matching logic
- future graph/entity resolution layer

## 5.18 SIGNATURE_DETECTION

### Description
Detect the presence and position of signatures.

### Minimum outputs
- signature detected yes/no
- location metadata
- confidence

### Candidate providers/modules
- internal CV/image heuristics
- external provider where needed
- future signature model

## 5.19 CLAUSE_EXTRACTION

### Description
Extract clause-like structured content for legal or policy documents.

### Minimum outputs
- clause segments
- labels/types where available
- document linkage

### Candidate providers/modules
- heuristic/NLP extraction
- future legal-document model
- external service where justified

## 5.20 QUESTION_ANSWER_SUPPORT

### Description
Support downstream question-answering over extracted document content.

### Minimum outputs
- structured content suitability markers
- document references / evidence spans where available

### Candidate providers/modules
- downstream QA layer over extracted content
- future retrieval and reasoning module

## 6. Provider Map

The following providers/modules are currently relevant.

### 6.1 Internal / open-source baseline
- Tesseract
- internal preprocessing lambda
- internal OCR worker
- internal table worker
- internal fraud worker
- internal aggregation worker
- OpenCV / CV heuristics
- lightweight NLP libraries
- barcode libraries

### 6.2 External / managed baseline
- AWS Textract DetectDocumentText
- AWS Textract AnalyzeDocument
- future specialist handwriting providers
- future external fraud/authenticity APIs

## 7. Bundled Capability Awareness

Some providers return multiple capabilities in a single paid execution.

Examples:
- Textract AnalyzeDocument may provide OCR, table extraction, key-value extraction, and selection mark outputs together

Therefore:
- if such a provider is selected, bundled outputs must be reused
- duplicate extraction through another provider for the same capability should be avoided unless explicitly justified
- execution planning must consider coverage, not only single capability choice

## 8. Capability-to-Provider Planning Rule

The execution decision ecosystem must choose providers/modules by evaluating:
- required capability coverage
- bundled capability overlap
- expected quality
- expected cost
- latency / SLA constraints
- fallback readiness
- future learning signals

This is not a single-provider decision problem.
It is a capability coverage optimisation problem.

## 9. Future Internalization Intent

The following capabilities are especially important for internalization over time:
- TEXT_OCR
- TABLE_STRUCTURE
- DOCUMENT_CLASSIFICATION
- AUTHENTICITY_SCORING
- TAMPER_DETECTION
- KEY_VALUE_EXTRACTION
- SIGNATURE_DETECTION

The reason is:
- cost control
- strategic differentiation
- reduced dependence on bundled external pricing
- improvement through owned data and evaluation loops

## 10. Strategic Outcome

This registry is successful when:
- all client-facing services can be decomposed into governed capabilities
- providers can be swapped without redesign
- bundled capability duplication is reduced
- execution decisions can optimise coverage, cost, and quality
- internalization priorities remain visible and explicit
