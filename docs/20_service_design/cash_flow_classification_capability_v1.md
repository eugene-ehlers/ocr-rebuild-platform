# Cash Flow Classification — Capability v1

## Purpose
Classify transactions into financial flow types to enable spending, income, and trend analysis.

## Inputs
- transaction_amount
- transaction_type
- primary_category
- secondary_category
- historical_transactions
- account_context

## Processing Logic
- Identify income, fixed expenses, variable essential, discretionary, debt-related, savings/investments
- Determine recurring vs non-recurring flows
- Apply rules-based logic, optional model refinement

## Outputs
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

## Failure Modes
- Misclassification
- Ambiguous transactions
- Insufficient historical data

## Dependencies
- Transaction parsing
- Category classification

## Cost Consideration
- Low to medium compute
- Mostly rules-based
- Optional model refinement cost

## Why this capability is critical
Enables affordability calculations, health scoring, debt capacity analysis, and optimisation recommendations.
