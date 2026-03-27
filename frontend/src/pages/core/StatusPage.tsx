import { useParams } from 'react-router-dom';
import { PageScaffold } from '../PageScaffold';

export function StatusPage() {
  const { request_id } = useParams();

  return (
    <PageScaffold
      title="Status"
      summary={`Placeholder status route for request: ${request_id ?? 'unknown'}. No status retrieval logic is implemented.`}
    />
  );
}
