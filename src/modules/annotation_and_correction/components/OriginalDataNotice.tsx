import React from "react";
import { Alert, PageSection } from "../../design_system/components";

export function OriginalDataNotice() {
  return (
    <PageSection title="Original Data Preservation">
      <Alert variant="warning">Original OCR data must never be overwritten.</Alert>
      <Alert variant="info">Original OCR value, system interpretation, user suggestion, reviewer status, and final resolved value must remain separately traceable.</Alert>
    </PageSection>
  );
}
