import { Link } from 'react-router-dom';
import { PageScaffold } from '../PageScaffold';

export function EntrySelectionPage() {
  return (
    <PageScaffold
      title="Start your request"
      summary="Choose how you want to begin and what type of request you want to prepare."
    >
      <div className="home-grid home-grid--3">

        <div className="card">
          <h3>Understand a document</h3>
          <p>Explore document structure and expected outcomes before submitting files.</p>
          <Link to="/entry/service" className="btn">Select</Link>
        </div>

        <div className="card">
          <h3>Submit documents</h3>
          <p>Proceed directly to structured submission with guided preparation steps.</p>
          <Link to="/entry/service" className="btn">Select</Link>
        </div>

        <div className="card">
          <h3>Business / organisation</h3>
          <p>Prepare organisation-level details and authorised submission context.</p>
          <Link to="/entry/service" className="btn secondary">Select</Link>
        </div>

      </div>
    </PageScaffold>
  );
}
