import React from "react";
import { Button, InputField, PageSection } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";

export function RevokeConsentPage() {
  return (
    <AppShell title="Revoke Consent">
      <PageSection title="Consent Revocation">
        <InputField label="Consent ID" name="consentId" />
        <InputField label="Revoked By" name="revokedBy" />
        <InputField label="Reason" name="reason" />
        <Button label="Revoke Consent" />
      </PageSection>
    </AppShell>
  );
}
