# Frontend Service Input Matrix Working v1

## Purpose
Working document to complete Section 11 of the governed page-by-page journey design.

## Rule
No coding. Complete this matrix first.

## Services to complete first
- ocr
- financial_management
- fica
- credit_decision

---


# Source: frontend service selection baseline
## OCR-OTC-001
- outcome_intent: extract_text
- required_inputs: payload.request.outcome_code|payload.document.document_type|payload.document.file_bytes_b64_or_s3_uri
- user_supplied_inputs: none
- document_supplied_inputs: uploaded document file
- system_or_config_inputs: request outcome code
- required_document_types: generic_document
- optional_document_types: none
- repeatable_document_groups: no
- subject_context_required: no
- business_context_required: no
- multi_period_supported: no
- mixed_format_supported: yes


# Source: docs/20_service_design/fica_input_to_outcome_rule_table_v1.md
## FICA-OTC-001
- outcome_intent: extract_identity_document_fields
- required_inputs: payload.request.outcome_code|payload.document.document_type|payload.document.file_bytes_b64_or_s3_uri
- user_supplied_inputs: none
- document_supplied_inputs: identity document
- system_or_config_inputs: request outcome code
- required_document_types: identity_document
- optional_document_types: none
- repeatable_document_groups: no
- subject_context_required: no
- business_context_required: no
- multi_period_supported: no
- mixed_format_supported: yes

## FICA-OTC-002
- outcome_intent: assess_identity_field_consistency
- required_inputs: payload.substrates.ocr.structured_fields.identity|payload.subject.first_name|payload.subject.last_name|payload.subject.id_number
- user_supplied_inputs: subject first name, subject last name, subject ID number
- document_supplied_inputs: extracted identity fields from identity document
- system_or_config_inputs: none
- required_document_types: identity_document
- optional_document_types: none
- repeatable_document_groups: no
- subject_context_required: yes
- business_context_required: no
- multi_period_supported: no
- mixed_format_supported: yes

## FICA-OTC-003
- outcome_intent: extract_proof_of_address_fields
- required_inputs: payload.request.outcome_code|payload.document.document_type|payload.document.file_bytes_b64_or_s3_uri
- user_supplied_inputs: none
- document_supplied_inputs: proof of address document
- system_or_config_inputs: request outcome code
- required_document_types: proof_of_address
- optional_document_types: none
- repeatable_document_groups: no
- subject_context_required: no
- business_context_required: no
- multi_period_supported: no
- mixed_format_supported: yes

## FICA-OTC-004
- outcome_intent: assess_proof_of_address_validity_and_recency
- required_inputs: payload.substrates.ocr.structured_fields.proof_of_address|payload.rules.proof_of_address.max_age_days
- user_supplied_inputs: none
- document_supplied_inputs: extracted proof of address fields from proof_of_address
- system_or_config_inputs: proof of address max age days rule
- required_document_types: proof_of_address
- optional_document_types: none
- repeatable_document_groups: no
- subject_context_required: no
- business_context_required: no
- multi_period_supported: no
- mixed_format_supported: yes

## FICA-OTC-005
- outcome_intent: extract_business_registration_fields
- required_inputs: payload.request.outcome_code|payload.document.document_type|payload.document.file_bytes_b64_or_s3_uri
- user_supplied_inputs: none
- document_supplied_inputs: business registration document
- system_or_config_inputs: request outcome code
- required_document_types: business_registration
- optional_document_types: none
- repeatable_document_groups: no
- subject_context_required: no
- business_context_required: yes
- multi_period_supported: no
- mixed_format_supported: yes

## FICA-OTC-006
- outcome_intent: assess_business_ownership_or_authority_consistency
- required_inputs: payload.substrates.ocr.structured_fields.business_registration|payload.subject.company_name|payload.subject.registration_number
- user_supplied_inputs: subject company name, subject registration number
- document_supplied_inputs: extracted business registration fields
- system_or_config_inputs: none
- required_document_types: business_registration
- optional_document_types: none
- repeatable_document_groups: no
- subject_context_required: no
- business_context_required: yes
- multi_period_supported: no
- mixed_format_supported: yes

