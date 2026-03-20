import React from "react";
import { Button, InputField, PageSection } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";

export function DocumentTelemetryPage() {
  return (
    <AppShell title="Document Telemetry">
      <PageSection title="Track Document Event">
        <InputField label="Event Type" name="eventType" />
        <InputField label="Module" name="module" />
        <InputField label="Action" name="action" />
        <Button label="Track Document Event" />
      </PageSection>
    </AppShell>
  );
}
