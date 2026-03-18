# Versioning Strategy

Status: ACTIVE - CONTROLLED BASELINE

## 1. Purpose

Define the governed versioning and traceability standard for OCR Rebuild deployable artifacts, workflow definitions, and controlled releases.

This document is authoritative for:
- ECS image tags
- Lambda deployment artifact traceability
- task definition image references
- release reproducibility
- deployment auditability

## 2. Core Rule

Every deployable artifact must be traceable to:
- repo source state
- deployment intent
- deployment date
- exact immutable artifact identifier

No live deployment may rely only on a floating, reusable, or ambiguous identifier.

## 3. ECS Image Versioning Standard

### 3.1 Required tag classes

Each ECS image build may produce:

1. A stable convenience tag for human navigation or phase grouping, for example:
- `phase5`

2. A required immutable deployment tag used for task definition registration, in the format:
- `<phase>-<service>-<yyyymmdd>-<gitsha>`

Example:
- `phase5-ocr-20260318-4522d81`

### 3.2 Required deployment rule

Stable tags may exist in ECR, but ECS task definitions must reference the immutable deployment tag actually intended for runtime.

Stable tags must not be treated as sufficient deployment traceability.

### 3.3 Service naming rule

Service segment in the immutable tag must match the deployable component, for example:
- `ocr`
- `table-extraction`
- `logo-recognition`
- `fraud-detection`
- `aggregation`

### 3.4 Rebuild rule

If source changes after an image was pushed, a new immutable tag must be produced.
Existing tags must not be reused to represent new source state.

## 4. Lambda Artifact Versioning Standard

Lambda deployment packages must be traceable to:
- runtime version
- dependency build method
- repo source state
- deployment date

At minimum, Lambda deployment execution records must capture:
- function name
- runtime
- artifact build location
- deployment date
- git commit identifier where available

## 5. Workflow and Infrastructure Versioning

The following are controlled deployment artifacts and must be traceable to repo source state:
- Step Functions definitions
- ECS task definitions
- IAM policy source files
- deployment scripts
- buildspecs

Task definition source in `infrastructure/ecs/` must be updated before registration whenever a new immutable image tag is promoted.

## 6. Deployment Record Minimum

Each controlled deployment should be attributable to:
- component name
- target environment
- AWS region
- immutable artifact identifier
- git commit identifier
- deployment operator
- deployment date

## 7. Current Baseline Decision

Effective immediately, OCR Rebuild ECS image deployments must use:
- optional stable phase tag
- required immutable deployment tag containing git commit identifier

Task definitions must reference the immutable deployment tag, not only the stable phase tag.
