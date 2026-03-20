# OCR Provider Interface and Execution Plan Contract

Status: CONTROL DOCUMENT — AUTHORITATIVE DESIGN CONSTRAINT

## 1. Purpose

Define the governed OCR provider execution contract for the OCR Rebuild platform.

This document establishes the authoritative design for:

- OCR provider selection control
- execution-plan-carried OCR instructions
- OCR provider abstraction interface
- fallback control rules
- normalized OCR output structure
- rejection rules for invalid OCR execution control

This document exists to ensure OCR remains:

- provider-agnostic
- decision-engine-controlled
- execution-plan-driven
- interface-normalized
- isolated from provider-specific architectural drift

---

## 2. Governing Rule

OCR provider choice is not owned by OCR worker implementation.

OCR provider choice is owned by the decision ecosystem and must be expressed through the governed execution plan.

The OCR worker is an execution component only.

It may:
- validate OCR provider instructions
- execute the assigned provider
- execute explicitly permitted fallback
- normalize provider output
- persist governed result structures

It must not:
- invent provider choice
- silently switch providers
- embed hidden routing logic
- treat one provider as default architectural truth

---

## 3. Control Ownership Model

### 3.1 Decision engine ownership

The decision engine owns:

- provider selection
- provider type selection
- execution mode selection
- fallback permission
- fallback order / fallback chain
- minimum output requirements
- quality thresholds
- escalation intent
- decision rationale

### 3.2 OCR worker ownership

The OCR worker owns:

- validation of OCR instruction block
- execution of assigned provider
- execution of governed fallback chain only when allowed
- normalization of provider output
- provider execution metadata capture
- structured success / failure result construction

### 3.3 Aggregation ownership

Aggregation owns:

- assembly of normalized OCR outputs into canonical document structures
- document-level summary derivation
- manifest update continuation

Aggregation does not own provider selection.

---

## 4. Execution Plan OCR Control Block

The execution plan must carry an explicit OCR instruction block.

Recommended governed structure:

~~~json
{
  "execution_plan": {
    "plan_id": "string",
    "manifest_id": "string",
    "plan_status": "planned|running|ready_for_final_validation|completed|failed",
    "capability_plan": {
      "TEXT_OCR": {
        "provider": "string",
        "provider_type": "external|internal|open_source|managed_service",
        "execution_mode": "primary|fallback|recovery",
        "fallback_allowed": true,
        "fallback_chain": [
          {
            "provider": "string",
            "provider_type": "string",
            "execution_mode": "fallback",
            "fallback_reason": "string"
          }
        ],
        "decision_reason": "string",
        "minimum_output_requirements": {
          "text_required": true,
          "page_confidence_required": false,
          "minimum_non_empty_pages": 1
        },
        "quality_thresholds": {
          "minimum_average_page_confidence": 0.0,
          "minimum_non_empty_page_ratio": 0.0
        }
      }
    }
  }
}
~~~

---

## 5. Mandatory OCR Instruction Fields

The governed OCR instruction block for `TEXT_OCR` must include:

- `provider`
- `provider_type`
- `execution_mode`
- `fallback_allowed`
- `decision_reason`

It should also include, where governed:

- `fallback_chain`
- `minimum_output_requirements`
- `quality_thresholds`

### 5.1 Missing instruction rule

If the OCR stage is reached and valid OCR provider instructions are missing, the OCR worker must reject execution safely.

It must not silently infer provider choice.

### 5.2 Unsupported instruction rule

If the plan specifies a provider not supported by the current governed runtime, the OCR worker must fail with a structured controlled error.

It must not substitute another provider unless:
- fallback is explicitly permitted
- the substitute provider exists in the governed fallback chain

---

## 6. OCR Provider Interface

All OCR providers must conform to a single logical interface before they are considered valid runtime providers.

### 6.1 Provider execution input

Each OCR provider execution must receive a normalized input model containing at minimum:

~~~json
{
  "manifest_id": "string",
  "document_id": "string",
  "page_id": "string",
  "page_number": 1,
  "source_bucket": "string",
  "source_key": "string",
  "provider_instruction": {
    "provider": "string",
    "provider_type": "string",
    "execution_mode": "string",
    "fallback_allowed": true,
    "decision_reason": "string"
  },
  "runtime_context": {
    "current_stage": "ocr",
    "correlation_id": "string",
    "request_timestamp": "iso-8601"
  }
}
~~~

