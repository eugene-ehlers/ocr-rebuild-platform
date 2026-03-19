# Debt / Indebtedness Detection — Capability v1

## Purpose
Detect debt, repayment schedules, and obligations to support credit evaluation and risk scoring.

## Inputs
- transaction_amount
- transaction_type
- primary_category
- secondary_category
- cash_flow_type
- account_context
- historical_transactions

## Processing Logic
- Identify loans, repayments, credit facilities
- Calculate outstanding balances
- Determine repayment trends and risk flags
- Rules-based first pass; optional model enrichment

## Outputs
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

## Failure Modes
- Misidentification of debt
- Missing historical data
- Ambiguous repayment patterns

## Dependencies
- Transaction parsing
- Category classification
- Cash flow classification

## Cost Consideration
- Medium compute if model enrichment used
- Optional external API for credit bureau validation

## Why this capability is critical
Supports credit evaluation, affordability assessment, and financial stress detection.
