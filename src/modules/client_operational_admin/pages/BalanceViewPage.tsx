import React from "react";
import { Button, InputField } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";
import { AuditabilityNotice } from "../components/AuditabilityNotice";
import { BalanceSummaryCard } from "../components/BalanceSummaryCard";

export function BalanceViewPage() {
  return (
    <AppShell title="Balance View">
      <AuditabilityNotice />
      <InputField label="Customer ID" name="customerId" />
      <Button label="Load Balance" />
      <BalanceSummaryCard />
    </AppShell>
  );
}
