import { useParams } from 'react-router-dom';
import { PageScaffold } from '../PageScaffold';

export function ResultPage() {
  const { request_id } = useParams();

  return (
    <PageScaffold
      title="Result"
      summary={`Placeholder result route for request: ${request_id ?? 'unknown'}. No result rendering logic is implemented.`}
    />
  );
}
