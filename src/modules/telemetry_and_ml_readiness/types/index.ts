export type TelemetryEventType =
  | "page_visit"
  | "time_on_page"
  | "drop_off"
  | "interaction"
  | "error"
  | "retry"
  | "document_upload"
  | "document_reupload"
  | "document_quality_issue"
  | "service_usage"
  | "service_failure"
  | "support_query"
  | "remediation_interaction"
  | "workflow_tracking";

export interface TelemetryEventRecord {
  event_type: TelemetryEventType | string;
  timestamp: string;
  user_id?: string;
  session_id?: string;
  module: string;
  action: string;
  metadata: Record<string, unknown>;
}

export interface WorkflowTrackingEvent {
  workflowId: string;
  requestId?: string;
  module: string;
  step: string;
  status: string;
  timestamp: string;
  metadata: Record<string, unknown>;
}
