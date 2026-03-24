# Financial Management — Capability Payloads v1

## Purpose

This document defines the input/output payloads for all Financial Management capabilities.  
It ensures the decision engine can orchestrate each capability and produce consistent outputs for internal and customer-facing services.

---

## 1. Transaction Parsing Payloads

### Inputs

| Field | Description | Source |
|-------|-------------|--------|
| raw_text | OCR extracted text | OCR engine |
| tables | Extracted tables | OCR engine |
| document_type | Statement type | Classification |
| layout_metadata | Page structure and layout hints | OCR engine |

### Outputs

| Field | Description |
|-------|------------|
| transactions | List of structured transactions with date, description, amount, type, balance |
| metadata | total_transactions, parsing_confidence |
| errors | List of parsing errors per page or row |

---

## 2. Category Classification Payloads

### Inputs

| Field | Description | Source |
|-------|-------------|--------|
| transaction_date | Normalised transaction date | Transaction parsing |
| transaction_description | Parsed narration | Transaction parsing |
| transaction_amount | Normalised amount | Transaction parsing |
| transaction_type | Debit/Credit | Transaction parsing |
| running_balance | Running balance | Transaction parsing |
| merchant_name | Normalised merchant | Merchant enrichment |
| language_code | Source language | Language detection |
| issuer_context | Bank/template/institution context | Classification |

### Outputs

| Field | Description |
|-------|------------|
| classified_transactions | List of transactions with primary/secondary categories, confidence, classification_method |
| metadata | total_classified, classification_confidence_overall |
| errors | List of classification errors or ambiguities |

---

## 3. Cash Flow Classification Payloads

### Inputs

| Field | Description | Source |
|-------|-------------|--------|
| transaction_id | ID of parsed transaction | Transaction parsing |
| primary_category | From category classification | Category classification |
| secondary_category | From category classification | Category classification |
| transaction_amount | Signed amount | Transaction parsing |
| transaction_type | Debit/Credit | Transaction parsing |
| historical_transactions | Prior period flows | Data store |
| account_context | Account type/profile | Metadata |

### Outputs

| Field | Description |
|-------|------------|
| cash_flow_classification | List of transactions with flow_type, sub_type, recurrence, confidence |
| metadata | income_total, fixed_expense_total, variable_expense_total, discretionary_total |
| errors | Misclassification, recurrence detection failures |

---

## 4. Debt / Indebtedness Detection Payloads

### Inputs

| Field | Description | Source |
|-------|-------------|--------|
| transaction_amount | Signed transaction amount | Transaction parsing |
| transaction_type | Debit/Credit | Transaction parsing |
| primary_category | From classification | Category classification |
| secondary_category | Optional sub-category | Category classification |
| cash_flow_type | From cash flow classification | Cash Flow Classification |
| account_context | Account type/profile | Metadata |
| historical_transactions | Prior debt-related transactions | Data store |

### Outputs

| Field | Description |
|-------|------------|
| debt_positions | List of debt accounts with outstanding balances, repayment schedules, risk_flag, confidence |
| metadata | total_debt_accounts, total_outstanding_balance, average_risk |
| errors | Missing historical data, ambiguous repayment patterns |

---

## 5. Behavioural Analysis Payloads

### Inputs

| Field | Description | Source |
|-------|-------------|--------|
| transactions | All classified transactions | Category classification |
| cash_flow | Cash flow classification | Cash Flow Classification |
| debt_positions | From debt detection | Debt detection |
| account_context | Account metadata | Metadata |

### Outputs

| Field | Description |
|-------|------------|
| behavioural_insights | Spending patterns, risk behaviours, recurring vs discretionary analysis |
| metadata | behaviour_summary |
| errors | Missing or insufficient data |

---

## 6. Benchmarking & Pricing Payloads

### Inputs

| Field | Description | Source |
|-------|-------------|--------|
| transactions | All classified transactions | Category classification |
| cash_flow | Cash flow classification | Cash Flow Classification |
| debt_positions | From debt detection | Debt detection |
| account_context | Account metadata | Metadata |
| external_rates | Pricing, benchmarks | External APIs |

### Outputs

