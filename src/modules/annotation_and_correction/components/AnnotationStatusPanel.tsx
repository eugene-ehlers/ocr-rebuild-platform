import React from "react";
import { EmptyState, PageSection } from "../../design_system/components";

export function AnnotationStatusPanel() {
  return (
    <PageSection title="Reviewer Status">
      <EmptyState
        title="Reviewer status placeholder"
        description="Reviewer workflow and final resolution status will be displayed here."
      />
    </PageSection>
  );
}
