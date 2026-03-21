# FICA Compliance — Capability to Provider Mapping v1

## Purpose

Defines the set of eligible providers for each FICA Compliance capability and their characteristics.

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

### FICA-CPM-001

- capability_id: document_validation
- provider_id: internal_rules_document_validator_v1
- provider_type: internal

- supported_outcome_intents: validate_document_authenticity|assess_compliance_risk
- coverage_level: full
- strengths: high_explainability|strong_integrity_rule_control|good_for_governed_issue_flags
- limitations: depends_on_visual_feature_quality|weaker_on_nonstandard_documents|limited_on_subtle_complex_tampering

- supported_ocr_feature_classes: text|layout|metadata|logos
- required_input_conditions: raw_document_features_required|governed_integrity_rule_set_required

- confidence_profile: high_consistency
- latency_profile: low
- cost_profile: low

- fallback_eligible: true
- fallback_restrictions: fallback_must_preserve_governed_validity_status_and_issue_schema
- parallelizable: true

- determinism_level: deterministic
- explainability_level: high
- auditability_support: true

- provider_status: approved
- version: v1

- notes: baseline internal validator for logo/layout/metadata/integrity checks

---

### FICA-CPM-002

- capability_id: document_validation
- provider_id: hybrid_visual_anomaly_validator_v1
- provider_type: hybrid

- supported_outcome_intents: validate_document_authenticity|assess_compliance_risk
- coverage_level: specialised
- strengths: better_on_complex_visual_tampering|stronger_on_nonstandard_patterns|useful_for_harder_fraud_cases
- limitations: higher_cost|lower_determinism|requires_strict_issue_normalization

- supported_ocr_feature_classes: text|layout|metadata|logos
- required_input_conditions: raw_document_features_required|governed_visual_anomaly_mapping_required

- confidence_profile: context_sensitive
- latency_profile: medium
- cost_profile: medium

- fallback_eligible: true
- fallback_restrictions: must_not_emit_unmapped_integrity_labels_or_free_text_decisions
- parallelizable: true

- determinism_level: semi_deterministic
- explainability_level: medium
- auditability_support: true

- provider_status: experimental
- version: v1

- notes: enrichment validator for harder anomaly and tamper scenarios

---

### FICA-CPM-003

- capability_id: identity_owner_verification
- provider_id: internal_rules_identity_matcher_v1
- provider_type: internal

- supported_outcome_intents: verify_identity_and_ownership|assess_compliance_risk
- coverage_level: full
- strengths: high_explainability|strong_customer_context_control|good_for_manual_review_triggering
- limitations: depends_on_customer_metadata_quality|issuer_reference_gaps_reduce_coverage|limited_on_ambiguous_identity_variants

- supported_ocr_feature_classes: text|metadata
- required_input_conditions: extracted_identity_fields_required|customer_metadata_required|issuer_fields_required

- confidence_profile: high_consistency
- latency_profile: low
- cost_profile: low

- fallback_eligible: true
- fallback_restrictions: fallback_must_preserve_governed_identity_status_and_discrepancy_schema
- parallelizable: true

- determinism_level: deterministic
- explainability_level: high
- auditability_support: true

- provider_status: approved
- version: v1

- notes: baseline identity and ownership matcher with governed discrepancy outputs

---

### FICA-CPM-004

- capability_id: identity_owner_verification
- provider_id: external_issuer_reference_check_v1
- provider_type: external_api

- supported_outcome_intents: verify_identity_and_ownership|assess_compliance_risk
- coverage_level: partial
- strengths: extends_issuer_reference_coverage|useful_where_internal_reference_data_is_insufficient
- limitations: external_dependency|higher_cost|must_not_override_governed_identity_status_without_normalization

- supported_ocr_feature_classes: text|metadata
- required_input_conditions: issuer_fields_required|governed_external_reference_contract_required

- confidence_profile: variable
- latency_profile: medium
- cost_profile: medium

- fallback_eligible: true
- fallback_restrictions: must_not_bypass_internal_identity_status_logic|must_preserve_governed_discrepancy_mapping
- parallelizable: true

- determinism_level: semi_deterministic
- explainability_level: medium
- auditability_support: true

- provider_status: approved
- version: v1

- notes: external issuer/reference enrichment for broader ownership verification support

---

### FICA-CPM-005

- capability_id: transaction_compliance_evaluation
- provider_id: internal_rules_transaction_compliance_engine_v1
- provider_type: internal

