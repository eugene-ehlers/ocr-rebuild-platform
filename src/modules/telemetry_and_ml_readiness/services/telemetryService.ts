import { apiClient } from "../../../api/client";
import { API_ROUTES } from "../../../api/routes";
import {
  TelemetryEventRecord,
  WorkflowTrackingEvent
} from "../types";

export async function logEvent(payload: TelemetryEventRecord) {
  return apiClient(`${API_ROUTES.telemetry}/event`, {
    method: "POST",
    body: payload
  });
}

export async function logWorkflow(payload: WorkflowTrackingEvent) {
  return apiClient(`${API_ROUTES.telemetry}/workflow`, {
    method: "POST",
    body: payload
  });
}

export async function logDocumentHandling(payload: TelemetryEventRecord) {
  return apiClient(`${API_ROUTES.telemetry}/document-handling`, {
    method: "POST",
    body: payload
  });
}

export async function logSupportInteraction(payload: TelemetryEventRecord) {
  return apiClient(`${API_ROUTES.telemetry}/support`, {
    method: "POST",
    body: payload
  });
}

export async function logRemediationInteraction(payload: TelemetryEventRecord) {
  return apiClient(`${API_ROUTES.telemetry}/remediation`, {
    method: "POST",
    body: payload
  });
}
