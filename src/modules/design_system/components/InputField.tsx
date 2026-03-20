import React, { InputHTMLAttributes } from "react";

interface InputFieldProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
}

export function InputField({ label, error, ...props }: InputFieldProps) {
  return (
    <div data-testid="input-field">
      <label>
        <div>{label}</div>
        <input {...props} />
      </label>
      {error ? <div role="alert">{error}</div> : null}
    </div>
  );
}
