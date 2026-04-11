# Services Data Architecture Master v1

## 1. Purpose
This document consolidates all approved System B design into a single governed authority.

It acts as the top-level reference for:
- service scope
- data model
- OLTP architecture
- mapping and aggregates
- schema intent
- design principles

---

## 2. System Boundary

### System B (Services Application)
Owns:
- user journeys
- request lifecycle
- service configuration
- audit and support
- OLTP persistence

### System A (OCR Platform)
Owns:
- execution plan
- manifest
- OCR runtime
- pipeline state

Boundary rule:
System B references System A only (no duplication).

---

## 3. Design Principles

- Append-only history (mandatory)
- Versioned entities (mandatory)
- Full reconstructability (mandatory)
- Flexible evolution (mandatory)
- OLTP-first (mandatory)
- Support/admin queryability (mandatory)
- Clean System A/B boundary (mandatory)

---

## 4. Logical Model Summary

Core entities:
- Request (aggregate root)
- User / Tenant / Membership
- Service Definition + Config Version
- Documents / Bundles
- Parties
- Consent / Declaration / Authorization
- Journey / Attempts / Decisions
- Result / Notification
- Support / Admin
- Audit / Events / Telemetry
- Integration Correlation

---

## 5. Architecture Pattern

Selected:
👉 Hybrid OLTP

Components:
- Relational Core → structured state
- Event Store → append-only history
- Projections → current state
- Integration refs → System A linkage

---

## 6. Aggregate Model

Primary:
- Request aggregate

Supporting:
- Journey aggregate
- Event/audit aggregate
- Support/admin aggregate
- Result aggregate

---

## 7. Write Model

- Event-first
- Append-only event store
- State updated after event
- Snapshots at key checkpoints

---

## 8. Read Model

- OLTP queries → relational core
- audit/reconstruction → event store
- reporting → projections / future lakehouse

---

## 9. Physical Design Intent

- UUID keys
- request_id central
- tenant_id enforced
- JSON only for flexible attributes
- strict separation:
  - state vs history

---

## 10. What This Enables

- full journey replay
- audit compliance
- resumable workflows
- service evolution
- continuous improvement

---

## 11. Out of Scope

- DDL
- migrations
- infra implementation

---

## 12. Authority Structure

Primary authority:
- services_data_architecture_master_v1.md

Supporting:
- services_oltp_data_architecture_v1.md

---

## 13. Next Steps

Next:
- DDL + migration definition

