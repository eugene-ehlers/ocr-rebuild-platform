export type PlaceholderStatus = "placeholder" | "ready" | "blocked";

export interface PlaceholderResponse<T = Record<string, unknown>> {
  success: boolean;
  status: PlaceholderStatus;
  message: string;
  data: T;
}
