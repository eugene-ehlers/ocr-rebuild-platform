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

