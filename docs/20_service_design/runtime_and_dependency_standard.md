# Runtime and Dependency Standard

## Purpose

Define the governed runtime and dependency standard for backend execution, orchestration, and AWS invocation.

---

## Core Runtime Standard

All backend/control-plane execution must align to:

- Python 3.11
- boto3 for AWS service invocation
- no dependency on system AWS CLI for governed runtime execution

In the governed decision runtime, backend execution is not considered complete merely because orchestration and provider invocation succeed.

Where execution output does not structurally satisfy governed service contracts, the governed runtime may require:
- an explicit transformation layer
- validation and sufficiency assessment against authoritative rulesets

These are governed runtime components, not optional post-processing conveniences.

---

## Execution Mode Standard

Execution is controlled by:

- `EXECUTION_MODE=local`
- `EXECUTION_MODE=aws`

### Local mode
- invokes local service/task stubs
- used for controlled local development and fallback

### AWS mode
- invokes AWS bridge path through boto3
- used for controlled infrastructure-aligned execution attempts

---

## AWS Runtime Requirements

AWS bridge execution requires:

- `AWS_DEFAULT_REGION`
- valid AWS credentials, or runtime IAM role
- valid ECS cluster/task/subnet/network configuration
- permissions to invoke ECS tasks

If any of these are missing:
- execution must fail safely
- structured error must be returned
- controlled fallback may be used in development mode

---

## Dependency Standard

Backend AWS invocation dependencies must use:

- `boto3`

The following is not the governed runtime dependency standard:
- shelling out to `aws` CLI from Python execution paths

## Governed Transformation and Validation Standard

Where approved by architecture and service design:
- transformation logic must be explicit, versioned, and auditable
- transformation may perform structural mapping, field alignment, and pass-through normalization only
- transformation must not infer or fabricate missing contract values
- validation and sufficiency assessment must operate against authoritative governed rulesets
- governed fail outcomes must be preserved explicitly where contract requirements are unmet

A runtime outcome of FAIL after transformation and validation is a valid governed result and must not be treated automatically as an infrastructure/runtime defect.

---

## Runtime Outcome Interpretation Standard

The governed runtime must distinguish clearly between:
- infrastructure/runtime failure
- execution failure
- governed contract failure
- degraded but accepted outcome
- escalated outcome

This distinction must remain explicit in:
- runtime result artifacts
- audit notes
- validation outputs
- service-level reporting

## Current Controlled State

As of Phase 21B / 21C:

- boto3-based AWS bridge is implemented
- region dependency confirmed
- credentials dependency confirmed
- controlled fallback to local execution is working

Current observed AWS bridge failure progression:
1. missing `aws` binary
2. missing AWS region
3. missing AWS credentials

---

## Next Controlled Infrastructure Requirement

To progress from AWS bridge to live ECS execution, the runtime must provide:

- region
- credentials / IAM role
- ECS cluster name
- ECS task definition
- valid subnet/network configuration
- ECS execution permissions

---

