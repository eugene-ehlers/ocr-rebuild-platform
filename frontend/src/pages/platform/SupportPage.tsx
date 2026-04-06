import { PageScaffold } from '../PageScaffold';

export function SupportPage() {
  return (
    <PageScaffold
      title="Support"
      summary="Get help and guidance for your request."
    >
      <div className="card">
        <h3>Common questions</h3>
        <p>Find answers to typical issues.</p>
      </div>

      <div className="card">
        <h3>Contact support</h3>
        <p>Submit a support request.</p>
      </div>
    </PageScaffold>
  );
}
