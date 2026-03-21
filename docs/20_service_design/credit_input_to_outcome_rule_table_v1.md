# Credit / Trade Credit Decision — Input to Outcome Rule Table v1

## Purpose

Defines how Credit / Trade Credit Decision service requests are interpreted into required outcome structures.

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

## Rule Table

---

### CREDIT-IOR-001

- service_family: credit_decision
- requested_service: document_verification_fraud_check
- requested_option_set: standard_internal_review
- request_scope: single_document
- audience_mode: internal
- document_type: bank_statement
- expected_document_type: bank_statement
- product_context: null
- complexity_mode: advanced
- outcome_intent: assess_document_and_transaction_integrity
- degradation_policy: internal_review_required

- required_determinations: integrity_status|manual_review
- required_scores: fraud_score
- required_flags: fraud_integrity_flags
- required_metrics: none
- required_summaries: integrity_assessment_summary
- required_recommendations: escalation_guidance
- required_traceability: audit_trace|input_evidence_linkage|decision_trace
- required_confidence_outputs: overall_confidence
- required_execution_metadata: processing_timestamp|service_status|execution_state|finalization_reason

- mandatory_outcome_conditions: integrity_assessment_must_reference_detected_anomalies_or_validation_findings
- optional_outcome_conditions: document_history_comparison_if_available

- notes: internal fraud and integrity assessment outcome

---

### CREDIT-IOR-002

- service_family: credit_decision
- requested_service: affordability_assessment
- requested_option_set: standard_affordability
- request_scope: single_document
- audience_mode: internal
- document_type: bank_statement
- expected_document_type: bank_statement
- product_context: loan
- complexity_mode: advanced
- outcome_intent: assess_affordability_and_repayment_capacity
- degradation_policy: escalate_for_missing_dependencies

- required_determinations: affordability_status|manual_review
- required_scores: affordability_score
- required_flags: affordability_risk_flags
- required_metrics: affordability_metrics
- required_summaries: affordability_summary
- required_recommendations: next_step_guidance
- required_traceability: audit_trace|input_evidence_linkage|decision_trace
- required_confidence_outputs: overall_confidence
- required_execution_metadata: processing_timestamp|service_status|execution_state|finalization_reason

- mandatory_outcome_conditions: affordability_output_must_reference_income_obligation_and_cash_flow_basis
- optional_outcome_conditions: historical_income_stability_if_available

- notes: internal affordability and repayment-capacity assessment outcome

---

### CREDIT-IOR-003

- service_family: credit_decision
- requested_service: credit_risk_scoring
- requested_option_set: standard_risk_assessment
- request_scope: single_document
- audience_mode: internal
- document_type: bank_statement
- expected_document_type: bank_statement
- product_context: loan
- complexity_mode: advisor_internal
- outcome_intent: assess_credit_risk
- degradation_policy: internal_review_required

- required_determinations: credit_risk_status|manual_review
- required_scores: payment_probability|credit_risk_score
- required_flags: credit_risk_flags
- required_metrics: risk_support_metrics
- required_summaries: credit_risk_summary
- required_recommendations: escalation_guidance
- required_traceability: audit_trace|input_evidence_linkage|decision_trace
- required_confidence_outputs: overall_confidence
- required_execution_metadata: processing_timestamp|service_status|execution_state|finalization_reason

- mandatory_outcome_conditions: risk_output_must_reference_score_basis_and_supporting_signals
- optional_outcome_conditions: historical_payment_pattern_if_available

- notes: internal credit-risk assessment outcome

---

### CREDIT-IOR-004

- service_family: credit_decision
- requested_service: collections_timing_optimisation
- requested_option_set: standard_collections_guidance
- request_scope: multi_period
- audience_mode: internal
- document_type: bank_statement
- expected_document_type: bank_statement
- product_context: collections
- complexity_mode: advisor_internal
- outcome_intent: optimize_collections_timing
- degradation_policy: degrade_with_caveat

- required_determinations: none
- required_scores: collections_timing_score
- required_flags: collections_risk_flags
- required_metrics: timing_optimization_metrics
- required_summaries: collections_timing_summary
- required_recommendations: timing_recommendations
- required_traceability: audit_trace|decision_trace
- required_confidence_outputs: overall_confidence
- required_execution_metadata: processing_timestamp|service_status|execution_state

- mandatory_outcome_conditions: timing_output_must_reference_cash_timing_or_recovery_basis
- optional_outcome_conditions: historical_repayment_patterns_if_available

- notes: internal collections timing guidance outcome

---

### CREDIT-IOR-005

- service_family: credit_decision
- requested_service: customer_credit_decision_status
- requested_option_set: customer_status_only
- request_scope: single_document
- audience_mode: customer
- document_type: bank_statement
- expected_document_type: bank_statement
- product_context: loan
- complexity_mode: simple
- outcome_intent: communicate_credit_decision_status
- degradation_policy: no_safe_degradation

- required_determinations: credit_decision_status|manual_review
- required_scores: none
- required_flags: none
- required_metrics: none
- required_summaries: credit_decision_status_summary
- required_recommendations: repayment_recommendations
- required_traceability: none
- required_confidence_outputs: none
- required_execution_metadata: processing_timestamp|service_status

- mandatory_outcome_conditions: customer_status_must_align_to_internal_credit_determination
- optional_outcome_conditions: payment_schedule_summary_if_available

- notes: customer-facing credit decision communication outcome

---

### CREDIT-IOR-006

- service_family: credit_decision
- requested_service: repayment_schedule_summary
- requested_option_set: customer_schedule_view
- request_scope: single_period
- audience_mode: customer
- document_type: bank_statement
- expected_document_type: bank_statement
- product_context: loan
- complexity_mode: standard
- outcome_intent: summarize_repayment_expectations
- degradation_policy: degrade_to_summary_only

- required_determinations: none
- required_scores: none
- required_flags: payment_risk_flags
- required_metrics: repayment_schedule_metrics
- required_summaries: repayment_schedule_summary
- required_recommendations: repayment_recommendations
- required_traceability: none
- required_confidence_outputs: none
- required_execution_metadata: processing_timestamp|service_status

- mandatory_outcome_conditions: repayment_summary_must_align_to_internal_schedule_basis
- optional_outcome_conditions: affordability_context_if_available

- notes: customer-facing repayment expectation outcome

---

### CREDIT-IOR-007

- service_family: credit_decision
- requested_service: consolidated_internal_credit_review
- requested_option_set: full_internal_review
- request_scope: multi_period
- audience_mode: internal
- document_type: bank_statement
- expected_document_type: bank_statement
- product_context: loan
- complexity_mode: advisor_internal
- outcome_intent: support_credit_decision_review
- degradation_policy: internal_review_required

- required_determinations: credit_decision_status|manual_review
- required_scores: fraud_score|affordability_score|payment_probability|credit_risk_score
- required_flags: fraud_integrity_flags|affordability_risk_flags|credit_risk_flags
- required_metrics: affordability_metrics|risk_support_metrics
- required_summaries: consolidated_credit_review_summary
- required_recommendations: escalation_guidance|next_step_guidance
- required_traceability: audit_trace|input_evidence_linkage|decision_trace
- required_confidence_outputs: overall_confidence
- required_execution_metadata: processing_timestamp|service_status|execution_state|finalization_reason

- mandatory_outcome_conditions: consolidated_credit_review_must_be_traceable_across_component_assessments
- optional_outcome_conditions: collections_timing_guidance_if_enabled

- notes: internal consolidated credit-review decision-support outcome

---

## End of Document
