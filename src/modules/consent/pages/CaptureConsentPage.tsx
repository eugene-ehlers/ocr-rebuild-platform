import React from "react";
import {
  Button,
  InputField,
  PageSection,
  SelectField
} from "../../design_system/components";
import { AppShell } from "../../design_system/layout";
import { ConsentTypeExplainer } from "../components/ConsentTypeExplainer";

export function CaptureConsentPage() {
  return (
    <AppShell title="Capture Consent">
      <ConsentTypeExplainer />
      <PageSection title="Consent Capture">
        <InputField label="Customer ID" name="customerId" />
        <InputField label="Granted By" name="grantedBy" />
        <SelectField
          label="Consent Type"
          name="consentType"
          options={[
            { label: "Processing", value: "processing" },
            { label: "Disclosure", value: "disclosure" }
          ]}
        />
        <SelectField
          label="Standing Consent"
          name="standingConsent"
          options={[
            { label: "No", value: "false" },
            { label: "Yes", value: "true" }
          ]}
        />
        <InputField label="Expiry Date" name="expiryDate" type="date" />
        <Button label="Capture Consent" />
      </PageSection>
    </AppShell>
  );
}
