import React, { ReactNode } from "react";

interface ModalProps {
  title: string;
  isOpen: boolean;
  children: ReactNode;
}

export function Modal({ title, isOpen, children }: ModalProps) {
  if (!isOpen) return null;

  return (
    <div role="dialog" aria-modal="true">
      <div>
        <h2>{title}</h2>
        <div>{children}</div>
      </div>
    </div>
  );
}
