# Financial Management — Outcome to Capability Rule Table v1

## Purpose

Defines how Financial Management outcome intents and required outcome structures map to capability requirements.

This table operates strictly at the **decision and design layer**:

outcome_intent + outcome_structure → capability requirements

It does NOT define:
- provider selection
- model selection
- worker invocation order
- runtime execution-plan state

---

## Governance Notes

- This table defines **WHAT capabilities are required**, not which provider or worker must be used
- Governed required fields must never mix `none` with populated values
- Conditional requirements must be expressed explicitly, not buried inside freeform tokens

### Outcome Family Rule

- `outcome_family: analytical`
  → analytical interpretation outcome

- `outcome_family: proof_verification`
  → provenance / proof / verification outcome

### Controlled Vocabulary Rule

Capability tokens in this table are normalized design-time vocabulary for outcome-to-capability mapping.

Where a token is not yet supported strongly enough to be treated as governed-required vocabulary:
- it must be placed in a `proposed_*` field
- it must be interpreted consistently
- it must not be promoted silently in implementation

---

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

---

### Capability Interpretation

- `mandatory_capabilities`
  → required for valid baseline fulfillment

- `optional_capabilities`
  → governed optional capability, not baseline-critical

- `enrichment_capabilities`
  → governed enrichment capability, not required for validity

- `proposed_optional_capabilities`
  → controlled vocabulary only, not yet governable as required design truth

- `proposed_enrichment_capabilities`
  → controlled vocabulary only, not yet governable as required design truth

---

### Conditional Requirement Interpretation

- `conditional_required_scores`
- `conditional_required_traceability`
- `conditional_required_internal_data_dependencies`
- `conditional_required_external_data_dependencies`
- `conditional_confidence_requirement`
- `conditional_sufficiency_rule`

must use explicit `condition=>requirement` form.

These fields define governed conditionality only.
They do not define runtime routing, provider choice, or worker behavior.

---

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

### FM-OTC-001

- service_family: financial_management
- outcome_family: analytical
- outcome_intent: explain_document
- degradation_policy: degrade_with_caveat

- required_determinations: none
- required_scores: none
- conditional_required_scores: internal_mode=>quality_score
- required_flags: missing_data_flags|document_quality_flags|coverage_flags
- required_metrics: balance_metrics|inflow_outflow_metrics
- required_summaries: statement_summary
- required_recommendations: none
- required_traceability: none
- conditional_required_traceability: internal_mode=>explanation_trace|section_confidence_trace|coverage_notes
- required_confidence_outputs: overall_confidence|section_confidence

- mandatory_capabilities: transaction_parsing|category_classification|cash_flow_classification|reporting_explanation
- optional_capabilities: debt_detection|translation
- enrichment_capabilities: benchmarking|behavioural_analysis

- prohibited_shortcuts: raw_ocr_only_without_transaction_parsing|summary_without_confidence_propagation

- required_data_dependencies: parsed_transactions|classified_transactions|cash_flow_summary|document_metadata
- required_ocr_feature_classes: text|tables|layout|metadata
- required_internal_data_dependencies: none
- conditional_required_internal_data_dependencies: multi_period_scope=>prior_statement_history
- required_external_data_dependencies: none

- confidence_requirement: baseline_overall_confidence_required
- conditional_confidence_requirement: internal_mode=>section_confidence_required
- sufficiency_rule: summary_plus_metrics_required
- conditional_sufficiency_rule: internal_mode=>traceability_required
- cost_sensitivity: medium

- notes: baseline human-facing and internal explanation intent

---

### FM-OTC-002

- service_family: financial_management
- outcome_family: analytical
- outcome_intent: analyse_cash_flow
- degradation_policy: degrade_with_caveat

- required_determinations: none
- required_scores: none
- required_flags: missing_period_flags|exclusion_flags
- required_metrics: inflow_outflow_metrics|trend_metrics
- required_summaries: cash_flow_summary
- required_recommendations: none
- required_traceability: none
- conditional_required_traceability: internal_mode=>inclusion_exclusion_trace
- required_confidence_outputs: overall_confidence

- mandatory_capabilities: transaction_parsing|category_classification|cash_flow_classification
- optional_capabilities: reporting_explanation|trend_analysis
- enrichment_capabilities: behavioural_analysis