| Field | Description |
|-------|------------|
| population_benchmarks | Relative comparison to peers or population segments |
| pricing_insights | Loan, insurance, or transaction pricing assessment |
| category_spend_comparison | Percentile and deviation analyses |
| errors | External API failures, missing benchmark data |

---

## 7. Reporting & Explanation Payloads

### Inputs

| Field | Description | Source |
|-------|-------------|--------|
| transactions | All transaction data | All prior capabilities |
| cash_flow | Cash flow classification | Cash Flow Classification |
| debt_positions | From debt detection | Debt detection |
| behavioural_insights | Behavioural analysis | Behavioural Analysis |
| benchmarks | Benchmarking & pricing | Benchmarking |

### Outputs

| Field | Description |
|-------|------------|
| customer_report | Summarised statement explanation, cash flow insights, debt summary, spending behaviour |
| internal_report | Confidence scores, audit trail, decision engine trace |
| errors | Missing or inconsistent data, low confidence segments |

---

## 8. Translation & Language Payloads (Optional)

### Inputs

| Field | Description | Source |
|-------|-------------|--------|
| raw_text | OCR text | OCR engine |
| language_code | Detected language | Language detection |

### Outputs

| Field | Description |
|-------|------------|
| translated_text | Translated text for further processing or customer-facing output |
| translation_confidence | Confidence of translation |
| errors | Unsupported language, translation API errors |


---

## 9. Multi-Period Analytical Substrate Contract (Governed)

### 9.1 Purpose

This section is the authoritative field-level contract for governed multi-period analytical substrate tokens referenced by the Financial Management rule tables.

Primary authority rule:
- requirement conditions and sufficiency triggers remain governed by the Financial Management rule tables
- field shape, controlled enum vocabulary, and fail-closed structural contract for the tokens below are governed here

### 9.2 Token-to-Structure Mapping

| Governed token | Authoritative structure in this document | Traceability |
|-------|-------------|--------|
| prior_statement_history | Section 9.4 | FM-OTC-001 conditional_required_internal_data_dependencies: multi_period_scope=>prior_statement_history; FM-OTC-002 conditional_required_internal_data_dependencies: multi_period_scope=>prior_statement_history and conditional_sufficiency_rule: multi_period_scope=>prior_statement_history_required; FM-OTC-003 conditional_required_internal_data_dependencies: comparative_scope=>prior_statement_history and conditional_sufficiency_rule: comparative_scope=>prior_period_data_required; FM-OTC-004 conditional_required_internal_data_dependencies: advanced_obligation_context=>account_context\|prior_statement_history; FM-OTC-006 required_internal_data_dependencies: prior_statement_history\|account_context and conditional_sufficiency_rule: multi_period_scope=>prior_statement_history_required |
| period_groupings | Section 9.5 | FM-OTC-002 required_data_dependencies: parsed_transactions\|classified_transactions\|cash_flow_summary\|period_groupings; FM-OTC-003 required_data_dependencies: parsed_transactions\|classified_transactions\|category_spend_summary\|period_groupings; FM-OTC-010 required_data_dependencies: parsed_transactions\|cash_flow_summary\|timing_features\|period_groupings |
| trend_metrics | Section 9.6 | FM-OTC-002 required_metrics: inflow_outflow_metrics\|trend_metrics; FM-OTC-003 required_metrics: category_spend_metrics\|trend_metrics; FM-OTC-006 required_metrics: trend_metrics\|debt_burden_metrics; FM-IOR-003 required_metrics: inflow_outflow_metrics\|trend_metrics; FM-IOR-004 required_metrics: category_spend_metrics\|trend_metrics; FM-IOR-007 required_metrics: trend_metrics\|debt_burden_metrics |
| missing_period_flags | Section 9.7 | FM-OTC-002 required_flags: missing_period_flags\|exclusion_flags; FM-IOR-003 required_flags: missing_period_flags |
| exclusion_flags | Section 9.8 | FM-OTC-002 required_flags: missing_period_flags\|exclusion_flags |
| multi_period_requirement_signal | Section 9.3 | minimal required extension — not defined in governed docs; required to convert governed condition names such as multi_period_scope, comparative_scope, and advanced_obligation_context into an explicit non-hidden contract signal in line with document_intelligence_operating_baseline.md sections 3.3, 3.5, 3.5S, and 3.5T |

