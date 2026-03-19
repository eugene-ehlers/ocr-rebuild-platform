# Transaction Parsing Capability — v1

## Purpose
Parse raw statement text and tables into structured transaction objects to feed downstream Financial Management capabilities. This is foundational for all other analysis and classification layers.

## Inputs

Field | Description | Source
------|------------|--------
raw_text | OCR extracted text from statement pages | OCR engine
tables | Extracted tables with positional metadata | Table Extraction
layout_metadata | Page structure hints (rows, columns, headers) | OCR / Preprocessing
document_type | Statement type (bank, credit card, utility, etc.) | Classification / Preprocessing

## Processing Logic

- Detect table and transaction regions in statement.
- Extract rows and cells into structured transaction objects.
- Identify transaction attributes:
  - Date
  - Narration / description
  - Debit / credit indicator
  - Transaction amount
  - Running balance (if present)
- Handle:
  - Multi-line descriptions
  - Missing or ambiguous headers
  - Issuer-specific statement layouts
- Apply normalization:
  - Dates into ISO 8601 format
  - Amounts into signed numeric values
  - Multi-currency handling if required

## Outputs

Example JSON output:

{
  "transactions": [
    {
      "transaction_id": "string",
      "date": "YYYY-MM-DD",
      "description": "string",
      "amount": -100.00,
      "type": "debit|credit",
      "balance": 1000.00,
      "confidence": 0.95
    }
  ],
  "metadata": {
    "total_transactions": 120,
    "parsing_confidence": 0.92,
    "document_id": "string",
    "source_uri": "s3://bucket/key"
  }
}

## Failure Modes

- Table region not detected
- Misaligned columns
- OCR errors in critical fields (amount, date)
- Missing or malformed transaction dates
- Multi-line descriptions split incorrectly
- Opening or closing balances misinterpreted as transactions

## Dependencies

- OCR output quality
- Table extraction accuracy
- Layout hints / issuer recognition
- Optional historical transaction context for consistency checks

## Cost Consideration

- Low compute cost for rules-based parsing
- Optional model-based enrichment may increase compute
- No external APIs required in baseline design

## Why this capability is critical

- Serves as the foundation for all downstream capabilities:
  - Transaction category classification
  - Cash flow analysis
  - Spending analysis
  - Debt / indebtedness analysis
  - Benchmarking
  - Explanation and reporting layers
- Incorrect parsing propagates errors throughout the Financial Management service.

