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
  trustText = 'We guide you through each step clearly before any processing begins.',
  actionLabel = 'Continue to the next step.',
}: PageScaffoldProps) {
  return (
    <section className="page-surface">
      <div className="page-stack">

        <header className="page-hero">
          <h1>{title}</h1>
          <p className="page-summary">{summary}</p>
        </header>

        <section className="page-trust">
          <strong>What to expect</strong>
          <p>{trustText}</p>
        </section>

        {children ? <div className="page-content">{children}</div> : null}

        <section className="page-action">
          <div className="page-action__panel">
            <strong>Next step</strong>
            <p>{actionLabel}</p>
          </div>
        </section>

      </div>
    </section>
  );
}
