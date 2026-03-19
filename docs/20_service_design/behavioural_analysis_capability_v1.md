# Behavioural Analysis Capability v1

## Purpose
Analyse customer financial behaviour patterns from transactions to support insights on spending habits, savings, recurring patterns, and deviations.

---

## Inputs

Field | Description | Source
------|-------------|--------
transaction_amount | Signed transaction amount | Transaction parsing
transaction_type | Debit or credit | Transaction parsing
primary_category | Category classification | Category classification
secondary_category | Optional sub-category | Category classification
cash_flow_type | Cash flow classification | Cash Flow Classification
historical_transactions | Past transactions | Data store
account_context | Account type, profile, and limits | Metadata

---

## Processing Logic

- Analyse frequency of spending per category
- Identify recurring transactions and habitual patterns
- Detect anomalies or deviations from normal behaviour
- Compute ratios such as:
  - savings to income
  - discretionary spend to total spend
  - debt repayment ratio
- Apply optional model-based enrichment for predictive insights

---

## Outputs

Example output structure:

{
  "behavioural_metrics": [
    {
      "metric_name": "savings_ratio",
      "value": 0.15,
      "confidence": 0.92
    },
    {
      "metric_name": "recurring_payment_consistency",
      "value": 0.98,
      "confidence": 0.95
    }
  ],
  "metadata": {
    "period_start": "YYYY-MM-DD",
    "period_end": "YYYY-MM-DD",
    "transactions_analyzed": 120
  }
}

---

## Failure Modes

- Insufficient historical data
- Misclassification of transactions
- Anomalies misinterpreted due to seasonal effects
- Data gaps due to missing statements

---

## Dependencies

- Transaction parsing
- Category classification
- Cash flow classification
- Historical account data

---

## Cost Consideration

- Medium compute
- Optional model-based enrichment may increase compute and storage requirements
- No external API required in baseline

---

## Why this capability is critical

- Enables insight into spending and saving habits
- Supports lending and affordability evaluation
- Provides foundation for trend detection and advisory services
