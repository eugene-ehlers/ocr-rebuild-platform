# Credit Decision — Input to Outcome Rule Table v1

## Purpose

Defines how approved OCR-first Credit requests are interpreted into governed Credit outcome structures.

This table operates strictly at the decision layer.

---

## Governance Notes

- This document is authoritative for the OCR-first Credit target basket in this application.
- Scope is limited to OCR-derived document evidence and governed analytical checks against OCR results.
- Bureau, PEP, PIP, Home Affairs, pricing, offer generation, and external credit data are out of scope for this app section.
- Extraction OTCs and analytical OTCs must remain distinct.
- Each request must resolve to exactly one governed outward outcome.
- Insufficient basis for the selected outcome must fail closed.

---

## Rule Table

### Credit-OTC-001
- outcome_code: Credit-OTC-001
- outcome_family: proof_verification
- outcome_intent: extract_payslip_fields
- degradation_policy: no_safe_degradation
- required_inputs: payload.request.outcome_code|payload.document.document_type|payload.document.file_bytes_b64_or_s3_uri
- required_outputs: extraction_status|extracted_payslip|overall_confidence|audit_trace|section_confidence_trace|provenance_trace|consent_trace|document_version_trace|fail_closed_reasons
- required_dependencies: payload.document.document_type=payslip|payload.substrates.ocr.raw_text|payload.substrates.ocr.page_traces|payload.substrates.ocr.engine_metadata
- required_capabilities: document_ocr|payslip_field_extraction|payroll_field_normalization|traceability_generation
- fail_closed_rules: missing_document_payload|unsupported_document_type|ocr_failure|missing_income_anchor_fields|missing_traceability
- prohibited_shortcuts: no_success_without_payslip_basis|no_manual_fill_as_ocr|no_inferred_income_values

### Credit-OTC-002
- outcome_code: Credit-OTC-002
- outcome_family: analytical
- outcome_intent: assess_payslip_income_validity
- degradation_policy: internal_review_required
- required_inputs: payload.substrates.ocr.structured_fields.payslip|payload.rules.credit.payslip_rules
- required_outputs: payslip_validity_determination|income_field_presence_flag|pay_period_presence_flag|name_presence_flag|anomaly_flags|summary|overall_confidence|audit_trace|section_confidence_trace|provenance_trace|consent_trace|document_version_trace|fail_closed_reasons
- required_dependencies: Credit-OTC-001 substrate|payslip_sufficiency_rules
- required_capabilities: pay_date_parsing|income_field_presence_check|component_coherence_check_optional|anomaly_flagging|traceability_generation
- fail_closed_rules: missing_payslip_substrate|required_income_anchor_missing|missing_traceability
- prohibited_shortcuts: no_usable_payslip_without_income_basis|no_validity_without_field_presence_check|no_inferred_pay_period

### Credit-OTC-003
- outcome_code: Credit-OTC-003
- outcome_family: proof_verification
- outcome_intent: extract_bank_statement_fields
- degradation_policy: no_safe_degradation
- required_inputs: payload.request.outcome_code|payload.document.document_type|payload.document.file_bytes_b64_or_s3_uri
- required_outputs: extraction_status|extracted_bank_statement|overall_confidence|audit_trace|section_confidence_trace|provenance_trace|consent_trace|document_version_trace|fail_closed_reasons
- required_dependencies: payload.document.document_type=bank_statement|payload.substrates.ocr.raw_text|payload.substrates.ocr.page_traces|payload.substrates.ocr.engine_metadata
- required_capabilities: document_ocr|statement_header_extraction|transaction_table_extraction|monetary_normalization|traceability_generation
- fail_closed_rules: missing_document_payload|unsupported_document_type|ocr_failure|missing_statement_period|missing_transaction_evidence|missing_traceability
- prohibited_shortcuts: no_success_without_statement_basis|no_inferred_transactions|no_manual_fill_as_ocr

### Credit-OTC-004
- outcome_code: Credit-OTC-004
- outcome_family: analytical
- outcome_intent: assess_bank_statement_income_signal
- degradation_policy: internal_review_required
- required_inputs: payload.substrates.ocr.structured_fields.bank_statement|payload.rules.credit.bank_income_rules
- required_outputs: bank_income_signal_determination|recurring_credit_count|estimated_recurring_income|salary_like_reference_flag|signal_score|summary|overall_confidence|audit_trace|section_confidence_trace|provenance_trace|consent_trace|document_version_trace|fail_closed_reasons
- required_dependencies: Credit-OTC-003 substrate|credit_transaction_detection_rules|recurring_pattern_rules
- required_capabilities: credit_transaction_detection|recurring_pattern_detection|salary_like_reference_detection_optional|income_signal_scoring|traceability_generation
- fail_closed_rules: missing_bank_statement_substrate|insufficient_transaction_data|missing_traceability
- prohibited_shortcuts: no_income_signal_without_transaction_basis|no_signal_score_without_trace_basis

