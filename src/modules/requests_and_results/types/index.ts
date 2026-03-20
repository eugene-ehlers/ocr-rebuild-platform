export type ServiceFamily = "financial_management" | "fica" | "credit_decision";
export type RequestStatus =
  | "draft"
  | "submitted"
  | "in_progress"
  | "needs_remediation"
  | "completed"
  | "failed";

export interface ServiceCatalogItem {
  serviceCode: string;
  serviceName: string;
  serviceFamily: ServiceFamily;
  description: string;
  requiresProcessingConsent: boolean;
  requiresDisclosureConsent: boolean;
}

export interface ServiceRequestInput {
  customerId: string;
  serviceCode: string;
  documentIds: string[];
  discloseToThirdParty: boolean;
}

export interface ServiceRequestRecord {
  requestId: string;
  customerId: string;
  serviceCode: string;
  serviceFamily: ServiceFamily;
  status: RequestStatus;
  createdAt: string;
  updatedAt: string;
}

export interface RemediationPrompt {
  promptId: string;
  requestId: string;
  reason: string;
  suggestedAction: string;
}

export interface ServiceResultRecord {
  requestId: string;
  resultStatus: "available" | "pending" | "blocked";
  summary: string;
  placeholder: boolean;
}
