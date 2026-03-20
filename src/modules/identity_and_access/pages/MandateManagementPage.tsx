import React from "react";
import { EmptyState, PageSection } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";

export function MandateManagementPage() {
  return (
    <AppShell title="Mandate Management">
      <PageSection title="Mandates">
        <EmptyState
          title="Mandate management placeholder"
          description="Act-on-behalf-of scaffolding for valid business mandate handling."
        />
      </PageSection>
    </AppShell>
  );
}
