import { Link } from 'react-router-dom';

export function ServiceContextPage() {
  return (
    <div className="page">
      <h1>What are you trying to do?</h1>
      <div className="card">
        <p>Select the option that best describes your goal.</p>
      </div>

      <Link to="/journey/document-selection" className="btn">Understand a document</Link>
      <Link to="/journey/document-selection" className="btn">Submit documents</Link>
      <Link to="/journey/document-selection" className="btn secondary">Business / organisation</Link>
    </div>
  );
}
