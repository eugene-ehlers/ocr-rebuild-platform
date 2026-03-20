import React from "react";
import { Button, InputField } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";
import { ActivityLogPanel } from "../components/ActivityLogPanel";

export function ActivityLogPage() {
  return (
    <AppShell title="Activity Log View">
      <InputField label="Customer ID" name="customerId" />
      <Button label="Load Activity Logs" />
      <ActivityLogPanel />
    </AppShell>
  );
}
