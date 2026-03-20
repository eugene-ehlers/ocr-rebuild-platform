import React from "react";
import { Button, InputField, PageSection, SelectField } from "../../design_system/components";
import { AppShell } from "../../design_system/layout";
import { DocumentLifecycleExplainer } from "../components/DocumentLifecycleExplainer";

export function DocumentUploadPage() {
  return (
    <AppShell title="Document Upload">
      <DocumentLifecycleExplainer />
      <PageSection title="Upload Registration">
        <InputField label="Customer ID" name="customerId" />
        <InputField label="File Name" name="fileName" />
        <InputField label="Content Type" name="contentType" />
        <SelectField
          label="Document Type"
          name="documentType"
          options={[
            { label: "Bank Statement", value: "bank_statement" },
            { label: "Identity Document", value: "identity_document" },
            { label: "Payslip", value: "payslip" },
            { label: "Other", value: "other" }
          ]}
        />
        <Button label="Register Upload" />
      </PageSection>
    </AppShell>
  );
}
