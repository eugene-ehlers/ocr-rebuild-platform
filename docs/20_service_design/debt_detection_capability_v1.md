# Debt / Indebtedness Detection Capability v1

## Purpose
Identify all debt-related transactions, repayment schedules, and outstanding obligations to enable risk scoring, credit evaluation, and affordability assessment.

---

## Inputs

Field | Description | Source
------|-------------|--------
transaction_amount | Signed transaction amount | Transaction parsing
transaction_type | Debit or credit | Transaction parsing
primary_category | Category classification | Category classification
secondary_category | Optional sub-category | Category classification
cash_flow_type | Cash flow classification | Cash Flow Classification
account_context | Account type, profile, and limits | Metadata
historical_transactions | Prior debt-related transactions | Data store

---

## Processing Logic

- Detect loans, credit facilities, and repayment obligations
- Calculate outstanding balances per facility
- Identify overdue or missed payments
- Track repayment schedules and obligations
- Determine repayment trends (on-time, late, default risk)
- Use rules-based first pass; optional model-based enrichment for complex cases

---

## Outputs

Example output structure:

{
  "debt_positions": [
    {
      "debt_id": "string",
      "outstanding_balance": 2000.00,
      "monthly_repayment": 500.00,
      "due_date": "YYYY-MM-DD",
      "risk_flag": "low|medium|high",
      "confidence": 0.92
    }
  ],
  "metadata": {
    "total_debt_accounts": 3,
    "total_outstanding_balance": 15000.00,
    "average_risk": "medium"
  }
}

---

## Failure Modes

- Misidentification of debt vs non-debt transactions
- Missing historical transaction data
- Ambiguous repayment patterns

---

## Dependencies

- Transaction parsing
- Category classification
- Cash flow classification
- Historical account data

---

## Cost Consideration

- Medium compute if model-based enrichment used
- Optional external API cost for credit bureau validation

---

## Why this capability is critical

- Core to credit evaluation, affordability assessment, and financial stress detection
- Provides structured inputs for downstream services in the Financial Management menu
