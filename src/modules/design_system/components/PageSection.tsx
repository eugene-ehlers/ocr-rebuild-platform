import React, { ReactNode } from "react";

interface PageSectionProps {
  title: string;
  children: ReactNode;
}

export function PageSection({ title, children }: PageSectionProps) {
  return (
    <section>
      <h2>{title}</h2>
      <div>{children}</div>
    </section>
  );
}
