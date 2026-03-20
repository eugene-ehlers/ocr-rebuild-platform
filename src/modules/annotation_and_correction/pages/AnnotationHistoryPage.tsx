import React from "react";
import { Button, InputField, PageSection } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";
import { AnnotationHistoryList } from "../components/AnnotationHistoryList";

export function AnnotationHistoryPage() {
  return (
    <AppShell title="Annotation History">
      <PageSection title="History">
        <InputField label="Document ID" name="documentId" />
        <Button label="Load Annotation History" />
        <AnnotationHistoryList items={[]} />
      </PageSection>
    </AppShell>
  );
}
