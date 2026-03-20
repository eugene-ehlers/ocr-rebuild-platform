import React from "react";
import { Button, InputField } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";
import { SupportThreadPanel } from "../components/SupportThreadPanel";

export function SupportThreadPage() {
  return (
    <AppShell title="Support Thread View">
      <InputField label="Support Request ID" name="supportRequestId" />
      <Button label="Load Support Thread" />
      <SupportThreadPanel />
    </AppShell>
  );
}
