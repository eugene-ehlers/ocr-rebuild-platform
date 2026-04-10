import { useNavigate } from "react-router-dom";
import { PageScaffold } from "../PageScaffold";
import { useJourney } from "../../context/JourneyContext";

const OPTIONS = [
  { key: "identity_document", label: "Identity document" },
  { key: "proof_of_address", label: "Proof of address" },
  { key: "financial_document", label: "Financial document" },
];

export function DocumentSelectionPage() {
  const navigate = useNavigate();
  const { draft, setDraft } = useJourney();

  function selectDocument(documentType: string) {
    setDraft((prev: any) => ({
      ...prev,
      serviceContext: {
        ...prev.serviceContext,
        documentType,
      },
    }));
  }

  return (
    <PageScaffold
      title="Select document type"
      summary="Choose the type of document you want to prepare and submit."
      actionLabel="Select a document type before continuing."
      actionNode={
        <button
          className="btn-primary"
          onClick={() => navigate("/journey/readiness")}
          disabled={!draft.serviceContext?.documentType}
        >
          Continue
        </button>
      }
    >
      <div className="journey-card-grid">
        {OPTIONS.map((option) => {
          const selected = draft.serviceContext?.documentType === option.key;
          return (
            <button
              key={option.key}
              className={`card journey-option-card ${selected ? "card--selected" : ""}`}
              onClick={() => selectDocument(option.key)}
            >
              <h3>{option.label}</h3>
              <span className={selected ? "btn-success" : "btn-secondary"}>{selected ? "Selected" : "Select"}</span>
            </button>
          );
        })}
      </div>

    </PageScaffold>
  );
}
