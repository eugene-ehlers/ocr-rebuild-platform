import React from "react";
import { Button, InputField, PageSection } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";

export function SupportQueryPage() {
  return (
    <AppShell title="Operational Support Query">
      <PageSection title="Submit Query or Issue">
        <InputField label="Customer ID" name="customerId" />
        <InputField label="Subject" name="subject" />
        <InputField label="Description" name="description" />
        <Button label="Submit Query" />
      </PageSection>
    </AppShell>
  );
}
