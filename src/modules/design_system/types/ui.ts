export type UiState = "idle" | "loading" | "success" | "error";

export interface ValidationMessage {
  field?: string;
  message: string;
}

export interface BaseComponentProps {
  testId?: string;
  className?: string;
}
