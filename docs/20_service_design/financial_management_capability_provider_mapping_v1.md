# Financial Management — Capability to Provider Mapping v1

## Purpose

Defines the set of eligible providers for each Financial Management capability and their characteristics.

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
- `provider_governance_classification` defines evidence strength and approval level
- Proposed roadmap candidates are not approved runtime design truth

---

## Controlled Vocabulary Rule

Tokens in this table must be interpreted according to governance strength.

- `governed_current_option`
  → governed eligible provider option

- `governed_future_placeholder`
  → governed placeholder, not current runtime truth

- `proposed_roadmap_candidate`
  → roadmap concept only, not governed eligible runtime truth unless later approved

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

- `provider_governance_classification` → governed_current_option | governed_future_placeholder | proposed_roadmap_candidate
- `provider_runtime_status` → runtime_enabled | not_runtime_enabled | runtime_unknown
- `version`

### Notes

- `notes`

---

## Rule Table

### FM-CPM-001

- capability_id: transaction_parsing
- provider_id: internal_rules_parser_v1
- provider_type: internal

- supported_outcome_intents: explain_document|analyse_cash_flow|analyse_spending_patterns|assess_financial_obligation_pressure|compare_against_reference|detect_financial_risk|generate_proof
- coverage_level: full
- strengths: low_cost|high_explainability|strong_control_over_schema|good_for_structured_bank_statements
- limitations: sensitive_to_layout_variability|dependent_on_table_extraction_quality|weaker_on_poorly_structured_inputs

- supported_ocr_feature_classes: text|tables|layout
- required_input_conditions: structured_statement_layout_expected|usable_table_extraction_required

- confidence_profile: context_sensitive
- latency_profile: low
- cost_profile: low

- fallback_eligible: true
- fallback_restrictions: requires_governed_alternative_parser_or_upstream_provider_change
- parallelizable: true

- determinism_level: deterministic
- explainability_level: high
- auditability_support: true

- provider_governance_classification: governed_current_option
- provider_runtime_status: runtime_unknown
- version: v1

- notes: baseline internal parser aligned to rules-first transaction parsing capability

---

### FM-CPM-002

- capability_id: transaction_parsing
- provider_id: hybrid_layout_aware_parser_v1
- provider_type: hybrid

- supported_outcome_intents: explain_document|analyse_cash_flow|analyse_spending_patterns|assess_financial_obligation_pressure|compare_against_reference|detect_financial_risk
- coverage_level: specialised
- strengths: better_on_layout_variability|improved_multiline_row_handling|supports_difficult_table_patterns
- limitations: higher_cost|lower_determinism_than_rules_only|requires_stronger_runtime_governance

- supported_ocr_feature_classes: text|tables|layout|metadata
- required_input_conditions: usable_text_and_layout_required|governed_hybrid_mode_enabled

- confidence_profile: variable
- latency_profile: medium
- cost_profile: medium

- fallback_eligible: true
- fallback_restrictions: must_not_bypass_governed_internal_schema_normalization
- parallelizable: true

- determinism_level: semi_deterministic
- explainability_level: medium
- auditability_support: true

- provider_governance_classification: proposed_roadmap_candidate
- provider_runtime_status: runtime_unknown
- version: v1

- notes: proposed hybrid option for harder layouts; not a replacement for schema-controlled normalization

---

### FM-CPM-003

- capability_id: category_classification
- provider_id: internal_rules_classifier_v1
- provider_type: internal

- supported_outcome_intents: explain_document|analyse_cash_flow|analyse_spending_patterns|assess_financial_obligation_pressure|compare_against_reference|detect_financial_risk
- coverage_level: full
- strengths: low_cost|high_explainability|consistent_primary_category_assignment|strong_auditability
- limitations: weaker_on_ambiguous_narrations|limited_semantic_generalization|dependent_on_merchant_quality

- supported_ocr_feature_classes: text|metadata
- required_input_conditions: parsed_transactions_required|usable_transaction_descriptions_required

