import { apiClient } from "../../../api/client";
import { API_ROUTES } from "../../../api/routes";
import { ServiceRequestInput } from "../types";

export async function getServiceCatalog() {
  return apiClient(`${API_ROUTES.requestsResults}/catalog`, {
    method: "GET"
  });
}

export async function createServiceRequest(payload: ServiceRequestInput) {
  return apiClient(`${API_ROUTES.requestsResults}/create`, {
    method: "POST",
    body: payload
  });
}

export async function getRequestStatus(requestId: string) {
  return apiClient(`${API_ROUTES.requestsResults}/status?requestId=${encodeURIComponent(requestId)}`, {
    method: "GET"
  });
}

export async function getRemediationPrompts(requestId: string) {
  return apiClient(`${API_ROUTES.requestsResults}/remediation?requestId=${encodeURIComponent(requestId)}`, {
    method: "GET"
  });
}

export async function getResult(requestId: string) {
  return apiClient(`${API_ROUTES.requestsResults}/result?requestId=${encodeURIComponent(requestId)}`, {
    method: "GET"
  });
}

export async function triggerRerun(requestId: string) {
  return apiClient(`${API_ROUTES.requestsResults}/rerun`, {
    method: "POST",
    body: { requestId }
  });
}
