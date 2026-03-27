# Credit Decision — Outcome to Capability Rule Table v1

## Purpose

Defines how OCR-first Credit outcome intents and required outcome structures map to capability requirements.

---

## Governance Notes

- This table is authoritative for Credit OCR-first target-state capability mapping in this application.
- Obsolete outward intents such as collections timing optimisation, customer decision status communication, and repayment expectation summary are not authoritative target state for this app section.
- Mandatory capabilities are sufficiency-critical.

---

## Rule Table

### Credit-OTC-001
- outcome_code: Credit-OTC-001
- outcome_intent: extract_payslip_fields
- mandatory_capabilities: document_ocr|payslip_field_extraction|payroll_field_normalization|traceability_generation
- optional_capabilities: employer_field_extraction
- enrichment_capabilities: none
- prohibited_shortcuts: no_success_without_income_anchor_extraction
- required_data_dependencies: document_page_data|ocr_text|payslip_field_candidates
- required_ocr_feature_classes: text|layout|metadata
- sufficiency_rule: payslip_extraction_requires_employee_name_and_income_anchor

### Credit-OTC-002
- outcome_code: Credit-OTC-002
- outcome_intent: assess_payslip_income_validity
- mandatory_capabilities: pay_date_parsing|income_field_presence_check|anomaly_flagging|traceability_generation
- optional_capabilities: component_coherence_check
- enrichment_capabilities: none
- prohibited_shortcuts: no_validity_without_income_basis
- required_data_dependencies: extracted_payslip_fields|payslip_rules
- required_ocr_feature_classes: text|metadata
- sufficiency_rule: payslip_validity_requires_income_anchor_and_period_basis

### Credit-OTC-003
- outcome_code: Credit-OTC-003
- outcome_intent: extract_bank_statement_fields
- mandatory_capabilities: document_ocr|statement_header_extraction|transaction_table_extraction|monetary_normalization|traceability_generation
- optional_capabilities: transaction_summary_generation
- enrichment_capabilities: none
- prohibited_shortcuts: no_success_without_statement_period_and_transaction_basis
- required_data_dependencies: document_page_data|ocr_text|transaction_rows
- required_ocr_feature_classes: text|tables|layout|metadata
- sufficiency_rule: bank_statement_extraction_requires_statement_period_and_transaction_evidence

### Credit-OTC-004
- outcome_code: Credit-OTC-004
- outcome_intent: assess_bank_statement_income_signal
- mandatory_capabilities: credit_transaction_detection|recurring_pattern_detection|income_signal_scoring|traceability_generation
- optional_capabilities: salary_like_reference_detection
- enrichment_capabilities: none
- prohibited_shortcuts: no_signal_without_credit_transaction_basis
- required_data_dependencies: parsed_transactions|income_signal_rules
- required_ocr_feature_classes: text|tables|layout
- sufficiency_rule: income_signal_requires_transaction_basis_and_signal_traceability

### Credit-OTC-005
- outcome_code: Credit-OTC-005
- outcome_intent: assess_bank_statement_expense_signal
- mandatory_capabilities: debit_extraction|recurring_debit_detection|obligation_signal_scoring|traceability_generation
- optional_capabilities: high_risk_debit_flagging
- enrichment_capabilities: none
- prohibited_shortcuts: no_signal_without_debit_basis
- required_data_dependencies: parsed_transactions|expense_signal_rules
- required_ocr_feature_classes: text|tables|layout
- sufficiency_rule: expense_signal_requires_debit_basis_and_signal_traceability

### Credit-OTC-006
- outcome_code: Credit-OTC-006
- outcome_intent: assess_payslip_to_bank_income_consistency
- mandatory_capabilities: cross_document_matching|timing_alignment|tolerance_band_evaluation|traceability_generation
- optional_capabilities: none
- enrichment_capabilities: none
- prohibited_shortcuts: no_consistency_without_both_document_bases
- required_data_dependencies: extracted_payslip_fields|extracted_bank_statement_fields|income_consistency_rules
- required_ocr_feature_classes: text|tables|metadata
- sufficiency_rule: consistency_requires_amount_anchor_and_period_alignment_basis

### Credit-OTC-007
- outcome_code: Credit-OTC-007
- outcome_intent: produce_ocr_based_affordability_snapshot
- mandatory_capabilities: signal_consolidation|affordability_surplus_calculation|constraint_flagging|traceability_generation
- optional_capabilities: none
- enrichment_capabilities: none
- prohibited_shortcuts: no_affordability_without_income_and_expense_signal_basis
- required_data_dependencies: bank_income_signal|bank_expense_signal|affordability_rules
- required_ocr_feature_classes: none
- sufficiency_rule: affordability_snapshot_requires_governed_signal_inputs_and_traceability

### Credit-OTC-008
- outcome_code: Credit-OTC-008
- outcome_intent: assess_credit_document_pack_completeness
- mandatory_capabilities: checklist_evaluation|missing_item_detection|dependency_readiness_evaluation|traceability_generation
- optional_capabilities: none
- enrichment_capabilities: none
- prohibited_shortcuts: no_completeness_without_checklist_and_inventory_basis
- required_data_dependencies: required_document_set|submitted_document_inventory|completed_outcomes
- required_ocr_feature_classes: none
- sufficiency_rule: completeness_requires_document_inventory_and_checklist_traceability

### Credit-OTC-009
- outcome_code: Credit-OTC-009
- outcome_intent: produce_ocr_based_credit_recommendation
- mandatory_capabilities: rule_based_recommendationing|blocker_propagation|uncertainty_handling|traceability_generation
- optional_capabilities: supporting_metric_projection
- enrichment_capabilities: none
- prohibited_shortcuts: no_recommendation_without_upstream_affordability_and_completeness_basis
- required_data_dependencies: affordability_snapshot|document_pack_completeness|recommendation_rules
- required_ocr_feature_classes: none
- sufficiency_rule: recommendation_requires_upstream_governed_basis_and_blocker_traceability

---

## End of Document
