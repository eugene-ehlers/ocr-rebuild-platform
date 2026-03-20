import React from "react";
import { Alert, PageSection } from "../../design_system/components";

export function AuditabilityNotice() {
  return (
    <PageSection title="Auditability Rules">
      <Alert variant="warning">All actions in operational administration must be auditable.</Alert>
      <Alert variant="info">Financial data, usage data, and activity logs must remain traceable.</Alert>
    </PageSection>
  );
}
