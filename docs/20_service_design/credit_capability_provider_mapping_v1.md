# Credit / Trade Credit Decision — Capability to Provider Mapping v1

## Purpose

Defines the set of eligible providers for each Credit / Trade Credit Decision capability and their characteristics.

This table operates at the **design and decision-support layer**:

capability → provider options (NOT selection)

It enables:
- execution plan construction
- provider comparison
- fallback design
- cost / confidence trade-offs

It does NOT:
- select providers
- define execution order
- embed routing logic
- override execution_plan control

---

## Governance Notes

- Providers listed are **eligible options**, not mandated selections
- Final provider choice is made by **decision engines via execution_plan**
- No worker may override this structure

---

## Controlled Vocabulary Rule

All tokens in this table are governed design-time vocabulary.

Where a token is not yet formally registered:
- treat it as proposed controlled vocabulary
- use consistently
- do not replace ad hoc in implementation

---

## Column Definitions

### Core Identification

- `capability_id`
- `provider_id`
- `provider_type` → internal | external_api | hybrid

### Capability Fit

- `supported_outcome_intents`
- `coverage_level` → full | partial | specialised
- `strengths`
- `limitations`

### Data & Feature Support

- `supported_ocr_feature_classes` → text | tables | layout | metadata | logos
- `required_input_conditions`

### Performance Characteristics

- `confidence_profile` → high_consistency | variable | context_sensitive
- `latency_profile` → low | medium | high
- `cost_profile` → low | medium | high

### Execution Constraints

- `fallback_eligible` → true | false
- `fallback_restrictions`
- `parallelizable` → true | false

### Governance & Control

- `determinism_level` → deterministic | semi_deterministic | probabilistic
- `explainability_level` → high | medium | low
- `auditability_support` → true | false

### Maturity & Lifecycle

- `provider_status` → approved | experimental | deprecated | fallback_only
- `version`

### Notes

- `notes`

---

## Rule Table

### CREDIT-CPM-001

- capability_id: fraud_detection
- provider_id: internal_rules_fraud_engine_v1
- provider_type: internal

- supported_outcome_intents: assess_document_and_transaction_integrity|support_credit_decision_review
- coverage_level: full
- strengths: high_explainability|strong_rule_control|good_for_governed_fraud_flags
- limitations: depends_on_upstream_quality|limited_on_complex_hidden_patterns|history_sensitive_for_pattern_strength

- supported_ocr_feature_classes: text|tables|layout|metadata|logos
- required_input_conditions: document_validation_or_transaction_inputs_required|governed_fraud_rule_set_required

- confidence_profile: high_consistency
- latency_profile: low
- cost_profile: low

- fallback_eligible: true
- fallback_restrictions: fallback_must_preserve_governed_fraud_flag_and_score_schema
- parallelizable: true

- determinism_level: deterministic
- explainability_level: high
- auditability_support: true

- provider_status: approved
- version: v1

- notes: baseline internal fraud and integrity engine

---

### CREDIT-CPM-002

- capability_id: fraud_detection
- provider_id: hybrid_pattern_enriched_fraud_engine_v1
- provider_type: hybrid

- supported_outcome_intents: assess_document_and_transaction_integrity|support_credit_decision_review
- coverage_level: specialised
- strengths: better_on_complex_pattern_detection|better_on_subtle_manipulation_signals|useful_for_harder_fraud_cases
- limitations: higher_cost|lower_determinism|requires_strict_flag_and_score_normalization

- supported_ocr_feature_classes: text|tables|layout|metadata|logos
- required_input_conditions: governed_fraud_signal_mapping_required|parsed_transactions_or_document_findings_required

- confidence_profile: context_sensitive
- latency_profile: medium
- cost_profile: medium

- fallback_eligible: true
- fallback_restrictions: must_not_emit_unmapped_fraud_labels_or_uncontrolled_scores
- parallelizable: true

- determinism_level: semi_deterministic
- explainability_level: medium
- auditability_support: true

- provider_status: experimental
- version: v1

- notes: enrichment fraud engine for harder manipulation and pattern cases

---

### CREDIT-CPM-003

- capability_id: affordability_classification
- provider_id: internal_rules_affordability_engine_v1
- provider_type: internal

- supported_outcome_intents: assess_affordability_and_repayment_capacity|support_credit_decision_review
- coverage_level: full
- strengths: high_explainability|strong_metric_control|good_for_governed_affordability_outputs
- limitations: depends_on_income_and_obligation_quality|limited_on_nonlinear_edge_cases|history_improves_stability

- supported_ocr_feature_classes: none
- required_input_conditions: parsed_transactions_required|cash_flow_classification_required|debt_detection_required

- confidence_profile: high_consistency
- latency_profile: low
- cost_profile: low

