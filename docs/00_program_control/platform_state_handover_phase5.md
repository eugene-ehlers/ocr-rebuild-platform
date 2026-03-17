# OCR Rebuild Platform
# Platform State Handover - Start of Phase 5

## 1. Purpose

This document describes the current system state at the completion of Phase 4.

It enables a new AI Chat Manager to begin Phase 5 deployment work immediately without re-investigating the repository.

## 2. Repository Location

Working repository root:

`/home/cloudshell-user/ocr-rebuild-platform`

Key structure:

- `services/`
- `infrastructure/`
- `tests/`
- `scripts/`
- `docs/`

## 3. Implemented Pipeline

The OCR processing pipeline contains seven stages.

### Stage 1 - Manifest Generation

Runtime:

AWS Lambda

Location:

`services/manifest_generator/`

Purpose:

- create document manifest
- register pipeline execution

### Stage 2 - Preprocessing

Runtime:

AWS Lambda

Location:

`services/preprocessing/`

Functionality:

- grayscale
- autocontrast
- median filtering
- processed image storage

### Stage 3 - OCR

Runtime:

ECS Fargate

Location:

`services/ocr/`

Engine:

Tesseract

Dependencies:

- `pytesseract`
- `tesseract-ocr`
- `Pillow`
- `opencv-python-headless`

### Stage 4 - Table Extraction

Runtime:

ECS Fargate

Location:

`services/table_extraction/`

Current method:

- heuristic text table detection

### Stage 5 - Logo / Template Recognition

Runtime:

ECS Fargate

Location:

`services/logo_recognition/`

Current method:

- template keyword detection

### Stage 6 - Fraud Detection

Runtime:

ECS Fargate

Location:

`services/fraud_detection/`

Current heuristics:

- blank pages
- repeated characters
- duplicate page text
- low text volume

### Stage 7 - Aggregation

Runtime:

ECS Fargate

Location:

`services/aggregation/`

Output:

- canonical document
- manifest update
- document summary metrics

## 4. Runtime Contracts


### Authoritative Contract

All pipeline stages now operate on a **normalized execution payload** defined in:

`docs/03_data_model/pipeline_execution_contract.md`

This contract governs:

- full payload propagation across all stages
- enrichment-only transformations (no payload reduction)
- standardized control structures:
  - `manifest_update`
  - `execution_state`
  - `service_status`
  - `pipeline_history`

### Key Principle

Each stage must:

- receive the full execution payload
- enrich the payload (never replace it)
- return the full payload to the next stage

### Current Implementation Detail (Temporary)

ECS workers currently use **file-based IO**:

- `/tmp/<stage>_input.json`
- `/tmp/<stage>_output.json`

This is:

- a **container execution mechanism only**
- **NOT the inter-stage contract**

Future orchestration updates will move toward direct payload passing via Step Functions.

### Current Alignment Status

- All workers have been **normalized to the execution contract**
- Orchestration (Step Functions) is **not yet fully aligned**
- Payload loss risk exists until orchestration alignment is completed
## 5. Infrastructure Configuration

Infrastructure definitions exist under:

`infrastructure/`

Includes:

### ECS Task Definitions

`infrastructure/ecs/`

Workers defined:

- `ocr`
- `table_extraction`
- `logo_recognition`
- `fraud_detection`
- `aggregation`

### Lambda Configurations

`infrastructure/lambda/`

Functions:

- `manifest_generator`
- `preprocessing`

### Step Functions


Pipeline definition:

`infrastructure/step_functions/master_pipeline/ocr_pipeline.asl.json`

### Current State

The Step Functions orchestration defines the pipeline flow:

- `GenerateManifest`
- `Preprocessing`
- `OCR`
- `TableExtraction`
- `LogoTemplateRecognition`
- `FraudDetection`
- `Aggregation`

### Important Alignment Note (Critical)

The orchestration structure (states, sequencing, retries, catch blocks) is implemented.

However:

- Step Functions is **NOT yet fully aligned with the execution contract**
- It may:
  - pass partial payloads
  - overwrite instead of enrich
  - not preserve `execution_state`, `service_status`, or `pipeline_history`

### Risk

This creates a **real risk of payload loss or state inconsistency** during execution.

### Required Next Step (Phase 5)

Step Functions must be updated to:

- pass full payload between all states
- ensure all stages:
  - enrich payload
  - return full payload
- preserve:
  - `manifest_update`
  - `execution_state`
  - `service_status`
  - `pipeline_history`

Until this is completed:

- local pipeline = reliable
- AWS pipeline = **not yet fully safe for production execution**
### Migration Status (Execution Handoff)

The platform is currently in a controlled migration from:

- implicit state passing / local worker file handoff assumptions

to:

- explicit S3-based execution payload handoff between orchestrated stages

Authoritative design references:

