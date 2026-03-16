# Phase 4 Implementation Design – Lambda & ECS Function Specifications

## 3. Lambda & ECS Function Specifications

### 3.1 General Conventions
- Function Naming: <pipeline>-lambda-<function>-<env>
- ECS Task Naming: <pipeline>-ecs-task-<env>
- Environment Variables: Store paths, bucket names, DB connections, feature flags
- Logging: CloudWatch log groups `/aws/lambda/<function-name>`, X-Ray enabled
- Compliance Notes: Mask PII, ephemeral /tmp cleared after execution, no sensitive data in logs

### 3.2 Preprocessing Pipeline
| Function | Runtime | Memory | Timeout | Trigger | Notes |
|----------|--------|--------|--------|--------|------|
| preprocessing-lambda-rotate | Python 3.11 | 512 MB | 3 min | S3 object upload | Rotate scanned documents |
| preprocessing-lambda-crop | Python 3.11 | 512 MB | 3 min | S3 object upload | Crop margins |
| preprocessing-lambda-contrast | Python 3.11 | 512 MB | 3 min | S3 object upload | Enhance contrast |

### 3.3 OCR Pipeline
| Function | Runtime | Memory | Timeout | Trigger | Notes |
|----------|--------|--------|--------|--------|------|
| ocr-lambda-tesseract-light | Python 3.11 | 1024 MB | 10 min | Step Function Map / SQS | Small documents, single language |
| ocr-ecs-task-tesseract-heavy | ECS/Fargate | 2 vCPU / 4 GB | 60 min | Step Function | Large/multi-language batch processing |

### 3.4 Table Extraction Pipeline
| Function | Runtime | Memory | Timeout | Trigger | Notes |
|----------|--------|--------|--------|--------|------|
| table-extraction-lambda | Python 3.11 | 1024 MB | 10 min | Step Function / SQS | Detect tables, convert to JSON |
| table-extraction-ecs-task | ECS/Fargate | 2 vCPU / 4 GB | 60 min | Step Function | Large table/multi-page PDFs |

### 3.5 Logo / Template Recognition
| Function | Runtime | Memory | Timeout | Trigger | Notes |
|----------|--------|--------|--------|--------|------|
| logo-lambda-recognition | Python 3.11 | 512 MB | 5 min | Step Function | Small logo matching |
| logo-ecs-task | ECS/Fargate | 2 vCPU / 4 GB | 30 min | Step Function | Heavy recognition |

### 3.6 Fraud Detection
| Function | Runtime | Memory | Timeout | Trigger | Notes |
|----------|--------|--------|--------|--------|------|
| fraud-lambda-score | Python 3.11 | 1024 MB | 10 min | Step Function / SQS | Risk scoring |
| fraud-ecs-task | ECS/Fargate | 2 vCPU / 4 GB | 60 min | Step Function | Complex ML scoring |

### 3.7 Aggregation / Canonical Output
| Function | Runtime | Memory | Timeout | Trigger | Notes |
|----------|--------|--------|--------|--------|------|
| aggregation-lambda | Python 3.11 | 1024 MB | 10 min | Step Function completion | Consolidate outputs, update manifest |

