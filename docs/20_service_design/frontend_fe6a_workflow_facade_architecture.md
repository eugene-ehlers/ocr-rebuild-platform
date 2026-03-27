# FE-6A — Workflow-Facade Architecture (Approved)

## 1. Governing architecture

Frontend → Workflow Facade → Application API Layer → Deterministic Decision Services + Capability Modules → Exception Intelligence Service

Frontend interacts ONLY with workflow facade.

---

## 2. Layer definitions

Workflow Facade:
- owns journeys
- stable frontend contract
- hides internal complexity
- supports stub/live modes

API Layer:
- routing
- normalization
- retries
- logging
- security hooks

Decision Services:
- consent
- credits
- fraud triggers
- routing eligibility
- entitlement

Modules:
- OCR
- payments
- consent service
- reporting
- support
- evidence retrieval

Exception Intelligence:
- handles non-standard flows
- chat, support, investigation
- controlled agent usage

---

## 3. Activation model

Modules can be:
- LIVE
- STUBBED
- DISABLED
- FORCED SCENARIO

Frontend must not depend on activation state.

---

## 4. Scope model

Executable now:
- landing
- registration/login
- submission
- consent
- processing
- result
- blocked/remediation
- status
- retry
- support

Architecturally in-scope:
- business users + mandates
- credits/payments
- document expansion
- full consent framework
- reporting
- chat/evidence layer
- fraud/security controls

Out of scope:
- bureau
- PEP/PIP
- Home Affairs

---

## 5. Actor model

- Visitor
- Individual
- Business user
- Subject customer
- Support/reviewer

---

## 6. Journey gates

1. identity
2. mandate
3. credits
4. consent
5. readiness
6. submission
7. processing
8. result
9. remediation
10. support
11. chat/evidence

---

## 7. Routes

/  
/register  
/login  

/submit  
/processing/:request_id  
/result/:request_id  
/blocked/:request_id  
/status/:request_id  

/account  
/billing  
/support  
/reports  

---

## 8. Identifier rule

Frontend uses request_id only.

---

## 9. State model

Backend:
- blocked
- completed
- failed
- result available

UI:
- loading
- submitting
- processing
- refreshing
- retrying

---

## 10. Security & fraud

Handled in:
- workflow facade
- API layer
- decision services

Includes:
- rate limiting
- anomaly detection
- entitlement checks

---

## 11. Result architecture

Layered:
- summary
- evidence
- entitlement
- chat seam

---

## 12. Retry

- refresh
- resubmit
- backend rerun only if supported

---

## Status

APPROVED ARCHITECTURE (FE-6A FINAL)
