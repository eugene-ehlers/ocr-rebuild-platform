import type { ReactNode } from 'react';

interface PageScaffoldProps {
  title: string;
  summary: string;
  children?: ReactNode;
  trustText?: string;
  actionLabel?: string;
}

export function PageScaffold({
  title,
  summary,
  children,
  trustText = 'We explain what this step is for before any connected workflow is introduced.',
  actionLabel = 'Next step available in a later phase.',
}: PageScaffoldProps) {
  return (
    <section className="page-surface">
      <div className="page-stack">
        <header className="page-hero">
          <p className="page-eyebrow">Frontend Shell Baseline</p>
          <h1>{title}</h1>
          <p className="page-summary">{summary}</p>
        </header>

        <section className="page-trust" aria-label="Guidance and trust information">
          <p className="page-trust__label">What to expect</p>
          <p className="page-trust__text">{trustText}</p>
        </section>

        {children ? <div className="page-content">{children}</div> : null}

        <section className="page-action" aria-label="Action area">
          <div className="page-action__panel">
            <p className="page-action__label">Action</p>
            <p className="page-action__text">{actionLabel}</p>
          </div>
        </section>
      </div>
    </section>
  );
}
