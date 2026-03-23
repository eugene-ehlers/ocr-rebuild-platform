# Execution Plan to Pipeline Integration Specification

Status: DRAFT - CONTROLLED INTEGRATION BASELINE

## 1. Purpose

Define how the governed `execution_plan` is embedded into, read by, updated by, and preserved within the runtime pipeline payload.

This document is authoritative for:
- where the execution plan lives in the runtime payload
- how pipeline stages consume it
- how decision gates update it
- how it relates to `routing_decision`, `evaluation`, and `manifest_update`
- how runtime components must behave to avoid architectural drift

This document exists to ensure that:
- service composition logic is not lost once execution starts
- execution decisions remain visible inside the runtime contract
- pipeline stages do not invent provider logic outside the plan
- future optimisation can improve plans without replacing the runtime payload model

## 2. Core Decision

For the current governed baseline, the execution plan is embedded directly inside the pipeline execution payload.

This means:
- no separate lookup is required during normal stage execution
- the full instruction object is visible in orchestration history
- debugging and validation are simpler
- the contract remains extensible for later externalisation if needed

## 3. Authoritative Integration Principle

The runtime pipeline payload remains the authoritative inter-stage execution object.

The `execution_plan` is embedded within that payload as the governed execution instruction set.

Therefore:
- the pipeline payload carries state
- the execution plan carries intent and provider/capability instructions
- stages must preserve both

## 4. Runtime Payload Relationship

The integrated runtime model is:

- top-level pipeline execution payload
- embedded `execution_plan`
- embedded `routing_decision`
- embedded `evaluation`
- embedded `manifest_update`
- page/document content and enrichment outputs
- transformed governed payload where runtime-to-contract transformation is required
- validation and sufficiency results where governed assessment has been executed

## 5. Required Top-Level Payload Shape

The pipeline execution payload must support the following integrated shape:

    {
      "manifest_id": "string",
      "document_id": "string",
      "source_uri": "string",
      "source_bucket": "string",
      "source_batch_uri": "string",
      "document_type": "string",
      "expected_document_type": "string",
      "ingestion_timestamp": "ISO-8601 string",
      "creation_timestamp": "ISO-8601 string",
      "processing_parameters": {},
      "requested_services": {},
      "service_status": {},
      "execution_state": {},
      "documents": [],
      "pages": [],
      "execution_plan": {},
      "routing_decision": {},
      "evaluation": {},
      "manifest_update": {}
    }

## 6. Integration Responsibilities by Object

## 6.1 execution_plan
Carries:
- service intent
- required capabilities
- provider/module plan
- fallback rules
- document/page overrides
- gate history
- plan lifecycle status

## 6.2 routing_decision
Carries:
- current routing view
- accepted route
- fallback decisions taken
- selected providers at a summarised level
- current decision-state interpretation

The `routing_decision` object is a summarised decision trace.
It must not replace the richer `execution_plan.decision_gate_history`.

## 6.3 evaluation
Carries:
- quality summaries
- completeness summaries
- gate-relevant metrics
- acceptance/rejection evidence
- future optimisation signals

## 6.4 manifest_update
Carries:
- durable execution control updates
- service lifecycle state
- pipeline history
- client notification state
- manifest-level summaries

## 6.5 transformed governed payload
Carries:
- structurally mapped runtime output prepared for governed validation
- explicit field alignment outputs
- pass-through normalized values approved for validation use

The transformed governed payload:
- is not a replacement for raw runtime evidence
- must remain traceable back to runtime sources
- must not contain inferred or fabricated values
- exists only where approved transformation is required

## 6.6 validation and sufficiency result
Carries:
- validation outcome
- sufficiency outcome
- missing contract requirements
- explicit governed fail / escalate / degrade state where applicable

## 7. Runtime Stage Rules

## 7.1 All stages must preserve execution_plan
No stage may remove, replace, or silently reset the `execution_plan`.

A stage may:
- read it
- act according to it
- append/update controlled sections
- mark status transitions relevant to the stage

A stage must not:
- invent a new execution plan outside governed decision rules
- discard plan history
- hard-code provider choices that contradict the plan

## 7.2 Stages may enrich but not redefine intent
Stages may add:
- execution evidence
- provider result metadata
- output summaries
- quality metrics
- plan status updates

Stages must not redefine:
- service objective
- required capabilities
- minimum output requirements

Those originate upstream in service composition and decision gates.

## 7.3 Plan changes require gate semantics
Any material change to provider assignment, fallback path, or capability route must be recorded as a gate-driven or gate-equivalent plan adjustment.

## 8. Stage-by-Stage Integration Guidance

## 8.1 GenerateManifest
Must:
- initialize the runtime payload
- preserve or initialize an embedded `execution_plan`
- initialize empty `routing_decision` and `evaluation` objects where required

If Gate 0 already ran upstream, GenerateManifest must carry that plan forward.
It must not discard it.

## 8.2 Preprocessing
Must:
- read `execution_plan` for document/page overrides relevant to normalization and preprocessing
- preserve the embedded plan
- update routing/evaluation only where preprocessing produces relevant evidence
- not invent OCR/provider decisions outside the plan

Preprocessing may add:
- normalization evidence
- document/page-level observations useful for Gate 1 or Gate 2 refinement

## 8.3 OCR
Must:
- read `execution_plan.capability_plan.TEXT_OCR`
- execute the selected provider/module path where this is already determined
- preserve the embedded plan
- write quality evidence into `evaluation`
- update `routing_decision` if an already-governed fallback has actually occurred
- append decision history only if a gate-driven adjustment is triggered

