import React from "react";
import { EmptyState, PageSection } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";

export function ChatPlaceholderPage() {
  return (
    <AppShell title="Future Chat Placeholder">
      <PageSection title="Chat Placeholder">
        <EmptyState
          title="Future chat placeholder"
          description="Live chat is out of scope in this phase and remains a placeholder only."
        />
      </PageSection>
    </AppShell>
  );
}
