# FICA Compliance — Input to Outcome Rule Table v1

## Purpose

Defines how approved OCR-first FICA requests are interpreted into governed FICA outcome structures.

This table operates strictly at the decision layer:

request -> outcome_intent -> outcome_structure

It does NOT define:
- providers
- execution logic
- worker sequencing
- implementation code

---

## Governance Notes

- This document is authoritative for the OCR-first FICA target basket in this application.
- Scope is limited to OCR-derived document evidence and governed analytical checks against OCR results.
- Bureau, PEP, PIP, Home Affairs, and other external compliance scope are explicitly out of scope for this app.
- Extraction OTCs and analytical OTCs must remain distinct.
- Each request must resolve to exactly one governed outward outcome.
- Insufficient basis for the selected outcome must fail closed.

### Controlled Vocabulary Rule

Tokens in this table are governed design-time normalized vocabulary for request-to-outcome mapping.

### Degradation Policy

Allowed values include:
- no_safe_degradation
- internal_review_required
- escalate_for_missing_dependencies

---

## Rule Table

### FICA-OTC-001
- outcome_code: FICA-OTC-001
- outcome_family: proof_verification
- outcome_intent: extract_identity_document_fields
- degradation_policy: no_safe_degradation
- required_inputs: payload.request.outcome_code|payload.document.document_type|payload.document.file_bytes_b64_or_s3_uri
- required_outputs: extraction_status|extracted_identity|overall_confidence|audit_trace|section_confidence_trace|provenance_trace|consent_trace|document_version_trace|fail_closed_reasons
- required_dependencies: payload.document.document_type=identity_document|payload.substrates.ocr.raw_text|payload.substrates.ocr.page_traces|payload.substrates.ocr.engine_metadata
- required_capabilities: document_ocr|identity_field_extraction|field_normalization|traceability_generation
- fail_closed_rules: missing_document_payload|unsupported_document_type|ocr_failure|missing_identity_anchor_fields|missing_traceability
- prohibited_shortcuts: no_manual_fill_as_ocr|no_success_without_extracted_identity_basis|no_missing_confidence_suppression

### FICA-OTC-002
- outcome_code: FICA-OTC-002
- outcome_family: analytical
- outcome_intent: assess_identity_field_consistency
- degradation_policy: no_safe_degradation
- required_inputs: payload.substrates.ocr.structured_fields.identity|payload.subject.first_name|payload.subject.last_name|payload.subject.id_number
- required_outputs: identity_match_determination|name_match_flag|id_number_match_flag|dob_match_flag|mismatch_reasons|summary|overall_confidence|audit_trace|section_confidence_trace|provenance_trace|consent_trace|document_version_trace|fail_closed_reasons
- required_dependencies: FICA-OTC-001 substrate|identity_matching_rules
- required_capabilities: exact_field_matching|normalized_field_matching|mismatch_reasoning|traceability_generation
- fail_closed_rules: missing_identity_substrate|missing_required_subject_fields|no_primary_identity_anchor|missing_traceability
- prohibited_shortcuts: no_match_without_document_basis|no_manual_review_without_discrepancy_basis|no_inferred_identity_confirmation

### FICA-OTC-003
- outcome_code: FICA-OTC-003
- outcome_family: proof_verification
- outcome_intent: extract_proof_of_address_fields
- degradation_policy: no_safe_degradation
- required_inputs: payload.request.outcome_code|payload.document.document_type|payload.document.file_bytes_b64_or_s3_uri
- required_outputs: extraction_status|extracted_address|overall_confidence|audit_trace|section_confidence_trace|provenance_trace|consent_trace|document_version_trace|fail_closed_reasons
- required_dependencies: payload.document.document_type=proof_of_address|payload.substrates.ocr.raw_text|payload.substrates.ocr.page_traces|payload.substrates.ocr.engine_metadata
- required_capabilities: document_ocr|address_field_extraction|address_normalization|traceability_generation
- fail_closed_rules: missing_document_payload|unsupported_document_type|ocr_failure|missing_address_content|missing_document_date|missing_traceability
- prohibited_shortcuts: no_success_without_address_basis|no_inferred_address_completion|no_manual_fill_as_ocr

### FICA-OTC-004
- outcome_code: FICA-OTC-004
- outcome_family: analytical
- outcome_intent: assess_proof_of_address_validity_and_recency
- degradation_policy: no_safe_degradation
- required_inputs: payload.substrates.ocr.structured_fields.proof_of_address|payload.rules.proof_of_address.max_age_days
- required_outputs: address_validity_determination|recency_pass_flag|address_completeness_flag|issuer_acceptance_flag|document_age_days|summary|overall_confidence|audit_trace|section_confidence_trace|provenance_trace|consent_trace|document_version_trace|fail_closed_reasons
- required_dependencies: FICA-OTC-003 substrate|date_normalization_rules|issuer_acceptance_rules_if_enabled
- required_capabilities: date_interpretation|recency_calculation|address_completeness_check|issuer_check_optional|traceability_generation
- fail_closed_rules: missing_proof_of_address_substrate|missing_document_date|required_recency_uncomputable|missing_traceability
- prohibited_shortcuts: no_validity_without_date_basis|no_recency_pass_without_age_calculation|no_issuer_acceptance_without_rule_basis

### FICA-OTC-005
- outcome_code: FICA-OTC-005
- outcome_family: proof_verification
- outcome_intent: extract_business_registration_fields
- degradation_policy: no_safe_degradation
- required_inputs: payload.request.outcome_code|payload.document.document_type|payload.document.file_bytes_b64_or_s3_uri
- required_outputs: extraction_status|extracted_business|overall_confidence|audit_trace|section_confidence_trace|provenance_trace|consent_trace|document_version_trace|fail_closed_reasons
- required_dependencies: payload.document.document_type=business_registration|payload.substrates.ocr.raw_text|payload.substrates.ocr.page_traces|payload.substrates.ocr.engine_metadata
- required_capabilities: document_ocr|business_field_extraction|entity_normalization|traceability_generation
- fail_closed_rules: missing_document_payload|unsupported_document_type|ocr_failure|missing_company_name|missing_registration_number|missing_traceability
- prohibited_shortcuts: no_success_without_company_identity_anchors|no_manual_fill_as_ocr|no_inferred_registration_number

### FICA-OTC-006
- outcome_code: FICA-OTC-006
- outcome_family: analytical
- outcome_intent: assess_business_ownership_or_authority_consistency
- degradation_policy: internal_review_required
- required_inputs: payload.substrates.ocr.structured_fields.business_registration|payload.subject.company_name|payload.subject.registration_number
- required_outputs: business_consistency_determination|company_name_match_flag|registration_match_flag|represented_person_found_flag|gaps|summary|overall_confidence|audit_trace|section_confidence_trace|provenance_trace|consent_trace|document_version_trace|fail_closed_reasons
- required_dependencies: FICA-OTC-005 substrate|entity_matching_rules|authority_presence_rules
- required_capabilities: company_identity_matching|registration_matching|authority_presence_check|gap_reasoning|traceability_generation
- fail_closed_rules: missing_business_registration_substrate|missing_claimed_company_anchors|missing_traceability
- prohibited_shortcuts: no_supported_authority_without_document_evidence|no_match_without_registration_or_name_basis|no_inferred_representative_authority

---

## End of Document
