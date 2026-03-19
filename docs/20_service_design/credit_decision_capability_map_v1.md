# Credit / Trade Credit Decision — Capability Map v1

## Purpose

Defines technical capabilities required to deliver the Credit / Trade Credit Decision services.

Sits between:
- Service design (what we promise)
- Decision engine (what to call when)
- OCR payload and auxiliary data (what is required to generate credit decisions)

---

## Capability Categories

### 1. OCR & Extraction
| Capability | Source | Build vs Buy | Notes |
|------------|--------|-------------|------|
| OCR text extraction | Textract / Google / Azure | Buy | Multi-engine routing |
| Table extraction | OCR engine / custom | Hybrid | Transaction extraction |
| Layout understanding | OCR engine | Buy | Needed for structured statements |

### 2. Normalisation & Structuring
| Capability | Build vs Buy | Notes |
|------------|-------------|------|
| Transaction parsing | Build | Loan, repayment, and inflows/outflows |
| Date normalisation | Build | Multi-format support |
| Amount normalisation | Build | Signed amounts, currencies |
| Account identification | Build | Multi-account handling |

### 3. Classification & Risk
| Capability | Build vs Buy | Notes |
|------------|-------------|------|
| Transaction category classification | Build/Model | Spending categories |
| Debt / Repayment detection | Build/Model | Loan, credit facility, repayments |
| Fraud detection | Model | Transaction integrity, manipulation probability |
| Affordability classification | Model | Ability to service loans |
| Deposit & income stability | Model | Income frequency and consistency |

### 4. Analytics & Decisioning
| Capability | Build vs Buy | Notes |
|------------|-------------|------|
| Risk scoring | Model | Probability to pay |
| Fraud scoring | Model | Likelihood of staged transactions |
| Collections timing optimisation | Build/Model | Probability of recovery by date |
| Trend and historical analysis | Build | Payment and credit history patterns |

### 5. Explanation & Reporting
| Capability | Build vs Buy | Notes |
|------------|-------------|------|
| Customer-facing summaries | Build/Model | Affordability, repayment schedules |
| Internal audit trace | Build | Decision engine reasoning, flags |
| Regulatory reports | Build | NCA / compliance requirements |

### Key Principles
- Multiple models per function (no single classifier)
- Decision engine orchestrates capabilities at runtime
- OCR is a supplier, not the system
- All capabilities declare: input schema, output schema, confidence, cost

