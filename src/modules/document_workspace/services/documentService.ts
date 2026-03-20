import { apiClient } from "../../../api/client";
import { API_ROUTES } from "../../../api/routes";
import {
  AppendPagesInput,
  MergeDocumentsInput,
  ReorderPagesInput,
  ReplaceDocumentInput,
  SplitDocumentInput,
  UploadRegistrationInput
} from "../types";

export async function registerUpload(payload: UploadRegistrationInput) {
  return apiClient(`${API_ROUTES.documents}/upload-registration`, {
    method: "POST",
    body: payload
  });
}

export async function retrieveDocument(documentId: string) {
  return apiClient(`${API_ROUTES.documents}/retrieve?documentId=${encodeURIComponent(documentId)}`, {
    method: "GET"
  });
}

export async function replaceDocument(payload: ReplaceDocumentInput) {
  return apiClient(`${API_ROUTES.documents}/replace`, {
    method: "POST",
    body: payload
  });
}

export async function appendPages(payload: AppendPagesInput) {
  return apiClient(`${API_ROUTES.documents}/append`, {
    method: "POST",
    body: payload
  });
}

export async function reorderPages(payload: ReorderPagesInput) {
  return apiClient(`${API_ROUTES.documents}/reorder`, {
    method: "POST",
    body: payload
  });
}

export async function mergeDocuments(payload: MergeDocumentsInput) {
  return apiClient(`${API_ROUTES.documents}/merge`, {
    method: "POST",
    body: payload
  });
}

export async function splitDocument(payload: SplitDocumentInput) {
  return apiClient(`${API_ROUTES.documents}/split`, {
    method: "POST",
    body: payload
  });
}

export async function validateCompleteness(documentId: string) {
  return apiClient(`${API_ROUTES.documents}/validate-completeness?documentId=${encodeURIComponent(documentId)}`, {
    method: "GET"
  });
}

export async function validateFreshness(documentId: string) {
  return apiClient(`${API_ROUTES.documents}/validate-freshness?documentId=${encodeURIComponent(documentId)}`, {
    method: "GET"
  });
}
