# FICA Compliance — Outcome to Capability Rule Table v1

## Purpose

Defines how FICA Compliance outcome intents and required outcome structures map to capability requirements.

This table operates strictly at the **decision and design layer**:

outcome_intent + outcome_structure → capability requirements

It does NOT define:
- provider selection
- model selection
- worker invocation order
- runtime execution-plan state

---

## Governance Notes

- All tokens used in this table are **proposed governed vocabulary**
- Tokens must be standardized before production enforcement
- This table defines **WHAT capabilities are required**, not which provider or worker must be used

### Controlled Vocabulary Rule

Capability tokens in this table are governed design-time normalized vocabulary for outcome-to-capability mapping.

Where a token is not yet persisted in a dedicated capability registry as a literal approved term:
- it must be treated as proposed controlled vocabulary
- it must be interpreted consistently
- it must not be replaced ad hoc in implementation

### Mandatory Capability Interpretation

`mandatory_capabilities` are **sufficiency-critical**.

If one or more mandatory capabilities are:
- absent
- invalid
- unsupported

then the outcome must NOT be treated as validly fulfilled.

Runtime behavior must:
- fail safely
- degrade in a governed way
- or escalate according to decision policy

### Capability Interpretation

- `mandatory_capabilities`
  → required for valid baseline fulfillment

- `optional_capabilities`
  → improve delivery but not baseline-critical

- `enrichment_capabilities`
  → differentiation only, not required for validity

### Degradation Policy

Defines how the system must behave if mandatory capability conditions cannot be fully met.

Allowed values include:
- no_safe_degradation
- degrade_with_caveat
- degrade_to_summary_only
- escalate_for_missing_dependencies
- internal_review_required

---

## Rule Table

---

### FICA-OTC-001

- service_family: fica_compliance
- outcome_intent: validate_document_authenticity
- degradation_policy: no_safe_degradation

- required_determinations: document_validity_status
- required_scores: document_validity_confidence
- required_flags: document_integrity_flags
- required_metrics: none
- required_summaries: validation_summary|validation_status_summary
- required_recommendations: remediation_request_if_invalid
- required_traceability: audit_trace|input_evidence_linkage|decision_trace
- conditional_required_traceability: customer_mode=>none
- required_confidence_outputs: overall_confidence
- conditional_required_confidence_outputs: customer_mode=>none

- mandatory_capabilities: document_validation|metadata_verification
- optional_capabilities: document_type_classification
- enrichment_capabilities: visual_anomaly_detection|template_matching

- prohibited_shortcuts: validity_status_without_integrity_checks|customer_status_without_internal_determination

- required_data_dependencies: document_page_data|document_metadata|integrity_findings
- required_ocr_feature_classes: text|layout|metadata|logos
- required_internal_data_dependencies: none
- required_external_data_dependencies: none

- confidence_requirement: internal_mode_requires_overall_confidence
- sufficiency_rule: authenticity_determination_required;internal_mode_requires_traceability
- cost_sensitivity: medium

- notes: determination-first compliance outcome for document authenticity

---

### FICA-OTC-002

- service_family: fica_compliance
- outcome_intent: verify_identity_and_ownership
- degradation_policy: escalate_for_missing_dependencies

- required_determinations: identity_match_status|manual_review
- required_scores: identity_match_confidence
- required_flags: identity_discrepancy_flags
- required_metrics: none
- required_summaries: identity_verification_summary|identity_status_summary
- required_recommendations: remediation_request_if_unverified
- required_traceability: audit_trace|input_evidence_linkage|decision_trace
- conditional_required_traceability: customer_mode=>none
- required_confidence_outputs: overall_confidence
- conditional_required_confidence_outputs: customer_mode=>none

- mandatory_capabilities: identity_owner_verification|issuer_reference_validation
- optional_capabilities: historical_document_cross_check
- enrichment_capabilities: external_identity_reference_check

- prohibited_shortcuts: identity_status_without_customer_context_match|manual_review_without_supporting_discrepancy_basis

- required_data_dependencies: extracted_identity_fields|issuer_fields|verification_findings
- required_ocr_feature_classes: text|metadata
- required_internal_data_dependencies: customer_metadata
- required_external_data_dependencies: none
- conditional_required_external_data_dependencies: issuer_validation_enabled=>issuer_reference_source

- confidence_requirement: internal_mode_requires_overall_confidence
- sufficiency_rule: ownership_determination_required;missing_customer_or_issuer_context_requires_escalation
- cost_sensitivity: medium

- notes: ownership verification outcome with explicit manual-review path

---

### FICA-OTC-003

- service_family: fica_compliance
- outcome_intent: evaluate_transaction_compliance
- degradation_policy: no_safe_degradation

- required_determinations: transaction_compliance_status|manual_review
- required_scores: transaction_compliance_confidence|compliance_score
- required_flags: transaction_compliance_flags
- required_metrics: transaction_compliance_metrics
- required_summaries: transaction_compliance_summary|compliance_status_summary
- required_recommendations: escalation_guidance|remediation_request_if_non_compliant
- required_traceability: audit_trace|input_evidence_linkage|decision_trace
- conditional_required_traceability: customer_mode=>none
- required_confidence_outputs: overall_confidence
- conditional_required_confidence_outputs: customer_mode=>none

- mandatory_capabilities: transaction_parsing|category_classification|cash_flow_classification|transaction_compliance_evaluation
- optional_capabilities: historical_pattern_comparison
- enrichment_capabilities: anomaly_detection|risk_pattern_enrichment

- prohibited_shortcuts: compliance_status_without_transaction_screening|compliance_score_without_issue_basis|customer_status_without_internal_determination

- required_data_dependencies: parsed_transactions|classified_transactions|cash_flow_summary|transaction_compliance_findings
- required_ocr_feature_classes: text|tables|layout|metadata
- required_internal_data_dependencies: none
- conditional_required_internal_data_dependencies: risk_profile_or_history_available=>customer_risk_profile|historical_transaction_data
- required_external_data_dependencies: none

- confidence_requirement: internal_mode_requires_overall_confidence
- sufficiency_rule: compliance_determination_and_issue_basis_required;manual_review_required_for_unresolved_high_risk_cases
- cost_sensitivity: medium

- notes: transaction-level regulatory compliance outcome

---

### FICA-OTC-004

- service_family: fica_compliance
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

- mandatory_capabilities: document_validation|identity_owner_verification|transaction_compliance_evaluation|compliance_risk_scoring|reporting_explanation
- optional_capabilities: historical_document_cross_check
- enrichment_capabilities: affordability_support_scoring|advanced_fraud_pattern_enrichment

- prohibited_shortcuts: consolidated_risk_status_without_component_checks|risk_summary_without_traceability|escalation_guidance_without_supporting_flags

- required_data_dependencies: document_validation_findings|identity_verification_findings|transaction_compliance_findings|risk_score_components
- required_ocr_feature_classes: text|tables|layout|metadata|logos
- required_internal_data_dependencies: customer_metadata|customer_risk_profile
- required_external_data_dependencies: none
- conditional_required_external_data_dependencies: issuer_validation_enabled=>issuer_reference_source

- confidence_requirement: overall_and_component_confidence_required
- sufficiency_rule: consolidated_risk_output_requires_component_findings_traceability_and_scores
- cost_sensitivity: high

- notes: consolidated compliance-risk outcome for internal review and decision support

---

## End of Document
