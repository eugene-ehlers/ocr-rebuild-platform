import { Link } from 'react-router-dom';
import { PageScaffold } from '../PageScaffold';

export function ReadinessCheckPage() {
  return (
    <PageScaffold
      title="Confirm readiness"
      summary="Please confirm all conditions are met before upload."
    >
      <div className="card">
        <ul className="home-list">
          <li>My document is ready</li>
          <li>Information is clear</li>
          <li>I understand the requirements</li>
        </ul>
      </div>

      <Link to="/journey/pre-upload" className="btn">
        Continue
      </Link>
    </PageScaffold>
  );
}
