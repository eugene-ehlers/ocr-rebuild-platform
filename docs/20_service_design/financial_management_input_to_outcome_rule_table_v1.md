# Financial Management — Input to Outcome Rule Table v1

## Purpose

Defines how Financial Management service requests are interpreted into required outcome structures.

This table operates strictly at the **decision layer**:

request → outcome_intent → outcome_structure

It does NOT define:
- capabilities
- providers
- execution logic
- OCR behavior

---

## Governance Notes

- All tokens used in this table are **proposed governed vocabulary**
- Tokens must be standardized before production enforcement
- This table defines **WHAT must be produced**, not HOW

### Controlled Vocabulary Rule

Tokens in this table are governed design-time normalized vocabulary for request-to-outcome mapping.

Where a token is not yet persisted in a dedicated registry or approved controlled vocabulary artifact as a literal term:
- it must be treated as proposed controlled vocabulary
- it must be interpreted consistently
- it must not be replaced ad hoc in implementation

### Outcome Sufficiency Interpretation

Required outcome fields in this table are sufficiency-critical for valid fulfillment of the rule.

If mandatory outcome conditions cannot be satisfied, runtime behavior must:
- fail safely
- degrade in a governed way
- or escalate according to decision policy

### Condition Interpretation

- `mandatory_outcome_conditions`
  → must be satisfied or the service must fail, degrade, or escalate

- `optional_outcome_conditions`
  → enrichment only, not required for baseline service delivery

### Degradation Policy

Defines how the system must behave if required outcome conditions cannot be fully met.

Allowed values include:
- no_safe_degradation
- degrade_with_caveat
- degrade_to_summary_only
- escalate_for_missing_dependencies
- internal_review_required

---


## Payload Contract Cross-Reference

Field-level contract authority for the following governed tokens is defined in `docs/20_service_design/financial_management_payloads_v1.md`, Section 9:

- prior_statement_history
- period_groupings
- trend_metrics
- missing_period_flags
- exclusion_flags
- multi_period_requirement_signal

This rule table remains the authority for when those tokens are required and when sufficiency must fail closed.


## Current Operational Exposure Constraint

Current operational exposure for outward Financial Management request selection is controlled as follows:

- request-governed selector field: `analysis_type`
- `analysis_type=explain_document` maps to `outcome_intent: explain_document`
- `analysis_type=cash_flow_multi_period` maps to `outcome_intent: analyse_cash_flow`
- omitted `analysis_type` defaults to the FM-OTC-001 explanation path
- outward runtime selection must remain mutually exclusive
- exactly one outward governed Financial Management outcome may be emitted
- where the selected cash-flow path lacks sufficient multi-period basis, fulfillment must fail closed rather than silently mixing or downgrading outcomes


---

## Rule Table

---

### FM-IOR-001

- service_family: financial_management
- requested_service: statement_explanation
- requested_option_set: simple_summary|per_statement|customer_friendly_explanation
- request_scope: single_document
- audience_mode: customer
- document_type: bank_statement
- expected_document_type: bank_statement
- product_context: null
- complexity_mode: simple
- outcome_intent: explain_document
- degradation_policy: degrade_with_caveat

- required_determinations: none
- required_scores: none
- required_flags: missing_data_flags|document_quality_flags|coverage_flags
- required_metrics: balance_metrics|inflow_outflow_metrics
- required_summaries: statement_summary
- required_recommendations: none
- required_traceability: none
- required_confidence_outputs: overall_confidence
- required_execution_metadata: processing_timestamp|service_status

- mandatory_outcome_conditions: explanation_must_be_plain_language
- optional_outcome_conditions: prior_period_change_if_history_available

- notes: customer-facing low-detail explanation outcome; current default outward path when `analysis_type` is omitted

---

### FM-IOR-002

- service_family: financial_management
- requested_service: statement_explanation
- requested_option_set: detailed_summary|per_statement|internal_detailed_operational_explanation
- request_scope: single_document
- audience_mode: internal
- document_type: bank_statement
- expected_document_type: bank_statement
- product_context: null
- complexity_mode: advisor_internal
- outcome_intent: explain_document
- degradation_policy: internal_review_required

- required_determinations: none
- required_scores: quality_score
- required_flags: missing_data_flags|document_quality_flags|coverage_flags
- required_metrics: balance_metrics|inflow_outflow_metrics
- required_summaries: statement_summary
- required_recommendations: none
- required_traceability: explanation_trace|section_confidence_trace|coverage_notes
- required_confidence_outputs: overall_confidence|section_confidence
- required_execution_metadata: processing_timestamp|service_status|execution_state

- mandatory_outcome_conditions: internal_mode_requires_traceability
- optional_outcome_conditions: prior_period_change_if_history_available

- notes: internal operational interpretation outcome

---

### FM-IOR-003

