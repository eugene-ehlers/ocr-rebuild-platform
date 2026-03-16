# Phase 4 Implementation Design – Compliance & Security

## 8. Compliance & Security

### 8.1 Data Encryption
- **At Rest:**
  - S3 buckets: SSE-KMS
  - DynamoDB / RDS (if used): KMS encryption
- **In Transit:**
  - HTTPS/TLS 1.2+ enforced for all S3, API, and internal service communications
- **Secrets Management:**
  - AWS Secrets Manager for DB credentials, API keys, encryption keys

### 8.2 Access Control
- **IAM Roles:**
  - Least privilege principle applied per Lambda, ECS, Step Functions
  - CI/CD roles scoped for build/deploy only
- **Security Groups:**
  - Lambda/ECS limited to required S3, DB, Step Functions endpoints
  - No unrestricted internet access

### 8.3 Data Retention & Lifecycle
- **POPIA/GDPR-aligned retention:**
  - Original documents retained only as needed
  - Preprocessed/OCR/results archived to Glacier after 90 days
  - Logs deleted after 30–60 days
- **Ephemeral storage:**
  - Lambda `/tmp` cleared automatically after execution
  - ECS task temporary files removed post-task

### 8.4 Audit & Observability
- CloudTrail enabled for all account activity
- CloudWatch logs and metrics for each function/task
- X-Ray tracing for performance and execution tracking
- SNS notifications for errors, partial failures, or anomalies
- Manifest updates maintain execution state per document

### 8.5 PII & Sensitive Data Handling
- PII removed or masked from logs and notifications
- Only required metadata stored in manifests
- Step Functions and Lambda do not persist sensitive raw data beyond pipeline execution

### 8.6 Compliance Notes per Pipeline
| Pipeline | Compliance Consideration |
|----------|-------------------------|
| Preprocessing | Ephemeral; no PII stored in S3 logs |
| OCR | Only derived text stored; raw documents in S3 secured |
| Table Extraction | Tables stored in processed bucket; sensitive fields masked if needed |
| Logo Recognition | Only template matches stored; no full image exposure |
| Fraud Detection | Risk scores stored; raw analysis kept ephemeral |
| Aggregation | Canonical JSON only; PII masked; audit trail recorded |