## 8.4 Table Extraction / Structured Extraction
Must:
- read the relevant capability entries from `execution_plan.capability_plan`
- preserve bundled-provider reuse semantics
- avoid duplicate extraction if bundled outputs already satisfy required capability coverage
- record quality/completeness evidence in `evaluation`

## 8.5 Signature / Fraud / Authenticity / Other Enrichment Stages
Must:
- read the relevant capability entries
- honour document/page overrides
- preserve the embedded plan
- update evidence, not redefine service intent

## 8.6 Aggregation
Must:
- preserve the final execution plan in the output payload
- preserve routing/evaluation summaries
- produce final document-level and manifest-level outputs consistent with the plan actually executed
- not erase provider or gate history
- preserve transformed governed payload where present
- preserve validation and sufficiency results where present

Aggregation must not collapse or hide the distinction between:
- raw runtime execution output
- transformed validation-ready payload
- final governed validation outcome

Aggregation is where the final executed path becomes part of the durable result lineage.

## 9. Plan Read Semantics

A runtime component should read the execution plan in this order:

### 9.1 Base capability plan
Read `execution_plan.capability_plan`

### 9.2 Document override
If applicable, read `execution_plan.document_overrides`

### 9.3 Page override
If applicable, read `execution_plan.page_overrides`

### 9.4 Fallback policy
Read `execution_plan.fallback_policy`

### 9.5 Gate history / current status
Read `execution_plan.decision_gate_history` and `execution_plan.plan_status`

This ordering ensures that the most specific valid instruction wins.

## 10. Plan Update Semantics

## 10.1 Non-material updates
These include:
- execution timestamps
- provider result metadata
- quality evidence
- completeness evidence
- stage-completion notes

These may be appended without changing overall plan intent.

## 10.2 Material updates
These include:
- provider reassignment
- page-level reroute
- document-level reroute
- external escalation
- fallback activation
- capability deferral or activation

These must:
- be reflected in `execution_plan`
- be captured in `decision_gate_history`
- be summarised in `routing_decision`
- be supported by evidence in `evaluation`

## 11. routing_decision Integration Rule

The `routing_decision` object should act as the runtime-readable summary of the current route.

It should support fields such as:
- selected_strategy
- primary_provider_summary
- fallback_used
- fallback_reason
- current_route_state
- route_confidence
- last_gate_applied

It must be consistent with, but may be simpler than, the embedded `execution_plan`.

## 12. evaluation Integration Rule

The `evaluation` object should accumulate gate-relevant evidence such as:
- ocr quality
- completeness
- table sufficiency
- signature confidence
- authenticity score
- missing required outputs
- accepted/rejected capability evidence
- optimisation-relevant tags

The evaluation object is the evidence base that justifies plan changes or final acceptance.

## 13. plan_status Integration Rule

The embedded `execution_plan.plan_status` must remain aligned with runtime behaviour.

Illustrative alignment:
- plan created → `planned`
- execution started → `in_progress`
- reroute/fallback applied → `adjusted`
- some capabilities executed only → `partially_executed`
- accepted for delivery → `completed`
- unable to continue → `failed`
- intentionally stopped → `cancelled`

## 14. Step Functions Mapping Principle

Step Functions should treat the embedded execution plan as part of the authoritative payload state.

This means:
- states pass it forward
- task outputs must preserve it
- null-result pathing must not destroy it
- retries must not corrupt it
- catch/failure handlers should preserve its last valid state where practical

## 15. Lambda / Worker Mapping Principle

Each Lambda or worker should:
- read only the parts of the plan relevant to its responsibility
- avoid interpreting unrelated capabilities
- preserve the full plan object in output
- append only controlled updates

This reduces coupling and prevents every worker from becoming a decision engine.

## 16. Current Controlled Baseline

For the initial implementation, the following simplifications are acceptable:
- coarse capability_plan entries
- limited document/page override use
- simplified routing_decision summaries
- simplified evaluation objects
- placeholder gate history entries

These are acceptable only if:
- the integrated payload shape is preserved
- future refinement does not require redesign
- developers do not bypass the embedded execution plan pattern

## 16A. Relationship to Transformation and Validation

This integration specification governs how execution-plan-driven runtime state is preserved through pipeline execution.

Where approved transformation is required:
- raw runtime output may be mapped into a transformed governed payload
- validation and sufficiency assessment may operate on that transformed payload
- the original runtime evidence must still remain preserved

A governed fail after transformation and validation is a valid integrated runtime outcome and must be retained explicitly in runtime artifacts.

## 17. Relationship to Existing Contracts

This integration specification must be interpreted together with:
- execution_plan_contract.md
- pipeline_execution_contract.md
- decision_ecosystem_and_gate_specification.md
- service_composition_model.md
- capability_registry_provider_map.md
- document_manifest_schema.json
- page_schema.json
- canonical_document_schema.json

Where conflicts appear, the governed direction is:
- service intent from service composition
- execution intent from execution_plan
- runtime state from pipeline payload
- durable control state from manifest_update

## 18. Strategic Outcome

This integration is successful when:
- the execution plan remains visible and preserved through runtime execution
- stages act according to governed plan instructions
- provider substitutions and reroutes are traceable
- routing/evaluation summaries remain aligned with the underlying plan
- future optimisation can improve behaviour without changing the embedded execution pattern
