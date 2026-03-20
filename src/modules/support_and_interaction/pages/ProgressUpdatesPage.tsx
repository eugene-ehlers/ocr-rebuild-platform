import React from "react";
import { Button, InputField } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";
import { ProgressUpdatePanel } from "../components/ProgressUpdatePanel";

export function ProgressUpdatesPage() {
  return (
    <AppShell title="Progress Updates View">
      <InputField label="Request ID" name="requestId" />
      <Button label="Load Progress Updates" />
      <ProgressUpdatePanel />
    </AppShell>
  );
}
