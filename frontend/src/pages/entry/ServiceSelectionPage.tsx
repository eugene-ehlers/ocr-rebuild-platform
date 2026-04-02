import { Link } from 'react-router-dom';

export function ServiceSelectionPage() {
  return (
    <div className="page">
      <h1>Select a service</h1>

      <div className="card">
        <p>Choose what you want to do.</p>
      </div>

      <Link to="/guided/start" className="btn">Continue</Link>
    </div>
  );
}
