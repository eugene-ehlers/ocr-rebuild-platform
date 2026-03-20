import React from "react";
import { Alert, EmptyState, PageSection } from "../../design_system/components";

export function RemediationPromptPanel() {
  return (
    <PageSection title="Remediation Prompts">
      <Alert variant="warning">Remediation prompts are placeholder-driven in this phase.</Alert>
      <EmptyState
        title="Remediation placeholder"
        description="Missing consent, document quality issues, or incomplete document sets will appear here."
      />
    </PageSection>
  );
}
