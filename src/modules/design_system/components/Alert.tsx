import React, { ReactNode } from "react";

type AlertVariant = "info" | "success" | "warning" | "error";

interface AlertProps {
  variant?: AlertVariant;
  children: ReactNode;
}

export function Alert({ variant = "info", children }: AlertProps) {
  return (
    <div role="alert" data-variant={variant}>
      {children}
    </div>
  );
}
