# OCR Rebuild Program
# Developer Prompt Library (Amazon Q)

## Purpose

This document contains standardized prompts developers should use when interacting with Amazon Q Developer to generate code for the OCR Rebuild platform.

Using consistent prompts ensures:

- architecture compliance
- schema compliance
- reproducible development
- faster onboarding for new developers

All prompts assume the developer is working inside the repository:

https://github.com/eugene-ehlers/ocr-rebuild-platform

---

# Prompt 1 — Generate Preprocessing Lambda

Prompt:

Generate a Python AWS Lambda function for the preprocessing pipeline.

Requirements:

Input: document pages stored in S3  
Output: normalized pages stored in the processed bucket  

Use schema definitions from:

docs/03_data_model/page_schema.json

Preprocessing operations include:

- skew correction
- contrast enhancement
- resolution normalization

Store metadata fields required by:

docs/03_data_model/canonical_document_schema.json

Lambda must:

- read from S3
- process page images
- update manifest
- write output to processed bucket

---

# Prompt 2 — Generate OCR Worker

Prompt:

Generate the OCR pipeline service.

Requirements:

Use ECS Fargate container.

Input:

preprocessed page images from S3.

Output:

OCR text results conforming to:

docs/03_data_model/ocr_output_schema.json

Support:

- multi-engine routing
- confidence scoring
- fallback OCR engine

Reference architecture:

docs/05_ocr_engines/engine_strategy.md

---

# Prompt 3 — Generate Table Extraction Service

Prompt:

Generate a Python service for table extraction.

Requirements:

Input:

OCR page outputs.

Output:

structured table JSON matching:

docs/03_data_model/entity_extraction_schema.json

Tables must be nested within the canonical document schema.

---

# Prompt 4 — Generate Fraud Detection Pipeline

Prompt:

Generate a fraud detection service for documents.

Requirements:

Use inputs:

OCR results  
logo detection  
metadata  

Output must match:

docs/03_data_model/fraud_findings_schema.json

Detection includes:

- structural anomalies
- visual tampering
- semantic inconsistencies

---

# Prompt 5 — Generate Step Functions Orchestration

Prompt:

Generate an AWS Step Functions workflow for the OCR pipeline.

Stages:

1. Manifest generation
2. Preprocessing
3. OCR
4. Table extraction
5. Logo/template recognition
6. Fraud detection
7. Aggregation
8. Notification

Reference architecture:

docs/09_orchestration/step_functions_master_flow.md

Ensure:

- retry policies
- error handling
- parallel processing

---

# Prompt 6 — Generate Aggregation Service

Prompt:

Generate a service that aggregates pipeline outputs into the canonical document schema.

Inputs:

OCR output  
tables  
logos  
fraud flags  

Output must match:

docs/03_data_model/canonical_document_schema.json

Store final result in:

results S3 bucket.

---

# Prompt 7 — Generate Infrastructure

Prompt:

Generate infrastructure definitions for the OCR pipeline using AWS services.

Include:

Lambda functions  
ECS tasks  
Step Functions  
IAM roles  
CloudWatch monitoring  

Reference architecture:

docs/02_aws_environment/phase4_implementation_design.md

Follow naming conventions defined in the environment documentation.

---

# Developer Guidance

When prompting Amazon Q:

1. Always reference schema files
2. Always reference architecture documents
3. Generate code inside the appropriate repository directory
4. Follow naming conventions defined in the AWS environment documents

This ensures generated code complies with the system design.

