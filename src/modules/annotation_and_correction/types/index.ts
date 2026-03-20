export type ReviewerStatus = "pending" | "in_review" | "accepted" | "rejected";

export interface AnnotationRecord {
  annotationId: string;
  documentId: string;
  fieldReference: string;
  originalValue: string;
  systemInterpretation: string;
  userSuggestion: string;
  reviewerStatus: ReviewerStatus;
  finalValue?: string;
  createdAt: string;
}

export interface CreateAnnotationInput {
  documentId: string;
  fieldReference: string;
  originalValue: string;
  systemInterpretation: string;
  userSuggestion: string;
}

export interface UpdateAnnotationInput {
  annotationId: string;
  userSuggestion: string;
}

export interface TriggerReprocessingInput {
  annotationId: string;
  requestId?: string;
}
