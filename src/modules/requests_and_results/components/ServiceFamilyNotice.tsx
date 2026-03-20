import React from "react";
import { Alert, PageSection } from "../../design_system/components";

export function ServiceFamilyNotice() {
  return (
    <PageSection title="Downstream Service Families">
      <Alert variant="info">Financial Management, FICA, and Credit Decision are downstream service families integrated by placeholder interfaces only in this phase.</Alert>
      <Alert variant="warning">This module scaffolds orchestration and retrieval flows, not downstream business logic.</Alert>
    </PageSection>
  );
}
