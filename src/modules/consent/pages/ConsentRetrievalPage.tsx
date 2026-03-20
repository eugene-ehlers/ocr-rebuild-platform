import React from "react";
import { Button, EmptyState, InputField, PageSection } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";

export function ConsentRetrievalPage() {
  return (
    <AppShell title="Retrieve Consent">
      <PageSection title="Consent Retrieval">
        <InputField label="Customer ID" name="customerId" />
        <Button label="Retrieve Consent Records" />
        <EmptyState
          title="Consent retrieval placeholder"
          description="Consent records and auditable history will appear here once connected."
        />
      </PageSection>
    </AppShell>
  );
}
