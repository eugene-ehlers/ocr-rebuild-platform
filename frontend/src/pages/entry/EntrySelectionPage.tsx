import { Link } from 'react-router-dom';

export function EntrySelectionPage() {
  return (
    <div className="page">
      <h1>What would you like to do?</h1>

      <div className="section">
        <p>Select how you want to start.</p>
      </div>

      <Link to="/entry/service" className="btn">Understand a document</Link>
      <Link to="/entry/service" className="btn">Submit documents</Link>
      <Link to="/entry/service" className="btn">Business / organisation</Link>
      <Link to="/entry/service" className="btn secondary">Test / explore</Link>
    </div>
  );
}
