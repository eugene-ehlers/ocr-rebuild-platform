import React from "react";
import { Button, EmptyState, InputField, PageSection } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";
import { OriginalDataNotice } from "../components/OriginalDataNotice";

export function OriginalResultViewPage() {
  return (
    <AppShell title="Original Result View">
      <OriginalDataNotice />
      <PageSection title="View Original Result">
        <InputField label="Document ID" name="documentId" />
        <Button label="Load Original Result" />
        <EmptyState
          title="Original result placeholder"
          description="Original OCR value and system interpretation will be displayed here."
        />
      </PageSection>
    </AppShell>
  );
}
