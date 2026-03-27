# Credit Decision Payloads v1

## Purpose

Defines governed payload carriers for OCR-first Credit outcomes and supporting substrates.

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

Allowed Credit OCR-first document types:
- `payslip`
- `bank_statement`

## Subject Carriers

- `payload.subject.subject_type`
- `payload.subject.full_name`
- `payload.subject.first_name`
- `payload.subject.last_name`
- `payload.subject.id_number`

## OCR Substrates

- `payload.substrates.ocr.raw_text`
- `payload.substrates.ocr.structured_fields.payslip`
- `payload.substrates.ocr.structured_fields.bank_statement`
- `payload.substrates.ocr.page_traces`
- `payload.substrates.ocr.engine_metadata`

## Analytics Substrates

- `payload.substrates.analytics.bank_income_signal`
- `payload.substrates.analytics.bank_expense_signal`
- `payload.substrates.analytics.income_consistency`
- `payload.substrates.analytics.affordability_snapshot`
- `payload.substrates.analytics.document_pack_completeness`
- `payload.substrates.analytics.recommendation_support_metrics`

## Rules Carriers

- `payload.rules.credit.payslip_rules`
- `payload.rules.credit.bank_income_rules`
- `payload.rules.credit.bank_expense_rules`
- `payload.rules.credit.income_consistency_rules`
- `payload.rules.credit.affordability_rules`
- `payload.rules.credit.required_document_set`
- `payload.rules.credit.recommendation_rules`

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

Every outward Credit outcome must carry:
- `audit_trace`
- `section_confidence_trace`
- `provenance_trace`
- `consent_trace`
- `document_version_trace`
- `fail_closed_reasons`

## Scope Constraint

This payload contract is limited to OCR-first credit-document extraction and document-evidence-based analytical checks.
No bureau, pricing, offer generation, PEP, PIP, or Home Affairs scope is included.

---

## End of Document
