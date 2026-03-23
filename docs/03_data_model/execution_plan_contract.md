# Execution Plan Contract

Status: DRAFT - RUNTIME ORCHESTRATION BASELINE

## 1. Purpose

Define the governed execution plan object that connects:

- service composition
- decision ecosystem gates
- provider/module selection
- runtime orchestration
- fallback and reprocessing
- final delivery traceability

This document is authoritative for the execution plan passed between decisioning and runtime execution components.

It exists to ensure that:
- service intent is preserved through execution
- capability requirements are translated into explicit execution instructions
- provider choices are traceable
- bundled capability reuse is governed
- fallback and reroute decisions are controlled
- future optimisation can occur without redesigning orchestration payloads

## 2. Core Principle

The execution plan is not the client request.

It is not the canonical output.

It is the governed runtime instruction set produced by the decision ecosystem to fulfill a composed service through a selected set of capabilities, providers, rules, and gate-specific controls.

## 3. Position in the Overall Model

The end-to-end relationship is:

- client request
- service composition
- required capability set
- decision ecosystem
- execution plan
- runtime execution
- governed transformation (where required)
- validation and sufficiency assessment
- aggregation and delivery

The execution plan is therefore the bridge between design-time service logic and run-time execution behaviour.

Where execution runtime output is not structurally sufficient to satisfy governed validation contracts, an explicit governed transformation layer may be applied after runtime execution and before validation and sufficiency assessment.

This transformation layer:
- is an explicit governed control component
- may perform structural mapping, field alignment, and pass-through normalization
- must not perform inference, fabrication, or hidden business logic
- must remain versioned, auditable, and reviewable

A governed validation fail after transformation is a valid system outcome and does not by itself indicate runtime instability or execution error.

## 4. Required Design Characteristics

The execution plan must be:

- service-aware
- capability-aware
- provider-aware
- document/page override aware
- gate-history aware
- fallback-aware
- substitution-ready
- extensible for future optimisation

## 5. Authoritative Top-Level Structure

The execution plan must support the following top-level shape:

    {
      "plan_id": "string",
      "manifest_id": "string",
      "service_id": "string",
      "service_name": "string",
      "service_objective": "string",
      "required_capabilities": [],
      "optional_capabilities": [],
      "minimum_output_requirements": {},
      "capability_plan": {},
      "bundled_provider_usage": {},
      "fallback_policy": {},
      "document_overrides": [],
      "page_overrides": [],
      "relevant_gates": [],
      "decision_gate_history": [],
      "plan_status": "planned"
    }

## 6. Required Top-Level Fields

### 6.1 Required identifiers
- `plan_id`
- `manifest_id`
- `service_id`

### 6.2 Required service traceability
- `service_name`
- `service_objective`

### 6.3 Required capability traceability
- `required_capabilities`

### 6.4 Required execution logic
- `capability_plan`

### 6.5 Required gate traceability
- `relevant_gates`
- `decision_gate_history`

### 6.6 Required lifecycle status
- `plan_status`

## 7. Field Definitions

## 7.1 plan_id
Unique identifier for the execution plan instance.

## 7.2 manifest_id
Identifier linking the plan to the governed manifest execution scope.

## 7.3 service_id
Identifier of the service definition selected by Gate 0.

## 7.4 service_name
Human-readable service name.

## 7.5 service_objective
Short business description of what the service must achieve.

## 7.6 required_capabilities
List of atomic capabilities that must be fulfilled for the service to be considered valid.

## 7.7 optional_capabilities
List of capabilities that may improve quality, completeness, or client value but are not mandatory for minimum delivery.

## 7.8 minimum_output_requirements
Structured summary of the minimum outputs required to satisfy the service.

Examples:
- extracted text required
- signature result required
- authenticity summary required
- structured table output required

## 7.9 capability_plan
The authoritative execution mapping of required capabilities to providers/modules and execution rules.

## 7.10 bundled_provider_usage
Structured record of where a provider has been selected partly because it returns multiple required capabilities in one execution.

## 7.11 fallback_policy
Rules and permissions for fallback, reroute, escalation, and partial acceptance.

## 7.12 document_overrides
Document-level variations to the base plan.

## 7.13 page_overrides
Page-level variations to the base plan.

## 7.14 relevant_gates
The fixed gates that are expected to participate materially for this service.

## 7.15 decision_gate_history
Chronological record of plan creation, revision, reroute, fallback, and acceptance decisions across gates.

## 7.16 plan_status
Lifecycle state of the plan.

Allowed baseline values:
- `planned`
- `in_progress`
- `adjusted`
- `partially_executed`
- `completed`
- `failed`
- `cancelled`

## 8. Capability Plan Contract

The `capability_plan` object is the core execution mapping.

It must support one entry per capability.

Illustrative shape:

    "capability_plan": {
      "TEXT_OCR": {
        "provider": "tesseract",
        "provider_type": "open_source",
        "execution_mode": "primary",
        "fallback_allowed": true,
        "fallback_provider": "textract_detect_document_text",
        "decision_reason": "low_cost_primary_for_printed_text"
      },
      "SIGNATURE_DETECTION": {
        "provider": "internal_cv_signature",
        "provider_type": "internal",
        "execution_mode": "primary",
        "fallback_allowed": false,
        "decision_reason": "internal_signature_detection_selected"
      }
    }

## 8.1 Required fields per capability entry

Each capability entry should support:
- `provider`
- `provider_type`
- `execution_mode`
- `fallback_allowed`
- `fallback_provider` when relevant
- `decision_reason`

