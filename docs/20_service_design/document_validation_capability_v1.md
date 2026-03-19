# FICA Service — Document Validation Capability v1

## Purpose
Detects tampering, ensures authenticity, and verifies document integrity. This is foundational for FICA compliance.

---

## Inputs

| Field | Description | Source |
|-------|-------------|--------|
| raw_text | Full OCR text | OCR engine |
| logos | Document logos | OCR engine |
| layout_metadata | Page layout info | OCR engine |
| font_info | Detected fonts | OCR engine |
| colors | Document colors | OCR engine |
| issue_date | Document issue date | OCR engine/metadata |
| issuer_name | Name of issuing institution | OCR engine/metadata |
| document_type | Type of document | Classification model |

---

## Processing Logic

- Check for:
  - Font inconsistencies
  - Logo placement and authenticity
  - Altered spacing or misalignments
  - Multi-layered edits or stamps
  - Issue date anomalies
- Combine these checks into a **document validity score**.
- Flag high-risk documents for manual review.

---

## Outputs

{
  "validity": "valid|invalid|suspicious",
  "issues_detected": [
    "logo_mismatch",
    "altered_text",
    "layout_anomaly",
    "duplicate_stamp"
  ],
  "confidence": 0.93
}

---

## Failure Modes

- OCR fails to extract content
- Non-standard document formats
- Poor scan quality
- Malformed metadata

---

## Dependencies

- OCR engine output
- Classification models for document type
- Metadata extraction

---

## Cost Consideration

- Low for rule-based validation
- Medium if model-based anomaly detection invoked

