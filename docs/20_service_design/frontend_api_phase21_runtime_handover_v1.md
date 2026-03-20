# Front-End / API Runtime Progress Handover — Through Phase 21E.10

## 1. Purpose

This handover captures the current implementation state of the Front-End / Control Plane, Incoming API, orchestration, persistence, enforcement, and early AWS/ECS runtime wiring.

It also records failed attempts and lessons learned so future developer chats do not repeat the same logic blindly.

---

## 2. Current Confirmed State

### Frontend / API scaffolding
Completed and committed through:
- Phase 1 to Phase 10

This includes:
- frontend module scaffolding
- API domain scaffolding
- design system
- identity and access
- consent
- document workspace
- requests and results
- annotation and correction
- operational admin
- support
- telemetry

### Orchestration / runtime control
Completed and committed through:
- Phase 11 — backend orchestration for requests/results
- Phase 12 — real execution wiring and request persistence
- Phase 13 — downstream task stub payload alignment
- Phase 14A — soft pre-execution enforcement
- Phase 15 — deep document readiness under soft enforcement
- Phase 16 — consent evidence and traceability
- Phase 17 — standing consent, expiry, revocation
- Phase 18 — hard enforcement layer
- Phase 19 — SQLite persistence replacement
- Phase 20 — AWS invocation bridge
- Phase 21 / 21B / 21C / 21E partial runtime work

### Persistence
Current governed local persistence:
- `runtime_data/request_store.db`
- backend: SQLite

### Enforcement
Current enforcement mode:
- hard enforcement active

This means:
- failed consent blocks execution
- failed document readiness blocks execution
- blocked requests are still persisted
- remediation prompts are still generated and retrievable

---

## 3. Current AWS / ECS Runtime State

### Confirmed available in AWS
Verified in CloudShell:
- AWS credentials available in CloudShell session
- region configured as `us-east-1`
- ECS cluster exists:
  - `ocr-rebuild-cluster`
- IAM roles exist:
  - `ocr-rebuild-ecs-execution-role`
  - `ocr-rebuild-ecs-task-role`

### Created during this work
Created and verified:
- ECR repositories:
  - `financial-management-worker`
  - `fica-compliance-worker`
  - `credit-decision-worker`
- CloudWatch log groups:
  - `/ecs/financial-management-worker`
  - `/ecs/fica-compliance-worker`
  - `/ecs/credit-decision-worker`

### ECS task definitions registered
Registered successfully:
- `financial-management-worker-task-prod:1`
- `fica-compliance-worker-task-prod:1`
- `credit-decision-worker-task-prod:1`

Task definition JSON files now exist at:
- `infrastructure/ecs/financial_management/task-definition.json`
- `infrastructure/ecs/fica_compliance/task-definition.json`
- `infrastructure/ecs/credit_decision/task-definition.json`

---

## 4. Current Worker Image Build State

### Build assets created
Created:
- `services/financial_management/Dockerfile`
- `services/fica_compliance/Dockerfile`
- `services/credit_decision/Dockerfile`

Created:
- `services/financial_management/requirements.txt`
- `services/fica_compliance/requirements.txt`
- `services/credit_decision/requirements.txt`

Created:
- `services/financial_management/worker.py`
- `services/fica_compliance/worker.py`
- `services/credit_decision/worker.py`

Created:
- `services/financial_management/service_runner.py`
- `services/fica_compliance/service_runner.py`
- `services/credit_decision/service_runner.py`

### Local image build result
Docker image build succeeded for:
- `financial-management-worker:phase5`
- `fica-compliance-worker:phase5`
- `credit-decision-worker:phase5`

### Current blocker
The original container runtime packaging blocker has been resolved.

Validated outcome:
- local Python 3.11 worker containers execute successfully
- ECR images were pushed successfully
- ECS task definitions were updated successfully
- Fargate tasks executed successfully for:
  - financial management
  - fica compliance
  - credit decision
- ECS payload override injection was validated successfully
- decision engine `EXECUTION_MODE=aws` routing was validated successfully
- `create_request(...)` in AWS mode was validated successfully under Python 3.11 container runtime
- SQLite persistence of AWS-mode orchestration records was validated successfully

Resolved root cause:
- worker execution by script path caused import resolution failure
- governed fix was module execution:
  - `python -m services.<service>.worker`

---

## 5. Failed Attempts and What Must NOT Be Repeated Blindly

