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

Workers communicate using JSON file input/output.

Example:

- `/tmp/<stage>_input.json`
- `/tmp/<stage>_output.json`

Environment variables define paths.

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

The orchestration includes:

- `GenerateManifest`
- `Preprocessing`
- `OCR`
- `TableExtraction`
- `LogoTemplateRecognition`
- `FraudDetection`
- `Aggregation`

Retry and catch logic are already implemented.

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

