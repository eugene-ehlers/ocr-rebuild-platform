import React from "react";
import { Button, EmptyState, InputField, PageSection } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";

export function DocumentFreshnessPage() {
  return (
    <AppShell title="Freshness and Reuse">
      <PageSection title="Freshness / Reuse Validation">
        <InputField label="Document ID" name="documentId" />
        <Button label="Validate Freshness" />
        <EmptyState
          title="Freshness placeholder"
          description="Expiry, freshness, and reuse eligibility will be surfaced here."
        />
      </PageSection>
    </AppShell>
  );
}