- fallback_eligible: true
- fallback_restrictions: fallback_must_preserve_governed_affordability_status_score_and_metric_schema
- parallelizable: true

- determinism_level: deterministic
- explainability_level: high
- auditability_support: true

- provider_status: approved
- version: v1

- notes: baseline affordability engine for governed affordability outputs

---

### CREDIT-CPM-004

- capability_id: affordability_classification
- provider_id: hybrid_signal_enriched_affordability_engine_v1
- provider_type: hybrid

- supported_outcome_intents: assess_affordability_and_repayment_capacity|support_credit_decision_review
- coverage_level: specialised
- strengths: better_on_complex_affordability_patterns|stronger_on_income_variability_cases|useful_for_harder_repayment_capacity_assessment
- limitations: higher_cost|lower_determinism|requires_strict_metric_and_status_normalization

- supported_ocr_feature_classes: none
- required_input_conditions: parsed_transactions_required|cash_flow_classification_required|debt_detection_required|historical_period_data_preferred

- confidence_profile: context_sensitive
- latency_profile: medium
- cost_profile: medium

- fallback_eligible: true
- fallback_restrictions: must_not_emit_unmapped_affordability_labels_or_uncontrolled_metrics
- parallelizable: true

- determinism_level: semi_deterministic
- explainability_level: medium
- auditability_support: true

- provider_status: experimental
- version: v1

- notes: enrichment affordability engine for harder income and repayment-capacity cases

---

### CREDIT-CPM-005

- capability_id: risk_scoring
- provider_id: internal_rules_risk_engine_v1
- provider_type: internal

- supported_outcome_intents: assess_credit_risk|support_credit_decision_review
- coverage_level: full
- strengths: high_traceability|strong_score_component_control|good_for_governed_internal_risk_scoring
- limitations: depends_on_upstream_signal_quality|limited_on_complex_nonlinear_risk_interactions

- supported_ocr_feature_classes: none
- required_input_conditions: parsed_transactions_required|cash_flow_classification_required|debt_detection_required|risk_feature_inputs_required

- confidence_profile: high_consistency
- latency_profile: low
- cost_profile: low

- fallback_eligible: true
- fallback_restrictions: fallback_must_preserve_governed_risk_score_and_status_schema
- parallelizable: true

- determinism_level: deterministic
- explainability_level: high
- auditability_support: true

- provider_status: approved
- version: v1

- notes: baseline internal risk scoring engine

---

### CREDIT-CPM-006

- capability_id: risk_scoring
- provider_id: hybrid_probability_risk_engine_v1
- provider_type: hybrid

- supported_outcome_intents: assess_credit_risk|support_credit_decision_review
- coverage_level: specialised
- strengths: better_on_probability_estimation|better_on_multisignal_risk_interactions|useful_for_harder_credit_risk_cases
- limitations: higher_cost|lower_determinism|requires_strict_score_normalization_and_trace_controls

- supported_ocr_feature_classes: none
- required_input_conditions: risk_feature_inputs_required|historical_period_data_preferred|governed_probability_mapping_required

- confidence_profile: context_sensitive
- latency_profile: medium
- cost_profile: medium

- fallback_eligible: true
- fallback_restrictions: must_not_emit_unmapped_risk_labels_or_uncontrolled_score_fields
- parallelizable: true

- determinism_level: semi_deterministic
- explainability_level: medium
- auditability_support: true

- provider_status: experimental
- version: v1

- notes: enrichment risk engine for more complex probability-to-pay assessment

---

### CREDIT-CPM-007

- capability_id: collections_timing_optimization
- provider_id: internal_rules_collections_timing_engine_v1
- provider_type: internal

- supported_outcome_intents: optimize_collections_timing
- coverage_level: full
- strengths: high_explainability|good_timing_basis_control|strong_for_governed_timing_recommendations
- limitations: depends_on_history_for_best_results|limited_on_complex_seasonality_patterns

- supported_ocr_feature_classes: none
- required_input_conditions: cash_flow_classification_required|historical_period_data_required|timing_features_required

- confidence_profile: high_consistency
- latency_profile: low
- cost_profile: low

- fallback_eligible: true
- fallback_restrictions: fallback_must_preserve_governed_timing_score_metric_and_recommendation_schema
- parallelizable: true

- determinism_level: deterministic
- explainability_level: high
- auditability_support: true

- provider_status: approved
- version: v1

- notes: baseline collections timing optimization engine

---

### CREDIT-CPM-008

- capability_id: reporting_explanation
- provider_id: internal_credit_reporter_v1
- provider_type: internal

