import React from "react";
import { EmptyState, PageSection } from "../../design_system/components";

export function ProgressUpdatePanel() {
  return (
    <PageSection title="Progress Updates">
      <EmptyState
        title="Progress updates placeholder"
        description="Request progress updates and guided workflow messages will appear here."
      />
    </PageSection>
  );
}
