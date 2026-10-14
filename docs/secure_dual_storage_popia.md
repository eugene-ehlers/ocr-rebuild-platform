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
- Content held: original file (or secure reference + hash), raw OCR output, pre-confirmation entities, confirmed entities, full request metadata.
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
3. OCR platform writes the file and all artefacts first into its internal store under the linkage keys.
4. A minimal, client-safe payload (document_id, confirmed entities, confidence) is returned to I-DIP.
5. I-DIP places that payload in the client vault.
6. I-DIP never receives credentials or direct access to the OCR internal store.

## Rules
- No open or shared S3 drop.
- No processing without valid processing consent.
- No disclosure to third parties without valid disclosure consent.
- Every access (upload, process, retrieve) is audited with client_id, document_id, request_id and timestamp.
