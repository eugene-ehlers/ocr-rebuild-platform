import { useParams } from 'react-router-dom';
import { PageScaffold } from '../PageScaffold';

export function ProcessingPage() {
  const { request_id } = useParams();

  return (
    <PageScaffold
      title="Processing request"
      summary={`Your request ${request_id ?? ''} is currently being processed.`}
    >
      <div className="card">
        <p>We are analysing your document. This may take a few moments.</p>
      </div>
    </PageScaffold>
  );
}
