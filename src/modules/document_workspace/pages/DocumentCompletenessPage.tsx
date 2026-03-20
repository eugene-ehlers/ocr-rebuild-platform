import React from "react";
import { Button, EmptyState, InputField, PageSection } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";
import { QualityFeedbackPanel } from "../components/QualityFeedbackPanel";

export function DocumentCompletenessPage() {
  return (
    <AppShell title="Completeness and Remediation">
      <QualityFeedbackPanel />
      <PageSection title="Completeness Validation">
        <InputField label="Document ID" name="documentId" />
        <Button label="Validate Completeness" />
        <EmptyState
          title="Completeness placeholder"
          description="Missing pages, quality issues, and remediation prompts will be shown here."
        />
      </PageSection>
    </AppShell>
  );
}
