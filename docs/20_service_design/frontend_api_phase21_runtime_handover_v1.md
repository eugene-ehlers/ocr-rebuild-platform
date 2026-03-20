
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

