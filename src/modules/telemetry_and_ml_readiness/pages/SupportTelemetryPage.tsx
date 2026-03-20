import React from "react";
import { Button, InputField, PageSection } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";

export function SupportTelemetryPage() {
  return (
    <AppShell title="Support Telemetry">
      <PageSection title="Track Support Event">
        <InputField label="Event Type" name="eventType" />
        <InputField label="Module" name="module" />
        <InputField label="Action" name="action" />
        <Button label="Track Support Event" />
      </PageSection>
    </AppShell>
  );
}
