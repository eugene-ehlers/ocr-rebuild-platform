import { Link } from 'react-router-dom';
import { PageScaffold } from '../PageScaffold';

export function ServiceContextPage() {
  return (
    <PageScaffold
      title="What are you trying to do?"
      summary="Select the option that best matches your objective so we can guide your flow correctly."
    >
      <div className="home-grid home-grid--3">

        <div className="card">
          <h3>Understand a document</h3>
          <Link to="/journey/document-selection" className="btn">Select</Link>
        </div>

        <div className="card">
          <h3>Submit documents</h3>
          <Link to="/journey/document-selection" className="btn">Select</Link>
        </div>

        <div className="card">
          <h3>Business / organisation</h3>
          <Link to="/journey/document-selection" className="btn secondary">Select</Link>
        </div>

      </div>
    </PageScaffold>
  );
}
