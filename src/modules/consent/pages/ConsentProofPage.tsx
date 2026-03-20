import React from "react";
import { Button, EmptyState, InputField, PageSection } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";

export function ConsentProofPage() {
  return (
    <AppShell title="Consent Proof">
      <PageSection title="Proof Retrieval">
        <InputField label="Consent ID" name="consentId" />
        <Button label="Retrieve Proof" />
        <EmptyState
          title="Proof retrieval placeholder"
          description="Auditable consent proof output will be displayed here."
        />
      </PageSection>
    </AppShell>
  );
}
