export type FieldErrors = Record<string,string>;

export type ApiError = {
  error_code: string;
  message: string;
  field_errors?: FieldErrors;
};

export async function createRequest(draft: any) {
  const payload = {
    journey_type: draft.journeyType,
    service_type: draft.serviceType,
    service_context: {
      document_type: draft.serviceContext.documentType,
      purpose: draft.serviceContext.purpose
    },
    readiness: {
      requirements_acknowledged: draft.readiness.requirementsAcknowledged,
      file_quality_confirmed: draft.readiness.fileQualityConfirmed,
      consent_confirmed: draft.readiness.consentConfirmed
    },
    submission: {
      declaration_confirmed: draft.submission.declarationConfirmed
    }
  };

  const res = await fetch("/api/requests", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  const data = await res.json();
  if (!res.ok) throw data;
  return data;
}

export async function uploadRequestDocument(requestId: string, documentType: string, file: File) {
  const fd = new FormData();
  fd.append("document_type", documentType);
  fd.append("file", file);

  const res = await fetch(`/api/requests/${requestId}/documents`, {
    method: "POST",
    body: fd
  });

  return res.json();
}

export async function getRequestStatus(requestId: string) {
  return fetch(`/api/requests/${requestId}`).then(r => r.json());
}

export async function getRequestResult(requestId: string) {
  return fetch(`/api/requests/${requestId}/result`).then(r => r.json());
}
