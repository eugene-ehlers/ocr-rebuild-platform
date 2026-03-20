import React from "react";

interface LoaderProps {
  label?: string;
}

export function Loader({ label = "Loading..." }: LoaderProps) {
  return (
    <div aria-busy="true" data-testid="loader">
      {label}
    </div>
  );
}
