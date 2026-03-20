import React from "react";
import {
  Button,
  FormErrorSummary,
  InputField,
  PageSection
} from "../../design_system/components";
import { AppShell } from "../../design_system/layout";

export function LoginPage() {
  return (
    <AppShell title="Login">
      <PageSection title="Access Control Plane">
        <p>Login scaffold for authenticated access.</p>
        <FormErrorSummary errors={[]} />
        <InputField label="Email" name="email" type="email" />
        <InputField label="Password" name="password" type="password" />
        <Button label="Login" />
      </PageSection>
    </AppShell>
  );
}
