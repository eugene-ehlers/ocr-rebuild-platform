import React from "react";
import { Alert, EmptyState, PageSection } from "../../design_system/components";

export function QualityFeedbackPanel() {
  return (
    <PageSection title="Quality Assistance">
      <Alert variant="warning">Quality feedback is a placeholder and does not implement OCR quality scoring in this phase.</Alert>
      <EmptyState
        title="Quality feedback placeholder"
        description="Missing pages, skew, and poor quality guidance will be surfaced here when connected."
      />
    </PageSection>
  );
}