### Failure 1 — AWS CLI invocation inside Python 3.11 container
Attempt:
- AWS bridge used subprocess call to `aws`

Observed failure:
- `[Errno 2] No such file or directory: 'aws'`

Conclusion:
- Do NOT rely on AWS CLI inside the Python runtime container path
- boto3 is the governed runtime invocation pattern

### Failure 2 — boto3 invocation without region
Attempt:
- boto3 ECS bridge used without region in verification container

Observed failure:
- `You must specify a region.`

Conclusion:
- AWS runtime path requires region to be explicitly available
- Runtime standard must require `AWS_DEFAULT_REGION`

### Failure 3 — boto3 invocation without credentials in container
Attempt:
- boto3 ECS bridge executed in Python 3.11 container without propagated AWS credentials

Observed failure:
- `Unable to locate credentials`

Conclusion:
- CloudShell has credentials, but the verification container does not inherit them automatically
- Do NOT assume containerized verification has AWS identity unless credentials or IAM context are explicitly provided

### Failure 4 — ECS registration before task definitions existed
Observed earlier state:
- ECS cluster existed
- no task definitions for financial/fica/credit service families

Conclusion:
- Do NOT assume service-family ECS task definitions already exist
- They had to be created and registered explicitly

### Failure 5 — ECS task definitions pointing to image tags before images existed
Observed state:
- ECR repos existed but had no images
- task definitions referenced `:phase5` tags that did not exist yet

Conclusion:
- Registration alone does not make a task runnable
- Image build/push must exist before live ECS execution is expected to work

### Failure 6 — worker import using `infrastructure...task`
Attempt:
- worker imported:
  - `from infrastructure.ecs.<service>.task import run_task`

Observed failure:
- `ModuleNotFoundError: No module named 'infrastructure'`

Conclusion:
- Do NOT retry that packaging pattern blindly inside container workers
- Container worker imports must align to packaged service-local modules

### Failure 7 — worker import using `services...service_runner`
Attempt:
- worker imported:
  - `from services.<service>.service_runner import run`

Observed failure:
- `ModuleNotFoundError: No module named 'services'`

Conclusion:
- The current container packaging/import path is still not resolved
- Do NOT assume top-level package imports will resolve automatically in the image
- The next step must inspect Python import path and package layout before another rewrite

### Repeated but harmless action
- task definition command alignment script was run twice
- no drift introduced
- final command values remained correct


### Resolution — module execution alignment
Validated fix:
- Dockerfile and ECS command were changed from script-path execution to module execution

Replaced pattern:
- `python services/<service>/worker.py`

Working pattern:
- `python -m services.<service>.worker`

Validated result:
- local Python 3.11 container execution succeeded
- ECS Fargate execution succeeded
- CloudWatch logs confirmed successful payload processing

### Resolution — ECS runtime alignment
Validated AWS runtime values:
- cluster:
  - `ocr-rebuild-cluster`
- task definitions:
  - `financial-management-worker-task-prod`
  - `fica-compliance-worker-task-prod`
  - `credit-decision-worker-task-prod`
- security group:
  - `sg-0ad48d96d00af793f`
- validated subnets:
  - `subnet-08bb8a5fb305fb74a`
  - `subnet-075eb014db65f8d57`

Validated image/tag state:
- ECR image tag `:phase5` exists for all three worker repos

### Resolution — decision engine AWS bridge alignment
Resolved drift in `services/decision_engine/engine.py`:
- corrected cluster name
- corrected task definition names
- added security groups
- replaced placeholder subnet config with validated subnet IDs
- enforced JSON payload serialization for `PAYLOAD`
- enforced explicit boto3 region usage
- normalized AWS response excerpt to JSON-safe values for persistence

Validated result:
- `execute_service_family(...)` succeeded in `EXECUTION_MODE=aws` for:
  - financial_management
  - fica
  - credit_decision

### Resolution — orchestration persistence validation
Validated under Python 3.11 container runtime:
- `api.requests_results.routes.create(...)` executed successfully in `EXECUTION_MODE=aws`
- request passed enforcement
- downstream ECS execution launched successfully
- orchestration record persisted successfully to SQLite
- stored request was read back successfully with JSON-safe downstream execution state

### Resolution — execution plan enforcement v1

Validated implementation:
- `services/decision_engine/frontend_request_orchestrator.py` now builds a persisted `execution_plan`
- validation, enforcement, downstream execution, and result finalization now run through plan-driven orchestration
- per-stage results are persisted under `stage_results`
- request/result state is now derived from plan finalization output
- current API behaviour remains compatible for:
  - `create`
  - `status`
  - `result`
  - `remediation`
  - `rerun`

