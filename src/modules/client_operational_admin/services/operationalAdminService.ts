import { apiClient } from "../../../api/client";
import { API_ROUTES } from "../../../api/routes";
import {
  SimulatedPaymentInput,
  SupportQueryInput
} from "../types";

export async function getBalance(customerId: string) {
  return apiClient(`${API_ROUTES.operationalAdmin}/balance?customerId=${encodeURIComponent(customerId)}`, {
    method: "GET"
  });
}

export async function getUsage(customerId: string) {
  return apiClient(`${API_ROUTES.operationalAdmin}/usage?customerId=${encodeURIComponent(customerId)}`, {
    method: "GET"
  });
}

export async function getActivityLogs(customerId: string) {
  return apiClient(`${API_ROUTES.operationalAdmin}/activity?customerId=${encodeURIComponent(customerId)}`, {
    method: "GET"
  });
}

export async function createSimulatedPayment(payload: SimulatedPaymentInput) {
  return apiClient(`${API_ROUTES.operationalAdmin}/simulated-payment`, {
    method: "POST",
    body: payload
  });
}

export async function submitSupportQuery(payload: SupportQueryInput) {
  return apiClient(`${API_ROUTES.operationalAdmin}/support-query`, {
    method: "POST",
    body: payload
  });
}
