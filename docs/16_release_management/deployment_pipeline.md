# Deployment Pipeline

Status: DRAFT - CONTROLLED UPDATE APPLIED

## 1. Purpose

Define the governed build and deployment standard for OCR Rebuild deployable components.

This document is authoritative for:
- Lambda packaging
- ECS image build and publish
- artifact compatibility rules
- deployment promotion discipline

## 2. Deployment Targets

Current deployment targets:

- Lambda
  - manifest-generator-lambda-prod
  - preprocessing-lambda-prod
- ECS
  - ocr-worker
  - table-extraction-worker
  - logo-recognition-worker
  - fraud-detection-worker
  - aggregation-worker

## 3. Core Compatibility Rule

Build artifacts must be compatible with their deployment runtime.

No artifact may be deployed unless:
- runtime version is known
- dependency set is known
- build environment is compatible with runtime ABI where applicable

## 4. Lambda Packaging Standard

### 4.1 Runtime baseline
Current Lambda runtime baseline:
- Python 3.11

### 4.2 Build compatibility rule
Lambda zip artifacts that include native or compiled dependencies must be built in a Python 3.11-compatible build environment suitable for AWS Lambda runtime execution.

Examples of native-sensitive libraries include:
- Pillow
- numpy
- pandas
- scipy
- opencv-python
- lxml
- pyarrow
- cryptography
- any package shipping `.so` compiled extensions

### 4.3 Disallowed build method
AWS CloudShell using Python 3.9 must not be used to package Python 3.11 Lambda artifacts with native dependencies.

### 4.4 Dependency management rule
Lambda dependencies must be pinned where practical, especially for native or ABI-sensitive libraries.

### 4.5 Build artifact rule
`./build/*` contents are generated artifacts only.
They are not source of truth.
They must be reproducible from:
- `services/*`
- `requirements.txt`
- governed build scripts / buildspecs

### 4.6 Validation rule
Before Lambda deployment, verify:
- runtime target
- dependency versions
- no incompatible compiled artifacts
- artifact contents match current repo source

## 5. ECS Build Standard

### 5.1 Runtime rule
ECS runtime compatibility is governed by the container image, not the local shell Python version.

### 5.2 Image build rule
Images must be built from Dockerfiles in the service directories and pushed to ECR with immutable, traceable tags.

### 5.3 Tagging rule
Required tagging baseline:
- optional stable phase tag where appropriate
- required immutable deployment tag including commit identifier

Required immutable tag format:
- `<phase>-<service>-<yyyymmdd>-<gitsha>`

Example:
- `phase5-ocr-20260318-4522d81`

### 5.4 Task definition rule
ECS task definitions in `infrastructure/ecs/` must reference the intended immutable image tag before registration.

Task definitions must not be registered against only a stable convenience tag such as `phase5` when an immutable deployment tag exists.

### 5.5 Deployment verification rule
After image push and task definition registration, verify:
- the expected ECR image digest exists
- the task definition revision references the intended immutable tag
- the live workload is using that registered task definition revision

## 6. CI/CD Standard

### 6.1 Buildspec requirement
Placeholder buildspecs are not sufficient for production packaging.

The following must be implemented:
- `ci_cd/buildspecs/lambda_buildspec.yml`
- `ci_cd/buildspecs/ecs_buildspec.yml`

### 6.2 Lambda buildspec minimum requirements
Lambda buildspec must:
- use Python 3.11-compatible build environment
- install dependencies per Lambda package
- package only intended Lambda artifacts
- produce reproducible deployment zips
- prevent incompatible native dependency packaging

### 6.3 ECS buildspec minimum requirements
ECS buildspec must:
- build targeted service images
- tag with immutable identifiers
- push to ECR
- emit deployment metadata for task registration

## 7. Promotion and Deployment Discipline

Deployment order must remain controlled:
1. source update
2. build artifact generation
3. artifact validation
4. deployment
5. runtime verification

No live deployment may rely on stale build output.

## 8. Current Known Gap

Current repository state indicates:
- CI/CD buildspecs exist only as placeholders
- preprocessing Lambda packaging has already failed due to runtime/build mismatch
- formal build pipeline implementation is required before native-dependency Lambda deployment can be considered governed

## 9. Immediate Required Follow-on

Next controlled follow-on must:
- implement the Lambda packaging standard
- implement buildspec logic
- preserve immutable ECS artifact traceability during all worker redeployments
- redeploy and revalidate pipeline execution in governed order