Validated stage model:
- `consent_check`
- `document_check`
- `enforcement_decision`
- `downstream_execution`
- `result_finalize`

Validated outcomes:
- blocked requests terminate with plan status:
  - `blocked`
- successful AWS-mode requests terminate with plan status:
  - `completed`
- downstream execution is now recorded as a plan stage result
- final request status and result status are now plan-derived

Controlled limitation:
- execution plan enforcement is currently implemented for the frontend/API orchestration path only
- broader OCR pipeline-wide execution-plan enforcement remains a separate governed scope

### Resolution — execution plan propagation and worker enforcement
Validated implementation:
- frontend orchestration now propagates `execution_plan` into downstream ECS payloads
- frontend orchestration now propagates `orchestration_context` into downstream ECS payloads
- downstream frontend service-family workers now emit `execution_plan_ack`
- downstream frontend service-family workers now enforce strict execution-plan validation
- invalid payloads are rejected safely with structured validation errors
- valid payloads continue to execute normally

Validated scope:
- `financial_management`
- `fica`
- `credit_decision`

Validated worker enforcement rules:
- `execution_plan` required
- `execution_plan.plan_version` required
- supported plan version enforced
- `execution_plan.service_family` must match expected service family
- `orchestration_context.current_stage` must equal `downstream_execution`

Validated runtime outcomes:
- local worker validation passed for valid and invalid payloads
- AWS ECS validation confirmed successful execution for valid payloads
- AWS ECS validation confirmed controlled rejection for invalid payloads missing `execution_plan`
- CloudWatch logs confirmed `execution_plan_ack` and validation output

### Resolution — finalization classification hardening
Validated implementation:
- frontend finalization now distinguishes:
  - `blocked`
  - `available`
  - `rejected`
  - `execution_failed`
- `finalization_reason` is now persisted in orchestration records
- `finalizationReason` is now surfaced through status/result responses
- fallback worker `status=executed` is now classified as success
- fallback worker `status=rejected` is now classified as governed rejection

Validated finalization reasons:
- `pre_execution_enforcement_failed`
- `downstream_execution_succeeded`
- `downstream_worker_rejected_payload`
- `downstream_execution_failed`

### Remaining controlled note
CloudShell host runtime remains:
- Python 3.9

Governed implication:
- host-side direct validation of Python 3.10+ syntax remains unreliable
- Python 3.11 container validation remains mandatory for runtime-sensitive checks

---

## 6. Current Safe Restart Point

A new developer chat should resume from:

### Stable, completed foundation
- all frontend/API scaffolding completed
- orchestration completed
- hard enforcement completed
- SQLite persistence completed
- AWS bridge completed
- ECS repos/log groups/task definitions created

### Immediate unresolved runtime area
- worker container import/path packaging issue
- images build successfully
- containers do not yet run successfully
- images have not yet been pushed to ECR
- ECS live task execution has not yet been validated end-to-end

---

## 7. Mandatory Next Step

The next developer must NOT jump directly to:
- ECR push
- ECS run-task live testing
- task definition redesign

The next step must be:

### Inspect and fix Python package/import resolution in built worker images

Specifically:
- inspect container filesystem under `/app`
- inspect whether `services` is importable
- determine whether to:
  - add package init structure
  - run with `python -m ...`
  - adjust `WORKDIR`
  - adjust container command
  - adjust `PYTHONPATH`
- make the smallest controlled change only after evidence

---

## 8. Governing Rules for Next Developer

The next developer must:
- read:
  - `docs/00_program_control/platform_state_handover_phase5.md`
  - `docs/00_program_control/known_gaps_and_improvement_register.md`
  - `docs/20_service_design/runtime_and_dependency_standard.md`
  - this handover file
- not repeat AWS CLI runtime invocation logic
- not assume CloudShell credentials exist inside Docker test containers
- not assume registered task definitions are runnable
- not redesign current orchestration contract
- not replace hard enforcement or SQLite persistence unless explicitly instructed

---

## 9. Current Gap Position

Most relevant live gaps now:
- GAP-003 — downstream execution still only partially complete
- GAP-015 — persistence is structured but not yet audit-grade append-only
- GAP-019 — observability still limited
- packaging/import resolution gap for new worker containers is active and must be handled next

