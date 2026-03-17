# Phase 5 Orchestration Handoff Design

## 1. Purpose

Define the runtime handoff mechanism required for Step Functions to safely orchestrate ECS-based stages in the OCR Rebuild platform.

## 2. Confirmed Current State

The local pipeline runner now proves that the normalized execution payload works end to end across:

- manifest generation
- preprocessing
- OCR
- table extraction
- logo recognition
- fraud detection
- aggregation

However, current ECS workers still use local container file paths for execution:

- input via `/tmp/<stage>_input.json`
- output via `/tmp/<stage>_output.json`

## 3. Confirmed Orchestration Gap

AWS Step Functions with `ecs:runTask.sync` can wait for task completion, but it does not automatically return the worker's JSON output payload from local container files back into workflow state.

Therefore, the current pipeline cannot yet perform safe end-to-end payload propagation across ECS states in AWS.

## 4. Required Design Goal

A safe handoff mechanism must allow:

- Step Functions to provide the full normalized payload to an ECS stage
- the ECS stage to persist its enriched full payload
- Step Functions to retrieve that enriched payload for the next stage
- no payload loss between states
- preservation of:
  - `manifest_update`
  - `execution_state`
  - `service_status`
  - `pipeline_history`

## 5. Candidate Handoff Options

### Option A - S3 payload handoff (preferred)

Pattern:

- Step Functions writes or passes an S3 input key reference
- ECS worker reads payload JSON from S3
- ECS worker writes enriched payload JSON back to S3
- Step Functions invokes a small Lambda or direct retrieval step to load the enriched payload for the next state

Advantages:

- durable
- simple to inspect
- fits current file-based worker implementation with minimal adaptation
- good auditability
- easy recovery and replay

Risks:

- more S3 reads/writes
- requires explicit key management

### Option B - Lambda wrapper around ECS stages

Pattern:

- Step Functions invokes Lambda
- Lambda writes input payload to S3 or temp location
- Lambda starts ECS task
- Lambda waits / retrieves output
- Lambda returns enriched payload to Step Functions

Advantages:

- Step Functions stays simpler
- payload re-entry to workflow state is controlled

Risks:

- extra orchestration layer
- more moving parts
- more Lambda timeout/retry concerns

### Option C - Direct container override with external persistence

Pattern:

- Step Functions passes input references as container overrides
- ECS writes enriched payload to durable storage
- next Step Functions state retrieves it

Advantages:

- keeps ECS as main compute unit

Risks:

- still needs explicit retrieval layer
- does not solve payload return by itself

## 6. Recommended Direction

Preferred approach:

### S3 payload handoff

Reason:

- safest fit with current implementation state
- least architectural surprise
- easiest to validate
- easiest to hand over
- preserves current worker model while making AWS orchestration viable

## 7. Required Follow-On Changes

If S3 handoff is approved, the next implementation steps will be:

1. define S3 payload location convention
2. update ECS workers to read payload from S3 when given an input key
3. update ECS workers to write enriched payload to S3 output key
4. update Step Functions ASL to:
   - pass input/output S3 keys
   - retrieve enriched payload between ECS stages
5. validate end-to-end AWS execution

## 8. Current Recommendation

Do not attempt final Step Functions alignment until the ECS payload handoff mechanism is explicitly implemented and documented.
