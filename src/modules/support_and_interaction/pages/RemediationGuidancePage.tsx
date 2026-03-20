import React from "react";
import { Button, InputField } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";
import { RemediationInteractionPanel } from "../components/RemediationInteractionPanel";

export function RemediationGuidancePage() {
  return (
    <AppShell title="Remediation Guidance View">
      <InputField label="Request ID" name="requestId" />
      <Button label="Load Remediation Guidance" />
      <RemediationInteractionPanel />
    </AppShell>
  );
}
