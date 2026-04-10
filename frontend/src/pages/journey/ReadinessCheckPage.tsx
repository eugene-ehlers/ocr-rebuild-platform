import { useNavigate } from "react-router-dom";
import { PageScaffold } from "../PageScaffold";
import { useJourney } from "../../context/JourneyContext";

export function ReadinessCheckPage() {
  const navigate = useNavigate();
  const { draft, setDraft } = useJourney();

  function setReadiness(key: "requirementsAcknowledged" | "fileQualityConfirmed" | "consentConfirmed", value: boolean) {
    setDraft((prev: any) => ({
      ...prev,
      readiness: {
        ...prev.readiness,
        [key]: value,
      },
    }));
  }

  const ready =
    draft.readiness?.requirementsAcknowledged &&
    draft.readiness?.fileQualityConfirmed &&
    draft.readiness?.consentConfirmed;

  return (
    <PageScaffold
      title="Confirm readiness"
      summary="Please confirm all conditions are met before upload."
      actionLabel="Complete all confirmations to continue to upload."
      actionNode={
        <button className="btn-primary" onClick={() => navigate("/journey/pre-upload")} disabled={!ready}>
          Continue
        </button>
      }
    >
      <section className="card">
        <div className="checklist-stack">
          <label className="check-row">
            <input
              type="checkbox"
              checked={!!draft.readiness?.requirementsAcknowledged}
              onChange={(e) => setReadiness("requirementsAcknowledged", e.target.checked)}
            />
            <span>I understand the requirements</span>
          </label>

          <label className="check-row">
            <input
              type="checkbox"
              checked={!!draft.readiness?.fileQualityConfirmed}
              onChange={(e) => setReadiness("fileQualityConfirmed", e.target.checked)}
            />
            <span>My document is clear and readable</span>
          </label>

          <label className="check-row">
            <input
              type="checkbox"
              checked={!!draft.readiness?.consentConfirmed}
              onChange={(e) => setReadiness("consentConfirmed", e.target.checked)}
            />
            <span>I confirm consent for processing</span>
          </label>
        </div>
      </section>

    </PageScaffold>
  );
}