- `docs/03_data_model/pipeline_execution_contract.md`
- `docs/03_data_model/pipeline_s3_payload_contract.md`
- `docs/02_aws_environment/phase5_orchestration_handoff_design.md`

#### Current migration state

| Stage boundary | Handoff model | Status |
| --- | --- | --- |
| Manifest Generation -> Preprocessing | Direct Step Functions / Lambda payload | Stable |
| Preprocessing -> OCR | S3 payload handoff | Implemented in repo |
| OCR -> Table Extraction | S3 payload handoff | Not yet implemented |
| Table Extraction -> Logo Recognition | S3 payload handoff | Not yet implemented |
| Logo Recognition -> Fraud Detection | S3 payload handoff | Not yet implemented |
| Fraud Detection -> Aggregation | S3 payload handoff | Not yet implemented |

#### Important operational meaning

- worker contracts are normalized end to end
- local pipeline is contract-aligned and stable
- AWS orchestration is only partially migrated to S3 payload handoff
- only the Preprocessing -> OCR bridge is currently implemented in orchestration code

#### Production readiness interpretation

The platform must not be treated as fully production-ready until all ECS stage boundaries are migrated to the S3 payload handoff model and validated in AWS.

## 6. Containerization

Each ECS worker contains:

- `Dockerfile`
- `requirements.txt`
- worker code

OCR Dockerfile includes:

- `tesseract-ocr`
- `pytesseract`

## 7. Testing

### Unit Tests

Location:

`tests/unit/`

Validates:

- pipeline stage contracts
- schema alignment

### Integration Tests

Location:

`tests/integration/`

Validates:

- end-to-end pipeline execution

### Local Pipeline Runner

Location:

`scripts/run_local_pipeline.py`

Simulates the entire pipeline locally.

Successful run example:

- `manifest_status: saved`
- `page_count: 1`
- `tables_detected: 1`
- `logos_detected: 1`
- `fraud_flags_detected: 0`

## 8. Current Commit State

Recent commits show structured pipeline construction.

Example:

- runtime contracts hardened
- orchestration hardened
- aggregation summary
- fraud detection
- logo recognition
- table extraction
- OCR
- preprocessing
- manifest persistence
- pipeline scaffold

The repository is stable and deployable.

## 9. Phase 4 Completion Status

Phase 4 delivered:

- complete pipeline architecture
- working local pipeline
- containerized ECS workers
- Lambda stages
- Step Functions skeleton
- infrastructure definitions
- test coverage

The platform is ready for AWS deployment work.

## 10. Phase 5 Objective

Phase 5 will deploy the platform to AWS.

Tasks will include:

- Create ECR repositories
- Build container images
- Push images to ECR
- Register ECS task definitions
- Create ECS cluster
- Deploy Step Functions
- Execute first AWS pipeline run

## 11. Phase 5 Start Point

Before starting Phase 5 the new AI manager must inspect:

- `git status`
- `git log`
- `find services`
- `find infrastructure`

This confirms repository integrity.

---

## IAM Runtime Roles (Phase 5 Deployment Baseline)

The OCR rebuild platform uses dedicated runtime IAM roles to enforce least-privilege access across Lambda, ECS workers, and Step Functions orchestration.

All roles were deployed during Phase 5 infrastructure initialization.

### Lambda Runtime Role

Role name:

ocr-rebuild-lambda-role

Purpose:

Execution role for Lambda functions responsible for:

- manifest generation
- preprocessing orchestration

Permissions include:

- CloudWatch logging
- DynamoDB access to `ocr-rebuild-manifest-store`
- S3 read/write access to:
  - `ocr-rebuild-original`
  - `ocr-rebuild-processed`
- KMS encryption/decryption using key:

alias/ocr-rebuild-platform


### ECS Worker Runtime Role

Role name:

ocr-rebuild-ecs-task-role

Purpose:

Runtime role used by all ECS Fargate workers:

- OCR worker
- Table extraction worker
- Logo recognition worker
- Fraud detection worker
- Aggregation worker

Permissions include:

- CloudWatch logging
- S3 access to:
  - `ocr-rebuild-original`
  - `ocr-rebuild-processed`
  - `ocr-rebuild-results`
- DynamoDB access to manifest store
- KMS encryption/decryption using the OCR rebuild key


### ECS Execution Role

Role name:

ocr-rebuild-ecs-execution-role

Purpose:

Infrastructure execution role used by ECS Fargate to:

- pull container images from ECR
- write container logs to CloudWatch

Permissions include:

- ECR image pull actions
- CloudWatch log stream creation and log event writes


### Step Functions Orchestration Role

Role name:

ocr-rebuild-stepfunctions-role

Purpose:

Runtime role used by the master OCR pipeline Step Functions state machine.

Permissions include:

- invoking Lambda functions
- running ECS tasks
- passing ECS task roles
- describing ECS cluster state


### Security Boundary

