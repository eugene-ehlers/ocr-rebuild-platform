# FICA Service — Identity & Owner Verification Capability v1

## Purpose
Ensures the document belongs to the claimed owner and matches issuer records. Core for KYC/FICA compliance.

---

## Inputs

| Field | Description | Source |
|-------|-------------|--------|
| account_holder_name | Extracted from document | OCR engine |
| account_number | Extracted from document | OCR engine |
| issuer_name | Name of issuing institution | OCR engine |
| issuer_address | Address of institution | OCR engine |
| customer_metadata | Known customer info | Internal DB |
| prior_verified_docs | Historical verification | Internal DB |

---

## Processing Logic

- Match account holder to known customer records
- Verify issuer identity via reference data or API
- Detect discrepancies in names, addresses, and account numbers
- Assign confidence scores for automatic approval
- Route uncertain cases to manual review

---

## Outputs

{
  "match_status": "verified|unverified|manual_review",
  "confidence_score": 0.95,
  "details": {
    "account_holder_name": "string",
    "issuer_name": "string",
    "issuer_address": "string",
    "verification_notes": ["name_mismatch","address_mismatch"]
  }
}

---

## Failure Modes

- Missing OCR data
- Ambiguous customer records
- Inconsistent issuer metadata

---

## Dependencies

- OCR engine
- Internal customer database
- Issuer reference data

---

## Cost Consideration

- Low if rule-based checks only
- Medium if external verification API is invoked

EOFcat > docs/20_service_design/transaction_compliance_capability_v1.md << 'EOF'
# FICA Service — Transaction Compliance Capability v1

## Purpose
Evaluates all transactions for regulatory compliance, anti-money laundering, and FICA rules.

---

## Inputs

| Field | Description | Source |
|-------|-------------|--------|
| transactions | Parsed transactions | Transaction parsing |
| category_classification | Transaction categories | Classification capability |
| cash_flow_classification | Flow types | Cash flow capability |
| document_validity_score | Validity confidence | Document Validation capability |
| identity_verification_status | Owner verification | Identity Verification capability |

---

## Processing Logic

- Flag unusual transactions based on:
  - Transaction type
  - Amount thresholds
  - Frequency and pattern
- Compare transactions to:
  - Historical transactions
  - Customer risk profile
  - Regulatory limits
- Produce FICA compliance score per transaction
- Aggregate results into document-level compliance rating

---

## Outputs

{
  "compliant": true,
  "issues_detected": [
    "high_value_unverified",
    "suspicious_transfer",
    "missing_declaration"
  ],
  "metrics": {
    "total_transactions": 120,
    "non_compliant_transactions": 3
  },
  "overall_score": 0.92
}

---

## Failure Modes

- Misclassified transactions
- Missing transaction data
- OCR errors propagating from parsing
- Ambiguous identities

---

## Dependencies

- Transaction parsing capability
- Category classification capability
- Cash flow classification capability
- Document Validation
- Identity Verification

---

## Cost Consideration

- Medium compute
- Optional model-based enhancement
- Rule-based baseline for low-cost execution