### 9.3 Multi-Period Requirement Signal

This signal is the explicit contract input that states whether multi-period analytical basis is required for the requested outcome.

#### Structure

| Field | Definition | Cardinality | Traceability |
|-------|------------|-------------|--------------|
| multi_period_requirement_signal.scope | Declares the required basis for the requested outcome | required | minimal required extension — not defined in governed docs |
| multi_period_requirement_signal.reason_codes | Lists the governed request or outcome condition that activated the scope | required | minimal required extension — not defined in governed docs |
| multi_period_requirement_signal.fail_closed | Must be true whenever the selected scope requires prior-period basis | required | minimal required extension — not defined in governed docs |

#### Controlled vocabulary — `multi_period_requirement_signal.scope`

| Value | Meaning | Traceability |
|-------|---------|--------------|
| single_period_only | No prior-period basis is required | minimal required extension — not defined in governed docs |
| multi_period_required | More than one statement period is required | aligns to governed condition name `multi_period_scope` used in FM-OTC-001, FM-OTC-002, and FM-OTC-006 |
| comparative_required | Prior-period comparison is required | aligns to governed condition name `comparative_scope` used in FM-OTC-003 and `prior_period_data_required_for_comparison` used in FM-IOR-004 |
| advanced_obligation_context_required | Prior-period obligation context is required | aligns to governed condition name `advanced_obligation_context` used in FM-OTC-004 |

#### Controlled vocabulary — `multi_period_requirement_signal.reason_codes`

| Value | Meaning | Traceability |
|-------|---------|--------------|
| over_multiple_statements | Request explicitly spans multiple statements | governed service menu wording under Statement Explanation customer options: `over multiple statements` |
| rolling_period_view | Request explicitly asks for rolling-period cash-flow view | governed service menu wording under Cash Flow Analysis customer options: `rolling period view` |
| compare_prior_period | Request explicitly asks to compare to prior period | governed service menu wording under Spending Analysis customer options: `compare to prior period`; FM-IOR-004 requested_option_set: category_breakdown\|compare_prior_period\|merchant_breakdown |
| stability_over_time | Request explicitly asks for stability over time | governed service menu wording under Income Analysis customer options: `stability over time` |
| health_tracking_over_time | Request explicitly asks for health tracking over time | governed service menu wording under Service family goals: `trend and health tracking over time` |

### 9.4 `prior_statement_history` Input Contract

`prior_statement_history` is the authoritative reusable input collection for prior statement periods when governed rules require multi-period or comparative basis.

#### Structure

| Field | Definition | Cardinality | Traceability |
|-------|------------|-------------|--------------|
| prior_statement_history.periods | Ordered list of prior statement periods available for governed analysis | required | governed token named in FM-OTC-001, FM-OTC-002, FM-OTC-003, FM-OTC-004, and FM-OTC-006; list structure is minimal required extension — not defined in governed docs |
| prior_statement_history.periods[].period_id | Stable identifier for the prior period record | required | minimal required extension — not defined in governed docs |
| prior_statement_history.periods[].period_start_date | Inclusive start date for the prior period | required | minimal required extension — not defined in governed docs |
| prior_statement_history.periods[].period_end_date | Inclusive end date for the prior period | required | minimal required extension — not defined in governed docs |
| prior_statement_history.periods[].statement_reference | Reference to the source statement or governed internal record | required | minimal required extension — not defined in governed docs |
| prior_statement_history.periods[].parsed_transactions | Parsed transaction substrate for that prior period, when available | optional | aligns to governed reusable substrate artifact `parsed_transactions` named in FM-OTC-002, FM-OTC-003, and FM-OTC-010 |
| prior_statement_history.periods[].classified_transactions | Classified transaction substrate for that prior period, when available | optional | aligns to governed reusable substrate artifact `classified_transactions` named in FM-OTC-002 and FM-OTC-003 |
| prior_statement_history.periods[].cash_flow_summary | Cash-flow substrate for that prior period, when available | optional | aligns to governed reusable substrate artifact `cash_flow_summary` named in FM-OTC-002 and FM-OTC-010 |
| prior_statement_history.periods[].debt_positions | Debt substrate for that prior period, when available | optional | aligns to governed reusable substrate artifact `debt_positions` named in FM-OTC-004 and FM-OTC-006 |
| prior_statement_history.periods[].account_context | Account context for that prior period, when available | optional | aligns to FM-OTC-004 conditional_required_internal_data_dependencies: advanced_obligation_context=>account_context\|prior_statement_history and FM-OTC-006 required_internal_data_dependencies: prior_statement_history\|account_context |

