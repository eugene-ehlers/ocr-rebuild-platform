import React from "react";
import { Button, InputField, PageSection } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";
import { StatusTimeline } from "../components/StatusTimeline";

export function RequestStatusPage() {
  return (
    <AppShell title="Request Status">
      <PageSection title="Status Tracking">
        <InputField label="Request ID" name="requestId" />
        <Button label="Retrieve Status" />
        <StatusTimeline
          statuses={[
            "submitted",
            "in_progress",
            "needs_remediation",
            "completed"
          ]}
        />
      </PageSection>
    </AppShell>
  );
}
