# Frontend System Map - Governed Source of Truth

## 1. Entry Point

- frontend/src/main.tsx
- Mounts React app
- Wraps App in:
  - BrowserRouter
  - JourneyProvider

---

## 2. Root Application

- frontend/src/App.tsx
- Renders:
  - AppRoutes

---

## 3. Routing Layer

Defined in:
- frontend/src/app/routes.tsx

### Key Journey Routes

| Route | Component | Purpose |
|------|----------|--------|
| /entry | EntrySelectionPage | Start page |
| /entry/service | ServiceSelectionPage | Service selection |
| /journey/document-selection | DocumentSelectionPage | Document selection |
| /journey/requirements | RequirementsDetailPage | Service-aware requirements |
| /journey/readiness | ReadinessCheckPage | Service-aware readiness |
| /journey/pre-upload | PreUploadPage | Service-aware upload preparation |
| /submit | SubmitPage | Review and submit request |

---

## 4. Journey Flow

Entry
-> Service Selection
-> Document Selection
-> Requirements
-> Readiness
-> Pre-Upload
-> Submit

---

## 5. Service Selection

Defined in:
- frontend/src/pages/entry/ServiceSelectionPage.tsx

Stores:

{
  "serviceCode": "ocr | financial_management | fica | credit_decision"
}

The frontend must use backend-facing service codes only.

---

## 6. Document Selection

Defined in:
- frontend/src/pages/journey/DocumentSelectionPage.tsx

Uses service-driven mapping:

- ocr -> generic_document
- financial_management -> bank_statement
- fica -> identity_document, proof_of_address
- credit_decision -> bank_statement, identity_document

Document selection is derived from serviceCode.

---

## 7. Requirements and Readiness

Defined in:
- frontend/src/pages/journey/RequirementsDetailPage.tsx
- frontend/src/pages/journey/ReadinessCheckPage.tsx
- frontend/src/pages/journey/PreUploadPage.tsx

These pages are now aligned to serviceCode and must remain service-aware.

---

## 8. State Model

Defined in:
- frontend/src/context/JourneyContext.tsx

Current governed draft shape:

draft = {
  journeyType,
  serviceCode,
  applicant,
  serviceContext: {
    documentType,
    purpose
  },
  readiness,
  upload,
  submission
}

---

## 9. Submit Contract

Defined in:
- frontend/src/pages/core/SubmitPage.tsx
- frontend/src/lib/apiRequests.ts

SubmitPage now builds a controlled payload for backend request creation.
apiRequests.ts now passes the payload through unchanged.

Current request creation contract from frontend:

{
  "serviceCode": "...",
  "processingConsent": true,
  "disclosureConsent": true
}

Document upload remains a separate step after request creation.

---

## 10. Governance Rules

- Frontend must NEVER invent service families or fake service categories
- Frontend must use serviceCode only
- Document selection must derive from selected serviceCode
- Service-aware requirements, readiness, and upload guidance must remain aligned to backend services
- API request wrappers must not reshape or corrupt governed payloads
- All structural frontend changes must update this document

---

## 11. CloudShell File Write Rule

- For non-trivial documentation or code content updates in CloudShell, use Python file writes as the default method
- Avoid shell heredocs for long structured content
- This frontend system map must be updated using the controlled file-write rule when structural changes are documented
