# Phase 4 Implementation Design – Pipelines

## 5. Pipelines

### 5.1 Preprocessing
- Input: `ocr-rebuild-original-prod`
- Functions: Rotate → Crop → Contrast (Lambda)
- Output: `ocr-rebuild-processed-prod`
- Manifest: `pipeline_status=processed`, `partial_execution=false`
- Notes: Ephemeral storage cleared, no PII in logs

### 5.2 OCR
- Input: Preprocessed docs
- Functions: Light OCR Lambda / Heavy OCR ECS
- Output: OCR text in `ocr-rebuild-processed-prod`
- Manifest: `ocr_status=completed` or `partial_failure=true`
- Notes: Fan-out via Step Functions, retries applied

### 5.3 Table Extraction
- Input: OCR docs
- Functions: Table extraction Lambda/ECS
- Output: JSON tables in `ocr-rebuild-processed-prod`
- Manifest: `tables_extracted=true` or `partial_failure=true`

### 5.4 Logo / Template Recognition
- Input: Preprocessed/OCR docs
- Functions: Logo recognition Lambda/ECS
- Output: Matches in `ocr-rebuild-processed-prod`
- Manifest: `logo_recognition=true` or `partial_failure=true`

### 5.5 Fraud Detection
- Input: Preprocessed & OCR docs
- Functions: Risk scoring Lambda/ECS
- Output: Risk scores in canonical JSON/manifest
- Manifest: `fraud_checked=true`, `risk_score=<value>`

### 5.6 Aggregation / Canonical Output
- Input: All prior outputs
- Function: aggregation-lambda
- Output: Canonical JSON in `ocr-rebuild-results-prod`
- Manifest: `pipeline_status=complete`, `all_partial_failures=false`
- Notifications: Success → `ocr-sns-complete-prod`, Failures → `ocr-sns-errors-prod`
- Notes: Compliance and PII masking enforced

