import React from "react";
import {
  Button,
  InputField,
  PageSection,
  SelectField
} from "../../design_system/components";
import { AppShell } from "../../design_system/layout";

export function RequestCreationPage() {
  return (
    <AppShell title="Create Service Request">
      <PageSection title="Request Creation">
        <InputField label="Customer ID" name="customerId" />
        <InputField label="Document IDs (comma separated)" name="documentIds" />
        <SelectField
          label="Service Code"
          name="serviceCode"
          options={[
            { label: "Financial Management", value: "financial_management" },
            { label: "FICA Compliance", value: "fica" },
            { label: "Credit Decision", value: "credit_decision" }
          ]}
        />
        <SelectField
          label="Disclosure to Third Party"
          name="discloseToThirdParty"
          options={[
            { label: "No", value: "false" },
            { label: "Yes", value: "true" }
          ]}
        />
        <Button label="Create Request" />
      </PageSection>
    </AppShell>
  );
}
