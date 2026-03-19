# Credit / Trade Credit Decision — Payloads v1

## Purpose
Define input and output payloads for the Credit / Trade Credit Decision service to ensure consistent communication between OCR, models, and decision engine.

---

## Input Payload (to OCR / Parsing Layer)

{
  "manifest_id": "string",
  "document_id": "string",
  "source_uri": "s3://bucket/key",
  "document_type": "bank_statement|invoice|ledger",
  "expected_document_type": "string",
  "requested_services": {
    "ocr": true,
    "transaction_parsing": true,
    "fraud_check": true,
    "affordability_analysis": true,
    "risk_scoring": true
  },
  "service_status": {
    "ocr": "pending|requested|running|succeeded|failed",
    "transaction_parsing": "pending|requested|running|succeeded|failed",
    "fraud_check": "pending|requested|running|succeeded|failed",
    "affordability_analysis": "pending|requested|running|succeeded|failed",
    "risk_scoring": "pending|requested|running|succeeded|failed"
  },
  "execution_state": {
    "current_stage": "manifest_generation|preprocessing|ocr|parsing|fraud_check|affordability|risk|reporting",
    "completed_stages": [],
    "failed_stages": [],
    "skipped_stages": []
  },
  "metadata": {
    "issuer_name": "string",
    "account_holder_name": "string",
    "account_number": "string",
    "document_period_start": "YYYY-MM-DD",
    "document_period_end": "YYYY-MM-DD",
    "document_date": "YYYY-MM-DD"
  }
}

---

## Output Payload (from OCR / Parsing to Decision Engine)

{
  "manifest_id": "string",
  "document_id": "string",
  "parsed_transactions": [
    {
      "transaction_id": "string",
      "date": "YYYY-MM-DD",
      "description": "string",
      "amount": 0.0,
      "type": "debit|credit",
      "balance": 0.0,
      "primary_category": "string",
      "secondary_category": "string",
      "confidence": 0.95
    }
  ],
  "fraud_assessment": {
    "fraud_score": 0.0,
    "issues_detected": ["staged_transactions", "duplicate_document", "issuer_mismatch"]
  },
  "affordability_analysis": {
    "monthly_income": 0.0,
    "fixed_expenses": 0.0,
    "discretionary_expenses": 0.0,
    "available_to_pay": 0.0,
    "recommendation": "amount|restructure|manual_review"
  },
  "risk_scoring": {
    "probability_to_pay": 0.0,
    "risk_level": "low|medium|high"
  },
  "reporting": {
    "decision_summary": "Approved|Declined|Manual Review",
    "decision_details": "string"
  },
  "execution_state": {
    "current_stage": "string",
    "completed_stages": [],
    "failed_stages": [],
    "skipped_stages": []
  },
  "processing_timestamp": "YYYY-MM-DDTHH:MM:SS.sssZ"
}