All runtime components operate inside the encryption boundary defined by:

KMS key alias:

alias/ocr-rebuild-platform

This key encrypts:

- S3 runtime buckets
- DynamoDB manifest store
- pipeline artifacts containing derived document data


### IAM Source of Truth

IAM policies and trust relationships are stored in the repository:

infrastructure/iam/

Files include:

- lambda-trust-policy.json
- lambda-runtime-policy.json
- ecs-task-trust-policy.json
- ecs-task-runtime-policy.json
- ecs-execution-policy.json
- stepfunctions-trust-policy.json
- stepfunctions-runtime-policy.json

These files represent the canonical infrastructure-as-code baseline for IAM in the OCR rebuild platform.


---

## Phase 5 Deployment Progress (Live AWS State)

The following deployment components have been completed and verified in AWS.

### Security and Storage Baseline
- Customer-managed KMS key created:
  - `alias/ocr-rebuild-platform`
- DynamoDB manifest store created:
  - `ocr-rebuild-manifest-store`
  - KMS encrypted
  - point-in-time recovery enabled
- S3 runtime buckets created and hardened:
  - `ocr-rebuild-original`
  - `ocr-rebuild-processed`
  - `ocr-rebuild-results`
  - `ocr-rebuild-logs`
- All runtime buckets:
  - use SSE-KMS
  - use the OCR platform KMS key
  - have versioning enabled

### ECR Deployment State
Repositories created and hardened:
- `ocr-worker`
- `table-extraction-worker`
- `logo-recognition-worker`
- `fraud-detection-worker`
- `aggregation-worker`

Repository baseline:
- immutable tags
- scan on push enabled
- KMS encryption enabled

### Container Image State
Images built and pushed:
- `ocr-worker:phase5`
- `table-extraction-worker:phase5`
- `logo-recognition-worker:phase5`
- `fraud-detection-worker:phase5`
- `aggregation-worker:phase5`

### ECS Deployment State
Cluster created:
- `ocr-rebuild-cluster`

Task definitions registered:
- `ocr-worker-task-prod:2`
- `table-extraction-worker-task-prod:1`
- `logo-recognition-worker-task-prod:1`
- `fraud-detection-worker-task-prod:1`
- `aggregation-worker-task-prod:1`

Task definition alignment completed:
- `ACCOUNT` placeholders resolved
- `REGION` placeholders resolved
- image references changed from `:latest` to `:phase5`
- OCR bucket names aligned to:
  - `ocr-rebuild-processed`
  - `ocr-rebuild-results`

### Lambda Deployment State
Functions deployed and active:
- `manifest-generator-lambda-prod`
- `preprocessing-lambda-prod`

Final verified configuration:

#### manifest-generator-lambda-prod
- runtime: python3.11
- timeout: 60
- memory: 512
- environment:
  - `MANIFEST_TABLE=ocr-rebuild-manifest-store`

#### preprocessing-lambda-prod
- runtime: python3.11
- timeout: 300
- memory: 1024
- environment:
  - `PROCESSED_BUCKET=ocr-rebuild-processed`

### Packaging Correction
A packaging correction was applied to preprocessing Lambda deployment inputs.

Change made:
- removed `opencv-python-headless` from `services/preprocessing/requirements.txt`

Reason:
- dependency was not imported by the current preprocessing Lambda code
- dependency caused unnecessary package bloat and CloudShell disk pressure during build
- final package now matches actual runtime requirements


### Remaining Phase 5 Work

The following Phase 5 tasks remain open:

#### 1. Step Functions Contract Alignment (Critical)

Although Step Functions is defined and partially deployed, it is **not yet aligned with the execution contract**.

Required actions:

- ensure full payload propagation between all states
- prevent payload overwrite between stages
- enforce enrichment-only stage behavior
- validate preservation of:
  - `manifest_update`
  - `execution_state`
  - `service_status`
  - `pipeline_history`

#### 2. First End-to-End AWS Pipeline Execution

- execute full pipeline via Step Functions
- validate:
  - no payload loss
  - correct stage sequencing
  - correct service_status updates
  - correct execution_state progression

#### 3. Manifest and Canonical Output Verification

- verify DynamoDB manifest entries:
  - pipeline_history completeness
  - retry_count correctness
  - partial_execution_flags behavior

- verify canonical output:
  - page-level enrichment preserved
  - aggregation summary correctness
  - fraud/table/logo outputs correctly reflected

#### 4. Failure and Retry Scenario Validation

- simulate controlled failures in:
  - OCR
  - table extraction
  - fraud detection

- confirm:
  - Step Functions retry behavior
  - manifest reflects partial execution
  - pipeline continues where expected

---

### Current Risk Status

- Local pipeline: **stable and contract-aligned**
- AWS deployment: **infrastructure complete but orchestration not yet safe**
- Production readiness: **BLOCKED until Step Functions alignment is completed**
