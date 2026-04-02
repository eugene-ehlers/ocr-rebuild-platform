import { Link } from 'react-router-dom';

export function DocumentSelectionPage() {
  return (
    <div className="page">
      <h1>Select your document</h1>
      <div className="card">
        <p>Choose the type of document you want to work with.</p>
      </div>

      <Link to="/journey/requirements" className="btn">Identity document</Link>
      <Link to="/journey/requirements" className="btn">Proof of address</Link>
      <Link to="/journey/requirements" className="btn">Financial document</Link>
    </div>
  );
}
