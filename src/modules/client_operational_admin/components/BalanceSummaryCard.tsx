import React from "react";
import { EmptyState, PageSection } from "../../design_system/components";

export function BalanceSummaryCard() {
  return (
    <PageSection title="Balance Summary">
      <EmptyState
        title="Balance placeholder"
        description="Customer balance and credits will be displayed here."
      />
    </PageSection>
  );
}
