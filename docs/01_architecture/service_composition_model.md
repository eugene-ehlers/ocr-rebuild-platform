# OCR Rebuild — Service Composition Model

Status: DRAFT - STRATEGIC OPERATING BASELINE

## 1. Purpose

Define how client-facing services are constructed from reusable document intelligence capabilities.

This document is authoritative for:
- the relationship between client requests and platform-delivered services
- decomposition of services into sub-services and atomic capabilities
- minimum output requirements for each service
- separation between service composition and execution decisioning
- future service creation without backend redesign

The platform must be:
- composable
- capability-driven
- provider-agnostic
- extensible without redesign

---

## 2. Core Principle

The platform must not implement fixed products directly.

Instead:

1. Client makes request
2. Service is defined logically
3. Service decomposes into sub-services
4. Sub-services map to atomic capabilities
5. Capabilities are fulfilled by execution decision engines

Services are assembled, not hard-coded.

---

## 3. Layer Separation

### 3.1 Client Service Layer
What the client requests.

Examples:
- OCR
- Fraud analysis
- Will validation
- CV intelligence
- Audit packs

---

### 3.2 Service Composition Layer
Determines:
- what must be delivered
- required capabilities
- minimum outputs
- applicable decision gates

Does NOT choose providers.

---

### 3.3 Capability Layer
Atomic building blocks.

Examples:
- TEXT_OCR
- TABLE_STRUCTURE
- SIGNATURE_DETECTION
- AUTHENTICITY_SCORING

---

### 3.4 Execution Decision Layer
Determines:
- which provider fulfills each capability
- routing and fallback
- optimisation

---

## 4. Service Composition Rules

- Every service must map to capabilities
- Capabilities must be reusable
- No provider logic in service definition
- Services define outcomes, not execution
- Minimum outputs must be defined

---

## 5. Service Model Structure

Each service must define:

- service_id
- service_name
- client_objective
- required_subservices
- required_capabilities
- optional_capabilities
- minimum_output_requirements
- relevant_decision_gates
- escalation_rules

---

## 6. Service Categories

### Foundational
- OCR
- classification
- extraction

### Trust & Fraud
- authenticity
- tamper detection

### Financial
- bank statements
- affordability

### Legal
- wills
- insurance

### Employment
- CVs
- onboarding packs

### Enterprise
- audit packs
- compliance bundles

---

## 7. Sub-Service Model

Examples:
- content extraction
- classification
- signature detection
- fraud analysis
- Q&A enablement

Sub-services are logical groupings above capabilities.

---

## 8. Capability Model (Illustrative)

- TEXT_OCR
- TEXT_STRUCTURE
- TABLE_DETECTION
- TABLE_STRUCTURE
- KEY_VALUE_EXTRACTION
- HANDWRITING_EXTRACTION
- DOCUMENT_CLASSIFICATION
- SIGNATURE_DETECTION
- CHECKBOX_DETECTION
- BARCODE_QR
- LANGUAGE_DETECTION
- LAYOUT_ANALYSIS
- FONT_ANALYSIS
- IMAGE_REGION
- AUTHENTICITY_SCORING
- TAMPER_DETECTION
- CONSISTENCY_CHECK
- CROSS_DOCUMENT_MATCH
- QUESTION_ANSWER_SUPPORT

Full registry defined separately.

---

## 9. Minimum Service Requirements

Each service must define:

- objective
- required capabilities
- optional capabilities
- minimum outputs
- partial completion rules
- escalation rules
- decision gates used

---

## 10. Decision Gate Usage

Standard gates:

- Gate 0: request interpretation
- Gate 1: document understanding
- Gate 2: extraction quality
- Gate 3: service completeness
- Gate 4: final validation

Services define which apply.

---

## 11. Example Services

### Basic OCR

Required:
- TEXT_OCR

Outputs:
- text
- confidence

Gates:
- 0,1,2,4

---

### Bank Statement Fraud

Required:
- TEXT_OCR
- TABLE_STRUCTURE
- AUTHENTICITY_SCORING
- CONSISTENCY_CHECK

Gates:
- all

---

### Will Validation

Required:
- TEXT_OCR
- SIGNATURE_DETECTION
- AUTHENTICITY_SCORING
- KEY_VALUE_EXTRACTION
- QUESTION_ANSWER_SUPPORT

Gates:
- all

---

### CV Intelligence

Required:
- TEXT_OCR
- DOCUMENT_CLASSIFICATION
- TEXT_STRUCTURE

Gates:
- all

---

## 12. Bundled Provider Awareness

Some providers deliver multiple capabilities.

The system must:
- avoid duplicate extraction
- reuse outputs from bundled calls

Service layer defines needs.
Execution layer optimizes providers.

---

## 13. Service Creation Rule

New services are created by:

1. defining objective
2. defining capabilities
3. defining outputs
4. defining gates

No backend redesign required if capabilities exist.

---

## 14. Strategic Outcome

Success means:

- services assembled dynamically
- no hard-coded products
- reusable capabilities
- flexible client offerings
- fast innovation capability

