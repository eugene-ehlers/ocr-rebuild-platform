# Credit / Trade Credit Decision — Outcome to Capability Rule Table v1

## Purpose

Defines how Credit / Trade Credit Decision outcome intents and required outcome structures map to capability requirements.

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

### CREDIT-OTC-001

- service_family: credit_decision
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

- mandatory_capabilities: document_validation|transaction_parsing|fraud_detection|reporting_explanation
- optional_capabilities: historical_document_comparison
- enrichment_capabilities: anomaly_detection|visual_tamper_enrichment

- prohibited_shortcuts: fraud_score_without_supporting_findings|integrity_status_without_validation_basis

- required_data_dependencies: document_validation_findings|parsed_transactions|fraud_findings
- required_ocr_feature_classes: text|tables|layout|metadata|logos
- required_internal_data_dependencies: none|historical_document_data
- required_external_data_dependencies: none

- confidence_requirement: overall_confidence_required
- sufficiency_rule: integrity_determination_requires_validation_or_fraud_basis_and_traceability
- cost_sensitivity: medium

- notes: internal integrity and fraud assessment outcome

---

### CREDIT-OTC-002

- service_family: credit_decision
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

- mandatory_capabilities: transaction_parsing|category_classification|cash_flow_classification|debt_detection|affordability_classification|reporting_explanation
- optional_capabilities: income_stability_assessment|trend_analysis
- enrichment_capabilities: benchmarking|behavioural_analysis

- prohibited_shortcuts: affordability_score_without_income_and_obligation_basis|affordability_status_without_supporting_metrics

- required_data_dependencies: parsed_transactions|classified_transactions|cash_flow_summary|debt_positions|affordability_inputs
- required_ocr_feature_classes: text|tables|layout|metadata
- required_internal_data_dependencies: none|historical_period_data|account_context
- required_external_data_dependencies: none

- confidence_requirement: overall_confidence_required
- sufficiency_rule: affordability_determination_requires_score_metrics_and_supporting_basis
- cost_sensitivity: medium

- notes: affordability and repayment-capacity outcome

---

### CREDIT-OTC-003

- service_family: credit_decision
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

- mandatory_capabilities: transaction_parsing|category_classification|cash_flow_classification|debt_detection|risk_scoring|reporting_explanation
- optional_capabilities: income_stability_assessment|trend_analysis
- enrichment_capabilities: behavioural_analysis|counterparty_exposure_analysis|seasonality_analysis

- prohibited_shortcuts: credit_risk_score_without_supporting_signals|credit_risk_status_without_traceability

- required_data_dependencies: parsed_transactions|classified_transactions|cash_flow_summary|debt_positions|risk_score_components
- required_ocr_feature_classes: text|tables|layout|metadata
- required_internal_data_dependencies: none|historical_period_data|account_context
- required_external_data_dependencies: none

- confidence_requirement: overall_confidence_required
- sufficiency_rule: credit_risk_output_requires_scores_supporting_metrics_and_traceability
- cost_sensitivity: high

- notes: internal credit-risk assessment outcome

---

### CREDIT-OTC-004

- service_family: credit_decision
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

- mandatory_capabilities: transaction_parsing|cash_flow_classification|collections_timing_optimization|trend_analysis|reporting_explanation
- optional_capabilities: debt_detection
- enrichment_capabilities: seasonality_analysis|behavioural_analysis

- prohibited_shortcuts: timing_recommendation_without_cash_timing_basis|collections_score_without_supporting_metrics

- required_data_dependencies: parsed_transactions|cash_flow_summary|timing_features|historical_period_data
- required_ocr_feature_classes: text|tables|layout
- required_internal_data_dependencies: historical_period_data
- required_external_data_dependencies: none

- confidence_requirement: overall_confidence_required
- sufficiency_rule: timing_guidance_requires_score_metrics_and_recommendation_basis
- cost_sensitivity: medium

- notes: internal collections timing optimization outcome

---

### CREDIT-OTC-005

- service_family: credit_decision
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

- mandatory_capabilities: reporting_explanation|decision_status_projection
- optional_capabilities: repayment_schedule_generation
- enrichment_capabilities: none

- prohibited_shortcuts: customer_status_without_internal_decision_basis|customer_summary_without_status_alignment

- required_data_dependencies: internal_credit_decision|decision_summary_basis
- required_ocr_feature_classes: none
- required_internal_data_dependencies: internal_decision_record
- required_external_data_dependencies: none

- confidence_requirement: internal_alignment_required
- sufficiency_rule: customer_status_requires_governed_alignment_to_internal_decision
- cost_sensitivity: low

- notes: customer-facing status communication outcome

---

### CREDIT-OTC-006

- service_family: credit_decision
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

- mandatory_capabilities: repayment_schedule_generation|reporting_explanation
- optional_capabilities: affordability_classification
- enrichment_capabilities: timing_optimization_projection

- prohibited_shortcuts: repayment_summary_without_schedule_basis|repayment_recommendations_without_schedule_alignment

- required_data_dependencies: repayment_schedule_basis|payment_expectation_inputs
- required_ocr_feature_classes: none
- required_internal_data_dependencies: internal_schedule_basis
- required_external_data_dependencies: none

- confidence_requirement: internal_alignment_required
- sufficiency_rule: repayment_summary_requires_schedule_basis_and_customer-safe_projection
- cost_sensitivity: low

- notes: customer-facing repayment expectation outcome

---

### CREDIT-OTC-007

- service_family: credit_decision
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

- mandatory_capabilities: document_validation|transaction_parsing|category_classification|cash_flow_classification|debt_detection|fraud_detection|affordability_classification|risk_scoring|reporting_explanation
- optional_capabilities: collections_timing_optimization|trend_analysis
- enrichment_capabilities: behavioural_analysis|seasonality_analysis|counterparty_exposure_analysis

- prohibited_shortcuts: consolidated_review_without_component_assessments|credit_decision_without_traceable_score_basis

- required_data_dependencies: document_validation_findings|parsed_transactions|classified_transactions|cash_flow_summary|debt_positions|risk_score_components|affordability_inputs
- required_ocr_feature_classes: text|tables|layout|metadata|logos
- required_internal_data_dependencies: historical_period_data|account_context|internal_decision_policy_context
- required_external_data_dependencies: none

- confidence_requirement: overall_confidence_required
- sufficiency_rule: consolidated_credit_review_requires_component_scores_flags_metrics_and_traceability
- cost_sensitivity: high

- notes: internal consolidated credit decision-support outcome

---

## End of Document
