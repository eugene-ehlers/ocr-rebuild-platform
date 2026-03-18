# OCR Rebuild Platform
# Phase 5 - AWS Deployment Execution Plan

## 1. Purpose

Phase 5 deploys the completed OCR pipeline platform to AWS so the system can execute real document processing workflows.

The deployment will create and configure:

- ECR container repositories
- ECS cluster
- ECS task definitions
- Lambda functions
- Step Functions orchestration
- S3 document and results buckets
- DynamoDB manifest store
- IAM execution roles

## 2. Phase 5 Deployment Sequence

Deployment must follow the exact order below.

Changing the order will break the pipeline.

1. Create S3 buckets
2. Create DynamoDB manifest table
3. Create IAM roles
4. Create ECR repositories
5. Build container images
6. Push images to ECR
7. Create ECS cluster
8. Register ECS task definitions
9. Deploy Lambda functions
10. Deploy Step Functions state machine
11. Execute first pipeline run

## 3. Required AWS Resources

### S3 Buckets

Required buckets:

- `ocr-rebuild-original`
- `ocr-rebuild-processed`
- `ocr-rebuild-results`
- `ocr-rebuild-logs`

Purpose:

| Bucket | Purpose |
|---|---|
| original | uploaded source documents |
| processed | preprocessing output |
| results | stage outputs and canonical outputs |
| logs | pipeline logs |

Operational baseline:

- versioning enabled where appropriate
- server-side encryption enabled with KMS-managed keys
- all buckets deployed in the same AWS region
- lifecycle and retention policies aligned to compliance requirements

### DynamoDB Manifest Store

Required table:

- `ocr-rebuild-manifest-store`

Purpose:

- manifest persistence
- pipeline state tracking
- retry tracking
- execution history updates

Operational baseline:

- server-side encryption enabled
- point-in-time recovery enabled
- least-privilege IAM access only

## 4. ECR Repository Creation

Repositories must be created for every ECS worker.

Required repositories:

- `ocr-worker`
- `table-extraction-worker`
- `logo-recognition-worker`
- `fraud-detection-worker`
- `aggregation-worker`

Operational baseline for all OCR rebuild ECR repositories:

- image tag mutability: `IMMUTABLE`
- image scanning on push: enabled
- encryption: KMS
- KMS key: `alias/ocr-rebuild-platform`

Example command:

    aws ecr create-repository --repository-name ocr-worker --image-tag-mutability IMMUTABLE --image-scanning-configuration scanOnPush=true --encryption-configuration encryptionType=KMS,kmsKey=alias/ocr-rebuild-platform

## 5. Container Image Build

Each worker image must be built locally.

Example:

    docker build --platform linux/amd64 -t ocr-worker services/ocr

Then tag for ECR with both:
- a stable convenience tag where useful
- a required immutable deployment tag

Required immutable tag format:

    <phase>-<service>-<yyyymmdd>-<gitsha>

Example:

    docker tag ocr-worker ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/ocr-worker:phase5
    docker tag ocr-worker ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/ocr-worker:phase5-ocr-20260318-4522d81

Push the immutable deployment tag intended for task registration.

Repeat for all workers.

## 6. ECS Cluster Creation

Create the cluster:

    aws ecs create-cluster --cluster-name ocr-rebuild-cluster

Cluster runtime:
- AWS Fargate

## 7. ECS Task Registration

Task definitions already exist in:
- `infrastructure/ecs/`

Before registration:
- update task definition source to reference the immutable deployment tag
- verify image exists in ECR
- verify repo task definition source matches intended runtime artifact

Register each task.

Example:

    aws ecs register-task-definition --cli-input-json file://infrastructure/ecs/ocr/task-definition.json

Repeat for:
- `table_extraction`
- `logo_recognition`
- `fraud_detection`
- `aggregation`

## 8. Lambda Deployment

Lambda functions:
- `manifest-generator-lambda-prod`
- `preprocessing-lambda-prod`

Source locations:
- `services/manifest_generator`
- `services/preprocessing`

Deployment must include:
- runtime
- handler
- IAM role
- environment variables

## 9. Step Functions Deployment

State machine definition:
- `infrastructure/step_functions/master_pipeline/ocr_pipeline.asl.json`

Deploy using:
    aws stepfunctions create-state-machine

Configuration must reference:
- Lambda functions
- ECS cluster
- ECS task definitions

## 10. IAM Roles

Required roles:
- `ocr-rebuild-ecs-task-role`
- `ocr-rebuild-ecs-execution-role`
- `ocr-rebuild-lambda-role`
- `step-functions-role`

Permissions must include:
- S3
- ECS
- ECR
- CloudWatch
- Lambda
- logs:CreateLogStream
- logs:PutLogEvents

## 11. Region Standard

All resources must be deployed in the same AWS region.

Default region:
- `us-east-1`

## 12. First Pipeline Execution

Example execution:

    aws stepfunctions start-execution

Input:

    {
      "document_id": "test-doc-1",
      "source_uri": "s3://ocr-rebuild-original/test.pdf"
    }

## 13. Expected Execution Flow

- Upload document
- Manifest created
- Pages preprocessed
- OCR executed
- Tables extracted
- Logos detected
- Fraud checks executed
- Document aggregated
- Results stored

## 14. Success Criteria

Phase 5 is complete when:
- containers run successfully
- Step Functions completes execution
- canonical document produced
- manifest updated
- no pipeline stage failures

## 15. Operational Monitoring

Monitoring services:
- CloudWatch Logs
- ECS task status
- Step Functions execution history
- S3 output validation
- manifest state inspection
