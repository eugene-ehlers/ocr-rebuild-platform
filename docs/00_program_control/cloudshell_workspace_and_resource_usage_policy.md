# CloudShell Workspace and Resource Usage Policy (v1)

## 1. Purpose

This policy defines how CloudShell must be used across all projects to ensure:
- no drift
- no unintended data persistence
- clear source-of-truth control
- safe and reversible changes
- consistent cross-project governance

This policy is mandatory for all implementation chats and developers.

---

## 2. Core Principle

CloudShell is a **temporary execution workspace**, not a source of truth.

---

## 3. Source of Truth Rule

The only valid sources of truth are:

- Repository source code
- Governed documentation under `docs/`
- Approved mirrored documentation (e.g. S3 governed doc set)

The following are NOT sources of truth:

- `/tmp` files
- local CloudShell files not committed to repo
- generated artifacts
- logs or intermediate outputs

---

## 3A. Working Directory Control (MANDATORY)

Before executing ANY command:
- explicitly set the working directory using `cd`
- verify the directory using `pwd`
- ensure all file paths are relative to the verified directory

Rules:
- never assume current directory
- never rely on previous steps
- every execution script must include:
  - `cd <expected directory> || exit 1`
  - `pwd`

Failure to control directory = automatic failure

## 4. CloudShell Usage Rule

CloudShell may only be used for:

- inspection
- controlled execution via heredoc scripts
- temporary backups during change execution

CloudShell must NOT be used for:

- long-term storage of code
- maintaining project state outside the repo
- storing permanent documentation

---

## 5. Temporary File Rule

- All execution scripts must be created under `/tmp`
- Files must be clearly named (e.g. `fe_w36_patch.sh`)
- Temporary files must be removed after task completion

---

## 6. Backup Control (MANDATORY)

Before ANY modification or deletion:

- a backup must be created
- backup must preserve full original content
- backup must allow exact restoration
- backup location must be shown in evidence

Failure to create backups = automatic failure

---

## 7. Change Boundary Rule

Before changes:

- explicitly list files to be modified
- explicitly list files that must NOT be touched

Any change outside scope = failure

---

## 8. Delete Safety Rule

No file may be deleted unless ALL are proven:

1. file is within project scope
2. file is not used anywhere
3. file is not required by build/runtime
4. file is not part of governed architecture
5. deletion will not affect adjacent/shared work

Untracked ≠ safe to delete

---

## 9. Project Boundary Rule

- Only operate within approved project scope
- Do not remove or modify adjacent/shared project assets
- Cross-project impact must be explicitly proven safe

---

## 10. Completion Rule

A task is NOT complete when code is written.

A task is complete ONLY when:

- changes are validated
- no unintended consequences exist
- policy compliance is verified
- documentation is updated (repo)
- documentation is synced (S3 if applicable)
- CloudShell temporary artifacts are removed

---

## 11. Enforcement

Any violation of this policy results in:

- task rejection
- mandatory recovery/revert
- re-execution under controlled conditions

---

## Status

ACTIVE — GOVERNED POLICY

## Worker Evidence and Completion Protocol (Mandatory Reference)

All worker-chat execution must comply with:

docs/00_program_control/worker_chat_execution_and_evidence_protocol.md

This protocol defines:
- allowed worker communication
- raw evidence requirements
- completion gates
- rejection recovery
- backup, /tmp, and boundary rules
- the standard governed evidence path
