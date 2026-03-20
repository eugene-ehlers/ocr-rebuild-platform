import { apiClient } from "../../../api/client";
import { API_ROUTES } from "../../../api/routes";
import {
  CreateAnnotationInput,
  TriggerReprocessingInput,
  UpdateAnnotationInput
} from "../types";

export async function createAnnotation(payload: CreateAnnotationInput) {
  return apiClient(`${API_ROUTES.annotations}/create`, {
    method: "POST",
    body: payload
  });
}

export async function updateAnnotation(payload: UpdateAnnotationInput) {
  return apiClient(`${API_ROUTES.annotations}/update`, {
    method: "POST",
    body: payload
  });
}

export async function getAnnotationHistory(documentId: string) {
  return apiClient(`${API_ROUTES.annotations}/history?documentId=${encodeURIComponent(documentId)}`, {
    method: "GET"
  });
}

export async function getAnnotationStatus(annotationId: string) {
  return apiClient(`${API_ROUTES.annotations}/status?annotationId=${encodeURIComponent(annotationId)}`, {
    method: "GET"
  });
}

export async function triggerReprocessing(payload: TriggerReprocessingInput) {
  return apiClient(`${API_ROUTES.annotations}/reprocess`, {
    method: "POST",
    body: payload
  });
}
