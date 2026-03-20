import React from "react";
import { AppShell } from "../../design_system/layout";
import { TelemetryEventSchemaPanel } from "../components/TelemetryEventSchemaPanel";
import { TelemetryStructureNotice } from "../components/TelemetryStructureNotice";

export function TelemetryOverviewPage() {
  return (
    <AppShell title="Telemetry Overview">
      <TelemetryStructureNotice />
      <TelemetryEventSchemaPanel />
    </AppShell>
  );
}
