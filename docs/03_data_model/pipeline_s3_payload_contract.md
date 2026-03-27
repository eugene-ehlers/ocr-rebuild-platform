# Pipeline S3 Payload Contract

## Purpose

Defines the governed pipeline payload carriers required for OCR-first document processing and governed outward outcome emission.

## Field-Level Additions and Clarifications for OCR-First FICA and Credit

### Request

- `payload.request.outcome_code`
- `payload.request.outcome_family`
- `payload.request.client_reference`
- `payload.request.request_timestamp`
- `payload.request.consent_reference`

### Document

- `payload.document.document_id`
- `payload.document.document_type`
- `payload.document.file_format`
- `payload.document.file_bytes_b64`
- `payload.document.s3_uri`
- `payload.document.document_country`
- `payload.document.document_language`

Rule:
- at least one of `payload.document.file_bytes_b64` or `payload.document.s3_uri` must be present

### Subject

- `payload.subject.subject_type`
- `payload.subject.first_name`
- `payload.subject.last_name`
- `payload.subject.full_name`
- `payload.subject.id_number`
- `payload.subject.date_of_birth`
- `payload.subject.company_name`
- `payload.subject.registration_number`

### OCR Substrates

- `payload.substrates.ocr.raw_text`
- `payload.substrates.ocr.structured_fields.identity`
- `payload.substrates.ocr.structured_fields.proof_of_address`
- `payload.substrates.ocr.structured_fields.business_registration`
- `payload.substrates.ocr.structured_fields.payslip`
- `payload.substrates.ocr.structured_fields.bank_statement`
- `payload.substrates.ocr.page_traces`
- `payload.substrates.ocr.engine_metadata`

### Analytics Substrates

- `payload.substrates.analytics.identity_consistency`
- `payload.substrates.analytics.proof_of_address_validity`
- `payload.substrates.analytics.business_consistency`
- `payload.substrates.analytics.bank_income_signal`
- `payload.substrates.analytics.bank_expense_signal`
- `payload.substrates.analytics.income_consistency`
- `payload.substrates.analytics.affordability_snapshot`
- `payload.substrates.analytics.document_pack_completeness`
- `payload.substrates.analytics.recommendation_support_metrics`

### Runtime Current Outcome

- `payload.runtime.current_outcome.outcome_code`
- `payload.runtime.current_outcome.outcome_family`
- `payload.runtime.current_outcome.outcome_payload`
- `payload.runtime.current_outcome.audit_trace`
- `payload.runtime.current_outcome.section_confidence_trace`
- `payload.runtime.current_outcome.provenance_trace`
- `payload.runtime.current_outcome.consent_trace`
- `payload.runtime.current_outcome.document_version_trace`
- `payload.runtime.current_outcome.fail_closed_reasons`

### Rules Carriers

- `payload.rules.proof_of_address.max_age_days`
- `payload.rules.credit.payslip_rules`
- `payload.rules.credit.bank_income_rules`
- `payload.rules.credit.bank_expense_rules`
- `payload.rules.credit.income_consistency_rules`
- `payload.rules.credit.affordability_rules`
- `payload.rules.credit.required_document_set`
- `payload.rules.credit.recommendation_rules`

## Scope Constraint

This contract update is limited to OCR-first FICA and Credit basket support.
It does not add bureau, PEP, PIP, Home Affairs, pricing, or offer-generation scope.

---

## End of Document
