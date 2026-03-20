import React from "react";
import { Button, InputField, PageSection } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";
import { RemediationPromptPanel } from "../components/RemediationPromptPanel";

export function RequestRemediationPage() {
  return (
    <AppShell title="Request Remediation">
      <PageSection title="Remediation Handling">
        <InputField label="Request ID" name="requestId" />
        <Button label="Load Remediation Prompts" />
      </PageSection>
      <RemediationPromptPanel />
    </AppShell>
  );
}
