# Credit / Trade Credit Decision — Payloads v1

## Purpose

Defines the structure of data exchanged between services, OCR, decision engine, and downstream systems.

---

### Example Payload Structure

{
  "manifest_id": "string",
  "document_id": "string",
  "source_uri": "s3://bucket/key",
  "document_type": "string",
  "account_holder": {
      "name": "string",
      "id_number": "string",
      "address": "string"
  },
  "transactions": [
    {
      "date": "YYYY-MM-DD",
      "description": "string",
      "amount": -100.00,
      "type": "debit|credit",
      "category": "string",
      "confidence": 0.95
    }
  ],
  "risk_scores": {
      "fraud_score": 0.0,
      "payment_probability": 0.0,
      "affordability_score": 0.0
  },
  "service_status": {
      "transaction_parsing": "pending|succeeded|failed",
      "classification": "pending|succeeded|failed",
      "risk_scoring": "pending|succeeded|failed"
  },
  "evaluation": {},
  "errors": [],
  "processing_timestamp": "YYYY-MM-DDTHH:MM:SS.sssZ"
}

