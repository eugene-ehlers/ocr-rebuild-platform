import { Link } from 'react-router-dom';
import { PageScaffold } from '../PageScaffold';

export function JourneyIntroPage() {
  return (
    <PageScaffold
      title="Before you begin"
      summary="We guide you step-by-step to ensure your submission is complete and valid."
    >
      <div className="card">
        <ul className="home-list">
          <li>Ensure documents are clear and readable</li>
          <li>Have all required information ready</li>
          <li>Follow each step carefully before submission</li>
        </ul>
      </div>

      <Link to="/journey/service-context" className="btn">
        Start journey
      </Link>
    </PageScaffold>
  );
}
