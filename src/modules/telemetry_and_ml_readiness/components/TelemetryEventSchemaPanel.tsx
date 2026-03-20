import React from "react";
import { EmptyState, PageSection } from "../../design_system/components";

export function TelemetryEventSchemaPanel() {
  return (
    <PageSection title="Telemetry Event Schema">
      <EmptyState
        title="Telemetry schema placeholder"
        description='Expected shape: {"event_type","timestamp","user_id","session_id","module","action","metadata"}.'
      />
    </PageSection>
  );
}
