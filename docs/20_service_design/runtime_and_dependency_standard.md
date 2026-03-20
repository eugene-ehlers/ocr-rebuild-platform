# Runtime and Dependency Standard

## Purpose

Define the governed runtime and dependency standard for backend execution, orchestration, and AWS invocation.

---

## Core Runtime Standard

All backend/control-plane execution must align to:

- Python 3.11
- boto3 for AWS service invocation
- no dependency on system AWS CLI for governed runtime execution

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

---

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

