import { apiClient } from "../../../api/client";
import { API_ROUTES } from "../../../api/routes";
import { SupportRequestInput } from "../types";

export async function createSupportRequest(payload: SupportRequestInput) {
  return apiClient(`${API_ROUTES.support}/create`, {
    method: "POST",
    body: payload
  });
}

export async function getSupportThread(supportRequestId: string) {
  return apiClient(`${API_ROUTES.support}/thread?supportRequestId=${encodeURIComponent(supportRequestId)}`, {
    method: "GET"
  });
}

export async function getProgressUpdates(requestId: string) {
  return apiClient(`${API_ROUTES.support}/progress?requestId=${encodeURIComponent(requestId)}`, {
    method: "GET"
  });
}

export async function getRemediationInteractions(requestId: string) {
  return apiClient(`${API_ROUTES.support}/remediation?requestId=${encodeURIComponent(requestId)}`, {
    method: "GET"
  });
}

export async function getChatPlaceholder() {
  return apiClient(`${API_ROUTES.support}/chat-placeholder`, {
    method: "GET"
  });
}
