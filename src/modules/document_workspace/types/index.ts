export type DocumentQualityStatus = "unknown" | "acceptable" | "poor";
export type DocumentFreshnessStatus = "fresh" | "stale" | "expired" | "unknown";
export type DocumentReuseStatus = "eligible" | "ineligible" | "review_required";

export interface DocumentPage {
  pageId: string;
  pageNumber: number;
  fileName: string;
}

export interface DocumentRecord {
  documentId: string;
  customerId: string;
  documentType: string;
  pages: DocumentPage[];
  qualityStatus: DocumentQualityStatus;
  freshnessStatus: DocumentFreshnessStatus;
  reuseStatus: DocumentReuseStatus;
  completenessStatus: "complete" | "incomplete" | "unknown";
  expiryDate?: string;
}

export interface UploadRegistrationInput {
  customerId: string;
  documentType: string;
  fileName: string;
  contentType: string;
}

export interface ReplaceDocumentInput {
  documentId: string;
  fileName: string;
  contentType: string;
}

export interface AppendPagesInput {
  documentId: string;
  fileNames: string[];
}

export interface ReorderPagesInput {
  documentId: string;
  orderedPageIds: string[];
}

export interface MergeDocumentsInput {
  sourceDocumentIds: string[];
  targetDocumentType: string;
}

export interface SplitDocumentInput {
  documentId: string;
  splitAfterPageId: string;
}
