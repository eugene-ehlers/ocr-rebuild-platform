# FICA Compliance Service — Payloads v1

## Purpose
Defines the input/output payloads required to execute the FICA Compliance Service. 
Ensures all Lambda functions, APIs, and the decision engine communicate reliably.

---

## Input Payload Structure

{
  "manifest_id": "string",
  "document_id": "string",
  "source_uri": "s3://bucket/key",
  "document_type": "string",
  "expected_document_type": "string",
  "requested_services": {
    "document_validation": true,
    "identity_verification": true,
    "transaction_compliance": true
  },
  "service_status": {
    "document_validation": "pending|requested|running|succeeded|failed",
    "identity_verification": "pending|requested|running|succeeded|failed",
    "transaction_compliance": "pending|requested|running|succeeded|failed"
  },
  "execution_state": {
    "current_stage": "manifest_generation|preprocessing|fic_checks|gate_evaluation",
    "completed_stages": [],
    "failed_stages": [],
    "skipped_stages": []
  },
  "pages": [
    {
      "page_number": 1,
      "text": "string",
      "tables": [],
      "logos": [],
      "confidence_score": 0.0
    }
  ],
  "evaluation": {
    "document_validity": "high|medium|low",
    "identity_match": "high|medium|low",
    "transaction_compliance": "high|medium|low"
  },
  "errors": [],
  "processing_timestamp": "YYYY-MM-DDTHH:MM:SSZ"
}

---

## Output Payload Structure

{
  "document_validation": {
    "validity": "valid|invalid|suspicious",
    "issues": ["missing_logo", "altered_text", "misaligned_columns"]
  },
  "identity_verification": {
    "match_status": "verified|unverified|manual_review",
    "confidence_score": 0.95,
    "details": {
      "account_holder_name": "string",
      "issuer_name": "string",
      "issuer_address": "string"
    }
  },
  "transaction_compliance": {
    "compliant": true,
    "issues": ["missing_declaration", "incorrect_amount", "unverified_transaction"],
    "metrics": {
      "total_transactions": 100,
      "non_compliant_transactions": 2
    }
  },
  "metadata": {
    "processing_time_seconds": 0,
    "pipeline_version": "v1"
  }
}

---

## Notes

- All stages must track status in `service_status`.
- Decision engine reads `execution_state` to determine next steps.
- OCR output is required; document-level validation may flag discrepancies.
- Confidence levels guide automated approvals vs manual review.
- Input and output schemas must be strictly followed by all services and Lambda functions.
- Future capabilities can add optional fields but must maintain backward compatibility.

