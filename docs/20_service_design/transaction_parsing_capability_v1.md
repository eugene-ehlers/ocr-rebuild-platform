# Transaction Parsing Capability v1

## Purpose
Parse raw OCR output (text and tables) into structured transaction objects for downstream financial services.

This capability converts unstructured document data into a consistent schema, enabling classification, cash flow analysis, debt detection, and reporting.

---

## Inputs

Field | Description | Source
------|-------------|--------
raw_text | OCR extracted text from document | OCR engine
tables | Extracted tables with positional coordinates | OCR engine
document_type | Type of statement/document | Classification
layout_metadata | Page layout, headers, and footers | OCR / Preprocessing
historical_transactions | Prior period transactions for reconciliation | Data store (optional)

---

## Processing Logic

1. Identify transaction table regions using layout hints and patterns.
2. Extract rows and columns into structured objects.
3. Parse and normalise:
   - Transaction date (YYYY-MM-DD)
   - Transaction narration / description
   - Debit or credit indicator
   - Transaction amount (signed)
   - Running balance where available
4. Handle edge cases:
   - Multi-line descriptions
   - Missing or inconsistent headers
   - Split or merged rows
   - Issuer-specific layouts
5. Generate confidence scores per row and field.
6. Produce structured JSON per page/document.

---

## Outputs

Example output structure:

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
    "parsing_confidence": 0.92
  }
}

---

## Failure Modes

- Table not detected
- Misaligned columns
- OCR errors in amounts or dates
- Missing rows or split descriptions
- Conflicting running balances

---

## Dependencies

- OCR output quality
- Table extraction accuracy
- Statement type / layout recognition

---

## Cost Consideration

- Low compute for baseline rules-first parsing
- Higher if multi-pattern or model-based extraction invoked
- Optional external API cost if validation needed

---

## Why this capability is critical

- Foundational for:
  - Transaction category classification
  - Cash flow analysis
  - Debt and affordability evaluation
  - Benchmarking
  - Customer and internal reporting
- Downstream services rely on accuracy and completeness of parsed transactions.

