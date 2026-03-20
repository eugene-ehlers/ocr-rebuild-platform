import React from "react";
import { EmptyState, PageSection } from "../../design_system/components";

export function ActivityLogPanel() {
  return (
    <PageSection title="Activity Logs">
      <EmptyState
        title="Activity log placeholder"
        description="User activity, login history, and action audit trails will appear here."
      />
    </PageSection>
  );
}
