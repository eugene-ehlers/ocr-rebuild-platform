import { useNavigate } from "react-router-dom";
import { PageScaffold } from "../PageScaffold";
import { useJourney } from "../../context/JourneyContext";

export function ServiceSelectionPage() {
  const navigate = useNavigate();
  const { draft, setDraft } = useJourney();

  function chooseService(serviceType: string, journeyType: "individual" | "business") {
    setDraft((prev: any) => ({
      ...prev,
      serviceType,
      journeyType,
    }));
    navigate("/journey/document-selection");
  }

  return (
    <PageScaffold
      title="Select a service"
      summary="Choose the service path that matches your request and continue into the guided journey."
      trustText="We explain what is required before upload and keep the request path structured and trackable."
      actionLabel="Select the most appropriate service to continue."
    >
      <div className="journey-card-grid">
        <button className="card journey-option-card" onClick={() => chooseService("document_understanding", "individual")}>
          <h3>Document understanding</h3>
          <p>Analyse document structure and extract meaning.</p>
          <p><strong>Requires:</strong> Clean readable files</p>
          <span className="btn-primary">Continue</span>
        </button>

        <button className="card journey-option-card" onClick={() => chooseService("document_submission", "individual")}>
          <h3>Structured submission</h3>
          <p>Prepare and submit documents into a guided workflow.</p>
          <p><strong>Requires:</strong> Full document set</p>
          <span className="btn-primary">Continue</span>
        </button>

        <button className="card journey-option-card" onClick={() => chooseService("business_submission", "business")}>
          <h3>Business submission</h3>
          <p>Provide organisation details with authority context.</p>
          <p><strong>Requires:</strong> Business and supporting documents</p>
          <span className="btn-secondary">Continue</span>
        </button>
      </div>
    </PageScaffold>
  );
}
