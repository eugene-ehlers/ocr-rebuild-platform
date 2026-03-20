import React from "react";
import { RequestStatus } from "../types";

interface StatusTimelineProps {
  statuses: RequestStatus[];
}

export function StatusTimeline({ statuses }: StatusTimelineProps) {
  return (
    <ol>
      {statuses.map((status, index) => (
        <li key={`${status}-${index}`}>{status}</li>
      ))}
    </ol>
  );
}