- confidence_profile: high_consistency
- latency_profile: low
- cost_profile: low

- fallback_eligible: true
- fallback_restrictions: fallback_must_preserve_primary_secondary_category_contract
- parallelizable: true

- determinism_level: deterministic
- explainability_level: high
- auditability_support: true

- provider_governance_classification: governed_current_option
- provider_runtime_status: runtime_unknown
- version: v1

- notes: baseline rules-first classifier aligned to capability docs and controlled category outputs

---

### FM-CPM-004

- capability_id: category_classification
- provider_id: hybrid_semantic_classifier_v1
- provider_type: hybrid

- supported_outcome_intents: analyse_spending_patterns|assess_financial_obligation_pressure|compare_against_reference|detect_financial_risk
- coverage_level: specialised
- strengths: better_on_ambiguous_narration|improved_secondary_category_support|useful_for_richer_behavioural_analysis
- limitations: lower_determinism|higher_cost|requires_governed_label_normalization

- supported_ocr_feature_classes: text|metadata
- required_input_conditions: parsed_transactions_required|governed_label_mapping_required

- confidence_profile: variable
- latency_profile: medium
- cost_profile: medium

- fallback_eligible: true
- fallback_restrictions: must_not_emit_unmapped_free_text_categories
- parallelizable: true

- determinism_level: semi_deterministic
- explainability_level: medium
- auditability_support: true

- provider_governance_classification: proposed_roadmap_candidate
- provider_runtime_status: runtime_unknown
- version: v1

- notes: proposed enrichment classifier for ambiguous descriptions; baseline remains internal rules-first

---

### FM-CPM-005

- capability_id: cash_flow_classification
- provider_id: internal_rules_cashflow_engine_v1
- provider_type: internal

- supported_outcome_intents: explain_document|analyse_cash_flow|assess_financial_obligation_pressure|detect_financial_risk
- coverage_level: full
- strengths: low_cost|high_explainability|strong_flow_type_control|good_for_affordability_support
- limitations: depends_on_category_quality|history_sensitive_for_recurrence|weaker_on_ambiguous_transfer_patterns

- supported_ocr_feature_classes: none
- required_input_conditions: parsed_transactions_required|category_classification_required|historical_data_optional_for_recurrence

- confidence_profile: high_consistency
- latency_profile: low
- cost_profile: low

- fallback_eligible: true
- fallback_restrictions: fallback_must_preserve_flow_type_contract_and_recurrence_fields
- parallelizable: true

- determinism_level: deterministic
- explainability_level: high
- auditability_support: true

- provider_governance_classification: governed_current_option
- provider_runtime_status: runtime_unknown
- version: v1

- notes: baseline cash flow engine; consumes upstream structured data rather than raw OCR features

---

### FM-CPM-006

- capability_id: cash_flow_classification
- provider_id: hybrid_pattern_enriched_cashflow_v1
- provider_type: hybrid

- supported_outcome_intents: analyse_cash_flow|assess_financial_obligation_pressure|detect_financial_risk
- coverage_level: specialised
- strengths: better_recurrence_detection|better_on_irregular_patterns|improves_complex_flow_segmentation
- limitations: higher_cost|requires_history_for_best_results|lower_determinism_than_rules_only

- supported_ocr_feature_classes: none
- required_input_conditions: parsed_transactions_required|category_classification_required|historical_period_data_preferred

- confidence_profile: context_sensitive
- latency_profile: medium
- cost_profile: medium

- fallback_eligible: true
- fallback_restrictions: must_not_override_governed_cash_flow_labels_without_normalization
- parallelizable: true

- determinism_level: semi_deterministic
- explainability_level: medium
- auditability_support: true

- provider_governance_classification: proposed_roadmap_candidate
- provider_runtime_status: runtime_unknown
- version: v1

- notes: enrichment option for higher-complexity recurrence and flow-pattern analysis

---


### FM-CPM-007