## 8.2 provider_type
Allowed baseline values:
- `internal`
- `open_source`
- `external_api`
- `managed_service`
- `placeholder`

## 8.3 execution_mode
Allowed baseline values:
- `primary`
- `fallback`
- `deferred`
- `conditional`
- `not_applicable`

## 9. Bundled Provider Usage Contract

The `bundled_provider_usage` object exists so the system can avoid paying twice for equivalent outputs.

Illustrative shape:

    "bundled_provider_usage": {
      "textract_analyze_document": {
        "selected_for": [
          "KEY_VALUE_EXTRACTION",
          "TABLE_STRUCTURE"
        ],
        "bundled_capabilities_reused": [
          "TEXT_OCR",
          "CHECKBOX_DETECTION"
        ],
        "duplication_block": true
      }
    }

## 9.1 Rule
If a bundled provider has already produced a required capability output of acceptable quality, duplicate extraction through another provider should not occur unless explicitly justified and recorded.

## 10. Fallback Policy Contract

The `fallback_policy` object defines how the plan may change if results are insufficient.

Illustrative shape:

    "fallback_policy": {
      "page_level_reroute_allowed": true,
      "document_level_reroute_allowed": true,
      "external_escalation_allowed": true,
      "max_quality_loops": 2,
      "max_enrichment_loops": 2,
      "partial_acceptance_allowed": true,
      "client_clarification_allowed": true
    }

## 10.1 Baseline rules
The fallback policy should control:
- whether fallback is allowed
- whether reroute is page-level or document-level
- whether external escalation is allowed
- how many bounded loops are permitted
- whether partial service delivery is allowed
- whether clarification or escalation is allowed

## 11. Document and Page Override Contract

The base plan may be overridden where one document or page materially differs from others.

## 11.1 document_overrides
Used when a specific document in a manifest needs a different capability/provider plan.

Illustrative shape:

    "document_overrides": [
      {
        "document_id": "doc_002",
        "override_reason": "handwriting_detected",
        "capability_plan_override": {
          "HANDWRITING_EXTRACTION": {
            "provider": "external_handwriting_provider",
            "provider_type": "external_api",
            "execution_mode": "primary",
            "fallback_allowed": false
          }
        }
      }
    ]

## 11.2 page_overrides
Used when specific pages need reroute or special handling.

Illustrative shape:

    "page_overrides": [
      {
        "document_id": "doc_001",
        "page_number": 3,
        "override_reason": "ocr_quality_below_threshold",
        "capability_plan_override": {
          "TEXT_OCR": {
            "provider": "textract_detect_document_text",
            "provider_type": "managed_service",
            "execution_mode": "fallback",
            "fallback_allowed": false
          }
        }
      }
    ]

## 12. Decision Gate History Contract

The `decision_gate_history` array is the authoritative trace of how the plan changed over time.

Each entry should support:
- `gate_id`
- `gate_name`
- `decision_engine_id`
- `decision_state`
- `decision_reason`
- `plan_change_summary`
- `timestamp`

Illustrative entry:

    {
      "gate_id": "2",
      "gate_name": "Extraction Quality and Fallback Decision",
      "decision_engine_id": "2",
      "decision_state": "ESCALATE_EXTERNAL",
      "decision_reason": "ocr_quality_below_threshold_on_selected_pages",
      "plan_change_summary": "TEXT_OCR rerouted to textract for pages 3 and 4",
      "timestamp": "2026-03-18T12:00:00Z"
    }

## 13. Plan Lifecycle Semantics

## 13.1 planned
The plan has been created but not yet materially executed.

## 13.2 in_progress
Execution has started and the plan is active.

## 13.3 adjusted
The plan has changed due to gate-based re-decision.

## 13.4 partially_executed
Some capabilities have run, but the full plan has not yet completed.

## 13.5 completed
The plan has been executed to the point required for service delivery.

## 13.6 failed
The plan could not be completed successfully.

## 13.7 cancelled
The plan was intentionally stopped or superseded.

## 13.8 Relationship to Transformation and Validation

The execution plan contract governs runtime execution instructions.

It does not by itself guarantee that raw execution output is validation-ready.

Where approved by architecture and runtime control:
- execution output may be transformed into a governed validation payload
- validation and sufficiency assessment may operate on the transformed payload rather than raw runtime output

This separation preserves:
- execution/runtime control integrity
- validation contract integrity
- explicit auditability of any structural mapping between the two

## 14. Relationship to Other Contracts

The execution plan must remain compatible with:
- service composition definitions
- capability registry and provider map
- decision ecosystem and gate specification
- pipeline execution contract
- manifest schema
- page schema
- canonical document schema

It must not replace those contracts.
It references and operationalizes them.

## 15. Runtime Mapping Principle

The execution plan must be consumable by orchestration and runtime components.

Illustrative usage:
- Step Functions uses it to determine stage execution path
- Lambda uses it to determine normalization rules or lightweight actions
- ECS workers use it to understand provider/module assignment per capability
- aggregation uses it to preserve routing and provider traceability

## 16. Initial Implementation Rule

The initial implementation may use:
- simplified capability plans
- simplified fallback policies
- coarse document/page override logic
- placeholder decision history entries

This is acceptable provided:
- the structure exists
- the fields are stable
- future refinement does not require redesign

## 17. Strategic Outcome

This contract is successful when:
- services can be translated into executable plans consistently
- providers can be swapped without redesign
- bundled provider reuse is explicit
- gate-driven plan evolution is traceable
- runtime components can execute against the same governed instruction object
- future optimisation engines can improve behaviour without replacing the contract