### 9.5 `period_groupings` Output Contract

`period_groupings` is the authoritative structural grouping of current and prior statement periods used by governed multi-period outcomes.

#### Structure

| Field | Definition | Cardinality | Traceability |
|-------|------------|-------------|--------------|
| period_groupings.grouping_basis | Declares the basis on which periods were grouped | required | minimal required extension — not defined in governed docs |
| period_groupings.current_period | Current statement period selected for analysis | required | minimal required extension — not defined in governed docs |
| period_groupings.prior_periods | Ordered list of prior periods included in the grouping | optional | minimal required extension — not defined in governed docs |
| period_groupings.current_period.period_start_date | Inclusive start date of the current period | required | minimal required extension — not defined in governed docs |
| period_groupings.current_period.period_end_date | Inclusive end date of the current period | required | minimal required extension — not defined in governed docs |
| period_groupings.current_period.statement_reference | Source statement or governed internal record for the current period | required | minimal required extension — not defined in governed docs |
| period_groupings.prior_periods[].period_id | Stable identifier for the grouped prior period | required when prior periods are present | minimal required extension — not defined in governed docs |
| period_groupings.prior_periods[].period_start_date | Inclusive start date of the grouped prior period | required when prior periods are present | minimal required extension — not defined in governed docs |
| period_groupings.prior_periods[].period_end_date | Inclusive end date of the grouped prior period | required when prior periods are present | minimal required extension — not defined in governed docs |
| period_groupings.prior_periods[].statement_reference | Source statement or governed internal record for the grouped prior period | required when prior periods are present | minimal required extension — not defined in governed docs |

#### Controlled vocabulary — `period_groupings.grouping_basis`

| Value | Meaning | Traceability |
|-------|---------|--------------|
| statement_period | Grouping is statement-to-statement by governed period boundaries | minimal required extension — not defined in governed docs |

### 9.6 `trend_metrics` Output Contract

`trend_metrics` is the authoritative reusable metric structure for governed multi-period change analysis.

#### Structure

| Field | Definition | Cardinality | Traceability |
|-------|------------|-------------|--------------|
| trend_metrics[] | List of governed trend metric objects | required when trend metrics are required by rule | governed token named in FM-OTC-002, FM-OTC-003, FM-OTC-006, FM-IOR-003, FM-IOR-004, and FM-IOR-007; list structure is minimal required extension — not defined in governed docs |
| trend_metrics[].metric_name | Name of the governed measure being compared | required | minimal required extension — not defined in governed docs |
| trend_metrics[].comparison_basis | Declares how the metric was compared | required | minimal required extension — not defined in governed docs |
| trend_metrics[].current_value | Current-period metric value | required | minimal required extension — not defined in governed docs |
| trend_metrics[].prior_value | Prior-period comparator value | optional | minimal required extension — not defined in governed docs |
| trend_metrics[].absolute_change | Arithmetic difference between current and prior value | optional | minimal required extension — not defined in governed docs |
| trend_metrics[].percent_change | Percent change between current and prior value | optional | minimal required extension — not defined in governed docs |
| trend_metrics[].direction | Normalized direction of change | required | minimal required extension — not defined in governed docs |

#### Controlled vocabulary — `trend_metrics[].comparison_basis`

| Value | Meaning | Traceability |
|-------|---------|--------------|
| current_vs_prior | Current period is compared directly to one prior period | minimal required extension — not defined in governed docs |
| rolling_multi_period | Current interpretation uses more than one prior period in ordered sequence | minimal required extension — not defined in governed docs |

#### Controlled vocabulary — `trend_metrics[].direction`

