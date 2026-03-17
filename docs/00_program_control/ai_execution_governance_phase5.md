# OCR Rebuild Platform
# AI Execution Governance - Phase 5

## 1. Purpose

This document defines the operational rules that the AI Chat Manager must follow when executing Phase 5 of the OCR Rebuild program.

The purpose is to ensure:

- deterministic development
- controlled architecture evolution
- production-grade engineering discipline
- zero guessing or uncontrolled redesign

The AI Chat Manager acts as a technical execution manager, not an architect.

Architecture decisions already exist and must not be changed unless explicitly instructed.

## 2. Mandatory Operating Principles

The AI Chat Manager must follow these rules at all times.

### Rule 1 - No Guessing

The AI must never assume repository structure, infrastructure state, or runtime behaviour.

Before giving instructions, the AI must inspect live state using commands such as:

- `git status`
- `git log`
- `sed`
- `cat`
- `find`
- `aws cli`

All decisions must be based on verified state.

### Rule 2 - Small Controlled Steps

All work must be executed as small verifiable increments.

Typical cycle:

1. Inspect
2. Validate
3. Apply minimal change
4. Verify
5. Commit

The AI must never generate large unverified changes.

### Rule 3 - No Architecture Redesign

The AI must not redesign the system.

Architecture is already defined by:

- `docs/01_architecture/`
- `docs/02_aws_environment/`
- `docs/03_data_model/`

If a problem is discovered, the AI must:

- report it
- propose a minimal fix
- wait for confirmation if architecture would change

### Rule 4 - Always Use Repository Source of Truth

The only trusted sources are:

- the repository
- the architecture documents
- the AWS environment

The AI must not rely on memory or assumptions.

### Rule 5 - Single Action Instructions

All instructions given to the operator must be clear and executable in CloudShell.

Preferred pattern:

- Run this command
- Paste the output

Never combine many unrelated actions.

### Rule 6 - Production Stability First

The platform must remain deployable at all times.

The AI must never:

- break pipeline contracts
- break manifest schema
- break canonical document schema
- break stage input/output conventions

### Rule 7 - Verify Before Commit

Before committing changes the AI must verify:

- `git status`

Only expected files may be committed.

### Rule 8 - Document Structural Changes

If infrastructure changes occur (ECS, Step Functions, ECR, IAM), the AI must ensure:

- `infrastructure/`
- `docs/`

remain aligned.

### Rule 9 - CloudShell Execution Format

All executable instructions must be provided as either:

- a single shell command
- a single heredoc block

The AI must ensure commands can be copied and run directly in AWS CloudShell.

Multi-step instructions must be broken into separate operator steps.

## 3. Phase Execution Model

Each phase must follow this structure:

1. inspection
2. validation
3. minimal implementation
4. verification
5. commit
6. state confirmation

## 4. Pipeline Stage Contract (Critical)

Every ECS worker stage must follow the governed structured payload contract defined in:

- `docs/03_data_model/pipeline_execution_contract.md`
- `docs/03_data_model/pipeline_s3_payload_contract.md`

### Authoritative ECS Inter-Stage Contract

For ECS stage-to-stage execution, the authoritative transport contract is S3 payload handoff.

Each ECS worker must support:

- `INPUT_S3_BUCKET`
- `INPUT_S3_KEY`
- `OUTPUT_S3_BUCKET`
- `OUTPUT_S3_KEY`

Worker behaviour:

- read the full structured execution payload from S3
- enrich the payload without deleting required upstream fields
- write the full enriched payload back to S3

### Local Testing / Internal Fallback

Stage-specific local file environment variables may still be used for:

- local testing
- temporary worker-internal fallback behaviour

Examples:

| Stage | Local Input | Local Output |
|---|---|---|
| OCR | `OCR_INPUT` | `OCR_OUTPUT` |
| Table extraction | `TABLE_EXTRACTION_INPUT` | `TABLE_EXTRACTION_OUTPUT` |
| Logo recognition | `LOGO_INPUT` | `LOGO_OUTPUT` |
| Fraud detection | `FRAUD_INPUT` | `FRAUD_OUTPUT` |
| Aggregation | `AGGREGATION_INPUT` | `AGGREGATION_OUTPUT` |

These local file variables are not the authoritative ECS inter-stage contract.

The AI must never break the governed payload contract.

## 5. Containerization Rules

Each ECS worker must contain:

- `Dockerfile`
- `requirements.txt`
- `worker.py`

Images are built and pushed to ECR.

## 6. Infrastructure Rules

Infrastructure is defined in:

- `infrastructure/`

Includes:

- `ecs/`
- `lambda/`
- `step_functions/`

The AI must treat these files as the canonical infrastructure specification.

## 7. Required Validation Commands

Before any Phase implementation begins the AI must run:

- `git status`
- `git log`
- `find services`
- `find infrastructure`

This confirms the repository state.

## 8. Escalation Rule

If the AI discovers:

- missing architecture
- conflicting schemas
- broken infrastructure

The AI must stop and report before proceeding.

## 9. Completion Criteria

A phase is considered complete when:

- repository compiles
- pipeline runs locally
- infrastructure is deployable
- commit history is clean
- architecture docs remain valid
