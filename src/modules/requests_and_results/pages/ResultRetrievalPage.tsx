import React from "react";
import { Button, EmptyState, InputField, PageSection } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";

export function ResultRetrievalPage() {
  return (
    <AppShell title="Result Retrieval">
      <PageSection title="Retrieve Result">
        <InputField label="Request ID" name="requestId" />
        <Button label="Retrieve Result" />
        <EmptyState
          title="Result placeholder"
          description="Structured downstream results will be displayed here when connected."
        />
      </PageSection>
    </AppShell>
  );
}
