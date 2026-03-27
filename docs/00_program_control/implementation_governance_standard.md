# Implementation Governance Standard — Structure, Naming, Module Reuse, Stack Discipline & Operational Hygiene
Date: 2026-03-27
Scope: Platform-wide (Frontend + Backend + Orchestration + Operational Workflows)
Status: Draft for governance approval

## 1. Purpose

This document defines mandatory implementation controls to:
- prevent architectural and code drift
- enforce reuse of approved modules and stack components
- standardise file structure and naming
- enforce disciplined CloudShell and workspace usage
- ensure long-term maintainability and stability

---

## 2. Core Governance Principles

1. Inspection-first, no guessing  
2. Reuse before create  
3. No uncontrolled file creation  
4. Strict stack adherence  
5. Separation of concerns enforced  
6. Clean workspace at all times  
7. No temporary artifacts in governed areas  
8. One scoped task at a time  

---

## 3. Module Reuse & Creation Rules

### 3.1 Reuse First
- Inspect repo before creating anything
- Use existing:
  - service runners
  - validators
  - payload handlers
  - utilities

### 3.2 Prohibited
- duplicate modules  
- shadow implementations  
- parallel utility libraries  

### 3.3 New Modules
Allowed only if:
- no suitable module exists
- extension is not viable
- location and naming are controlled

---

## 4. Stack Discipline

### 4.1 Runtime
- Python 3.11 mandatory

### 4.2 CloudShell
Allowed:
- CLI
- git
- heredoc
- inspection

NOT allowed:
- builds
- runtime validation

---

## 5. File Structure

Program control → docs/00_program_control/  
Environment → docs/02_aws_environment/  
Legal → docs/10_legal/  
Data → docs/03_data_model/  
Service design → docs/20_service_design/  

No undocumented directories allowed.

---

## 6. Naming

Files:
- lowercase_with_underscores

Python:
- snake_case (vars/functions)
- PascalCase (classes)

Frontend:
- PascalCase components
- lowercase routes

---

## 7. Frontend Rules

- No business logic
- No OCR logic
- API Gateway only
- No inline styling

---

## 8. Workspace & File Hygiene

### Save Rules
- governed → docs/
- runtime → NOT in repo
- working → isolated

### CloudShell
- use /tmp for scripts
- do not store permanent files

### Cleanup
- remove temp files
- remove test outputs
- remove scratch backups

### Promotion
temp → working → governed

### Repo Cleanliness
- no root artifacts
- no runtime files
- no temp leftovers

---

## 9. Worker Execution

Before:
- inspect
- confirm paths

During:
- narrow scope
- follow naming

After:
- clean workspace
- no commit unless instructed

---

## 10. Enforcement

Violations:
- module duplication
- bad file placement
- temp file leakage
- stack misuse

Must be corrected immediately.

---

## Status

MANDATORY STANDARD
