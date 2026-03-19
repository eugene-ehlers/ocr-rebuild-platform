# Transaction Category Classification Capability — v1

## Purpose
Assign each parsed transaction to one or more semantic categories, enabling downstream services to analyse spending, income, indebtedness, pricing, behaviour, and trends.

## Inputs

Field | Description | Source
------|------------|--------
transaction_date | Normalised transaction date | Transaction Parsing
transaction_description | Parsed transaction narration | Transaction Parsing
transaction_amount | Normalised signed amount | Transaction Parsing
transaction_type | Debit or credit indicator | Transaction Parsing
running_balance | Running balance if available | Transaction Parsing
issuer_context | Bank, template, or institution context | Classification / Issuer Recognition
language_code | Language of source text | Language Detection
merchant_name | Normalised merchant name if available | Merchant Enrichment

## Processing Logic

- Classify each transaction into categories such as:
  - Salary / income
  - Groceries
  - Transport
  - Utilities
  - Rent
  - Loan repayment
  - Insurance
  - Transfers
  - Fees and charges
  - Cash withdrawals
  - Entertainment
  - Medical
  - Education
  - Savings / investments
- Support primary and optional secondary categories.
- Assign classification confidence per transaction.
- Use rules-first baseline with optional ML model refinement.
- Apply issuer-, merchant-, and language-aware adjustments.

## Outputs

Example JSON output:

{
  "classified_transactions": [
    {
      "transaction_id": "string",
      "primary_category": "transport",
      "secondary_category": "fuel",
      "classification_confidence": 0.93,
      "classification_method": "rules|model|hybrid"
    }
  ],
  "metadata": {
    "total_classified": 120,
    "classification_confidence_overall": 0.89
  }
}

## Failure Modes

- Transaction description too vague for classification
- Merchant not recognised
- Language ambiguity
- OCR narration errors affecting classification

## Dependencies

- Transaction Parsing capability
- Merchant Enrichment (optional)
- Language Detection capability
- Issuer Recognition (optional)

## Cost Consideration

- Low to medium compute for rules-first approach
- Higher if ML-based enrichment is used
- Optional external API cost for merchant enrichment

## Why this capability is critical

- Foundational for:
  - Spending analysis
  - Income analysis
  - Indebtedness evaluation
  - Pricing and benchmarking
  - Behavioural insights
  - Trend detection
- Multiple classifiers required; a single model is insufficient for all downstream services.

