import { useParams } from 'react-router-dom';
import { PageScaffold } from '../PageScaffold';

export function ProcessingPage() {
  const { request_id } = useParams();

  return (
    <PageScaffold
      title="Processing"
      summary={`Placeholder processing route for request: ${request_id ?? 'unknown'}. No polling or workflow calls are implemented.`}
    />
  );
}
