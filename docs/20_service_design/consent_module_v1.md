# Consent Module v1

## 1. Purpose

Handles all consent-related requirements for:

- processing documents
- sharing documents or results

---

## 2. Types of Consent

### 2.1 Processing Consent
Required to:
- ingest documents
- perform OCR
- run analysis

---

### 2.2 Disclosure Consent
Required to:
- share documents
- share results with third parties

---

### 2.3 Standing Consent
- valid for a defined period
- reusable across requests

---

## 3. Capabilities

- capture consent
- validate consent
- revoke consent
- manage expiry
- retrieve proof

---

## 4. Rules

- no processing without processing consent
- no sharing without disclosure consent
- consent must be auditable
- expired consent must block execution

---

## 5. Data Model (Conceptual)

- consent_id
- customer_id
- consent_type
- granted_by
- timestamp
- expiry_date
- status

---

## 6. Integration

Used by:
- document workspace
- request execution
- result sharing
- API layer

