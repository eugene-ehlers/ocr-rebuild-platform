# FE-6A — Scope, Actors, Journeys, Route & Modular Architecture (Decision Engine Model)

## 1. Core architectural principle

### Frontend ↔ Decision Engine
Frontend interacts ONLY with the decision engine (application-facing API).

The decision engine orchestrates:
- consent
- credits
- payments
- document readiness
- OCR execution
- results
- remediation
- future chat/evidence

Modules behind it can be:
- LIVE
- STUBBED
- DISABLED
- FORCED SCENARIO

---

## 2. Product scope model

### Layer A — Executable now
- landing / visitor entry
- registration + login (lightweight)
- bank statement submission
- basic document readiness guidance
- consent capture (current fields)
- request submission
- processing page
- blocked/remediation handling
- result display
- status check
- retry/resubmit
- support entry

### Layer B — Architecturally in-scope now
- business users + mandates
- credits & payments
- multi-document support (payslip, ID, passport placeholders)
- full consent framework
- reporting
- support workflows
- deeper OCR evidence
- chat-ready architecture

### Layer C — Out of scope
- bureau
- PEP / PIP
- Home Affairs

---

## 3. Actor model

- Visitor
- Individual user
- Business user (mandate-based)
- Subject customer (via customerId)

Frontend must support structure for all, even if not fully active.

---

## 4. Journey model (gate-based)

1. identity/account
2. credits
3. consent
4. document readiness
5. submission
6. processing
7. result
8. remediation
9. support

---

## 5. Core routes

Public:
- /
- /register
- /login

Flow:
- /submit
- /processing/:request_id
- /result/:request_id
- /blocked/:request_id
- /status/:request_id

System:
- /account
- /billing
- /support
- /reports (placeholder)

---

## 6. Page purposes

/submit:
- collect payload
- validate
- call decision engine

/processing:
- transitional state
- fetch status/result

/result:
- show summary result
- future-ready for deeper evidence

/blocked:
- show remediation prompts

/status:
- show backend truth

/account:
- user context + credits placeholder

/billing:
- payment entry point

/support:
- help / escalation

---

## 7. Document readiness (pre-submit)

- validate presence
- basic quality guidance
- enforce minimum before submission

---

## 8. Consent model

- processing consent
- authority consent
- third-party disclosure

Only supported fields sent now, structure supports full model.

---

## 9. Credits model

- balance visibility
- insufficient credits state
- redirect to billing

---

## 10. Result architecture (chat-ready)

Layer 1: summary  
Layer 2: deeper evidence (future)  
Layer 3: entitlement boundary  
Layer 4: chat seam  

---

## 11. Retry model

- manual refresh
- resubmit
- backend rerun only if supported later

---

## 12. Navigation

- flow-based
- minimal
- extensible
- no heavy dashboard yet

---

## Status

FE-6A COMPLETE  
Aligned to:
- FE-5B backend evidence
- modular decision-engine architecture
- future-safe extensibility
