# OCR Rebuild — Decision Engine Rule Placeholders v1

Status: DRAFT - INITIAL RULE BASELINE

## 1. Purpose

Define the first-pass rule sets and scorecard placeholders for Decision Engines 0–4.

This document is authoritative for:
- initial rule logic per gate
- minimum required inputs per decision
- baseline decision outputs
- placeholder scorecards and thresholds
- controlled “pass-through” behavior where logic is not yet mature

This document exists to ensure:
- no uncontrolled logic is invented by developers
- every decision point produces structured outputs
- rule logic is explicit and replaceable
- future optimisation can plug into a stable structure

## 2. Core Principle

The first implementation must be:
- simple
- explicit
- deterministic
- replaceable

Rules may initially be:
- static
- coarse
- equal-weighted
- even pass-through

BUT:
- they must exist
- they must write structured outputs
- they must populate execution_plan, routing_decision, and evaluation

## 3. Rule Model Structure

Each decision engine must follow a consistent structure:

- inputs
- rule set / scorecard
- decision logic
- outputs
- decision_state
- decision_reason

## 4. Decision Engine 0 — Service Assembly Rules

### Inputs
- requested_services
- client request payload
- optional client constraints (if present)

### Rule Set (v1)
- If no service specified → default to `OCR`
- If multiple services specified → accept all (no restriction v1)
- No rejection logic in v1 unless payload is invalid

### Decision Logic
- Map requested_services → service definition
- Assign required capabilities using service_composition_model
- Assign optional capabilities as defined
- Assign full gate set [0–4] for all services

### Outputs
- service_id
- required_capabilities
- optional_capabilities
- minimum_output_requirements
- relevant_gates

### Decision State
- ACCEPT_REQUEST

### Decision Reason
- "default_service_mapping_v1"

---

## 5. Decision Engine 1 — Initial Planning Rules

### Inputs
- execution_plan seed (from Gate 0)
- document metadata (file type, size, page count if known)
- requested_services

### Rule Set (v1)

#### TEXT_OCR
- default provider: `tesseract`
- fallback provider: `textract_detect_document_text`

#### TABLE_STRUCTURE
- if table_extraction requested → use `textract_analyze_document`
- else → do not activate

#### HANDWRITING
- not actively routed (placeholder only)

#### FRAUD / AUTHENTICITY
- placeholder internal heuristic module

#### GENERAL RULE
- prefer single provider if it satisfies multiple capabilities (bundling allowed but not optimised)

### Decision Logic
- assign provider per capability
- create capability_plan
- set fallback_policy:
  - page_level_reroute_allowed = true
  - max_quality_loops = 1

### Outputs
- execution_plan.capability_plan
- execution_plan.fallback_policy
- routing_decision.selected_strategy = "baseline_v1"

### Decision State
- PLAN_ACCEPTED

### Decision Reason
- "baseline_provider_mapping_v1"

---

## 6. Decision Engine 2 — Quality & Fallback Rules

### Inputs
- OCR outputs
- confidence scores (if available)
- presence of extracted text
- expected outputs from plan

### Rule Set (v1)

#### OCR Quality Check
- If no text extracted → FAIL
- If text length < minimal threshold → LOW_QUALITY
- If confidence available:
  - confidence < 0.7 → LOW_QUALITY

#### Fallback Rule
- If LOW_QUALITY:
  - and fallback allowed → escalate to fallback provider
  - else → accept partial

### Decision Logic
- evaluate each page
- mark:
  - ACCEPT
  - REPROCESS
  - ESCALATE_EXTERNAL

### Outputs
- updated execution_plan (if fallback triggered)
- routing_decision.fallback_used = true/false
- evaluation.quality_score (simple heuristic)
- evaluation.required_fields_present (true/false)

### Decision State
- ACCEPT_PRIMARY_RESULT
- or ESCALATE_EXTERNAL
- or PARTIAL_ACCEPT

### Decision Reason
- "ocr_quality_threshold_v1"

---

## 7. Decision Engine 3 — Service Sufficiency Rules

### Inputs
- outputs from OCR and enrichment
- minimum_output_requirements
- service definition

### Rule Set (v1)

#### OCR Service
- sufficient if:
  - text exists

#### Table Service
- sufficient if:
  - at least one table detected

#### Fraud / Authenticity
- sufficient if:
  - placeholder output exists

#### General Rule
- if required capability output missing → NOT_SUFFICIENT

### Decision Logic
- compare outputs vs required_capabilities
- determine:
  - SERVICE_READY
  - ENRICHMENT_REQUIRED
  - PARTIAL_SERVICE_ONLY

### Outputs
- execution_plan updates (if enrichment triggered)
- evaluation.completeness_score (simple ratio)
- routing_decision.selected_capability_path

### Decision State
- SERVICE_READY
- or ENRICHMENT_REQUIRED
- or PARTIAL_SERVICE_ONLY

### Decision Reason
- "minimum_output_check_v1"

---

## 8. Decision Engine 4 — Final Validation Rules

### Inputs
- aggregated outputs
- evaluation summary
- routing_decision
- service sufficiency result

### Rule Set (v1)

#### Acceptance
- if SERVICE_READY → FINAL_ACCEPT

#### Partial
- if PARTIAL_SERVICE_ONLY → FINAL_ACCEPT_PARTIAL

#### Failure
- if no meaningful output → FINAL_REJECT

#### Qualification
- if fallback used → FINAL_ACCEPT_WITH_QUALIFICATION

### Decision Logic
- determine final state
- attach qualification metadata

### Outputs
- final decision state
- evaluation.final_status
- routing_decision.final_route_state

### Decision State
- FINAL_ACCEPT
- FINAL_ACCEPT_PARTIAL
- FINAL_ACCEPT_WITH_QUALIFICATION
- FINAL_REJECT

### Decision Reason
- "final_validation_v1"

---

## 9. Evaluation Object (v1 Structure)

Minimum fields to populate:

- quality_score (0–1 heuristic)
- completeness_score (0–1 heuristic)
- required_fields_present (boolean)
- routing_acceptance_reason (string)

---

## 10. Routing Decision Object (v1 Structure)

Minimum fields:

- selected_strategy
- fallback_used
- fallback_provider
- selected_capability_path
- decision_basis

---

## 11. Execution Plan Update Rules (v1)

- Only Decision Engines may make material updates
- Workers may append evidence only
- All updates must:
  - preserve history
  - append decision_gate_history entry

---

## 12. First Iteration Limitations

The v1 rule system:
- does not optimise cost vs accuracy
- does not use ML scoring
- does not perform advanced document classification
- does not optimise bundling fully

This is intentional.

---

## 13. Strategic Outcome

This baseline is successful when:
- every gate produces a structured decision
- no worker invents logic
- execution plans are consistently created and updated
- routing and evaluation data exist for every run
- the system is ready for optimisation without redesign