- capability_id: debt_detection
- provider_id: internal_rules_debt_engine_v1
- provider_type: internal

- supported_outcome_intents: assess_financial_obligation_pressure|detect_financial_risk|analyse_cash_flow
- coverage_level: full
- strengths: high_explainability|strong_repayment_pattern_control|good_for_structured_obligation_outputs
- limitations: depends_on_upstream_classification_quality|limited_on_complex_or_ambiguous_credit_patterns|history_sensitive_for_trend_accuracy

- supported_ocr_feature_classes: none
- required_input_conditions: parsed_transactions_required|category_classification_required|cash_flow_classification_required

- confidence_profile: high_consistency
- latency_profile: low
- cost_profile: low

- fallback_eligible: true
- fallback_restrictions: fallback_must_preserve_governed_debt_position_schema
- parallelizable: true

- determinism_level: deterministic
- explainability_level: high
- auditability_support: true

- provider_governance_classification: governed_current_option
- provider_runtime_status: runtime_unknown
- version: v1

- notes: baseline debt detection engine aligned to debt position and repayment schedule outputs

---

### FM-CPM-008

- capability_id: debt_detection
- provider_id: hybrid_pattern_enriched_debt_engine_v1
- provider_type: hybrid

- supported_outcome_intents: assess_financial_obligation_pressure|detect_financial_risk
- coverage_level: specialised
- strengths: better_on_ambiguous_repayment_patterns|improved_risk_flag_detection|better_for_mixed_credit_behaviour
- limitations: higher_cost|lower_determinism|requires_strict_output_normalization

- supported_ocr_feature_classes: none
- required_input_conditions: parsed_transactions_required|category_classification_required|cash_flow_classification_required|historical_period_data_preferred

- confidence_profile: context_sensitive
- latency_profile: medium
- cost_profile: medium

- fallback_eligible: true
- fallback_restrictions: must_not_emit_uncontrolled_debt_labels_or_free_text_risk_flags
- parallelizable: true

- determinism_level: semi_deterministic
- explainability_level: medium
- auditability_support: true

- provider_governance_classification: proposed_roadmap_candidate
- provider_runtime_status: runtime_unknown
- version: v1

- notes: enrichment option for harder debt-pattern interpretation; baseline remains rules-first

---

### FM-CPM-009

- capability_id: reporting_explanation
- provider_id: internal_template_reporter_v1
- provider_type: internal

- supported_outcome_intents: explain_document|analyse_cash_flow|analyse_spending_patterns|assess_financial_obligation_pressure|compare_against_reference|detect_financial_risk|generate_proof
- coverage_level: full
- strengths: high_explainability|strong_schema_control|high_auditability|stable_internal_trace_generation
- limitations: less_flexible_natural_language|less_expressive_for_complex_narratives|depends_on_upstream_data_completeness

- supported_ocr_feature_classes: none
- required_input_conditions: governed_upstream_outputs_required|section_confidence_inputs_required_for_internal_modes

- confidence_profile: high_consistency
- latency_profile: low
- cost_profile: low

- fallback_eligible: true
- fallback_restrictions: must_not_drop_required_trace_or_confidence_sections
- parallelizable: true

- determinism_level: deterministic
- explainability_level: high
- auditability_support: true

- provider_governance_classification: governed_current_option
- provider_runtime_status: runtime_unknown
- version: v1

- notes: baseline reporting and explanation provider for customer summaries and internal trace outputs

---

### FM-CPM-010

- capability_id: reporting_explanation
- provider_id: hybrid_nlg_reporter_v1
- provider_type: hybrid

- supported_outcome_intents: explain_document|analyse_spending_patterns|compare_against_reference|detect_financial_risk
- coverage_level: specialised
- strengths: richer_plain_language|better_customer_readability|stronger_narrative_summaries
- limitations: lower_determinism|higher_governance_need|must_be_constrained_by_governed_section_schema

- supported_ocr_feature_classes: none
- required_input_conditions: governed_structured_inputs_required|template_guardrails_required|section_schema_must_be_preserved

