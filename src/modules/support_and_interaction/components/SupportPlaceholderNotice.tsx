import React from "react";
import { Alert, PageSection } from "../../design_system/components";

export function SupportPlaceholderNotice() {
  return (
    <PageSection title="Support Placeholder Rules">
      <Alert variant="info">Support threads are placeholders in this phase.</Alert>
      <Alert variant="warning">Future live chat is represented only by a placeholder and is not implemented.</Alert>
    </PageSection>
  );
}