- supported_outcome_intents: evaluate_transaction_compliance|assess_compliance_risk
- coverage_level: full
- strengths: high_explainability|strong_threshold_control|good_for_governed_issue_basis_and_metrics
- limitations: depends_on_upstream_transaction_quality|limited_on_complex_hidden_patterns|history_sensitive_for_pattern_checks

- supported_ocr_feature_classes: text|tables|layout|metadata
- required_input_conditions: parsed_transactions_required|classification_required|cash_flow_classification_required|document_validation_and_identity_status_preferred

- confidence_profile: high_consistency
- latency_profile: low
- cost_profile: low

- fallback_eligible: true
- fallback_restrictions: fallback_must_preserve_governed_compliance_status_issue_and_metric_schema
- parallelizable: true

- determinism_level: deterministic
- explainability_level: high
- auditability_support: true

- provider_status: approved
- version: v1

- notes: baseline transaction compliance engine for thresholds, issue flags, and compliance metrics

---

### FICA-CPM-006

- capability_id: transaction_compliance_evaluation
- provider_id: hybrid_pattern_enriched_compliance_engine_v1
- provider_type: hybrid

- supported_outcome_intents: evaluate_transaction_compliance|assess_compliance_risk
- coverage_level: specialised
- strengths: better_on_suspicious_pattern_detection|better_on_complex_frequency_analysis|useful_for_harder_aml_style_patterns
- limitations: higher_cost|lower_determinism|requires_strict_issue_and_score_normalization

- supported_ocr_feature_classes: text|tables|layout|metadata
- required_input_conditions: parsed_transactions_required|classification_required|cash_flow_classification_required|historical_transaction_data_preferred

- confidence_profile: context_sensitive
- latency_profile: medium
- cost_profile: medium

- fallback_eligible: true
- fallback_restrictions: must_not_emit_unmapped_issue_labels_or_uncontrolled_scores
- parallelizable: true

- determinism_level: semi_deterministic
- explainability_level: medium
- auditability_support: true

- provider_status: experimental
- version: v1

- notes: enrichment engine for harder transaction-pattern compliance analysis

---

### FICA-CPM-007

- capability_id: compliance_risk_scoring
- provider_id: internal_rules_risk_consolidator_v1
- provider_type: internal

- supported_outcome_intents: assess_compliance_risk
- coverage_level: full
- strengths: high_traceability|strong_component_score_control|good_for_consolidated_internal_review_outputs
- limitations: depends_on_component_check_quality|limited_on_complex_nonlinear_signal_interactions

- supported_ocr_feature_classes: none
- required_input_conditions: document_validation_findings_required|identity_verification_findings_required|transaction_compliance_findings_required

- confidence_profile: high_consistency
- latency_profile: low
- cost_profile: low

- fallback_eligible: true
- fallback_restrictions: fallback_must_preserve_governed_component_traceability_and_risk_status_schema
- parallelizable: true

- determinism_level: deterministic
- explainability_level: high
- auditability_support: true

- provider_status: approved
- version: v1

- notes: baseline consolidator for internal compliance-risk assessment and escalation support

---

### FICA-CPM-008

- capability_id: reporting_explanation
- provider_id: internal_compliance_reporter_v1
- provider_type: internal

- supported_outcome_intents: validate_document_authenticity|verify_identity_and_ownership|evaluate_transaction_compliance|assess_compliance_risk
- coverage_level: full
- strengths: high_auditability|strong_schema_control|stable_internal_trace_outputs|good_for_customer_status_projection_from_internal_determinations
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

- notes: governed reporter for internal audit outputs and customer-facing status summaries

---

---

### FICA-CPM-009

- capability_id: metadata_verification
- provider_id: future_metadata_verification_engine_v1
- provider_type: internal

- supported_outcome_intents: validate_document_authenticity|assess_compliance_risk
- coverage_level: specialised
- strengths: placeholder_for_metadata_integrity_checks
- limitations: not_implemented

- supported_ocr_feature_classes: metadata
- required_input_conditions: document_metadata_required

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

- notes: placeholder for metadata verification capability

---

### FICA-CPM-010

- capability_id: document_type_classification
- provider_id: future_document_type_classifier_v1
- provider_type: internal

- supported_outcome_intents: validate_document_authenticity
- coverage_level: specialised
- strengths: placeholder_for_document_type_detection
- limitations: not_implemented

- supported_ocr_feature_classes: text|layout|metadata
- required_input_conditions: document_features_required

- confidence_profile: context_sensitive
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

- notes: placeholder for document type classification capability

---

### FICA-CPM-011

- capability_id: visual_anomaly_detection
- provider_id: future_visual_anomaly_engine_v1
- provider_type: hybrid