- service_family: financial_management
- requested_service: cash_flow_analysis
- requested_option_set: rolling_period_view|include_transaction_type_breakdown
- request_scope: multi_period
- audience_mode: customer
- document_type: bank_statement
- expected_document_type: bank_statement
- product_context: null
- complexity_mode: standard
- outcome_intent: analyse_cash_flow
- degradation_policy: degrade_with_caveat

- required_determinations: none
- required_scores: none
- required_flags: missing_period_flags
- required_metrics: inflow_outflow_metrics|trend_metrics
- required_summaries: cash_flow_summary
- required_recommendations: none
- required_traceability: none
- required_confidence_outputs: overall_confidence
- required_execution_metadata: processing_timestamp|service_status

- mandatory_outcome_conditions: multi_period_history_required
- optional_outcome_conditions: chart_rendering_if_frontend_supports

- notes: customer cash-flow trend outcome; current controlled outward FM-OTC-002 path when `analysis_type=cash_flow_multi_period`; fail closed if multi-period history is insufficient

---

### FM-IOR-004

- service_family: financial_management
- requested_service: spending_analysis
- requested_option_set: category_breakdown|compare_prior_period|merchant_breakdown
- request_scope: comparative_period
- audience_mode: internal
- document_type: bank_statement
- expected_document_type: bank_statement
- product_context: null
- complexity_mode: advanced
- outcome_intent: analyse_spending_patterns
- degradation_policy: degrade_with_caveat

- required_determinations: none
- required_scores: none
- required_flags: missing_data_flags|caveat_flags
- required_metrics: category_spend_metrics|trend_metrics
- required_summaries: spending_summary
- required_recommendations: none
- required_traceability: section_confidence_trace
- required_confidence_outputs: category_confidence|merchant_confidence|overall_confidence
- required_execution_metadata: processing_timestamp|service_status|execution_state

- mandatory_outcome_conditions: prior_period_data_required_for_comparison
- optional_outcome_conditions: business_personal_split_if_supported

- notes: internal comparative spending analysis outcome

---

### FM-IOR-005

- service_family: financial_management
- requested_service: indebtedness_obligations
- requested_option_set: affordability_style_summary|debt_committed_expenses
- request_scope: single_period
- audience_mode: customer
- document_type: bank_statement
- expected_document_type: bank_statement
- product_context: loan
- complexity_mode: standard
- outcome_intent: assess_financial_obligation_pressure
- degradation_policy: escalate_for_missing_dependencies

- required_determinations: none
- required_scores: affordability_support_score
- required_flags: overload_flags
- required_metrics: debt_burden_metrics
- required_summaries: debt_summary
- required_recommendations: next_step_guidance
- required_traceability: none
- required_confidence_outputs: overall_confidence
- required_execution_metadata: processing_timestamp|service_status

- mandatory_outcome_conditions: debt_and_commitment_interpretation_required
- optional_outcome_conditions: pressure_periods_if_history_available

- notes: customer debt-pressure interpretation outcome

---

### FM-IOR-006

- service_family: financial_management
- requested_service: pricing_cost_benchmarking
- requested_option_set: compare_peer_averages|compare_selected_spend_types_only
- request_scope: single_period
- audience_mode: customer
- document_type: bank_statement
- expected_document_type: bank_statement
- product_context: transport_cost
- complexity_mode: advanced
- outcome_intent: compare_against_reference
- degradation_policy: no_safe_degradation

- required_determinations: none
- required_scores: benchmark_deviation_score
- required_flags: caveat_flags
- required_metrics: benchmark_comparison_metrics
- required_summaries: benchmark_summary
- required_recommendations: optimisation_recommendations
- required_traceability: none
- required_confidence_outputs: benchmark_applicability_confidence|overall_confidence
- required_execution_metadata: processing_timestamp|service_status

- mandatory_outcome_conditions: benchmark_source_must_exist
- optional_outcome_conditions: external_market_comparison_if_available

- notes: customer benchmark and optimization outcome

---

### FM-IOR-007

- service_family: financial_management
- requested_service: financial_stress_detection
- requested_option_set: full_financial_stress_view|multi_period_trend|debt_weighted
- request_scope: multi_period
- audience_mode: internal
- document_type: bank_statement
- expected_document_type: bank_statement
- product_context: null
- complexity_mode: advisor_internal
- outcome_intent: detect_financial_risk
- degradation_policy: internal_review_required

- required_determinations: none
- required_scores: stress_score
- required_flags: overload_flags|escalation_flags
- required_metrics: trend_metrics|debt_burden_metrics
- required_summaries: health_summary
- required_recommendations: escalation_guidance
- required_traceability: audit_trace|section_confidence_trace
- required_confidence_outputs: overall_confidence|scenario_confidence
- required_execution_metadata: processing_timestamp|service_status|execution_state|finalization_reason

- mandatory_outcome_conditions: multi_period_history_required
- optional_outcome_conditions: trigger_decomposition_if_supported

- notes: internal risk-oriented stress outcome

---

## End of Rule Table v1

## End of Document
