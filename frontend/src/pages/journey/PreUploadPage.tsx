import { useNavigate } from "react-router-dom";
import { PageScaffold } from "../PageScaffold";
import { useJourney } from "../../context/JourneyContext";

export function PreUploadPage() {
  const navigate = useNavigate();
  const { draft, setDraft } = useJourney();

  function setFile(file: File | null) {
    setDraft((prev: any) => ({
      ...prev,
      upload: {
        ...prev.upload,
        file,
        filename: file?.name ?? "",
        mimeType: file?.type ?? "",
        size: file?.size ?? 0,
      },
    }));
  }

  function setDeclaration(value: boolean) {
    setDraft((prev: any) => ({
      ...prev,
      submission: {
        ...prev.submission,
        declarationConfirmed: value,
      },
    }));
  }

  return (
    <PageScaffold
      title="Prepare upload"
      summary="Choose your file and confirm the declaration before continuing to review and submit."
      actionLabel="Select a file and confirm the declaration to continue."
      actionNode={
        <button
          className="btn-primary"
          onClick={() => navigate("/submit")}
          disabled={!draft.upload?.file || !draft.submission?.declarationConfirmed}
        >
          Continue to review
        </button>
      }
    >
      <section className="card">
        <div className="upload-stack">
          <label className="upload-label" htmlFor="journey-upload">Choose file</label>
          <input
            id="journey-upload"
            type="file"
            accept=".pdf,.jpg,.jpeg,.png"
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
          />
          <p className="upload-help">Accepted formats: PDF, JPG, PNG. Maximum 10MB.</p>
          <p><strong>Selected file:</strong> {draft.upload?.filename || "No file selected"}</p>

          <label className="check-row">
            <input
              type="checkbox"
              checked={!!draft.submission?.declarationConfirmed}
              onChange={(e) => setDeclaration(e.target.checked)}
            />
            <span>I confirm the selected file and submission details are correct.</span>
          </label>
        </div>
      </section>

    </PageScaffold>
  );
}
