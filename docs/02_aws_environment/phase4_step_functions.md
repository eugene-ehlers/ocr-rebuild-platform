# Phase 4 Implementation Design – Step Functions Orchestration

## 4. Step Functions Orchestration

### 4.1 General Conventions
- State Machine Naming: <pipeline>-sf-<env>
- Execution Type: 
  - Express Workflows for high-volume/short tasks
  - Standard Workflows for long-running/critical tasks
- Fan-Out: Map state per document/page
- Partial Execution & Retry:
  - Retry: 3 attempts, exponential backoff
  - Catch: Log failed items, continue remaining
- Compliance: Sensitive PII handled in ephemeral memory, not logged

### 4.2 Preprocessing
- Map State: Rotate → Crop → Contrast
- Retries: 3 attempts, exponential backoff
- Catch: SNS `ocr-sns-errors-prod`, manifest `partial_failure`

### 4.3 OCR Pipeline
- Map State: Light OCR Lambda or Heavy OCR ECS task
- Conditional Branching: Small → Lambda, Large → ECS
- Retries: 2 for Lambda, 1 for ECS
- Partial Execution: Failed pages logged, manifest updated

### 4.4 Table Extraction
- Map State: Table extraction Lambda/ECS
- Retries: 2 Lambda, 1 ECS
- Catch: SNS errors, continue remaining documents

### 4.5 Logo / Template Recognition
- Map State: Lambda/ECS per document
- Retries: 2 Lambda, 1 ECS
- Catch: Failures logged, continue aggregation

### 4.6 Fraud Detection
- Map State: Lambda/ECS per document
- Retries: 1 Lambda, 1 ECS
- Catch: Flag failed documents in manifest, continue workflow

### 4.7 Aggregation / Canonical Output
- Sequential State: Wait for all prior stages
- Function: aggregation-lambda → canonical JSON, update manifest
- Notifications: Success → `ocr-sns-complete-prod`, Failures → `ocr-sns-errors-prod`

### 4.8 Observability
- X-Ray enabled for Lambda/ECS
- CloudWatch metrics: duration, failures, retries
- Alarms: SNS notifications for thresholds exceeded

