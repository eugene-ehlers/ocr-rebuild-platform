import React from "react";
import { Button, EmptyState, InputField, PageSection } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";

export function ReprocessingTriggerPage() {
  return (
    <AppShell title="Reprocessing Trigger">
      <PageSection title="Trigger Reprocessing">
        <InputField label="Annotation ID" name="annotationId" />
        <InputField label="Request ID" name="requestId" />
        <Button label="Trigger Reprocessing" />
        <EmptyState
          title="Reprocessing placeholder"
          description="Accepted corrections can trigger downstream reprocessing via placeholder integration in this phase."
        />
      </PageSection>
    </AppShell>
  );
}
