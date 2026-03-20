import React from "react";
import { Alert } from "../../design_system/components";

interface AuthStatusBannerProps {
  isAuthenticated: boolean;
}

export function AuthStatusBanner({ isAuthenticated }: AuthStatusBannerProps) {
  return (
    <Alert variant={isAuthenticated ? "success" : "warning"}>
      {isAuthenticated ? "Authenticated session placeholder." : "Unauthenticated session placeholder."}
    </Alert>
  );
}
