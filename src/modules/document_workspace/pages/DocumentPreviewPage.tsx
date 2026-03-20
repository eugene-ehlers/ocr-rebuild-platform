import React from "react";
import { EmptyState, InputField, PageSection, Button } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";

export function DocumentPreviewPage() {
  return (
    <AppShell title="Document Preview">
      <PageSection title="Preview">
        <InputField label="Document ID" name="documentId" />
        <Button label="Retrieve Document" />
        <EmptyState
          title="Preview placeholder"
          description="Document preview rendering will appear here once connected."
        />
      </PageSection>
    </AppShell>
  );
}
