import { Link } from 'react-router-dom';
import { PageScaffold } from '../PageScaffold';

export function ServiceSelectionPage() {
  return (
    <PageScaffold
      title="Select a service"
      summary="Understand what each service does, what is required, and how to proceed."
    >
      <div className="home-grid home-grid--3">

        <div className="card">
          <h3>Document understanding</h3>
          <p>Analyse document structure and extract meaning.</p>
          <p><strong>Requires:</strong> Clean readable files</p>
          <Link to="/guided/start" className="btn">Continue</Link>
        </div>

        <div className="card">
          <h3>Structured submission</h3>
          <p>Prepare and submit documents into a guided workflow.</p>
          <p><strong>Requires:</strong> Full document set</p>
          <Link to="/guided/start" className="btn">Continue</Link>
        </div>

        <div className="card">
          <h3>Business submission</h3>
          <p>Provide organisation details with authority context.</p>
          <p><strong>Requires:</strong> Business + supporting docs</p>
          <Link to="/guided/start" className="btn secondary">Continue</Link>
        </div>

      </div>
    </PageScaffold>
  );
}