- prohibited_shortcuts: cash_flow_without_transaction_direction|cash_flow_without_period_grouping_for_multi_period_scope

- required_data_dependencies: parsed_transactions|classified_transactions|cash_flow_summary|period_groupings
- required_ocr_feature_classes: text|tables|layout
- required_internal_data_dependencies: none
- conditional_required_internal_data_dependencies: multi_period_scope=>prior_statement_history
- required_external_data_dependencies: none

- confidence_requirement: baseline_overall_confidence_required
- sufficiency_rule: inflow_outflow_metrics_required
- conditional_sufficiency_rule: multi_period_scope=>prior_statement_history_required
- cost_sensitivity: medium

- notes: flow analysis intent, not risk interpretation

---

### FM-OTC-003

- service_family: financial_management
- outcome_family: analytical
- outcome_intent: analyse_spending_patterns
- degradation_policy: degrade_with_caveat

- required_determinations: none
- required_scores: none
- required_flags: missing_data_flags|caveat_flags
- required_metrics: category_spend_metrics|trend_metrics
- required_summaries: spending_summary
- required_recommendations: none
- required_traceability: none
- conditional_required_traceability: internal_mode=>section_confidence_trace
- required_confidence_outputs: overall_confidence|category_confidence|merchant_confidence

- mandatory_capabilities: transaction_parsing|category_classification
- optional_capabilities: cash_flow_classification|reporting_explanation|merchant_enrichment
- enrichment_capabilities: behavioural_analysis|trend_analysis

- prohibited_shortcuts: spending_summary_without_category_classification|merchant_breakdown_without_entity_resolution

- required_data_dependencies: parsed_transactions|classified_transactions|category_spend_summary|period_groupings
- required_ocr_feature_classes: text|tables|layout
- required_internal_data_dependencies: none
- conditional_required_internal_data_dependencies: comparative_scope=>prior_statement_history
- required_external_data_dependencies: none
- conditional_required_external_data_dependencies: merchant_breakdown_requested=>merchant_enrichment_source

- confidence_requirement: category_confidence_required_when_category_breakdown_requested
- sufficiency_rule: category_metrics_required
- conditional_sufficiency_rule: comparative_scope=>prior_period_data_required
- cost_sensitivity: medium

- notes: spending pattern interpretation intent

---

### FM-OTC-004

- service_family: financial_management
- outcome_family: analytical
- outcome_intent: assess_financial_obligation_pressure
- degradation_policy: escalate_for_missing_dependencies

- required_determinations: none
- required_scores: affordability_support_score
- required_flags: overload_flags|risk_markers
- required_metrics: debt_burden_metrics
- required_summaries: debt_summary
- required_recommendations: next_step_guidance
- required_traceability: none
- conditional_required_traceability: internal_mode=>obligation_trace
- required_confidence_outputs: overall_confidence

- mandatory_capabilities: transaction_parsing|category_classification|cash_flow_classification|debt_detection|reporting_explanation
- optional_capabilities: financial_stress_detection
- proposed_optional_capabilities: counterparty_classification
- enrichment_capabilities: benchmarking|trend_analysis

- prohibited_shortcuts: debt_summary_without_debt_detection|affordability_style_output_without_cash_flow_classification

- required_data_dependencies: parsed_transactions|classified_transactions|cash_flow_summary|debt_positions
- required_ocr_feature_classes: text|tables|layout|metadata
- required_internal_data_dependencies: none
- conditional_required_internal_data_dependencies: advanced_obligation_context=>account_context|prior_statement_history
- required_external_data_dependencies: none

- confidence_requirement: baseline_overall_confidence_required
- sufficiency_rule: debt_positions_and_burden_metrics_required;guidance_invalid_without_supporting_analysis
- cost_sensitivity: medium

- notes: obligation pressure assessment intent

---

### FM-OTC-005

- service_family: financial_management
- outcome_family: analytical
- outcome_intent: compare_against_reference
- degradation_policy: no_safe_degradation

