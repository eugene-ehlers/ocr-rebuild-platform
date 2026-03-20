import React from "react";
import { Alert, PageSection } from "../../design_system/components";

export function DocumentLifecycleExplainer() {
  return (
    <PageSection title="Document Lifecycle Rules">
      <Alert variant="info">Documents may consist of multiple pages and multiple files forming one logical document.</Alert>
      <Alert variant="warning">Completeness, ordering, freshness, and reuse eligibility must be validated before service usage.</Alert>
      <Alert variant="info">Poor quality, missing pages, and incorrect ordering must produce remediation guidance.</Alert>
    </PageSection>
  );
}
