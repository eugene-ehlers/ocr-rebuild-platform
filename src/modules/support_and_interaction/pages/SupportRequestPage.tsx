import React from "react";
import { Button, InputField, PageSection } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";
import { SupportPlaceholderNotice } from "../components/SupportPlaceholderNotice";

export function SupportRequestPage() {
  return (
    <AppShell title="Support Request">
      <SupportPlaceholderNotice />
      <PageSection title="Create Support Request">
        <InputField label="Customer ID" name="customerId" />
        <InputField label="Request ID (optional)" name="requestId" />
        <InputField label="Subject" name="subject" />
        <InputField label="Description" name="description" />
        <Button label="Create Support Request" />
      </PageSection>
    </AppShell>
  );
}
