import React from "react";
import { Button, PageSection } from "../../design_system/components";

interface IdentityJourneySelectorProps {
  onSelect: (journey: "personal" | "business") => void;
}

export function IdentityJourneySelector({ onSelect }: IdentityJourneySelectorProps) {
  return (
    <PageSection title="Choose Registration Journey">
      <p>Select the appropriate onboarding journey.</p>
      <Button label="Personal Journey" onClick={() => onSelect("personal")} />
      <Button label="Business Journey" onClick={() => onSelect("business")} />
    </PageSection>
  );
}
