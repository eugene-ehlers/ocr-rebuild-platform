import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { PageScaffold } from "../PageScaffold";
import { useJourney } from "../../context/JourneyContext";
import { createRequest, uploadRequestDocument, type ApiError } from "../../lib/apiRequests";

function formatValue(value: unknown, fallback = "Not provided") {
  if (typeof value === "string" && value.trim()) return value;
  if (typeof value === "number") return String(value);
  if (typeof value === "boolean") return value ? "Yes" : "No";
  return fallback;
}

function humanizeKey(key: string) {
  return key
    .replace(/\./g, " / ")
    .replace(/([a-z])([A-Z])/g, "$1 $2")
    .replace(/_/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

export function SubmitPage() {
  const navigate = useNavigate();
  const { draft } = useJourney();
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<ApiError | null>(null);

  const validation = useMemo(() => {
    const errs: Record<string, string> = {};

    if (draft.journeyType === "individual") {
      const a = draft.applicant?.individual;
      if (!a?.firstNames) errs["firstNames"] = "First names are required";
      if (!a?.surname) errs["surname"] = "Surname is required";
      if (!a?.idNumber) errs["idNumber"] = "ID number is required";
      if (!a?.email) errs["email"] = "Email is required";
      if (!a?.mobile) errs["mobile"] = "Mobile is required";
      if (!a?.bankName) errs["bankName"] = "Bank name is required";
      if (!a?.bankAccountNumber) errs["bankAccountNumber"] = "Bank account number is required";
    } else {
      const b = draft.applicant?.business;
      if (!b?.businessName) errs["businessName"] = "Business name is required";
      if (!b?.registrationNumber) errs["registrationNumber"] = "Registration number is required";
      if (!b?.responsiblePerson?.firstNames) errs["responsiblePerson.firstNames"] = "Responsible person first names are required";
      if (!b?.responsiblePerson?.surname) errs["responsiblePerson.surname"] = "Responsible person surname is required";
      if (!b?.responsiblePerson?.idNumber) errs["responsiblePerson.idNumber"] = "Responsible person ID number is required";
      if (!b?.responsiblePerson?.email) errs["responsiblePerson.email"] = "Responsible person email is required";
      if (!b?.responsiblePerson?.mobile) errs["responsiblePerson.mobile"] = "Responsible person mobile is required";
      if (!b?.bankName) errs["bankName"] = "Bank name is required";
      if (!b?.bankAccountNumber) errs["bankAccountNumber"] = "Bank account number is required";
      if (!b?.authorityIndicator) errs["authorityIndicator"] = "Authority must be confirmed";
    }

    if (!draft.serviceContext?.documentType) errs["documentType"] = "Document type is required";
    if (!draft.readiness?.requirementsAcknowledged) errs["requirementsAcknowledged"] = "Requirements must be acknowledged";
    if (!draft.readiness?.fileQualityConfirmed) errs["fileQualityConfirmed"] = "File quality must be confirmed";
    if (!draft.readiness?.consentConfirmed) errs["consentConfirmed"] = "Consent must be confirmed";
    if (!draft.upload?.file) errs["upload.file"] = "A file must be selected";
    if (!draft.submission?.declarationConfirmed) errs["declarationConfirmed"] = "Declaration must be confirmed";

    return errs;
  }, [draft]);

  const summaryItems = useMemo(() => {
    if (draft.journeyType === "business") {
      const b = draft.applicant?.business;
      return [
        { label: "Journey type", value: formatValue(draft.journeyType) },
        { label: "Business name", value: formatValue(b?.businessName) },
        { label: "Registration number", value: formatValue(b?.registrationNumber) },
        { label: "Responsible person", value: [b?.responsiblePerson?.firstNames, b?.responsiblePerson?.surname].filter(Boolean).join(" ") || "Not provided" },
        { label: "Document type", value: formatValue(draft.serviceContext?.documentType, "Not selected") },
        { label: "Selected file", value: formatValue(draft.upload?.filename, "No file selected") },
      ];
    }

    const a = draft.applicant?.individual;
    return [
      { label: "Journey type", value: formatValue(draft.journeyType) },
      { label: "Applicant", value: [a?.firstNames, a?.surname].filter(Boolean).join(" ") || "Not provided" },
      { label: "ID number", value: formatValue(a?.idNumber) },
      { label: "Email", value: formatValue(a?.email) },
      { label: "Document type", value: formatValue(draft.serviceContext?.documentType, "Not selected") },
      { label: "Selected file", value: formatValue(draft.upload?.filename, "No file selected") },
    ];
  }, [draft]);

  async function handleSubmit() {
    if (Object.keys(validation).length > 0) {
      setError({
        error_code: "VALIDATION_ERROR",
        message: "Please fix validation errors before submitting.",
        field_errors: validation,
      });
      return;
    }

    try {
      setSubmitting(true);
      setError(null);

      const created = await createRequest(draft);

      if (draft.upload?.file) {
        await uploadRequestDocument(
          created.request_id,
          draft.serviceContext.documentType,
          draft.upload.file,
        );
      }

      navigate(`/status/${created.request_id}`);
    } catch (e) {
      setError(e as ApiError);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <PageScaffold
      title="Review and submit your request"
      summary="Confirm your details, selected document, and readiness checks before creating a trackable request."
      trustText="Submitting will create a request ID, upload your selected document, and move you into a live status-tracking journey."
      actionLabel="When you submit, the platform will create your request and redirect you to the status page."
    >
      <div className="submit-stack">
        <section className="card card--selected">
          <h3>Request summary</h3>
          <div className="submit-summary-grid">
            {summaryItems.map((item) => (
              <div key={item.label} className="submit-summary-item">
                <strong>{item.label}</strong>
                <p>{item.value}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="card">
          <h3>What happens next</h3>
          <ul className="submit-list">
            <li>A request record will be created for this submission.</li>
            <li>Your selected document will be uploaded against that request.</li>
            <li>You will be redirected to a status page where progress can be tracked.</li>
          </ul>
        </section>

        <section className="card">
          <h3>Declarations and validation</h3>
          {Object.keys(validation).length === 0 ? (
            <p className="text-success">All submission checks are currently satisfied.</p>
          ) : (
            <>
              <p>Please resolve the remaining items before submitting.</p>
              <ul className="submit-list">
                {Object.entries(validation).map(([k, v]) => (
                  <li key={k}>
                    <strong>{humanizeKey(k)}</strong>: {v}
                  </li>
                ))}
              </ul>
            </>
          )}
        </section>

        {error && (
          <section className="card card--error">
            <h3>{error.message}</h3>
            {error.field_errors && (
              <ul className="submit-list">
                {Object.entries(error.field_errors).map(([k, v]) => (
                  <li key={k}>
                    <strong>{humanizeKey(k)}</strong>: {v}
                  </li>
                ))}
              </ul>
            )}
          </section>
        )}

        <div className="action-bar">
          <button className="btn-primary" onClick={handleSubmit} disabled={submitting}>
            {submitting ? "Submitting..." : "Submit request"}
          </button>
        </div>
      </div>
    </PageScaffold>
  );
}
