# OCR Rebuild — Technology and Service Compatibility Baseline

Status: DRAFT - STACK COMPATIBILITY BASELINE

## 1. Purpose

Define the governed technology and service stack baseline for OCR Rebuild so that:

- all runtime components use compatible versions
- packaging choices are decided before detailed implementation
- container and Lambda build strategies are controlled
- provider selection starts from a known-good baseline
- future capability additions do not repeatedly break builds, images, or deployment flows

This document is authoritative for:
- runtime version baseline
- packaging baseline
- approved library baseline
- approved managed-service baseline
- compatibility status
- licensing constraints
- approved / provisional / rejected stack components

## 2. Core Principle

The platform must not adopt libraries and services incrementally without checking stack compatibility.

Before detailed feature implementation continues, the platform must define:

- what runtime families are approved
- what packaging models are approved
- what libraries and versions are approved
- what managed services are approved
- what combinations are known to work together
- what combinations are intentionally not allowed

## 3. Current Governed Stack Direction

The current architecture direction is:

- AWS-first orchestration and runtime
- Python 3.11 baseline
- hybrid internal/open-source first where justified
- AWS Textract as the governed external fallback direction
- container-based packaging where dependency weight or OS-level dependencies make Lambda zip fragile
- execution-plan-driven provider selection

This is the current governed direction, not necessarily the final long-term winner for every capability.

## 4. Runtime Baseline

## 4.1 Approved runtime family
- Python 3.11

## 4.2 Approved execution platforms
- AWS Lambda for lighter orchestration-adjacent components
- AWS Lambda container image packaging where dependencies justify it
- ECS/Fargate for heavier or longer-running capability workers

## 4.3 Runtime approval rationale
Python 3.11 is the approved current runtime baseline because:
- it is supported by AWS Lambda
- it aligns with current container and worker direction
- it is modern enough for current dependencies
- it reduces version sprawl across services

## 5. Packaging Baseline

## 5.1 Approved packaging models
- Lambda zip package for lightweight functions only
- Lambda container image for dependency-heavy functions that still suit Lambda execution
- ECS container for heavier workers and binary-dependent services

## 5.2 Packaging rules
- do not force heavy binary dependencies into Lambda zip if container packaging is the cleaner governed choice
- use container packaging where OS-level dependency management is required
- use ECS/Fargate when runtime weight, execution duration, or binary/library complexity justifies it

## 5.3 Initial packaging direction
- preprocessing: Lambda-compatible but container option remains acceptable if dependency weight grows
- OCR worker: container-based
- table extraction: likely container-based
- fraud/authenticity: container-based or lightweight worker depending on dependency mix
- aggregation: lightweight runtime acceptable

## 6. Approved Technology Baseline by Capability Area

## 6.1 Preprocessing baseline
### Approved now
- Python 3.11
- Pillow==12.1.1
- PyMuPDF==1.23.26
- boto3

### Packaging direction
- approved for current baseline
- must remain under governed packaging limits if kept outside containers

### Notes
- PyMuPDF is used for PDF page rendering
- PyMuPDF licensing must remain explicitly governed
- current stack proof succeeded with:
  - PyMuPDF 1.23.26
  - Pillow 12.1.1
  - boto3 1.40.4

## 6.2 OCR baseline
### Approved now
- Python 3.11
- pytesseract
- system tesseract-ocr package
- Pillow==12.1.1
- boto3
- opencv-python-headless (approved baseline dependency candidate where required)

### Packaging direction
- container-based baseline preferred

### Notes
- pytesseract is a wrapper, not the OCR engine itself
- Tesseract OS package availability and compatibility must be controlled through the image build
- OCR provider selection must move to execution_plan control rather than remain hardcoded
- current OCR container stack proof build succeeded for:
  - python:3.11-slim
  - tesseract-ocr
  - pytesseract
  - Pillow
  - opencv-python-headless

## 6.3 Managed fallback baseline
### Approved now
- AWS Textract DetectDocumentText
- AWS Textract AnalyzeDocument

### Notes
- Textract is the governed external fallback direction in the current baseline
- Google Document AI is not part of the approved current baseline
- other providers may be evaluated later, but are not currently governed as part of the standard stack

## 6.4 Table / structured extraction baseline
### Approved now
- current internal heuristic worker
- AWS Textract AnalyzeDocument fallback
- OpenCV-based internal support where justified

### Status
- approved as baseline direction
- not yet final long-term winner

