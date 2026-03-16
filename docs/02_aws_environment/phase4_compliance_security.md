# Phase 4 Implementation Design – Compliance & Security

## 8. Compliance & Security

### 8.1 Data Encryption
- **At Rest:**
  - S3 buckets: SSE-KMS using customer-managed key `alias/ocr-rebuild-platform`
  - DynamoDB manifest store: KMS encryption using customer-managed key `alias/ocr-rebuild-platform`
  - RDS (if later introduced): KMS encryption and Secrets Manager-managed credentials
- **In Transit:**
  - HTTPS/TLS 1.2+ enforced for all S3, API, and internal service communications
- **Secrets Management:**
  - AWS Secrets Manager for DB credentials, API keys, encryption keys

### 8.2 Access Control
- **IAM Roles:**
  - Least privilege principle applied per Lambda, ECS, Step Functions
  - CI/CD roles scoped for build/deploy only
  - KMS key access limited to approved OCR runtime and deployment roles
- **Security Groups:**
  - Lambda/ECS limited to required S3, DynamoDB, and Step Functions endpoints
  - No unrestricted internet access

### 8.3 Data Retention & Lifecycle
- **POPIA/GDPR-aligned retention:**
  - Original documents retained only as needed
  - Preprocessed/OCR/results archived according to controlled lifecycle policy
  - Logs deleted after 30–60 days
- **Versioning and recovery:**
  - S3 runtime buckets use versioning for recovery and audit protection
  - DynamoDB manifest store uses point-in-time recovery
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
- Original uploaded documents are stored only in the secured original bucket
- Processed page artifacts and derived outputs are stored in separately secured buckets
- Manifest state is stored in DynamoDB as structured execution metadata, not raw document binaries
- PII removed or masked from logs and notifications
- Only required metadata stored in manifests
- Step Functions and Lambda do not persist sensitive raw data beyond pipeline execution
- Canonical outputs and derived text must be treated as sensitive data and protected accordingly

### 8.6 Implemented Security Baseline for OCR Rebuild
- **Customer-managed KMS key:**
  - Alias: `alias/ocr-rebuild-platform`
  - Purpose: dedicated encryption boundary for OCR rebuild PII workloads
- **DynamoDB manifest store:**
  - Table: `ocr-rebuild-manifest-store`
  - Encryption: KMS with `alias/ocr-rebuild-platform`
  - Recovery: point-in-time recovery enabled
- **S3 runtime buckets:**
  - `ocr-rebuild-original`
  - `ocr-rebuild-processed`
  - `ocr-rebuild-results`
  - `ocr-rebuild-logs`
  - Encryption: SSE-KMS with `alias/ocr-rebuild-platform`
  - Bucket keys: enabled
  - Versioning: enabled
- **Storage separation principle:**
  - S3 stores source documents, processed artifacts, results, and logs
  - DynamoDB stores manifest state, retry state, and execution history
  - This separation reduces unnecessary duplication of sensitive document content in metadata stores

### 8.7 Compliance Notes per Pipeline
| Pipeline | Compliance Consideration |
|----------|-------------------------|
| Preprocessing | Ephemeral processing; no PII stored in logs; processed artifacts encrypted in S3 |
| OCR | Derived text treated as sensitive; raw documents remain in secured S3 storage |
| Table Extraction | Tables stored as encrypted derived outputs; sensitive fields masked if needed |
| Logo Recognition | Only template matches stored; no full image exposure outside secured runtime storage |
| Fraud Detection | Risk scores stored; raw analysis kept ephemeral where possible |
| Aggregation | Canonical JSON only; PII masked where required; audit trail recorded in manifest state |
