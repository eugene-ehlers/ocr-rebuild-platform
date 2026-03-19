# Cash Flow Classification Capability v1

## Purpose
Identify and classify each transaction into cash flow types (income, fixed expenses, variable expenses, discretionary, debt-related, savings/investment) to enable financial analysis, affordability calculations, and trend tracking.

---

## Inputs

Field | Description | Source
------|-------------|--------
transaction_amount | Signed transaction amount | Transaction parsing
transaction_type | Debit or credit | Transaction parsing
primary_category | Category classification | Category classification
secondary_category | Optional sub-category | Category classification
historical_transactions | Prior period transactions | Data store
account_context | Account type and profile | Metadata

---

## Processing Logic

- Classify transactions into flow types:
  - income (salary, transfers in)
  - fixed essential expenses (rent, insurance, loan repayments)
  - variable essential expenses (groceries, utilities)
  - discretionary expenses (entertainment, dining)
  - debt-related flows (repayments, new credit)
  - savings and investments
- Determine recurring vs non-recurring flows
- Apply rules based on category + patterns
- Optional model refinement for ambiguous cases
- Aggregate totals per flow type and sub-type

---

## Outputs

Example output structure:

{
  "cash_flow_classification": [
    {
      "transaction_id": "string",
      "flow_type": "fixed_expense",
      "sub_type": "insurance",
      "recurrence": "monthly|irregular",
      "confidence": 0.91
    }
  ],
  "metadata": {
    "income_total": 50000.00,
    "fixed_expense_total": 20000.00,
    "variable_expense_total": 15000.00,
    "discretionary_total": 8000.00
  }
}

---

## Failure Modes

- Misclassification due to poor category input
- Recurrence detection failure due to limited history
- Ambiguous transactions (e.g., transfers between own accounts)

---

## Dependencies

- Transaction parsing
- Transaction category classification
- Historical account data

---

## Cost Consideration

- Low to medium compute
- Mostly rules-based with optional model enhancement
- No external API required in baseline

---

## Why this capability is critical

- Supports affordability calculations, financial health scoring, debt capacity analysis, optimisation recommendations, and lending integration
- Serves as the core bridge between raw transaction data and higher-level financial intelligence
