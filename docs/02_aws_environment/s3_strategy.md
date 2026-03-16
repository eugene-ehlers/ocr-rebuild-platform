# S3 Strategy

## 1 Purpose

Define the S3 usage strategy for Project OCR Rebuild.

## 2 Canonical Repository Rule

The canonical project documentation repository is:

s3://ocr-rebuild-program/docs/

CloudShell is a temporary editing workspace only.

## 3 Expected S3 Usage Areas

Expected S3 usage areas include:

- controlled documentation storage
- source document intake
- processing manifests
- intermediate processing artefacts
- benchmark inputs and outputs
- operational logs or exports

Actual bucket layout beyond documentation root: UNKNOWN

## 4 Repository Structure Rule

Documentation must remain organised under the controlled `docs/` hierarchy using lowercase snake_case file naming.

## 5 Object Management Rules

- verify identity before AWS changes
- use admin-role for infrastructure work
- create documents locally in CloudShell
- verify local content before upload
- copy verified documents to S3
- verify uploaded objects in S3
- do not rely on CloudShell as canonical storage

## 6 Versioning

Bucket versioning status for `ocr-rebuild-program`: ENABLED

Verification date: 2026-03-15

## 7 Retention and Lifecycle

Retention, lifecycle, archival, and deletion rules: UNKNOWN

## 8 Security Controls

Encryption, access policy, KMS usage, and bucket policy details: UNKNOWN

## 9 Current Status

This document is a Phase 1 controlled placeholder.
Detailed S3 design remains UNKNOWN until verified from live AWS configuration and approved project documentation.
