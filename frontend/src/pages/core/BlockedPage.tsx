import { useParams } from 'react-router-dom';
import { PageScaffold } from '../PageScaffold';

export function BlockedPage() {
  const { request_id } = useParams();

  return (
    <PageScaffold
      title="Blocked"
      summary={`Placeholder blocked route for request: ${request_id ?? 'unknown'}. No exception or review handling is implemented.`}
    />
  );
}
