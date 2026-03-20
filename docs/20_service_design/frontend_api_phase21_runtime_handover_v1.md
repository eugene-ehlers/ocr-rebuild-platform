
### Execution Plan Enforcement Scope (Current State)

Execution Plan v1 is currently enforced in:

- Frontend API orchestration layer
- Frontend service-family workers:
  - financial_management
  - fica_compliance
  - credit_decision

These components:
- build and persist execution plans
- propagate execution plans downstream
- enforce strict validation
- reject invalid payloads safely
- persist stage results and finalization outcomes

### Pipeline Enforcement Status

Execution Plan enforcement is NOT yet active in:

- preprocessing
- OCR
- aggregation

These services continue to operate using the prior payload model.

Pipeline-wide enforcement remains a controlled future enhancement and must not be assumed as active runtime behaviour.

### Runtime Interpretation Control

Runtime interpretation must follow the governed source-of-truth hierarchy.

Authoritative interpretation must rely on:
- approved governed documentation under `docs/`
- live implementation source under:
  - `services/`
  - `api/`
  - `infrastructure/`

The following are supporting artifacts only and must not be treated as design or runtime truth:
- `build/`
- `__pycache__/`
- `*.pyc`
- backup files
- generated packaging artifacts
- temporary or local output files

If any conflict exists, governed documentation and live implementation source take precedence.

### Governed Document References

The current governed document stack for interpretation and change control is:

- Design Authority:
  - `docs/00_program_control/document_intelligence_operating_baseline.md`
  - `docs/00_program_control/known_gaps_and_improvement_register.md`
- Decision Register:
  - `docs/00_program_control/decision_register.md`
- Runtime State:
  - `docs/20_service_design/frontend_api_phase21_runtime_handover_v1.md`
- Document stack map:
  - `docs/00_program_control/governed_document_map.md`

### Validated Runtime Baseline — Full OCR Pipeline Execution

A controlled live Step Functions execution has been validated for the current OCR pipeline baseline.

Validated execution:
- state machine: `ocr-pipeline-sf-prod`
- execution name: `test-1774044490`
- manifest id: `manifest-5a87dc9c738a4317bb74429a834fe5ed`
- source object: `s3://ocr-rebuild-original/test-docs/test.png`
- validation timestamp: `2026-03-20T22:09:51Z`

Validated live stages completed in AWS:
- manifest_generation
- preprocessing
- ocr
- gate2_quality_evaluation
- gate3_service_sufficiency
- aggregation
- gate4_final_validation

Validated live outcome:
- Step Functions execution succeeded
- `manifest_update.pipeline_status = completed`
- `execution_plan.plan_status = completed`
- `execution_plan.final_status = FINAL_ACCEPT`
- `routing_decision.gate4_final_decision = FINAL_ACCEPT`
- `routing_decision.delivery_ready = true`

Validated boundary:
- this confirms successful baseline pipeline execution for a controlled image input
- this does NOT change the governed interpretation that preprocessing, OCR, and aggregation are still not execution-plan-enforced in the same strict way as the frontend/API orchestration path and governed service-family workers

### OCR Runtime Control Boundary

Current live OCR pipeline validation includes a Tesseract-backed OCR execution path.

This must be interpreted as:
- a controlled bootstrap provider
- a runtime validation baseline
- not the final architectural ownership model for OCR

Current governed boundary:
- OCR runtime is operational in AWS for the validated baseline pipeline
- OCR provider abstraction is not yet fully implemented as design-governed runtime control
- execution-plan-driven provider selection for OCR remains incomplete
- current Tesseract-backed OCR must not be treated as permanent design truth

### OCR Provider Interface Contract Boundary

The governed OCR provider interface and execution-plan contract now exists in design authority.

Current runtime interpretation remains strict:

- OCR worker now enforces explicit TEXT_OCR instruction presence and required-field validation
- manifest generation now emits a governed TEXT_OCR instruction block aligned to the provider-interface contract
- OCR worker now rejects missing or unsupported OCR provider instructions safely
- OCR worker now normalizes provider execution metadata into the governed OCR payload shape
- OCR worker now records attempted provider-chain and fallback traceability in OCR payload structures
- provider registry now includes a governed AWS Textract adapter baseline in addition to the Tesseract adapter
- OCR fallback-chain iteration now continues safely across governed provider candidates when an earlier candidate is invalid, not runtime-enabled, or execution-fails
- AWS Textract remains runtime-disabled unless explicitly enabled by environment control
- governed executable multi-provider fallback-chain runtime proof is not yet governed runtime truth across the OCR stage

Current Tesseract-backed OCR runtime remains:
- operational as bootstrap runtime
- valid behind the governed provider-interface boundary
- still not sufficient to claim complete multi-provider contract enforcement

