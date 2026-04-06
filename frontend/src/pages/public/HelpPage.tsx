import { PageScaffold } from '../PageScaffold';

export function HelpPage() {
  return (
    <PageScaffold
      title="Help and support"
      summary="Guidance for using the platform and completing requests."
    >
      <div className="card">
        <h3>Getting started</h3>
        <p>Follow guided steps from entry to submission.</p>
      </div>

      <div className="card">
        <h3>Need assistance?</h3>
        <p>Contact support for help.</p>
      </div>
    </PageScaffold>
  );
}
