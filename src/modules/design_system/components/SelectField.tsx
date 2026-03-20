import React, { SelectHTMLAttributes } from "react";

interface SelectOption {
  label: string;
  value: string;
}

interface SelectFieldProps extends SelectHTMLAttributes<HTMLSelectElement> {
  label: string;
  options: SelectOption[];
  error?: string;
}

export function SelectField({ label, options, error, ...props }: SelectFieldProps) {
  return (
    <div data-testid="select-field">
      <label>
        <div>{label}</div>
        <select {...props}>
          {options.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </label>
      {error ? <div role="alert">{error}</div> : null}
    </div>
  );
}
