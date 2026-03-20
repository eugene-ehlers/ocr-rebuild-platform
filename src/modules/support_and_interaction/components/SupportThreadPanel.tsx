import React from "react";
import { EmptyState, PageSection } from "../../design_system/components";

export function SupportThreadPanel() {
  return (
    <PageSection title="Support Thread">
      <EmptyState
        title="Support thread placeholder"
        description="Support conversation history will be displayed here when connected."
      />
    </PageSection>
  );
}
