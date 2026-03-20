export type SupportRequestStatus = "open" | "in_progress" | "waiting_on_customer" | "resolved" | "closed";
export type SupportInteractionType = "support_request" | "progress_update" | "remediation_prompt" | "chat_placeholder";

export interface SupportRequestInput {
  customerId: string;
  subject: string;
  description: string;
  requestId?: string;
}

export interface SupportRequestRecord {
  supportRequestId: string;
  customerId: string;
  requestId?: string;
  subject: string;
  description: string;
  status: SupportRequestStatus;
  createdAt: string;
}

export interface SupportThreadMessage {
  messageId: string;
  supportRequestId: string;
  interactionType: SupportInteractionType;
  message: string;
  createdAt: string;
  placeholder: boolean;
}

export interface ProgressUpdateRecord {
  requestId: string;
  status: string;
  message: string;
  createdAt: string;
}

export interface RemediationInteractionRecord {
  requestId: string;
  reason: string;
  suggestedAction: string;
  createdAt: string;
}