- supported_outcome_intents: validate_document_authenticity
- coverage_level: specialised
- strengths: placeholder_for_visual_anomaly_detection
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

- notes: placeholder for visual anomaly detection capability

---

### FICA-CPM-012

- capability_id: template_matching
- provider_id: future_template_matching_engine_v1
- provider_type: internal

- supported_outcome_intents: validate_document_authenticity
- coverage_level: specialised
- strengths: placeholder_for_template_matching
- limitations: not_implemented

- supported_ocr_feature_classes: layout|metadata
- required_input_conditions: template_library_required

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

- notes: placeholder for template matching capability

---

### FICA-CPM-013

- capability_id: historical_document_cross_check
- provider_id: future_document_history_engine_v1
- provider_type: internal

- supported_outcome_intents: verify_identity_and_ownership|assess_compliance_risk
- coverage_level: specialised
- strengths: placeholder_for_document_history_comparison
- limitations: not_implemented

- supported_ocr_feature_classes: metadata
- required_input_conditions: historical_document_store_required

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

- notes: placeholder for historical document cross-check capability

---

### FICA-CPM-014

- capability_id: external_identity_reference_check
- provider_id: future_external_identity_service_v1
- provider_type: external_api

- supported_outcome_intents: verify_identity_and_ownership
- coverage_level: specialised
- strengths: placeholder_for_external_identity_validation
- limitations: not_implemented

- supported_ocr_feature_classes: none
- required_input_conditions: external_reference_contract_required

- confidence_profile: variable
- latency_profile: medium
- cost_profile: high

- fallback_eligible: false
- fallback_restrictions: no_runtime_available
- parallelizable: true

- determinism_level: probabilistic
- explainability_level: medium
- auditability_support: true

- provider_status: fallback_only
- version: v1

- notes: placeholder for external identity reference capability

---

### FICA-CPM-015

- capability_id: historical_pattern_comparison
- provider_id: future_transaction_pattern_engine_v1
- provider_type: internal

- supported_outcome_intents: evaluate_transaction_compliance
- coverage_level: specialised
- strengths: placeholder_for_pattern_comparison
- limitations: not_implemented

- supported_ocr_feature_classes: none
- required_input_conditions: historical_transaction_data_required

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

- notes: placeholder for historical pattern comparison capability

---

### FICA-CPM-016

- capability_id: risk_pattern_enrichment
- provider_id: future_risk_pattern_engine_v1
- provider_type: hybrid

- supported_outcome_intents: evaluate_transaction_compliance
- coverage_level: specialised
- strengths: placeholder_for_risk_pattern_enrichment
- limitations: not_implemented

- supported_ocr_feature_classes: none
- required_input_conditions: transaction_data_required

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

- notes: placeholder for risk pattern enrichment capability

---

### FICA-CPM-017

- capability_id: affordability_support_scoring
- provider_id: future_affordability_support_engine_v1
- provider_type: internal

- supported_outcome_intents: assess_compliance_risk
- coverage_level: specialised
- strengths: placeholder_for_affordability_support
- limitations: not_implemented

- supported_ocr_feature_classes: none
- required_input_conditions: financial_data_required

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

- notes: placeholder for affordability support scoring capability

---

### FICA-CPM-018

- capability_id: advanced_fraud_pattern_enrichment
- provider_id: future_advanced_fraud_engine_v1
- provider_type: hybrid

- supported_outcome_intents: assess_compliance_risk
- coverage_level: specialised
- strengths: placeholder_for_advanced_fraud_detection
- limitations: not_implemented

- supported_ocr_feature_classes: none
- required_input_conditions: transaction_and_identity_data_required

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

- notes: placeholder for advanced fraud pattern enrichment capability

---

### FICA-CPM-019

- capability_id: reporting_explanation
- provider_id: internal_template_reporter_v1
- provider_type: internal

- supported_outcome_intents: assess_compliance_risk|validate_document_authenticity|verify_identity_and_ownership|evaluate_transaction_compliance
- coverage_level: full
- strengths: high_explainability|strong_schema_control|high_auditability
- limitations: depends_on_upstream_data_completeness

- supported_ocr_feature_classes: none
- required_input_conditions: governed_structured_outputs_required

- confidence_profile: high_consistency
- latency_profile: low
- cost_profile: low

- fallback_eligible: true
- fallback_restrictions: must_not_drop_required_trace_or_confidence_sections
- parallelizable: true

- determinism_level: deterministic
- explainability_level: high
- auditability_support: true

- provider_status: approved
- version: v1

- notes: aligned reporting capability reused across services

---

## End of Document
