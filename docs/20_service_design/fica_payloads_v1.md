# FICA Payloads v1

## Purpose

Defines governed payload carriers for OCR-first FICA outcomes and supporting substrates.

## Root Carriers

{
  "payload": {
    "request": {},
    "document": {},
    "subject": {},
    "substrates": {
      "ocr": {},
      "analytics": {}
    },
    "runtime": {
      "current_outcome": {}
    }
  }
}

## Request Carriers

- `payload.request.outcome_code`
- `payload.request.outcome_family`
- `payload.request.client_reference`
- `payload.request.request_timestamp`
- `payload.request.consent_reference`

## Document Carriers

- `payload.document.document_id`
- `payload.document.document_type`
- `payload.document.file_format`
- `payload.document.file_bytes_b64`
- `payload.document.s3_uri`
- `payload.document.document_country`
- `payload.document.document_language`

Allowed FICA OCR-first document types:
- `identity_document`
- `proof_of_address`
- `business_registration`

## Subject Carriers

- `payload.subject.subject_type`
- `payload.subject.first_name`
- `payload.subject.last_name`
- `payload.subject.full_name`
- `payload.subject.id_number`
- `payload.subject.date_of_birth`
- `payload.subject.company_name`
- `payload.subject.registration_number`

## OCR Substrates

- `payload.substrates.ocr.raw_text`
- `payload.substrates.ocr.structured_fields.identity`
- `payload.substrates.ocr.structured_fields.proof_of_address`
- `payload.substrates.ocr.structured_fields.business_registration`
- `payload.substrates.ocr.page_traces`
- `payload.substrates.ocr.engine_metadata`

## Analytics Substrates

- `payload.substrates.analytics.identity_consistency`
- `payload.substrates.analytics.proof_of_address_validity`
- `payload.substrates.analytics.business_consistency`

## Runtime Current Outcome

- `payload.runtime.current_outcome.outcome_code`
- `payload.runtime.current_outcome.outcome_family`
- `payload.runtime.current_outcome.outcome_payload`
- `payload.runtime.current_outcome.audit_trace`
- `payload.runtime.current_outcome.section_confidence_trace`
- `payload.runtime.current_outcome.provenance_trace`
- `payload.runtime.current_outcome.consent_trace`
- `payload.runtime.current_outcome.document_version_trace`
- `payload.runtime.current_outcome.fail_closed_reasons`

## Traceability Expectation

Every outward FICA outcome must carry:
- `audit_trace`
- `section_confidence_trace`
- `provenance_trace`
- `consent_trace`
- `document_version_trace`
- `fail_closed_reasons`

## Scope Constraint

This payload contract is limited to OCR-first FICA document extraction and document-evidence-based analytical checks.
No bureau, PEP, PIP, Home Affairs, or other external compliance-enrichment scope is included.

---

## End of Document
