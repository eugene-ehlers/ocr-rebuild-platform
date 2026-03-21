# FICA Compliance — Input to Outcome Rule Table v1

## Purpose

Defines how FICA Compliance service requests are interpreted into required outcome structures.

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

### FICA-IOR-001

- service_family: fica_compliance
- requested_service: document_validation
- requested_option_set: standard_validation
- request_scope: single_document
- audience_mode: internal
- document_type: bank_statement
- expected_document_type: bank_statement
- product_context: null
- complexity_mode: standard
- outcome_intent: validate_document_authenticity
- degradation_policy: no_safe_degradation

- required_determinations: document_validity_status
- required_scores: document_validity_confidence
- required_flags: document_integrity_flags
- required_metrics: none
- required_summaries: validation_summary
- required_recommendations: none
- required_traceability: audit_trace|input_evidence_linkage|decision_trace
- required_confidence_outputs: overall_confidence
- required_execution_metadata: processing_timestamp|service_status|execution_state

- mandatory_outcome_conditions: authenticity_decision_must_be_traceable
- optional_outcome_conditions: none

- notes: internal document authenticity determination outcome

---

### FICA-IOR-002

- service_family: fica_compliance
- requested_service: document_validation
- requested_option_set: customer_status_only
- request_scope: single_document
- audience_mode: customer
- document_type: bank_statement
- expected_document_type: bank_statement
- product_context: null
- complexity_mode: simple
- outcome_intent: validate_document_authenticity
- degradation_policy: no_safe_degradation

- required_determinations: document_validity_status
- required_scores: none
- required_flags: none
- required_metrics: none
- required_summaries: validation_status_summary
- required_recommendations: remediation_request_if_invalid
- required_traceability: none
- required_confidence_outputs: none
- required_execution_metadata: processing_timestamp|service_status

- mandatory_outcome_conditions: customer_status_must_align_to_internal_determination
- optional_outcome_conditions: none

- notes: customer-facing validation status outcome derived from governed internal determination

---

### FICA-IOR-003

- service_family: fica_compliance
- requested_service: identity_verification
- requested_option_set: standard_identity_match
- request_scope: single_document
- audience_mode: internal
- document_type: bank_statement
- expected_document_type: bank_statement
- product_context: null
- complexity_mode: standard
- outcome_intent: verify_identity_and_ownership
- degradation_policy: escalate_for_missing_dependencies

- required_determinations: identity_match_status|manual_review
- required_scores: identity_match_confidence
- required_flags: identity_discrepancy_flags
- required_metrics: none
- required_summaries: identity_verification_summary
- required_recommendations: none
- required_traceability: audit_trace|input_evidence_linkage|decision_trace
- required_confidence_outputs: overall_confidence
- required_execution_metadata: processing_timestamp|service_status|execution_state

- mandatory_outcome_conditions: ownership_verification_must_reference_customer_and_issuer_context
- optional_outcome_conditions: historical_cross_check_if_available

- notes: internal identity and ownership determination outcome

---

### FICA-IOR-004

- service_family: fica_compliance
- requested_service: identity_verification
- requested_option_set: customer_status_only
- request_scope: single_document
- audience_mode: customer
- document_type: bank_statement
- expected_document_type: bank_statement
- product_context: null
- complexity_mode: simple
- outcome_intent: verify_identity_and_ownership
- degradation_policy: escalate_for_missing_dependencies

- required_determinations: identity_match_status|manual_review
- required_scores: none
- required_flags: none
- required_metrics: none
- required_summaries: identity_status_summary
- required_recommendations: remediation_request_if_unverified
- required_traceability: none
- required_confidence_outputs: none
- required_execution_metadata: processing_timestamp|service_status

- mandatory_outcome_conditions: customer_status_must_align_to_internal_identity_determination
- optional_outcome_conditions: none

- notes: customer-facing identity verification status outcome

---

### FICA-IOR-005

- service_family: fica_compliance
- requested_service: transaction_compliance
- requested_option_set: standard_transaction_screening
- request_scope: single_document
- audience_mode: internal
- document_type: bank_statement
- expected_document_type: bank_statement
- product_context: null
- complexity_mode: advanced
- outcome_intent: evaluate_transaction_compliance
- degradation_policy: no_safe_degradation

- required_determinations: transaction_compliance_status|manual_review
- required_scores: transaction_compliance_confidence|compliance_score
- required_flags: transaction_compliance_flags
- required_metrics: transaction_compliance_metrics
- required_summaries: transaction_compliance_summary
- required_recommendations: escalation_guidance
- required_traceability: audit_trace|input_evidence_linkage|decision_trace
- required_confidence_outputs: overall_confidence
- required_execution_metadata: processing_timestamp|service_status|execution_state|finalization_reason

- mandatory_outcome_conditions: compliance_decision_must_reference_detected_issues_and_metrics
- optional_outcome_conditions: historical_pattern_comparison_if_available

- notes: internal transaction compliance determination outcome

---

### FICA-IOR-006

- service_family: fica_compliance
- requested_service: transaction_compliance
- requested_option_set: customer_status_only
- request_scope: single_document
- audience_mode: customer
- document_type: bank_statement
- expected_document_type: bank_statement
- product_context: null
- complexity_mode: simple
- outcome_intent: evaluate_transaction_compliance
- degradation_policy: no_safe_degradation

- required_determinations: transaction_compliance_status|manual_review
- required_scores: none
- required_flags: none
- required_metrics: none
- required_summaries: compliance_status_summary
- required_recommendations: remediation_request_if_non_compliant
- required_traceability: none
- required_confidence_outputs: none
- required_execution_metadata: processing_timestamp|service_status

- mandatory_outcome_conditions: customer_status_must_align_to_internal_compliance_determination
- optional_outcome_conditions: none

- notes: customer-facing transaction compliance status outcome

---

### FICA-IOR-007

- service_family: fica_compliance
- requested_service: compliance_risk_assessment
- requested_option_set: consolidated_internal_review
- request_scope: single_document
- audience_mode: internal
- document_type: bank_statement
- expected_document_type: bank_statement
- product_context: null
- complexity_mode: advisor_internal
- outcome_intent: assess_compliance_risk
- degradation_policy: internal_review_required

- required_determinations: compliance_risk_status|manual_review
- required_scores: fraud_score|compliance_score
- required_flags: document_integrity_flags|identity_discrepancy_flags|transaction_compliance_flags
- required_metrics: transaction_compliance_metrics
- required_summaries: compliance_risk_summary
- required_recommendations: escalation_guidance
- required_traceability: audit_trace|input_evidence_linkage|decision_trace
- required_confidence_outputs: overall_confidence
- required_execution_metadata: processing_timestamp|service_status|execution_state|finalization_reason

- mandatory_outcome_conditions: consolidated_risk_output_must_be_traceable_across_component_checks
- optional_outcome_conditions: affordability_support_if_enabled

- notes: consolidated internal compliance risk outcome

---

## End of Document
