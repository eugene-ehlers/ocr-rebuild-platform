import { Link } from 'react-router-dom';
import { PageScaffold } from '../PageScaffold';

export function RequirementsDetailPage() {
  return (
    <PageScaffold
      title="Document requirements"
      summary="Ensure your document meets all conditions before continuing."
    >
      <div className="home-grid home-grid--2">

        <div className="card">
          <h3>Required</h3>
          <ul className="home-list">
            <li>Clear and readable</li>
            <li>All information visible</li>
            <li>Correct document type</li>
          </ul>
        </div>

        <div className="card">
          <h3>Not accepted</h3>
          <ul className="home-list">
            <li>Blurry or cropped</li>
            <li>Obstructed text</li>
            <li>Incorrect document</li>
          </ul>
        </div>

      </div>

      <Link to="/journey/readiness" className="btn">
        I understand
      </Link>
    </PageScaffold>
  );
}
