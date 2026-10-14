# Dual-Store Model for I-DIP OCR Integration (POPIA-aligned)

## Purpose
Documents containing personal information must be handled under two distinct stores with strict access controls and durable linkage.

## Store 1: I-DIP client vault
- Owner: the client (and mandated appointees while valid disclosure consent exists).
- Access path: authenticated I-DIP / Passport session only.
- Content held: original file reference, client-confirmed entities, document_id, request_id.
- Retention: follows existing I-DIP vault rules (hidden but retained if archived/cancelled).

## Store 2: OCR platform internal audit / training store
- Owner: OCR platform service roles only.
- Access path: no client, no I-DIP, no other product. Used for audit, client query support, dispute, and future training (subject to consent/opt-out).
- Bucket: value of environment variable `OCR_INTERNAL_BUCKET` (recommended name pattern `ocr-internal-audit-026465780614`).
- Key layout:
  - `clients/{client_id}/documents/{document_id}/original/{filename}`
  - `clients/{client_id}/documents/{document_id}/linkage.json`
- Encryption: SSE-S3 (AES256) minimum; SSE-KMS recommended for production.
- Content held: original file, raw OCR output, pre-confirmation entities, confirmed entities, full request metadata.
- Retention: longer if required for audit/training, still subject to POPIA deletion requests.

## Linkage (mandatory on every object in both stores)
- request_id
- document_id
- client_id (or opaque reference)
- source_app (e.g. "idip" / "passport")
- timestamp
- consent_record_ids that authorised processing

Both sides store the same request_id and document_id so an audit or query can join records without exposing the internal store.

## Upload and processing flow
1. Authenticated I-DIP session calls the OCR control plane.
2. Processing consent is verified or captured.
3. OCR platform writes the file and linkage first into its internal store under the client-scoped keys.
4. A minimal, client-safe payload (document_id, confirmed entities, confidence) is returned to I-DIP.
5. I-DIP places that payload in the client vault.
6. I-DIP never receives credentials or direct access to the OCR internal store.

## IAM requirements for the OCR service role
- s3:PutObject, s3:GetObject, s3:DeleteObject on `arn:aws:s3:::${OCR_INTERNAL_BUCKET}/clients/*`
- No s3:ListBucket granted to any I-DIP or Passport role.
- Bucket policy denies all principals except the OCR service role.

## Rules
- No open or shared S3 drop.
- No processing without valid processing consent.
- No disclosure to third parties without valid disclosure consent.
- Every access (upload, process, retrieve) is audited with client_id, document_id, request_id and timestamp.
