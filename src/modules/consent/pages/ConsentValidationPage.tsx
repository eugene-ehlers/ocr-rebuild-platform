import React from "react";
import {
  Button,
  InputField,
  PageSection,
  SelectField
} from "../../design_system/components";
import { AppShell } from "../../design_system/layout";

export function ConsentValidationPage() {
  return (
    <AppShell title="Validate Consent">
      <PageSection title="Consent Validation">
        <InputField label="Customer ID" name="customerId" />
        <SelectField
          label="Consent Type"
          name="consentType"
          options={[
            { label: "Processing", value: "processing" },
            { label: "Disclosure", value: "disclosure" }
          ]}
        />
        <InputField label="Action" name="action" />
        <Button label="Validate Consent" />
      </PageSection>
    </AppShell>
  );
}
