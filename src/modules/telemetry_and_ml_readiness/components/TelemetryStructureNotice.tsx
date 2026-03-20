import React from "react";
import { Alert, PageSection } from "../../design_system/components";

export function TelemetryStructureNotice() {
  return (
    <PageSection title="Telemetry Structure Rules">
      <Alert variant="info">Telemetry must be structured for analytics and future ML readiness.</Alert>
      <Alert variant="warning">All major actions should emit structured events with module, action, timestamp, and metadata.</Alert>
    </PageSection>
  );
}
