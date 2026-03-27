import { ReactNode } from 'react';

type LegalDocumentLayoutProps = {
  title: string;
  children: ReactNode;
};

export function LegalDocumentLayout({ title, children }: LegalDocumentLayoutProps) {
  return (
    <section className="page-surface legal-document">
      <div className="page-stack legal-document__stack">
        <header className="page-hero legal-document__hero">
          <p className="page-eyebrow">Governed Legal Content</p>
          <h1>{title}</h1>
          <p className="page-summary">
            Rendered from governed markdown content. Presentation is handled in the frontend shell.
          </p>
        </header>
        <div className="legal-document__content">{children}</div>
      </div>
    </section>
  );
}