# Source: docs/20_service_design/credit_input_to_outcome_rule_table_v1.md
## Credit-OTC-001
- outcome_intent: extract_payslip_fields
- required_inputs: payload.request.outcome_code|payload.document.document_type|payload.document.file_bytes_b64_or_s3_uri
- user_supplied_inputs: none
- document_supplied_inputs: payslip document
- system_or_config_inputs: request outcome code
- required_document_types: payslip
- optional_document_types: none
- repeatable_document_groups: yes (multiple payslips supported)
- subject_context_required: yes
- business_context_required: no
- multi_period_supported: yes
- mixed_format_supported: yes

## Credit-OTC-002
- outcome_intent: assess_payslip_income_validity
- required_inputs: payload.substrates.ocr.structured_fields.payslip|payload.rules.credit.payslip_rules
- user_supplied_inputs: none
- document_supplied_inputs: extracted payslip fields
- system_or_config_inputs: payslip validation rules
- required_document_types: payslip
- optional_document_types: none
- repeatable_document_groups: yes
- subject_context_required: yes
- business_context_required: no
- multi_period_supported: yes
- mixed_format_supported: yes

## Credit-OTC-003
- outcome_intent: extract_bank_statement_fields
- required_inputs: payload.request.outcome_code|payload.document.document_type|payload.document.file_bytes_b64_or_s3_uri
- user_supplied_inputs: none
- document_supplied_inputs: bank statement document
- system_or_config_inputs: request outcome code
- required_document_types: bank_statement
- optional_document_types: none
- repeatable_document_groups: yes (multiple statements supported)
- subject_context_required: yes
- business_context_required: no
- multi_period_supported: yes
- mixed_format_supported: yes

## Credit-OTC-004
- outcome_intent: assess_bank_statement_income_signal
- required_inputs: payload.substrates.ocr.structured_fields.bank_statement|payload.rules.credit.bank_income_rules
- user_supplied_inputs: none
- document_supplied_inputs: extracted bank statement fields
- system_or_config_inputs: bank income rules
- required_document_types: bank_statement
- optional_document_types: none
- repeatable_document_groups: yes
- subject_context_required: yes
- business_context_required: no
- multi_period_supported: yes
- mixed_format_supported: yes

## Credit-OTC-005
- outcome_intent: assess_bank_statement_expense_signal
- required_inputs: payload.substrates.ocr.structured_fields.bank_statement|payload.rules.credit.bank_expense_rules
- user_supplied_inputs: none
- document_supplied_inputs: extracted bank statement fields
- system_or_config_inputs: bank expense rules
- required_document_types: bank_statement
- optional_document_types: none
- repeatable_document_groups: yes
- subject_context_required: yes
- business_context_required: no
- multi_period_supported: yes
- mixed_format_supported: yes

## Credit-OTC-006
- outcome_intent: assess_payslip_to_bank_income_consistency
- required_inputs: payload.substrates.ocr.structured_fields.payslip|payload.substrates.ocr.structured_fields.bank_statement|payload.rules.credit.income_consistency_rules
- user_supplied_inputs: none
- document_supplied_inputs: payslip + bank statement extracted fields
- system_or_config_inputs: income consistency rules
- required_document_types: payslip, bank_statement
- optional_document_types: none
- repeatable_document_groups: yes
- subject_context_required: yes
- business_context_required: no
- multi_period_supported: yes
- mixed_format_supported: yes

## Credit-OTC-007
- outcome_intent: produce_ocr_based_affordability_snapshot
- required_inputs: payload.substrates.analytics.bank_income_signal|payload.substrates.analytics.bank_expense_signal|payload.rules.credit.affordability_rules
- user_supplied_inputs: none
- document_supplied_inputs: derived from bank statements
- system_or_config_inputs: affordability rules
- required_document_types: bank_statement
- optional_document_types: payslip
- repeatable_document_groups: yes
- subject_context_required: yes
- business_context_required: no
- multi_period_supported: yes
- mixed_format_supported: yes

## Credit-OTC-008
- outcome_intent: assess_credit_document_pack_completeness
- required_inputs: payload.rules.credit.required_document_set|payload.documents_submitted|payload.substrates.completed_outcomes
- user_supplied_inputs: none
- document_supplied_inputs: submitted document set
- system_or_config_inputs: required document set rules
- required_document_types: bank_statement, payslip
- optional_document_types: none
- repeatable_document_groups: yes
- subject_context_required: yes
- business_context_required: no
- multi_period_supported: yes
- mixed_format_supported: yes

