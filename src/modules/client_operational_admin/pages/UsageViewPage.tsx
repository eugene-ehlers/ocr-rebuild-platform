import React from "react";
import { Button, InputField } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";
import { UsageSummaryPanel } from "../components/UsageSummaryPanel";

export function UsageViewPage() {
  return (
    <AppShell title="Usage View">
      <InputField label="Customer ID" name="customerId" />
      <Button label="Load Usage" />
      <UsageSummaryPanel />
    </AppShell>
  );
}
