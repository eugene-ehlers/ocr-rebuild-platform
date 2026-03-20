import React from "react";
import { Button, EmptyState, InputField, PageSection } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";

export function RerunRequestPage() {
  return (
    <AppShell title="Rerun Request">
      <PageSection title="Rerun Placeholder">
        <InputField label="Request ID" name="requestId" />
        <Button label="Trigger Rerun" />
        <EmptyState
          title="Rerun placeholder"
          description="Downstream rerun integration is represented by a placeholder in this phase."
        />
      </PageSection>
    </AppShell>
  );
}
