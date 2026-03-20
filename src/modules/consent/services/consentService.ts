import { apiClient } from "../../../api/client";
import { API_ROUTES } from "../../../api/routes";
import {
  CaptureConsentInput,
  RevokeConsentInput,
  ValidateConsentInput
} from "../types";

export async function captureConsent(payload: CaptureConsentInput) {
  return apiClient(`${API_ROUTES.consent}/capture`, {
    method: "POST",
    body: payload
  });
}

export async function validateConsent(payload: ValidateConsentInput) {
  return apiClient(`${API_ROUTES.consent}/validate`, {
    method: "POST",
    body: payload
  });
}

export async function retrieveConsent(customerId: string) {
  return apiClient(`${API_ROUTES.consent}/retrieve?customerId=${encodeURIComponent(customerId)}`, {
    method: "GET"
  });
}

export async function revokeConsent(payload: RevokeConsentInput) {
  return apiClient(`${API_ROUTES.consent}/revoke`, {
    method: "POST",
    body: payload
  });
}

export async function retrieveConsentProof(consentId: string) {
  return apiClient(`${API_ROUTES.consent}/proof?consentId=${encodeURIComponent(consentId)}`, {
    method: "GET"
  });
}
