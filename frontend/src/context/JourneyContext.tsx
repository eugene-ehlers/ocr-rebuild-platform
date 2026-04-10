import { createContext, useContext, useState } from "react";

const JourneyContext = createContext<any>(undefined);

export function JourneyProvider({ children }: any) {
  const [draft, setDraft] = useState({
    journeyType: "individual",
    serviceType: "document_submission",
    applicant: {},
    serviceContext: { documentType: "", purpose: "submission" },
    readiness: {
      requirementsAcknowledged: false,
      fileQualityConfirmed: false,
      consentConfirmed: false
    },
    upload: { file: null },
    submission: { declarationConfirmed: false }
  });

  return (
    <JourneyContext.Provider value={{ draft, setDraft }}>
      {children}
    </JourneyContext.Provider>
  );
}

export function useJourney() {
  const ctx = useContext(JourneyContext);
  if (!ctx) throw new Error("useJourney must be used within JourneyProvider");
  return ctx;
}