## Credit-OTC-009
- outcome_intent: produce_ocr_based_credit_recommendation
- required_inputs: payload.substrates.analytics.affordability_snapshot|payload.substrates.analytics.document_pack_completeness|payload.rules.credit.recommendation_rules
- user_supplied_inputs: none
- document_supplied_inputs: derived analytics from documents
- system_or_config_inputs: recommendation rules
- required_document_types: bank_statement, payslip
- optional_document_types: none
- repeatable_document_groups: yes
- subject_context_required: yes
- business_context_required: no
- multi_period_supported: yes
- mixed_format_supported: yes

# Source: docs/20_service_design/financial_management_input_to_outcome_rule_table_v1.md
## FM-IOR-001
- outcome_intent: explain_document
- required_inputs: document
- user_supplied_inputs: none
- document_supplied_inputs: uploaded document
- system_or_config_inputs: none
- required_document_types: generic_document
- optional_document_types: none
- repeatable_document_groups: yes
- subject_context_required: no
- business_context_required: no
- multi_period_supported: no
- mixed_format_supported: yes

## FM-IOR-002
- outcome_intent: explain_document
- required_inputs: document
- user_supplied_inputs: none
- document_supplied_inputs: uploaded document
- system_or_config_inputs: none
- required_document_types: generic_document
- optional_document_types: none
- repeatable_document_groups: yes
- subject_context_required: no
- business_context_required: no
- multi_period_supported: no
- mixed_format_supported: yes

## FM-IOR-003
- outcome_intent: analyse_cash_flow
- required_inputs: bank statements
- user_supplied_inputs: none
- document_supplied_inputs: bank statements
- system_or_config_inputs: cash flow analysis rules
- required_document_types: bank_statement
- optional_document_types: none
- repeatable_document_groups: yes
- subject_context_required: yes
- business_context_required: no
- multi_period_supported: yes
- mixed_format_supported: yes

## FM-IOR-004
- outcome_intent: analyse_spending_patterns
- required_inputs: bank statements
- user_supplied_inputs: none
- document_supplied_inputs: bank statements
- system_or_config_inputs: spending pattern rules
- required_document_types: bank_statement
- optional_document_types: none
- repeatable_document_groups: yes
- subject_context_required: yes
- business_context_required: no
- multi_period_supported: yes
- mixed_format_supported: yes

## FM-IOR-005
- outcome_intent: assess_financial_obligation_pressure
- required_inputs: bank statements
- user_supplied_inputs: none
- document_supplied_inputs: bank statements
- system_or_config_inputs: obligation rules
- required_document_types: bank_statement
- optional_document_types: none
- repeatable_document_groups: yes
- subject_context_required: yes
- business_context_required: no
- multi_period_supported: yes
- mixed_format_supported: yes

## FM-IOR-006
- outcome_intent: compare_against_reference
- required_inputs: document + reference
- user_supplied_inputs: reference selection
- document_supplied_inputs: uploaded document
- system_or_config_inputs: reference dataset
- required_document_types: generic_document
- optional_document_types: none
- repeatable_document_groups: yes
- subject_context_required: no
- business_context_required: no
- multi_period_supported: no
- mixed_format_supported: yes

## FM-IOR-007
- outcome_intent: detect_financial_risk
- required_inputs: bank statements
- user_supplied_inputs: none
- document_supplied_inputs: bank statements
- system_or_config_inputs: risk detection rules
- required_document_types: bank_statement
- optional_document_types: none
- repeatable_document_groups: yes
- subject_context_required: yes
- business_context_required: no
- multi_period_supported: yes
- mixed_format_supported: yes

## 1. Completion Order (MANDATORY)

Complete in this order:
1. OCR
2. FICA
3. Credit Decision
4. Financial Management

## 2. Completion Rule

For each selectable service / outcome-intent, fill all of:
- user_supplied_inputs
- document_supplied_inputs
- system_or_config_inputs
- required_document_types
- optional_document_types
- repeatable_document_groups
- subject_context_required
- business_context_required
- multi_period_supported
- mixed_format_supported

No TODO values may remain for approved selectable services.

## 3. Derivation Rule

After the matrix is complete, derive:
- Context Setup rules
- Document Selection rules
- Upload model rules
- Validation / Recovery rules

No further coding before that derivation is documented.

## 4. Sign-off Rule

Design is only 100% when:
- matrix is complete
- derived page behavior is complete
- trust layer is complete
- navigation / resume model is complete
- continue conditions are complete
