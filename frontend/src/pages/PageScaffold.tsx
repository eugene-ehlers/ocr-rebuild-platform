import { ReactNode } from 'react';

type PageScaffoldProps = {
  title: string;
  summary: string;
  children?: ReactNode;
};

export function PageScaffold({ title, summary, children }: PageScaffoldProps) {
  return (
    <section className="page-surface">
      <div className="page-stack">
        <header className="page-hero">
          <p className="page-eyebrow">Frontend Shell Baseline</p>
          <h1>{title}</h1>
          <p className="page-summary">{summary}</p>
        </header>
        {children ? <div className="page-content">{children}</div> : null}
      </div>
    </section>
  );
}
