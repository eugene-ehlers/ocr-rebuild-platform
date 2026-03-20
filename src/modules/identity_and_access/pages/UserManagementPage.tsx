import React from "react";
import { EmptyState, PageSection } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";

export function UserManagementPage() {
  return (
    <AppShell title="User Management">
      <PageSection title="Users">
        <EmptyState
          title="User management placeholder"
          description="Create and update users will be wired into the identity/admin API scaffold."
        />
      </PageSection>
    </AppShell>
  );
}
