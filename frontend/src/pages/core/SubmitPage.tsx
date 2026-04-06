import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useJourney } from "../../context/JourneyContext";
import { createRequest, uploadRequestDocument, type ApiError } from "../../lib/apiRequests";

export function SubmitPage() {
  const navigate = useNavigate();
  const { draft } = useJourney();
  const [error, setError] = useState<ApiError | null>(null);

  function validate() {
    const errs: Record<string,string> = {};

    if (!draft.serviceContext.documentType) errs.documentType = "Required";
    if (!draft.upload?.file) errs.file = "Required";
    if (!draft.readiness?.consentConfirmed) errs.consent = "Required";
    if (!draft.submission?.declarationConfirmed) errs.declaration = "Required";

    return errs;
  }

  async function handleSubmit() {
    const errs = validate();
    if (Object.keys(errs).length > 0) {
      setError({
        error_code: "VALIDATION_ERROR",
        message: "Please fix validation errors",
        field_errors: errs
      });
      return;
    }

    try {
      const created = await createRequest(draft);

      await uploadRequestDocument(
        created.request_id,
        draft.serviceContext.documentType,
        draft.upload.file
      );

      navigate(`/status/${created.request_id}`);
    } catch (e) {
      setError(e as ApiError);
    }
  }

  return (
    <div>
      <h1>Submit</h1>

      {error && (
        <div style={{color:"red"}}>
          <p>{error.message}</p>
          {error.field_errors && (
            <ul>
              {Object.entries(error.field_errors).map(([k,v]) => (
                <li key={k}>{k}: {v}</li>
              ))}
            </ul>
          )}
        </div>
      )}

      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
}