- supported_outcome_intents: assess_document_and_transaction_integrity|assess_affordability_and_repayment_capacity|assess_credit_risk|optimize_collections_timing|communicate_credit_decision_status|summarize_repayment_expectations|support_credit_decision_review
- coverage_level: full
- strengths: high_auditability|strong_schema_control|stable_internal_trace_outputs|good_for_customer_safe_projections_from_internal_decisions
- limitations: less_flexible_narrative_expression|depends_on_upstream_trace_completeness

- supported_ocr_feature_classes: none
- required_input_conditions: governed_upstream_findings_required|decision_trace_inputs_required_for_internal_modes

- confidence_profile: high_consistency
- latency_profile: low
- cost_profile: low

- fallback_eligible: true
- fallback_restrictions: must_not_drop_required_traceability_or_customer_status_alignment_rules
- parallelizable: true

- determinism_level: deterministic
- explainability_level: high
- auditability_support: true

- provider_status: approved
- version: v1

- notes: governed reporter for internal review outputs and customer-facing credit summaries

---

---

### CREDIT-CPM-009

- capability_id: fraud_detection
- provider_id: future_fraud_detection_engine_v1
- provider_type: hybrid

- supported_outcome_intents: assess_document_and_transaction_integrity|support_credit_decision_review
- coverage_level: specialised
- strengths: placeholder_for_fraud_pattern_detection
- limitations: not_implemented

- supported_ocr_feature_classes: text|tables|layout|metadata
- required_input_conditions: parsed_transactions_required|validation_findings_required

- confidence_profile: context_sensitive
- latency_profile: medium
- cost_profile: medium

- fallback_eligible: false
- fallback_restrictions: no_runtime_available
- parallelizable: true

- determinism_level: semi_deterministic
- explainability_level: medium
- auditability_support: true

- provider_status: fallback_only
- version: v1

- notes: placeholder for fraud detection capability

---

### CREDIT-CPM-010

- capability_id: affordability_classification
- provider_id: future_affordability_engine_v1
- provider_type: internal

- supported_outcome_intents: assess_affordability_and_repayment_capacity|support_credit_decision_review
- coverage_level: full
- strengths: placeholder_for_affordability_classification
- limitations: not_implemented

- supported_ocr_feature_classes: none
- required_input_conditions: financial_inputs_required

- confidence_profile: context_sensitive
- latency_profile: medium
- cost_profile: medium

- fallback_eligible: false
- fallback_restrictions: no_runtime_available
- parallelizable: true

- determinism_level: deterministic
- explainability_level: high
- auditability_support: true

- provider_status: fallback_only
- version: v1

- notes: placeholder for affordability classification capability

---

### CREDIT-CPM-011

- capability_id: risk_scoring
- provider_id: future_risk_scoring_engine_v1
- provider_type: internal

- supported_outcome_intents: assess_credit_risk|support_credit_decision_review
- coverage_level: full
- strengths: placeholder_for_credit_risk_scoring
- limitations: not_implemented

- supported_ocr_feature_classes: none
- required_input_conditions: risk_inputs_required

- confidence_profile: context_sensitive
- latency_profile: medium
- cost_profile: medium

- fallback_eligible: false
- fallback_restrictions: no_runtime_available
- parallelizable: true

- determinism_level: deterministic
- explainability_level: high
- auditability_support: true

- provider_status: fallback_only
- version: v1

- notes: placeholder for risk scoring capability

---

### CREDIT-CPM-012

- capability_id: collections_timing_optimization
- provider_id: future_collections_timing_engine_v1
- provider_type: internal

- supported_outcome_intents: optimize_collections_timing|support_credit_decision_review
- coverage_level: specialised
- strengths: placeholder_for_collections_timing_logic
- limitations: not_implemented

- supported_ocr_feature_classes: none
- required_input_conditions: historical_cash_flow_required

- confidence_profile: context_sensitive
- latency_profile: medium
- cost_profile: medium

- fallback_eligible: false
- fallback_restrictions: no_runtime_available
- parallelizable: true

- determinism_level: deterministic
- explainability_level: high
- auditability_support: true

- provider_status: fallback_only
- version: v1

- notes: placeholder for collections timing optimization capability

---

### CREDIT-CPM-013

- capability_id: decision_status_projection
- provider_id: future_decision_projection_engine_v1
- provider_type: internal

- supported_outcome_intents: communicate_credit_decision_status
- coverage_level: specialised
- strengths: placeholder_for_decision_projection
- limitations: not_implemented

- supported_ocr_feature_classes: none
- required_input_conditions: internal_decision_required

- confidence_profile: high_consistency
- latency_profile: low
- cost_profile: low

- fallback_eligible: false
- fallback_restrictions: no_runtime_available
- parallelizable: true

- determinism_level: deterministic
- explainability_level: high
- auditability_support: true

- provider_status: fallback_only
- version: v1

- notes: placeholder for decision status projection capability

