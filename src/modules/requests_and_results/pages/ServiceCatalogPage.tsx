import React from "react";
import { Button, EmptyState, PageSection } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";
import { ServiceFamilyNotice } from "../components/ServiceFamilyNotice";

export function ServiceCatalogPage() {
  return (
    <AppShell title="Service Catalog">
      <ServiceFamilyNotice />
      <PageSection title="Available Services">
        <Button label="Load Service Catalog" />
        <EmptyState
          title="Catalog placeholder"
          description="Service catalog items will be displayed here."
        />
      </PageSection>
    </AppShell>
  );
}
