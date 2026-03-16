# Phase 4 Implementation Design – Reference Diagrams

## 9. Reference Diagrams

### 9.1 AWS Architecture Diagram
- PNG Diagram: [Phase 4 AWS Architecture](https://s3.console.aws.amazon.com/s3/object/ocr-rebuild-program/docs/01_architecture/phase4_reference_diagrams.png)
- Shows S3 buckets (Original, Processed, Results, Logs, Manifests), Lambda/ECS tasks for preprocessing, OCR, table extraction, logo recognition, fraud detection, aggregation, manifest updates, and CloudWatch logging.

### 9.2 Step Functions Orchestration Diagram
- Included in the same PNG above.
- Shows Step Functions fan-out per document/page, Map states, retries, and aggregation flow.

### 9.3 Notes
- Diagrams are now centralized in S3 for developers.
- All buckets, functions, and orchestration flows are reflected.
- Developers can download the PNG for local reference or documentation purposes.

