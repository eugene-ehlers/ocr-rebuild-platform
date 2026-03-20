import React from "react";
import { EmptyState, PageSection } from "../../design_system/components";

export function UsageSummaryPanel() {
  return (
    <PageSection title="Usage Visibility">
      <EmptyState
        title="Usage placeholder"
        description="Services used, request history, and consumption metrics will appear here."
      />
    </PageSection>
  );
}
