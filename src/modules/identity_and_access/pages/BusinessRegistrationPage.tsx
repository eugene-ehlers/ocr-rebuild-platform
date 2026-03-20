import React from "react";
import {
  Button,
  FormErrorSummary,
  InputField,
  PageSection
} from "../../design_system/components";
import { AppShell } from "../../design_system/layout";

export function BusinessRegistrationPage() {
  return (
    <AppShell title="Business Registration">
      <PageSection title="Business Onboarding">
        <p>Business registration scaffold with organization context.</p>
        <FormErrorSummary errors={[]} />
        <InputField label="Business Name" name="businessName" />
        <InputField label="Registration Number" name="registrationNumber" />
        <InputField label="Admin First Name" name="adminFirstName" />
        <InputField label="Admin Last Name" name="adminLastName" />
        <InputField label="Email" name="email" type="email" />
        <InputField label="Password" name="password" type="password" />
        <Button label="Register Business User" />
      </PageSection>
    </AppShell>
  );
}
