# Category Classification Capability v1

## Purpose
Assign each parsed transaction to one or more semantic financial categories to enable downstream services like cash flow analysis, indebtedness detection, benchmarking, and reporting.

Multiple classifiers are used; one model is not sufficient.

---

## Inputs

Field | Description | Source
------|-------------|--------
transaction_date | Normalised transaction date | Transaction parsing
transaction_description | Parsed transaction narration | Transaction parsing
transaction_amount | Signed transaction amount | Transaction parsing
transaction_type | Debit or credit indicator | Transaction parsing
running_balance | Running balance where available | Transaction parsing
issuer_context | Bank, template, or institution context | Classification / issuer recognition
merchant_name | Normalised merchant where available | Merchant enrichment
language_code | Language of source text | Language detection

---

## Processing Logic

- Classify each transaction into categories, e.g.:
  - salary or income
  - groceries
  - transport
  - utilities
  - rent
  - loan repayment
  - insurance
  - transfers
  - fees and charges
  - cash withdrawal
  - entertainment
  - medical
  - education
  - savings or investment
- Support:
  - primary category
  - optional secondary category
  - confidence score per classification
- Allow:
  - issuer-specific rules
  - language-aware rules
  - merchant-aware overrides
  - rule-first baseline with optional model refinement

---

## Outputs

Example output structure:

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

---

## Failure Modes

- Vague or ambiguous descriptions
- Merchant not recognised
- Language ambiguity
- OCR quality insufficient

---

## Dependencies

- Transaction parsing
- Merchant enrichment
- Language detection
- Issuer recognition

---

## Cost Consideration

- Low to medium compute for rules-first
- Higher if model-based enrichment used
- External API may incur cost

---

## Why this capability is critical

- Foundational for:
  - Spending analysis
  - Income analysis
  - Debt and affordability analysis
  - Behaviour insights
  - Trend and benchmarking services