- confidence_profile: variable
- latency_profile: medium
- cost_profile: medium

- fallback_eligible: true
- fallback_restrictions: must_not_replace_internal_trace_with_free_text_only|must_preserve_required_section_structure
- parallelizable: true

- determinism_level: semi_deterministic
- explainability_level: medium
- auditability_support: true

- provider_governance_classification: proposed_roadmap_candidate
- provider_runtime_status: runtime_unknown
- version: v1

- notes: enrichment option for customer-facing narrative quality; not a substitute for governed trace outputs

---

### FM-CPM-011

- capability_id: behavioural_analysis
- provider_id: internal_rules_behaviour_engine_v1
- provider_type: internal

- supported_outcome_intents: analyse_spending_patterns|compare_against_reference|detect_financial_risk
- coverage_level: full
- strengths: strong_ratio_calculation_control|high_explainability|good_for_repeatable_behaviour_metrics
- limitations: depends_on_history_quality|limited_predictive_depth|sensitive_to_upstream_category_errors

- supported_ocr_feature_classes: none
- required_input_conditions: parsed_transactions_required|category_classification_required|cash_flow_classification_required|historical_period_data_preferred

- confidence_profile: high_consistency
- latency_profile: low
- cost_profile: low

- fallback_eligible: true
- fallback_restrictions: fallback_must_preserve_governed_metric_names_and_ratio_definitions
- parallelizable: true

- determinism_level: deterministic
- explainability_level: high
- auditability_support: true

- provider_governance_classification: governed_current_option
- provider_runtime_status: runtime_unknown
- version: v1

- notes: baseline behavioural metrics engine for repeatable spending and habit analysis

---

### FM-CPM-012

- capability_id: behavioural_analysis
- provider_id: hybrid_predictive_behaviour_engine_v1
- provider_type: hybrid

- supported_outcome_intents: analyse_spending_patterns|detect_financial_risk|compare_against_reference
- coverage_level: specialised
- strengths: richer_pattern_detection|better_on_deviation_analysis|useful_for_advanced_behaviour_insights
- limitations: higher_cost|lower_determinism|requires_strict_metric_normalization

- supported_ocr_feature_classes: none
- required_input_conditions: parsed_transactions_required|category_classification_required|cash_flow_classification_required|historical_period_data_required_for_best_results

- confidence_profile: context_sensitive
- latency_profile: medium
- cost_profile: medium

- fallback_eligible: true
- fallback_restrictions: must_not_emit_unmapped_behaviour_labels_or_uncontrolled_scores
- parallelizable: true

- determinism_level: semi_deterministic
- explainability_level: medium
- auditability_support: true

- provider_governance_classification: proposed_roadmap_candidate
- provider_runtime_status: runtime_unknown
- version: v1

- notes: enrichment option for advanced behaviour pattern analysis and deviation detection

---

### FM-CPM-013

- capability_id: benchmarking
- provider_id: internal_population_benchmark_engine_v1
- provider_type: internal

- supported_outcome_intents: compare_against_reference|detect_financial_risk|analyse_spending_patterns
- coverage_level: partial
- strengths: high_control_over_cohort_logic|good_internal_explainability|strong_auditability
- limitations: requires_data_scale|limited_until_population_data_matures|may_have_cohort_coverage_gaps

- supported_ocr_feature_classes: none
- required_input_conditions: category_spend_summary_required|behavioural_metrics_required|governed_population_dataset_required

- confidence_profile: context_sensitive
- latency_profile: medium
- cost_profile: medium

- fallback_eligible: true
- fallback_restrictions: must_not_claim_population_comparison_without_valid_cohort_basis
- parallelizable: true

- determinism_level: deterministic
- explainability_level: high
- auditability_support: true

- provider_governance_classification: proposed_roadmap_candidate
- provider_runtime_status: runtime_unknown
- version: v1

