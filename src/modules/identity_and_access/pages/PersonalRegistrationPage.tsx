import React from "react";
import {
  Button,
  FormErrorSummary,
  InputField,
  PageSection
} from "../../design_system/components";
import { AppShell } from "../../design_system/layout";

export function PersonalRegistrationPage() {
  return (
    <AppShell title="Personal Registration">
      <PageSection title="Personal Onboarding">
        <p>Simple onboarding scaffold for personal users.</p>
        <FormErrorSummary errors={[]} />
        <InputField label="First Name" name="firstName" />
        <InputField label="Last Name" name="lastName" />
        <InputField label="Email" name="email" type="email" />
        <InputField label="Password" name="password" type="password" />
        <Button label="Register Personal User" />
      </PageSection>
    </AppShell>
  );
}
