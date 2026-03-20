import React, { ButtonHTMLAttributes } from "react";

type ButtonVariant = "primary" | "secondary" | "danger";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  label: string;
  variant?: ButtonVariant;
}

export function Button({ label, variant = "primary", ...props }: ButtonProps) {
  return (
    <button data-variant={variant} {...props}>
      {label}
    </button>
  );
}