- required_determinations: none
- required_scores: benchmark_deviation_score
- required_flags: caveat_flags
- required_metrics: benchmark_comparison_metrics
- required_summaries: benchmark_summary
- required_recommendations: optimisation_recommendations
- required_traceability: none
- conditional_required_traceability: internal_mode=>benchmark_source_trace
- required_confidence_outputs: overall_confidence|benchmark_applicability_confidence

- mandatory_capabilities: transaction_parsing|category_classification|benchmarking|reporting_explanation
- optional_capabilities: cash_flow_classification|debt_detection
- enrichment_capabilities: behavioural_analysis
- proposed_enrichment_capabilities: external_pricing_enrichment

- prohibited_shortcuts: benchmarking_without_reference_data|benchmark_summary_without_applicability_confidence|optimisation_without_comparison_basis

- required_data_dependencies: parsed_transactions|classified_transactions|benchmark_dataset|category_spend_summary
- required_ocr_feature_classes: text|tables|layout
- required_internal_data_dependencies: none
- conditional_required_internal_data_dependencies: cohort_comparison_mode=>customer_segment
- required_external_data_dependencies: benchmark_source|external_pricing_source

- confidence_requirement: benchmark_applicability_confidence_required
- sufficiency_rule: benchmark_source_required;recommendations_invalid_without_reference_basis
- cost_sensitivity: high

- notes: reference comparison and benchmark intent

---

### FM-OTC-006

- service_family: financial_management
- outcome_family: analytical
- outcome_intent: detect_financial_risk
- degradation_policy: internal_review_required

- required_determinations: none
- required_scores: stress_score
- required_flags: overload_flags|escalation_flags
- required_metrics: trend_metrics|debt_burden_metrics
- required_summaries: health_summary
- required_recommendations: escalation_guidance
- required_traceability: audit_trace|section_confidence_trace|trigger_decomposition_trace
- required_confidence_outputs: overall_confidence|scenario_confidence

- mandatory_capabilities: transaction_parsing|category_classification|cash_flow_classification|debt_detection|financial_stress_detection|reporting_explanation
- optional_capabilities: behavioural_analysis
- proposed_optional_capabilities: timing_analysis
- enrichment_capabilities: benchmarking
- proposed_enrichment_capabilities: anomaly_detection

- prohibited_shortcuts: stress_score_without_multi_signal_analysis|risk_summary_without_traceability|escalation_guidance_without_supporting_flags

- required_data_dependencies: parsed_transactions|classified_transactions|cash_flow_summary|debt_positions|historical_period_data
- required_ocr_feature_classes: text|tables|layout|metadata
- required_internal_data_dependencies: prior_statement_history|account_context
- required_external_data_dependencies: none

- confidence_requirement: overall_and_trace_confidence_required
- sufficiency_rule: risk_output_invalid_without_scores_flags_and_trace
- conditional_sufficiency_rule: multi_period_scope=>prior_statement_history_required
- cost_sensitivity: high

- notes: internal risk detection and escalation intent

---

## Proof and Verification Outcome Mapping

### FM-OTC-007

- service_family: financial_management
- outcome_family: proof_verification
- outcome_intent: generate_proof
- degradation_policy: no_safe_degradation

- required_determinations: proof_verification_status
- required_scores: none
- required_flags: provenance_flags
- required_metrics: reference_match_metrics
- required_summaries: proof_summary
- required_recommendations: none
- required_traceability: provenance_trace|consent_trace|document_version_trace
- required_confidence_outputs: overall_confidence

- mandatory_capabilities: transaction_parsing|document_proof_generation|reporting_explanation
- optional_capabilities: none
- proposed_optional_capabilities: document_validation|consent_validation
- enrichment_capabilities: none
- proposed_enrichment_capabilities: authenticity_validation

- prohibited_shortcuts: proof_without_source_document_linkage|proof_without_provenance_trace

- required_data_dependencies: parsed_transactions|source_document_reference|transaction_reference
- required_ocr_feature_classes: text|tables|metadata
- required_internal_data_dependencies: stored_document_history|consent_state
- required_external_data_dependencies: none

- confidence_requirement: provenance_confidence_required
- sufficiency_rule: proof_invalid_without_document_linkage_and_trace
- cost_sensitivity: medium

- notes: proof and verification intent

---

## End of Rule Table v1

## End of Document
