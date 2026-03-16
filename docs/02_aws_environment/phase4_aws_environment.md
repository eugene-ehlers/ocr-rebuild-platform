# Phase 4 Implementation Design – AWS Environment Setup

## 1. Purpose
Define concrete AWS infrastructure, Lambda/ECS functions, orchestration, S3 layout, CI/CD, logging, and compliance controls for Phase 4.

## 2. AWS Environment Setup

### 2.1 VPC and Networking
- VPC Name: vpc-ocr-rebuild-prod
- CIDR: 10.10.0.0/16
- Subnets:
  | Name | Type    | CIDR        | Purpose |
  |------|--------|------------|---------|
  | subnet-ocr-private-1 | Private | 10.10.1.0/24 | Lambda, Step Functions, ECS tasks |
  | subnet-ocr-private-2 | Private | 10.10.2.0/24 | Redundancy / high availability |

- Notes:
  - NAT Gateway eliminated; all S3/DynamoDB access via VPC endpoints
  - Security Groups:
    - sg-ocr-lambda → HTTPS to S3 endpoints only
    - sg-ocr-ecs → Internal traffic + Step Functions
    - sg-ocr-db → Private DB access from ECS/Lambda

### 2.2 IAM Roles & Policies
- Role Naming: <service>-role-<env>
- Roles per service:
  | Service | Role Name           | Permissions |
  |---------|-------------------|------------|
  | Lambda  | lambda-ocr-role-prod | S3 read/write, CloudWatch logs, X-Ray, SQS send/receive, Step Functions invoke |
  | Step Functions | sf-ocr-role-prod | Lambda invoke, SQS publish, CloudWatch logs |
  | ECS/Fargate | ecs-ocr-role-prod | S3 read/write, CloudWatch, ECR pull, Step Functions invoke |
  | CI/CD | ci-cd-ocr-role-prod | CodeBuild, CodePipeline, S3 deploy, Lambda update |

### 2.3 S3 Buckets
- Naming: <project>-<bucket-type>-<env> (project=ocr-rebuild)
- Buckets:
  | Bucket Name | Purpose |
  |-------------|---------|
  | ocr-rebuild-original-prod  | Raw uploaded documents |
  | ocr-rebuild-processed-prod | Preprocessed & OCR outputs |
  | ocr-rebuild-results-prod   | Canonical JSON outputs |
  | ocr-rebuild-logs-prod      | Lambda/Step Functions logs export |
  | ocr-rebuild-manifests-prod | Document manifests / metadata |

- Settings:
  - Versioning enabled
  - SSE-KMS encryption
  - Lifecycle policies:
    - Logs → delete after 30–60 days
    - Processed → archive to Glacier after 90 days
  - Intelligent-Tiering enabled for processed/results buckets

### 2.4 Messaging
- SQS Queues:
  - ocr-sqs-tasks-prod → all asynchronous pipeline messages
- SNS Topics:
  - ocr-sns-errors-prod → pipeline error notifications
  - ocr-sns-complete-prod → pipeline completion notifications

### 2.5 ECS / Fargate Clusters
- Cluster Name: ecs-ocr-prod
- Tasks: table extraction, logo recognition, fraud detection
- Auto-scaling: CPU/memory-based
- Network: Private subnets, security groups as above

