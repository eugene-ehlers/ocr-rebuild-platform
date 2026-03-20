import React from "react";
import { Button, InputField, PageSection } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";

export function AddAnnotationPage() {
  return (
    <AppShell title="Add Annotation">
      <PageSection title="Submit Annotation">
        <InputField label="Document ID" name="documentId" />
        <InputField label="Field Reference" name="fieldReference" />
        <InputField label="Original Value" name="originalValue" />
        <InputField label="System Interpretation" name="systemInterpretation" />
        <InputField label="User Suggestion" name="userSuggestion" />
        <Button label="Store Suggestion" />
      </PageSection>
    </AppShell>
  );
}