---

### CREDIT-CPM-014

- capability_id: repayment_schedule_generation
- provider_id: future_repayment_schedule_engine_v1
- provider_type: internal

- supported_outcome_intents: summarize_repayment_expectations|communicate_credit_decision_status
- coverage_level: full
- strengths: placeholder_for_schedule_generation
- limitations: not_implemented

- supported_ocr_feature_classes: none
- required_input_conditions: schedule_inputs_required

- confidence_profile: high_consistency
- latency_profile: low
- cost_profile: low

- fallback_eligible: false
- fallback_restrictions: no_runtime_available
- parallelizable: true

- determinism_level: deterministic
- explainability_level: high
- auditability_support: true

- provider_status: fallback_only
- version: v1

- notes: placeholder for repayment schedule generation capability

---

### CREDIT-CPM-015

- capability_id: income_stability_assessment
- provider_id: future_income_stability_engine_v1
- provider_type: internal

- supported_outcome_intents: assess_affordability_and_repayment_capacity|assess_credit_risk
- coverage_level: specialised
- strengths: placeholder_for_income_stability_analysis
- limitations: not_implemented

- supported_ocr_feature_classes: none
- required_input_conditions: historical_income_required

- confidence_profile: context_sensitive
- latency_profile: medium
- cost_profile: medium

- fallback_eligible: false
- fallback_restrictions: no_runtime_available
- parallelizable: true

- determinism_level: deterministic
- explainability_level: high
- auditability_support: true

- provider_status: fallback_only
- version: v1

- notes: placeholder for income stability assessment capability

---

### CREDIT-CPM-016

- capability_id: counterparty_exposure_analysis
- provider_id: future_counterparty_exposure_engine_v1
- provider_type: hybrid

- supported_outcome_intents: assess_credit_risk|support_credit_decision_review
- coverage_level: specialised
- strengths: placeholder_for_counterparty_exposure_analysis
- limitations: not_implemented

- supported_ocr_feature_classes: none
- required_input_conditions: transaction_counterparty_data_required

- confidence_profile: context_sensitive
- latency_profile: medium
- cost_profile: medium

- fallback_eligible: false
- fallback_restrictions: no_runtime_available
- parallelizable: true

- determinism_level: semi_deterministic
- explainability_level: medium
- auditability_support: true

- provider_status: experimental
- version: v1

- notes: placeholder for counterparty exposure analysis capability

---

### CREDIT-CPM-017

- capability_id: seasonality_analysis
- provider_id: future_seasonality_engine_v1
- provider_type: internal

- supported_outcome_intents: assess_credit_risk|optimize_collections_timing|support_credit_decision_review
- coverage_level: specialised
- strengths: placeholder_for_seasonality_analysis
- limitations: not_implemented

- supported_ocr_feature_classes: none
- required_input_conditions: historical_period_data_required

- confidence_profile: context_sensitive
- latency_profile: medium
- cost_profile: medium

- fallback_eligible: false
- fallback_restrictions: no_runtime_available
- parallelizable: true

- determinism_level: deterministic
- explainability_level: high
- auditability_support: true

- provider_status: fallback_only
- version: v1

- notes: placeholder for seasonality analysis capability

---

### CREDIT-CPM-018

- capability_id: timing_optimization_projection
- provider_id: future_timing_projection_engine_v1
- provider_type: internal

- supported_outcome_intents: summarize_repayment_expectations
- coverage_level: specialised
- strengths: placeholder_for_timing_projection
- limitations: not_implemented

- supported_ocr_feature_classes: none
- required_input_conditions: repayment_schedule_inputs_required

- confidence_profile: context_sensitive
- latency_profile: medium
- cost_profile: medium

- fallback_eligible: false
- fallback_restrictions: no_runtime_available
- parallelizable: true

- determinism_level: deterministic
- explainability_level: high
- auditability_support: true

- provider_status: fallback_only
- version: v1

- notes: placeholder for timing optimization projection capability

---

### CREDIT-CPM-019

- capability_id: visual_tamper_enrichment
- provider_id: future_visual_tamper_engine_v1
- provider_type: hybrid

- supported_outcome_intents: assess_document_and_transaction_integrity
- coverage_level: specialised
- strengths: placeholder_for_visual_tamper_detection
- limitations: not_implemented

- supported_ocr_feature_classes: layout|logos
- required_input_conditions: document_image_features_required

- confidence_profile: variable
- latency_profile: medium
- cost_profile: medium

- fallback_eligible: false
- fallback_restrictions: no_runtime_available
- parallelizable: true

- determinism_level: semi_deterministic
- explainability_level: medium
- auditability_support: true

- provider_status: experimental
- version: v1

- notes: placeholder for visual tamper enrichment capability

---

## End of Document
