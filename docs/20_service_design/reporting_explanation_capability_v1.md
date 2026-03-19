# Reporting & Explanation — Capability v1

## Purpose
Generate customer-friendly reports and internal explanations from all processed financial data.

## Inputs
- transactions
- classifications
- cash flow
- debt positions
- benchmarking outputs

## Processing Logic
- Generate statement summaries
- Produce plain-language explanations
- Provide internal trace and confidence information
- Highlight anomalies or outliers

## Outputs
{
  "report": {
    "summary": "string",
    "confidence": 0.95,
    "sections": [
      {
        "title": "string",
        "content": "string",
        "confidence": 0.90
      }
    ]
  }
}

## Failure Modes
- Missing upstream data
- Low-confidence classification
- Report generation errors

## Dependencies
- Transaction parsing
- Category classification
- Cash flow
- Debt detection
- Benchmarking

## Cost Consideration
- Low compute
- Optional model refinement for natural language
- Minimal storage for report caching

## Why this capability is critical
Ensures clients understand their financials and supports internal auditing and explanations.