- notes: target-state internal benchmark engine; partial until sufficient governed benchmark data exists

---

### FM-CPM-014

- capability_id: benchmarking
- provider_id: external_reference_benchmark_service_v1
- provider_type: external_api

- supported_outcome_intents: compare_against_reference
- coverage_level: specialised
- strengths: faster_time_to_value|useful_where_internal_population_data_is_insufficient|supports_external_reference_comparisons
- limitations: external_dependency|higher_cost|cohort_alignment_and_applicability_must_be_governed

- supported_ocr_feature_classes: none
- required_input_conditions: category_spend_summary_required|governed_reference_mapping_required|external_source_contract_required

- confidence_profile: variable
- latency_profile: medium
- cost_profile: high

- fallback_eligible: true
- fallback_restrictions: must_not_be_used_without_applicability_checks|must_not_override_governed_benchmark_schema
- parallelizable: true

- determinism_level: semi_deterministic
- explainability_level: medium
- auditability_support: true

- provider_governance_classification: governed_current_option
- provider_runtime_status: runtime_unknown
- version: v1

- notes: interim external benchmark source option where internal benchmark coverage is not yet sufficient

### FM-CPM-015

- capability_id: financial_stress_detection
- provider_id: internal_rules_stress_engine_v1
- provider_type: internal

- supported_outcome_intents: detect_financial_risk|assess_financial_obligation_pressure
- coverage_level: full
- strengths: high_explainability|strong_threshold_control|good_for_governed_risk_banding
- limitations: depends_on_upstream_cash_flow_and_debt_quality|limited_on_complex_nonlinear_patterns|history_sensitive_for_multi_period_accuracy

- supported_ocr_feature_classes: none
- required_input_conditions: cash_flow_classification_required|debt_detection_required|historical_period_data_preferred_for_multi_period_modes

- confidence_profile: high_consistency
- latency_profile: low
- cost_profile: low

- fallback_eligible: true
- fallback_restrictions: fallback_must_preserve_governed_stress_score_and_severity_schema
- parallelizable: true

- determinism_level: deterministic
- explainability_level: high
- auditability_support: true

- provider_governance_classification: governed_current_option
- provider_runtime_status: runtime_unknown
- version: v1

- notes: baseline stress engine for governed stress scoring, severity bands, and escalation support

---

### FM-CPM-016

- capability_id: financial_stress_detection
- provider_id: hybrid_signal_enriched_stress_engine_v1
- provider_type: hybrid

- supported_outcome_intents: detect_financial_risk|assess_financial_obligation_pressure
- coverage_level: specialised
- strengths: better_multi_signal_interpretation|improved_complex_pattern_detection|useful_for_advanced_risk_decomposition
- limitations: higher_cost|lower_determinism|requires_strict_output_normalization_and_trace_controls

- supported_ocr_feature_classes: none
- required_input_conditions: cash_flow_classification_required|debt_detection_required|historical_period_data_required_for_best_results|governed_signal_mapping_required

- confidence_profile: context_sensitive
- latency_profile: medium
- cost_profile: medium

- fallback_eligible: true
- fallback_restrictions: must_not_emit_uncontrolled_risk_labels_or_unmapped_score_components
- parallelizable: true

- determinism_level: semi_deterministic
- explainability_level: medium
- auditability_support: true

- provider_governance_classification: proposed_roadmap_candidate
- provider_runtime_status: runtime_unknown
- version: v1

- notes: enrichment option for harder stress and overload interpretation; baseline remains rules-first

---

### FM-CPM-017

- capability_id: document_proof_generation
- provider_id: internal_proof_compiler_v1
- provider_type: internal

- supported_outcome_intents: generate_proof
- coverage_level: full
- strengths: high_auditability|strong_provenance_control|stable_output_schema|good_for_document_linkage
- limitations: depends_on_governed_source_references|limited_if_upstream_trace_is_incomplete|not_a_document_authenticity_engine_by_itself

