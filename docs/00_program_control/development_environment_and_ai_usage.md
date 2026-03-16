# OCR Rebuild Program
# Development Environment & AI Usage

## 1. Purpose

This document explains the development environment, repositories, and AI tooling used to build the OCR Rebuild platform.  
It ensures that future developers or program managers can access and continue the project without dependency on a single individual.

---

# 2. System of Record

The OCR Rebuild program uses three primary system layers.

| Layer | Purpose | Location |
|------|--------|---------|
| Architecture & Program Documentation | Authoritative system design and program governance | S3 |
| Development Repository | Source code and infrastructure definitions | GitHub |
| Runtime Environment | Deployed AWS services | AWS Account |

---

# 3. Documentation Repository (Design Authority)

Primary documentation is stored in:

s3://ocr-rebuild-program/docs

This repository contains:

- Architecture design
- AWS environment design
- Data schemas
- Pipeline definitions
- Security and compliance documentation
- Testing strategy
- Cost modelling
- Build instructions

Documentation folders include:

00_program_control  
01_architecture  
02_aws_environment  
03_data_model  
04_document_processing  
05_ocr_engines  
06_preprocessing  
07_fraud_detection  
08_logo_template_recognition  
09_orchestration  
10_review_and_qa  
11_benchmarks  
12_operations  
13_security_compliance  
14_cost_management  
15_build_instructions  
16_release_management  
17_testing  

S3 acts as the authoritative design reference.

---

# 4. Development Repository

All development work is performed in the GitHub repository:

https://github.com/eugene-ehlers/ocr-rebuild-platform

Repository structure:

docs/  
services/  
infrastructure/  
schemas/  
scripts/  
tests/

### services

Contains pipeline implementations:

services/preprocessing  
services/ocr  
services/table_extraction  
services/logo_template_recognition  
services/fraud_detection  
services/aggregation  

### infrastructure

Contains AWS infrastructure definitions:

infrastructure/lambda  
infrastructure/ecs  
infrastructure/step_functions  
infrastructure/iam  
infrastructure/s3  
infrastructure/monitoring  

### schemas

Canonical schema definitions used by pipelines.

---

# 5. AI-Assisted Development

The project uses **Amazon Q Developer** to accelerate development.

Amazon Q assists with:

- generating Lambda functions
- generating ECS service code
- writing Step Functions
- infrastructure templates
- testing scripts
- debugging AWS integration issues

Amazon Q is used inside:

- AWS Console
- AWS IDE integrations
- AWS CloudShell

Developers interact with Q by prompting it with references to the repository code and documentation.

Example prompt:

Use the schema defined in  
docs/03_data_model/canonical_document_schema.json  

Generate the Lambda function for the preprocessing pipeline.

---

# 6. Development Workflow

Standard workflow:

1. Documentation defined in S3
2. Code implemented in GitHub
3. AI assistance used through Amazon Q
4. Infrastructure deployed in AWS
5. Testing performed using pipeline tests
6. Release process defined in:

docs/16_release_management/

---

# 7. Access Requirements

Developers require access to:

### AWS

Role required:

admin-role

Access typically via:

aws sts assume-role

### GitHub

Repository access required:

ocr-rebuild-platform

### Amazon Q

Available within the AWS Console and supported IDEs.

---

# 8. Development Principles

The OCR rebuild program follows these rules:

1. Documentation first  
2. Code follows documented architecture  
3. AI used to accelerate but not redesign architecture  
4. Infrastructure defined in the repository  
5. Changes follow program change control  

Change control defined in:

docs/00_program_control/change_control_process.md

---

# 9. Repository Initialization

Initial documentation and architecture were imported from:

s3://ocr-rebuild-program/docs

into the GitHub repository to create the development workspace.

All future development occurs in GitHub with periodic synchronization of design documentation.

