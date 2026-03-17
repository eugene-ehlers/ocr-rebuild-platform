# Pipeline S3 Payload Contract

## 1. Purpose

Define how execution payloads are passed between ECS stages via S3.

This enables Step Functions to orchestrate ECS workers while preserving the full execution payload.

## 2. Core Principle

- The **entire execution payload** is stored and passed via S3
- No partial payloads
- No field loss
- Each stage:
  - reads full payload
  - enriches payload
  - writes full payload

## 3. S3 Bucket

Payload storage bucket:

`ocr-rebuild-results`

## 4. Key Structure

Each pipeline execution uses a deterministic structure:

`payloads/{manifest_id}/{stage}/payload.json`

Examples:

- `payloads/man-123/ocr/payload.json`
- `payloads/man-123/table_extraction/payload.json`
- `payloads/man-123/logo_recognition/payload.json`
- `payloads/man-123/fraud_detection/payload.json`
- `payloads/man-123/aggregation/payload.json`

## 5. Input Contract (ECS)

Each ECS worker receives:

- `INPUT_S3_BUCKET`
- `INPUT_S3_KEY`

Worker must:

- read full payload JSON from S3
- treat it as authoritative input

## 6. Output Contract (ECS)

Each ECS worker must write full enriched payload JSON to:

- `OUTPUT_S3_BUCKET`
- `OUTPUT_S3_KEY`

## 7. Step Functions Responsibility

Step Functions must:

- pass correct input S3 key to each stage
- track output S3 key per stage
- ensure next stage reads from previous stage output

## 8. Payload Integrity Rules

- payload must remain complete
- no field deletion allowed
- only enrichment allowed
- required fields must persist:
  - `manifest_update`
  - `execution_state`
  - `service_status`
  - `pipeline_history`

## 9. Failure Handling

If a stage fails:

- partial payload must still exist in S3
- manifest must reflect failure
- Step Functions decides retry or continue

## 10. Observability

S3 payloads provide:

- full audit trail
- replay capability
- debugging visibility
- validation checkpoints
