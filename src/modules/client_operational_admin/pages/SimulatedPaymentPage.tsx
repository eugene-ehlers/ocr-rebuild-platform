import React from "react";
import { Button, InputField, PageSection } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";

export function SimulatedPaymentPage() {
  return (
    <AppShell title="Simulated Payment">
      <PageSection title="Create Simulated Payment">
        <InputField label="Customer ID" name="customerId" />
        <InputField label="Amount" name="amount" type="number" />
        <InputField label="Currency" name="currency" />
        <InputField label="Reference" name="reference" />
        <Button label="Submit Simulated Payment" />
      </PageSection>
    </AppShell>
  );
}
