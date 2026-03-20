import React from "react";
import { Button, InputField, PageSection } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";

export function WorkflowTrackingPage() {
  return (
    <AppShell title="Workflow Tracking">
      <PageSection title="Track Workflow Event">
        <InputField label="Workflow ID" name="workflowId" />
        <InputField label="Request ID" name="requestId" />
        <InputField label="Module" name="module" />
        <InputField label="Step" name="step" />
        <InputField label="Status" name="status" />
        <Button label="Track Workflow Event" />
      </PageSection>
    </AppShell>
  );
}