## 6.5 Fraud / authenticity baseline
### Approved now
- current internal heuristic fraud/authenticity worker
- rule-based initial implementation
- future external specialist providers may be evaluated later

### Status
- approved as baseline direction
- not yet final long-term winner

## 7. Version Baseline Matrix

The following versions are currently treated as baseline-approved unless revised through controlled change:

| Component | Approved Version / Baseline | Status | Notes |
| --- | --- | --- | --- |
| Python runtime | 3.11 | Approved | Standardize across services |
| boto3 | version policy still to be standardized; 1.40.4 proven in preprocessing stack proof | Approved | Standardize explicitly in controlled follow-on |
| Pillow | 12.1.1 | Approved | Proven in preprocessing stack proof |
| PyMuPDF | 1.23.26 | Approved | Chosen because compatible wheel availability was demonstrated in current build path |
| pytesseract | current repo baseline | Approved | Wrapper only |
| tesseract-ocr | OS package in OCR image | Approved | Must be container-managed |
| opencv-python-headless | current repo baseline | Provisional | Keep only where justified |
| AWS Textract | managed service | Approved | Governed external fallback |
| Google Document AI | not in baseline | Rejected for current baseline | Can be evaluated later |
| PyMuPDF commercial extensions / Pro | not in baseline | Provisional | Only if Office-format strategy requires it and licensing is approved |

## 8. Licensing Baseline

## 8.1 PyMuPDF
PyMuPDF licensing must be treated as a governed decision because it is offered under AGPL and commercial licensing terms.

### Rule
- do not assume unrestricted production use without confirming licensing posture
- legal/commercial review must determine whether AGPL obligations are acceptable or whether a commercial license is required

## 8.2 General rule
Every dependency added to the governed stack must have:
- license identified
- compatibility with intended use confirmed
- approval status recorded

## 9. Approval Status Model

Each component in the compatibility baseline must carry one of these statuses:

- Approved
- Provisional
- Rejected

### Approved
Allowed for current implementation.

### Provisional
Promising but not yet fully ratified for standard use.

### Rejected
Not part of the current governed baseline.

## 10. Known-Good Baseline Combination (Current)

The current known-good baseline combination to standardize on is:

- Python 3.11
- AWS-first runtime
- Lambda + Lambda container image + ECS/Fargate mix
- Pillow
- PyMuPDF==1.23.26
- pytesseract
- system tesseract-ocr
- boto3
- current OCR/image workers using container-friendly packaging where needed
- AWS Textract as governed managed fallback

This combination is the current approved build baseline.

### Current proof status
The following baseline compatibility proofs have been completed:

- OCR container stack proof: passed
- preprocessing dependency/runtime proof: passed

This means the current baseline is considered implementable for:
- preprocessing
- OCR
- AWS-first runtime execution

It does not yet mean the full future capability stack has been proven.

## 11. What Is Not Yet Finalized

The following remain intentionally open for later evaluation:

- final long-term OCR champion
- final handwriting provider
- final table extraction champion
- final key-value/forms champion
- final authenticity/tamper stack
- final champion/challenger configuration
- any Google-based provider usage

These are not required to be finalized before continuing implementation, provided the approved baseline above is used consistently.

## 11.1 Still requiring explicit proof or standardization

The following remain open and must be handled through controlled follow-on validation:

- explicit boto3 version standardization across services
- end-to-end preprocessing to OCR proof under governed payload contracts
- execution-plan-driven OCR provider selection
- Textract fallback wiring
- future handwriting, key-value, signature, checkbox, barcode, and tamper stacks

## 12. Implementation Rule

No developer may introduce a new dependency, provider, runtime version, or packaging model into the standard stack unless this document is updated or the change is explicitly governed in the same change set.

## 13. Immediate Baseline Actions Required

The next implementation steps must align code to this baseline:

1. preprocessing must preserve execution-plan-aware payloads
2. OCR worker must read provider choice from execution_plan
3. OCR worker must assume Tesseract as current primary baseline and Textract as governed fallback path
4. runtime packaging decisions must be made from this baseline, not ad hoc per task
5. future capability additions must first be added to this baseline before being treated as standard stack components

6. boto3 version policy must be explicitly standardized before broader service expansion
7. stack-proof evidence must be updated whenever a baseline dependency or provider is changed

## 14. Strategic Outcome

This document is successful when:

- the platform has a known-good, compatible baseline stack
- build and packaging decisions are no longer ad hoc
- future implementation uses approved combinations
- dependency and provider drift are controlled
- container/image/runtime issues are reduced by deciding stack compatibility up front
