# Phase 4 Implementation Design – CI/CD & Deployment

## 7. CI/CD & Deployment

### 7.1 Folder Structure
Repository organized per pipeline and service:

/ocr-rebuild
 ├─ /preprocessing
 │    ├─ lambda/
 │    └─ ecs/
 ├─ /ocr
 │    ├─ lambda/
 │    └─ ecs/
 ├─ /table_extraction
 │    ├─ lambda/
 │    └─ ecs/
 ├─ /logo_recognition
 │    ├─ lambda/
 │    └─ ecs/
 ├─ /fraud_detection
 │    ├─ lambda/
 │    └─ ecs/
 ├─ /aggregation
 │    └─ lambda/
 ├─ /infrastructure
 │    ├─ step_functions/
 │    └─ cloudformation/
 └─ /ci_cd
      ├─ buildspecs/
      └─ pipeline_configs/

### 7.2 Git Workflow
- Branching:
  - main → production-ready
  - develop → integration/testing
  - feature branches → pipeline/function-specific changes
- Pull Request reviews mandatory
- Semantic version tagging per pipeline deployment

### 7.3 Lambda Deployment
- Package using AWS SAM or CodeBuild
- Environment variables via Parameter Store or Secrets Manager
- Deployment automated via CodePipeline:
  - Build → Package → Deploy → Validate
- Rollback enabled if post-deploy tests fail

### 7.4 ECS / Fargate Deployment
- Container build outside CloudShell for large OCR images
- Push images to ECR
- Update ECS Task Definitions via CodePipeline
- Auto-scaling per CPU/memory for each task type

### 7.5 Step Functions Updates
- Definitions stored in CloudFormation
- CodePipeline updates state machines after Lambda/ECS deployment
- Versioned and validated per update

### 7.6 Compliance & Security
- CI/CD builds do not store PII
- IAM roles scoped per pipeline
- Deployment logs stored in CloudWatch with retention policies

