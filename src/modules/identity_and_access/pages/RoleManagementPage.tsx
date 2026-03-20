import React from "react";
import { EmptyState, PageSection } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";

export function RoleManagementPage() {
  return (
    <AppShell title="Role Management">
      <PageSection title="Roles">
        <EmptyState
          title="Role management placeholder"
          description="Role-based access scaffolding for business and admin journeys."
        />
      </PageSection>
    </AppShell>
  );
}
