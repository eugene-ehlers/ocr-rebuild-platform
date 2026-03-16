# Working Method and Change Control

## 1 Purpose

This document defines the mandatory working method for planning, documenting, implementing, troubleshooting, and changing Project OCR Rebuild.

It exists to ensure that all future work is controlled, evidence-based, testable, and safe.

This document must be read first by any future chat or engineer working on the project.

## 2 Mandatory Working Rules

The following rules are mandatory:

- No guesses
- No assumptions
- No unnecessary explanations
- No summaries of user-provided information unless explicitly requested
- No debate unless explicitly requested
- No redesign unless explicitly requested
- Retrieve live state before proposing or making changes
- Smallest safe change only
- One step at a time
- Validate each step before moving to the next
- If evidence is missing, write UNKNOWN

## 3 Engagement Method Between User and ChatGPT

The working relationship is strictly execution-oriented.

The method is:

1. ChatGPT reads the governing documents first
2. ChatGPT gives one action at a time
3. The user performs the action
4. The user returns the result
5. ChatGPT interprets the result
6. ChatGPT gives the next single action

ChatGPT must not:

- provide long explanations unless explicitly requested
- restate the user's strategy unless explicitly requested
- give multiple implementation steps at once unless explicitly requested
- convert unknowns into assumptions
- continue past failed commands without diagnosis

The default style must be direct, controlled, and action-oriented.

## 4 Documentation-First Rule

Before technical work begins, the relevant project documents must be read.

The governing order is:

1. `docs/00_program_control/working_method_and_change_control.md`
2. `docs/00_program_control/program_overview.md`
3. `docs/01_architecture/system_overview.md`
4. `docs/01_architecture/aws_reference_architecture.md`
5. `docs/02_aws_environment/s3_strategy.md`
6. any other document directly relevant to the task

No implementation work should begin before the relevant documents have been checked.

## 5 Live-State-First Rule

Before any change is proposed or made, the live state relevant to the task must be retrieved where applicable.

This includes, where relevant:

- current AWS resources
- deployed code
- current configuration
- IAM settings
- environment variables
- Step Functions definitions
- S3 paths and objects
- logs
- queue state
- triggers
- architecture documents
- build instructions

Changes must not be proposed without first retrieving the relevant live evidence.

## 6 File and Editing Rules

The following rules are mandatory:

- Use heredoc for file creation and file edits
- Do not edit Lambda code in the AWS console
- Do not make multiple unrelated changes in one step
- Do not skip verification after a change
- Diagnose command failures before proceeding
- Prefer the smallest isolated change that can be tested safely
- Use clear file names in lowercase snake_case
- Do not use ambiguous names such as `final`, `new`, `test`, or `v2`

## 7 Change Control Sequence

All changes must follow this sequence:

1. Confirm the exact objective or problem
2. Read the governing documents
3. Retrieve live evidence
4. Identify the minimum root cause or required action
5. Propose the smallest safe change
6. Apply one change only
7. Test and verify
8. Record the result
9. Only then proceed to the next step

If evidence does not support a conclusion, the status must remain `UNKNOWN`.

## 8 Chat Operating Rules

Every future project chat must follow these rules:

- Read the governance and architecture documents first
- Stay inside the current task only
- Give one action at a time by default
- Keep responses concise and operational
- Do not provide background explanation unless requested
- Do not summarize existing project content unless requested
- Do not introduce alternative designs unless requested
- Do not infer missing facts
- Mark missing facts as `UNKNOWN`
- Keep the project state aligned with the documents

## 9 Investigation Start Pattern

Every future investigation or build stream should start with this sequence:

1. Move to the workspace root
2. Verify the required documentation paths exist
3. Read the mandatory governance document
4. Read the task-relevant architecture and build documents
5. Identify the exact AWS resources or files involved
6. Retrieve live evidence
7. Proceed one step at a time

## 10 Risk Controls

The following controls are mandatory:

- No unverified assumptions
- No undocumented changes
- No direct console code edits
- No skipping verification
- No continuation after failed commands without diagnosis
- No architecture redesign unless explicitly requested
- No mixing discovery and implementation without control
- No silent deviations from documented structure or naming

## 11 Documentation Update Rule

If a change affects architecture, AWS structure, naming, process, build sequence, or operating method, the relevant document must be updated as part of the controlled change.

Documentation must remain aligned with the actual state.

If documentation is missing, create it before proceeding where necessary.

## 12 Status of Unknowns

Where information cannot be proven from live evidence or verified documentation, it must be explicitly marked:

`UNKNOWN`

Unknowns must not be silently converted into assumptions.

## 13 Expected Use

This document applies to:

- project setup
- S3 and repository structure
- architecture definition
- controlled AWS build work
- implementation streams
- issue diagnosis
- troubleshooting
- handover
- audit support

## 14 Enforcement

This document is mandatory.

If a future chat or engineer does not follow this method, the work is out of control and must be corrected before continuing.

## 15 AWS Role Requirement

All AWS infrastructure work must be performed using the **admin-role**.

The base IAM user must not perform infrastructure changes directly.

Before performing any AWS operation that modifies infrastructure, the following sequence must be executed.

### Step 1 — Verify Current Identity

Run:

aws sts get-caller-identity

If the ARN does not contain:

assumed-role/admin-role

then the admin role must be assumed.

### Step 2 — Assume Admin Role

Run:

aws sts assume-role \
--role-arn arn:aws:iam::026465780614:role/admin-role \
--role-session-name OCRRebuildSession

### Step 3 — Export Temporary Credentials

Export the credentials returned by the assume-role command:

export AWS_ACCESS_KEY_ID="VALUE"
export AWS_SECRET_ACCESS_KEY="VALUE"
export AWS_SESSION_TOKEN="VALUE"

### Step 4 — Verify Role Switch

Run:

aws sts get-caller-identity

Expected ARN format:

arn:aws:sts::<account>:assumed-role/admin-role/OCRRebuildSession

If this identity is not confirmed, infrastructure commands must not proceed.

### Step 5 — Session Expiration

Assumed role credentials expire.

If AWS commands begin failing with authorization errors, the role must be assumed again.

### Enforcement

All infrastructure work must use the admin-role session.

Direct execution as the base IAM user is not permitted for project infrastructure changes.

