# OCR Provider Abstraction Control

Status: CONTROL DOCUMENT — AUTHORITATIVE DESIGN CONSTRAINT

## 1. Purpose

Define the strict control boundary for OCR execution within the OCR Rebuild platform.

This document exists to prevent:
- accidental hard-coding of OCR engine behavior into pipeline logic
- drift from provider-agnostic architecture
- confusion between bootstrap runtime implementation and target design
- uncontrolled direct integration of OCR vendors into unrelated stages

---

## 2. Governing Principle

The platform is not an OCR product implementation.

The platform is a:
- decision-driven orchestration system
- provider-selecting execution controller
- quality and fallback manager
- canonical output assembler

OCR is a capability that must be invoked through a governed provider abstraction boundary.

---

## 3. Hard Rule — No Direct OCR Engine Ownership In Pipeline Logic

No pipeline stage outside the governed OCR provider abstraction layer may:

- hard-code a specific OCR engine as design truth
- assume Tesseract is the permanent OCR implementation
- embed provider-specific routing rules directly into unrelated orchestration logic
- treat current bootstrap OCR code as the architectural target model

The orchestration system may decide which provider to use.

It must not be designed around one provider implementation.

---

## 4. Current Controlled Runtime Position

Current runtime baseline includes a Tesseract-backed OCR implementation.

This is permitted only as:

- a controlled bootstrap execution provider
- a deterministic baseline for integrated runtime validation
- a reference implementation until governed provider abstraction is completed

It must be interpreted as runtime scaffolding, not permanent design truth.

---

## 5. Required End-State

The OCR stage must operate through a provider abstraction model.

At minimum, the design must support:

- selected provider
- provider type
- execution mode
- fallback permission
- fallback provider(s)
- provider decision reason
- normalized provider output contract

Provider choice must be controlled through governed runtime instructions, not hidden code paths.

---

## 6. Execution Plan Control Requirement

OCR provider selection must be driven by the governed execution plan.

The execution plan must become the authoritative control object for:

- OCR provider selection
- fallback routing
- provider switching decisions
- quality-triggered escalation paths

No hidden provider decision may exist outside the governed execution plan.

---

## 7. Interface Control Requirement

A governed OCR provider interface must exist between orchestration and provider implementation.

That interface must normalize:

- input contract
- output contract
- error contract
- provider metadata
- confidence / quality metadata

All OCR providers must conform to that interface before they are treated as valid runtime providers.

---

## 8. Tesseract Control Boundary

Tesseract is currently allowed only under these constraints:

- as a reference execution provider
- as a bootstrap validation engine
- as a provider implementation behind the abstraction boundary
- not as the architectural definition of OCR for this platform

Any future direct spread of Tesseract-specific assumptions into orchestration, gates, aggregation, or design documents is invalid.

---

## 9. Change Control

No future OCR provider integration is complete unless all of the following are aligned:

- Design Authority
- Decision Register
- Runtime State
- Implementation

No provider may be treated as governed runtime truth based only on code presence.