| Value | Meaning | Traceability |
|-------|---------|--------------|
| increase | Current value is greater than comparator | minimal required extension — not defined in governed docs |
| decrease | Current value is less than comparator | minimal required extension — not defined in governed docs |
| flat | Current value is materially unchanged from comparator | minimal required extension — not defined in governed docs |
| unknown | Direction cannot be established from available governed basis | minimal required extension — not defined in governed docs |

### 9.7 `missing_period_flags` Controlled Vocabulary

| Value | Meaning | Traceability |
|-------|---------|--------------|
| PRIOR_STATEMENT_HISTORY_MISSING | Required prior statement history was not supplied | aligns to FM-OTC-002 conditional_sufficiency_rule: multi_period_scope=>prior_statement_history_required and FM-OTC-006 conditional_sufficiency_rule: multi_period_scope=>prior_statement_history_required |
| PRIOR_PERIOD_COMPARISON_UNAVAILABLE | A requested prior-period comparison cannot be computed from available history | aligns to FM-OTC-003 conditional_sufficiency_rule: comparative_scope=>prior_period_data_required and FM-IOR-004 mandatory_outcome_conditions: prior_period_data_required_for_comparison |
| PERIOD_GROUPING_INCOMPLETE | Current or prior period grouping structure is incomplete | minimal required extension — not defined in governed docs |
| NON_CONTIGUOUS_PERIOD_SEQUENCE | Available periods do not form the sequence required for the requested governed comparison | minimal required extension — not defined in governed docs |

### 9.8 `exclusion_flags` Controlled Vocabulary

| Value | Meaning | Traceability |
|-------|---------|--------------|
| EXCLUDED_INCOMPLETE_PERIOD | A period was excluded because required period dates or statement reference were incomplete | minimal required extension — not defined in governed docs |
| EXCLUDED_UNCOMPARABLE_PERIOD | A period was excluded because it could not support the governed comparison basis | minimal required extension — not defined in governed docs |
| EXCLUDED_MISSING_SUBSTRATE | A period was excluded because required reusable substrate artifacts were missing for that period | minimal required extension — not defined in governed docs |

### 9.9 Fail-Closed Rules

| Rule | Effect | Traceability |
|------|--------|--------------|
| If `multi_period_requirement_signal.scope = multi_period_required` and `prior_statement_history.periods` is absent or empty, the governed outcome must fail closed for missing required prior-period basis. | fail closed | FM-OTC-002 conditional_sufficiency_rule: multi_period_scope=>prior_statement_history_required; FM-OTC-006 conditional_sufficiency_rule: multi_period_scope=>prior_statement_history_required |
| If `multi_period_requirement_signal.scope = comparative_required` and no usable prior period exists, the governed comparison outcome must fail closed and surface `PRIOR_PERIOD_COMPARISON_UNAVAILABLE`. | fail closed | FM-OTC-003 conditional_sufficiency_rule: comparative_scope=>prior_period_data_required; FM-IOR-004 mandatory_outcome_conditions: prior_period_data_required_for_comparison |
| If a rule requires `period_groupings` and the current period block is missing required dates or statement reference, the governed outcome must fail closed. | fail closed | FM-OTC-002 required_data_dependencies: parsed_transactions\|classified_transactions\|cash_flow_summary\|period_groupings; FM-OTC-003 required_data_dependencies: parsed_transactions\|classified_transactions\|category_spend_summary\|period_groupings; FM-OTC-010 required_data_dependencies: parsed_transactions\|cash_flow_summary\|timing_features\|period_groupings |
| If a rule requires `trend_metrics`, `trend_metrics` must not be replaced by prose-only explanation or omitted derived change interpretation. | fail closed | FM-OTC-002 required_metrics: inflow_outflow_metrics\|trend_metrics; FM-OTC-003 required_metrics: category_spend_metrics\|trend_metrics; FM-OTC-006 required_metrics: trend_metrics\|debt_burden_metrics |
| If a period is excluded from multi-period analysis, the exclusion must be explicit in `exclusion_flags`; silent exclusion is prohibited. | fail closed | minimal required extension — not defined in governed docs; aligns to document_intelligence_operating_baseline.md sections 3.3, 3.5, 3.5S, and 3.5T prohibiting hidden decisioning |

