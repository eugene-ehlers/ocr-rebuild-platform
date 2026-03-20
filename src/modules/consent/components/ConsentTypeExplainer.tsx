import React from "react";
import { Alert, PageSection } from "../../design_system/components";

export function ConsentTypeExplainer() {
  return (
    <PageSection title="Consent Types">
      <Alert variant="info">
        Processing consent is required before document ingestion, OCR, or analysis.
      </Alert>
      <Alert variant="info">
        Disclosure consent is required before sharing documents or results with third parties.
      </Alert>
      <Alert variant="warning">
        Standing consent may expire and must be validated before critical actions.
      </Alert>
    </PageSection>
  );
}
