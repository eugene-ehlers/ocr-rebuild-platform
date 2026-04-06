import { createContext, useContext, useState } from "react";

const JourneyContext = createContext<any>(null);

export function JourneyProvider({ children }: any) {
  const [draft, setDraft] = useState({
    journeyType: "individual",
    serviceType: "document_submission",
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
  return useContext(JourneyContext);
}
