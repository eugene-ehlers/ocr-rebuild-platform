import React from "react";

interface FormErrorSummaryProps {
  errors: string[];
}

export function FormErrorSummary({ errors }: FormErrorSummaryProps) {
  if (!errors.length) return null;

  return (
    <div role="alert">
      <h3>Please correct the following:</h3>
      <ul>
        {errors.map((error, index) => (
          <li key={`${error}-${index}`}>{error}</li>
        ))}
      </ul>
    </div>
  );
}
