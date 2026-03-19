# FICA Compliance — Capability Map v1

## Purpose
This document defines the **technical capabilities** required to deliver FICA compliance checks on financial statements.

It sits between:
- Service design (what we promise)
- Decision engine (what to call when)
- OCR payload design (what data must exist)

---

## Capability Categories

### 1. Document Validation

| Capability | Build vs Buy | Notes |
|-----------|-------------|------|
| Document authenticity verification | Build | Check logos, fonts, colors, spacing, tampering |
| Metadata verification | Build | Date created, document type, issuer info |

### 2. Identity & Owner Verification

| Capability | Build vs Buy | Notes |
|-----------|-------------|------|
| Name & address verification | Build/API | Verify account holder matches statement |
| Account holder context | Build | For multiple accounts or joint accounts |
| Historical document cross-check | Build | Compare previous statements for consistency |

### 3. Transaction-Level Compliance

| Capability | Build vs Buy | Notes |
|-----------|-------------|------|
| Transaction verification | Build/Model | Fraud detection / staged transactions |
| Consistency with account | Build | Compare with other documents for anomalies |
| FICA rules check | Build | Check for completeness against regulations |

### 4. Scoring & Decision Support

| Capability | Build vs Buy | Notes |
|-----------|-------------|------|
| Fraud score | Model | Probability of staged or manipulated data |
| Compliance score | Model | Probability document meets FICA standards |
| Affordability check | Model | Supports risk-based decisions |

---

## Key Design Principles

- Multiple models per function (NOT single classifier)
- Decision engine chooses capability at runtime
- OCR is ONLY a supplier, not the system
- All capabilities must declare:
  - input schema
  - output schema
  - confidence
  - cost