- supported_ocr_feature_classes: text|tables|metadata
- required_input_conditions: parsed_transactions_required|source_document_reference_required|transaction_reference_required|governed_trace_inputs_required

- confidence_profile: high_consistency
- latency_profile: low
- cost_profile: low

- fallback_eligible: false
- fallback_restrictions: no_safe_fallback_without_preserving_document_linkage_and_provenance_contract
- parallelizable: true

- determinism_level: deterministic
- explainability_level: high
- auditability_support: true

- provider_governance_classification: governed_current_option
- provider_runtime_status: runtime_unknown
- version: v1

- notes: baseline proof generation provider for proof objects, references, and provenance-linked outputs

---

### FM-CPM-018

- capability_id: translation
- provider_id: external_translation_service_v1
- provider_type: external_api

- supported_outcome_intents: explain_document|generate_proof
- coverage_level: specialised
- strengths: multilingual_support|faster_time_to_value|useful_for_scale_outside_single_language_baseline
- limitations: external_dependency|higher_cost_than_no_translation|translation_quality_and_structure_preservation_must_be_governed

- supported_ocr_feature_classes: text|metadata
- required_input_conditions: source_text_required|language_detection_required_or_language_known|governed_translation_schema_required

- confidence_profile: variable
- latency_profile: medium
- cost_profile: medium

- fallback_eligible: true
- fallback_restrictions: must_not_break_required_section_structure|must_not_override_source_traceability|fallback_only_when_translation_permitted_by_plan
- parallelizable: true

- determinism_level: probabilistic
- explainability_level: medium
- auditability_support: true

- provider_governance_classification: governed_current_option
- provider_runtime_status: runtime_unknown
- version: v1

- notes: optional scale capability for multilingual operation; not required for single-language baseline delivery

---

### FM-CPM-019

- capability_id: merchant_enrichment
- provider_id: internal_merchant_resolver_v1
- provider_type: internal

- supported_outcome_intents: analyse_spending_patterns|compare_against_reference
- coverage_level: partial
- strengths: low_cost|high_control_over_normalized_names|good_for_known_merchant_patterns
- limitations: partial_coverage|weaker_on_long_tail_entities|depends_on_description_quality

- supported_ocr_feature_classes: text|metadata
- required_input_conditions: parsed_transactions_required|transaction_descriptions_required|governed_merchant_mapping_dictionary_required

- confidence_profile: high_consistency
- latency_profile: low
- cost_profile: low

- fallback_eligible: true
- fallback_restrictions: fallback_must_preserve_governed_merchant_identity_schema
- parallelizable: true

- determinism_level: deterministic
- explainability_level: high
- auditability_support: true

- provider_governance_classification: governed_current_option
- provider_runtime_status: runtime_unknown
- version: v1

- notes: baseline merchant/entity resolution for spending breakdown and merchant-aware classification support

---

### FM-CPM-020

- capability_id: merchant_enrichment
- provider_id: external_merchant_enrichment_service_v1
- provider_type: external_api

- supported_outcome_intents: analyse_spending_patterns|compare_against_reference
- coverage_level: specialised
- strengths: broader_entity_coverage|better_on_long_tail_merchants|useful_for_richer_merchant_breakdown
- limitations: external_dependency|higher_cost|requires_governed_normalization_before_use

- supported_ocr_feature_classes: text|metadata
- required_input_conditions: parsed_transactions_required|transaction_descriptions_required|governed_external_mapping_contract_required

- confidence_profile: variable
- latency_profile: medium
- cost_profile: medium

- fallback_eligible: true
- fallback_restrictions: must_not_emit_unmapped_external_labels|must_not_bypass_governed_name_normalization
- parallelizable: true

- determinism_level: semi_deterministic
- explainability_level: medium
- auditability_support: true

- provider_governance_classification: proposed_roadmap_candidate
- provider_runtime_status: runtime_unknown
- version: v1

- notes: enrichment option for broader merchant/entity coverage where internal resolver coverage is insufficient

---

## End of Document
