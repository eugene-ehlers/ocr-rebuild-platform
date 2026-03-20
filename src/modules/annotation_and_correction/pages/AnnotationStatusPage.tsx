import React from "react";
import { Button, InputField, PageSection } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";
import { AnnotationStatusPanel } from "../components/AnnotationStatusPanel";

export function AnnotationStatusPage() {
  return (
    <AppShell title="Annotation Status">
      <PageSection title="Status Tracking">
        <InputField label="Annotation ID" name="annotationId" />
        <Button label="Load Annotation Status" />
      </PageSection>
      <AnnotationStatusPanel />
    </AppShell>
  );
}
