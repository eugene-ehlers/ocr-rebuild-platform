# FICA Compliance — Outcome to Capability Rule Table v1

## Purpose

Defines how OCR-first FICA outcome intents and required outcome structures map to capability requirements.

This table operates strictly at the decision and design layer.

---

## Governance Notes

- This table is authoritative for FICA OCR-first target-state capability mapping in this application.
- Obsolete transaction-compliance and consolidated compliance-risk outward intents are not authoritative target state for this app section.
- Mandatory capabilities are sufficiency-critical.

---

## Rule Table

### FICA-OTC-001
- outcome_code: FICA-OTC-001
- outcome_intent: extract_identity_document_fields
- mandatory_capabilities: document_ocr|identity_field_extraction|field_normalization|traceability_generation
- optional_capabilities: image_quality_assessment|document_type_confirmation
- enrichment_capabilities: none
- prohibited_shortcuts: no_success_without_identity_anchor_extraction
- required_data_dependencies: document_page_data|ocr_text|identity_field_candidates
- required_ocr_feature_classes: text|layout|metadata
- sufficiency_rule: identity_extraction_requires_name_and_document_anchor_fields

### FICA-OTC-002
- outcome_code: FICA-OTC-002
- outcome_intent: assess_identity_field_consistency
- mandatory_capabilities: exact_field_matching|normalized_field_matching|mismatch_reasoning|traceability_generation
- optional_capabilities: dob_matching
- enrichment_capabilities: none
- prohibited_shortcuts: no_identity_match_without_document_and_subject_basis
- required_data_dependencies: extracted_identity_fields|subject_identity_fields
- required_ocr_feature_classes: text|metadata
- sufficiency_rule: consistency_determination_requires_primary_identity_anchor_comparison

### FICA-OTC-003
- outcome_code: FICA-OTC-003
- outcome_intent: extract_proof_of_address_fields
- mandatory_capabilities: document_ocr|address_field_extraction|address_normalization|traceability_generation
- optional_capabilities: issuer_extraction
- enrichment_capabilities: none
- prohibited_shortcuts: no_success_without_address_and_date_basis
- required_data_dependencies: document_page_data|ocr_text|address_field_candidates
- required_ocr_feature_classes: text|layout|metadata
- sufficiency_rule: proof_of_address_extraction_requires_address_content_and_document_date

### FICA-OTC-004
- outcome_code: FICA-OTC-004
- outcome_intent: assess_proof_of_address_validity_and_recency
- mandatory_capabilities: date_interpretation|recency_calculation|address_completeness_check|traceability_generation
- optional_capabilities: issuer_acceptance_check
- enrichment_capabilities: none
- prohibited_shortcuts: no_recency_pass_without_date_basis
- required_data_dependencies: extracted_address_fields|max_age_rule
- required_ocr_feature_classes: text|metadata
- sufficiency_rule: validity_requires_document_date_and_address_completeness_basis

### FICA-OTC-005
- outcome_code: FICA-OTC-005
- outcome_intent: extract_business_registration_fields
- mandatory_capabilities: document_ocr|business_field_extraction|entity_normalization|traceability_generation
- optional_capabilities: director_or_member_extraction
- enrichment_capabilities: none
- prohibited_shortcuts: no_success_without_company_name_and_registration_number
- required_data_dependencies: document_page_data|ocr_text|business_field_candidates
- required_ocr_feature_classes: text|layout|metadata
- sufficiency_rule: business_registration_extraction_requires_company_identity_anchors

### FICA-OTC-006
- outcome_code: FICA-OTC-006
- outcome_intent: assess_business_ownership_or_authority_consistency
- mandatory_capabilities: company_identity_matching|registration_matching|authority_presence_check|gap_reasoning|traceability_generation
- optional_capabilities: represented_person_name_match
- enrichment_capabilities: none
- prohibited_shortcuts: no_authority_support_without_document_evidence
- required_data_dependencies: extracted_business_fields|claimed_company_fields
- required_ocr_feature_classes: text|metadata
- sufficiency_rule: business_consistency_requires_company_anchor_comparison_and_gap_traceability

---

## End of Document
