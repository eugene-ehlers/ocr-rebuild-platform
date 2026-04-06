import { useParams } from 'react-router-dom';
import { PageScaffold } from '../PageScaffold';

export function BlockedPage() {
  const { request_id } = useParams();

  return (
    <PageScaffold
      title="Request blocked"
      summary={`Request ${request_id ?? ''} requires attention.`}
    >
      <div className="card">
        <p>Your document could not be processed.</p>
      </div>

      <div className="card">
        <h3>What to do next</h3>
        <p>Review requirements and resubmit.</p>
      </div>
    </PageScaffold>
  );
}
