import React from "react";
import { Alert } from "../../design_system/components";
import { ConsentStatus } from "../types";

interface ConsentStatusBadgeProps {
  status: ConsentStatus;
}

export function ConsentStatusBadge({ status }: ConsentStatusBadgeProps) {
  const variant =
    status === "granted"
      ? "success"
      : status === "pending"
      ? "info"
      : status === "expired"
      ? "warning"
      : "error";

  return <Alert variant={variant}>Consent status: {status}</Alert>;
}