### 6.2 Provider execution output

Each OCR provider must return a normalized result model containing at minimum:

~~~json
{
  "status": "completed|failed",
  "provider": "string",
  "provider_type": "string",
  "engine_name": "string",
  "engine_version": "string",
  "page_result": {
    "page_id": "string",
    "page_number": 1,
    "extracted_text": "string",
    "line_block_word_confidence": {
      "page_confidence": 0.0
    }
  },
  "provider_metadata": {
    "execution_mode": "primary|fallback|recovery",
    "decision_reason": "string"
  },
  "error": null
}
~~~

---

## 7. Normalized OCR Page Output Contract

Regardless of provider used, the OCR stage must write normalized page results aligned to the governed page-level payload model.

Required page-level fields include:

- `document_id`
- `page_id`
- `page_number`
- `source_bucket`
- `source_key`
- `processed_bucket`
- `processed_key`
- `extracted_text`
- `line_block_word_confidence`
- `engine_name`
- `engine_version`
- `provider`
- `routing_decision`
- `evaluation`
- `metadata`

### 7.1 Required metadata fields

OCR page metadata must include, where applicable:

- `stage`
- `result_bucket`
- `source_processed_key`
- `provider_type`
- `execution_mode`
- `decision_reason`

### 7.2 Provider isolation rule

Provider-specific raw response structures must not become the governed runtime payload shape.

Raw provider outputs may be retained only as controlled supporting evidence if separately governed, but not as the canonical execution payload contract.

---

## 8. Fallback Control Rules

Fallback execution is allowed only when explicitly permitted in the execution plan.

### 8.1 Fallback prerequisites

Fallback may occur only if all of the following are true:

- `fallback_allowed = true`
- a governed `fallback_chain` exists
- the primary provider failed or failed policy thresholds
- the fallback provider is explicitly listed in the plan

### 8.2 Forbidden fallback behavior

The OCR worker must not:

- invent a fallback provider
- reorder the fallback chain
- skip directly to an unlisted provider
- fallback merely because another provider is easier to run

### 8.3 Fallback traceability

Any fallback execution must be recorded in:

- `routing_decision`
- `evaluation`
- `execution_plan.decision_gate_history` where applicable
- `manifest_update.pipeline_history`

---

## 9. Structured Rejection Rules

The OCR worker must reject safely under any of the following conditions:

- missing OCR instruction block
- OCR instruction block not a dictionary/object
- missing `provider`
- missing `provider_type`
- missing `execution_mode`
- missing `fallback_allowed`
- missing `decision_reason`
- unsupported provider
- unsupported execution mode
- invalid fallback configuration

### 9.1 Rejection behavior

When rejecting, the OCR worker must:

- not execute OCR provider code
- not invent defaults
- return structured error details
- preserve traceability in governed runtime payload structures

### 9.2 Controlled error model

The rejection result should include:

- `status = failed`
- `error_code`
- `error_category`
- `error_message`
- `provider = planned provider if present`
- `decision_reason = planned decision reason if present`

---

## 10. Runtime Interpretation Boundary

Current Tesseract-backed OCR remains permitted only as:

- bootstrap runtime provider
- baseline validation provider
- provider implementation behind the governed abstraction boundary

It must not be interpreted as:

- the permanent OCR architecture
- the sole valid OCR provider
- a reason to bypass execution-plan control
- a reason to hard-code Tesseract behavior into orchestration logic

---

## 11. Implementation Constraint

No implementation change is valid unless it preserves all of the following:

- decision engine ownership of provider choice
- execution-plan-driven provider control
- normalized OCR provider interface
- structured fallback control
- structured rejection on invalid instructions
- provider-neutral runtime payload contract

---

## 12. Required Future Alignment

The following must be aligned before OCR provider abstraction is considered implemented:

- decision-engine-generated OCR provider instructions
- execution plan contract update
- OCR worker validation of instruction block
- OCR provider adapter layer
- normalized provider response mapping
- fallback governance implementation
- runtime handover update
- gap register update
- live AWS validation of governed provider-controlled behavior

---

## 13. Non-Negotiable Interpretation Rule

Code that currently executes OCR is not by itself the design truth.

The design truth is:

- provider-agnostic control
- execution-plan-directed execution
- governed abstraction boundary
- normalized runtime output

Any implementation that drifts from this is invalid and must be corrected.