### Credit-OTC-005
- outcome_code: Credit-OTC-005
- outcome_family: analytical
- outcome_intent: assess_bank_statement_expense_signal
- degradation_policy: internal_review_required
- required_inputs: payload.substrates.ocr.structured_fields.bank_statement|payload.rules.credit.bank_expense_rules
- required_outputs: bank_expense_signal_determination|estimated_recurring_expenses|recurring_obligation_count|high_risk_debit_flags|signal_score|summary|overall_confidence|audit_trace|section_confidence_trace|provenance_trace|consent_trace|document_version_trace|fail_closed_reasons
- required_dependencies: Credit-OTC-003 substrate|debit_classification_rules|recurring_debit_rules
- required_capabilities: debit_extraction|recurring_debit_detection|obligation_signal_scoring|traceability_generation
- fail_closed_rules: missing_bank_statement_substrate|insufficient_statement_coverage|missing_traceability
- prohibited_shortcuts: no_expense_signal_without_debit_basis|no_signal_score_without_trace_basis

### Credit-OTC-006
- outcome_code: Credit-OTC-006
- outcome_family: analytical
- outcome_intent: assess_payslip_to_bank_income_consistency
- degradation_policy: internal_review_required
- required_inputs: payload.substrates.ocr.structured_fields.payslip|payload.substrates.ocr.structured_fields.bank_statement|payload.rules.credit.income_consistency_rules
- required_outputs: income_consistency_determination|payslip_net_income|bank_supported_income|amount_variance|period_alignment_flag|summary|overall_confidence|audit_trace|section_confidence_trace|provenance_trace|consent_trace|document_version_trace|fail_closed_reasons
- required_dependencies: Credit-OTC-001 substrate|Credit-OTC-003 substrate|timing_alignment_rules|tolerance_band_rules
- required_capabilities: cross_document_matching|timing_alignment|tolerance_band_evaluation|traceability_generation
- fail_closed_rules: missing_required_substrate|missing_period_or_amount_anchor|missing_traceability
- prohibited_shortcuts: no_consistency_determination_without_both_document_bases|no_alignment_flag_without_period_basis

### Credit-OTC-007
- outcome_code: Credit-OTC-007
- outcome_family: analytical
- outcome_intent: produce_ocr_based_affordability_snapshot
- degradation_policy: internal_review_required
- required_inputs: payload.substrates.analytics.bank_income_signal|payload.substrates.analytics.bank_expense_signal|payload.rules.credit.affordability_rules
- required_outputs: affordability_snapshot_determination|estimated_income|estimated_expenses|estimated_surplus|constraint_flags|summary|overall_confidence|audit_trace|section_confidence_trace|provenance_trace|consent_trace|document_version_trace|fail_closed_reasons
- required_dependencies: Credit-OTC-004 substrate|Credit-OTC-005 substrate|affordability_rules
- required_capabilities: signal_consolidation|affordability_surplus_calculation|constraint_flagging|traceability_generation
- fail_closed_rules: missing_income_signal|missing_expense_signal|materially_incomplete_evidence|missing_traceability
- prohibited_shortcuts: no_affordability_without_signal_basis|no_surplus_without_income_and_expense_basis

### Credit-OTC-008
- outcome_code: Credit-OTC-008
- outcome_family: analytical
- outcome_intent: assess_credit_document_pack_completeness
- degradation_policy: no_safe_degradation
- required_inputs: payload.rules.credit.required_document_set|payload.documents_submitted|payload.substrates.completed_outcomes
- required_outputs: document_pack_completeness_determination|present_documents|missing_documents|blocking_gaps|summary|overall_confidence|audit_trace|section_confidence_trace|provenance_trace|consent_trace|document_version_trace|fail_closed_reasons
- required_dependencies: governed_document_checklist|submitted_document_inventory|completed_outcome_inventory
- required_capabilities: checklist_evaluation|missing_item_detection|dependency_readiness_evaluation|traceability_generation
- fail_closed_rules: missing_document_checklist|missing_inventory_basis|missing_traceability
- prohibited_shortcuts: no_complete_status_without_checklist_evidence|no_readiness_without_dependency_basis

### Credit-OTC-009
- outcome_code: Credit-OTC-009
- outcome_family: analytical
- outcome_intent: produce_ocr_based_credit_recommendation
- degradation_policy: internal_review_required
- required_inputs: payload.substrates.analytics.affordability_snapshot|payload.substrates.analytics.document_pack_completeness|payload.rules.credit.recommendation_rules
- required_outputs: credit_recommendation_determination|primary_reasons|blocking_flags|supporting_metrics|summary|overall_confidence|audit_trace|section_confidence_trace|provenance_trace|consent_trace|document_version_trace|fail_closed_reasons
- required_dependencies: Credit-OTC-007 substrate|Credit-OTC-008 substrate|recommendation_rules
- required_capabilities: rule_based_recommendationing|blocker_propagation|uncertainty_handling|traceability_generation
- fail_closed_rules: missing_upstream_substrate|missing_rule_basis|missing_traceability
- prohibited_shortcuts: no_recommendation_without_upstream_basis|no_proceed_status_without_sufficient_document_and_affordability_basis

---

## End of Document
