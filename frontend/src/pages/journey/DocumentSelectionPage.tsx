import { Link } from 'react-router-dom';
import { PageScaffold } from '../PageScaffold';

export function DocumentSelectionPage() {
  return (
    <PageScaffold
      title="Select document type"
      summary="Choose the type of document you want to prepare and submit."
    >
      <div className="home-grid home-grid--3">

        <div className="card">
          <h3>Identity document</h3>
          <Link to="/journey/requirements" className="btn">Select</Link>
        </div>

        <div className="card">
          <h3>Proof of address</h3>
          <Link to="/journey/requirements" className="btn">Select</Link>
        </div>

        <div className="card">
          <h3>Financial document</h3>
          <Link to="/journey/requirements" className="btn">Select</Link>
        </div>

      </div>
    </PageScaffold>
  );
}
