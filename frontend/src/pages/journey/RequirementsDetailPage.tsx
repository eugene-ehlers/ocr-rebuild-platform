import { Link } from 'react-router-dom';

export function RequirementsDetailPage() {
  return (
    <div className="page">
      <h1>What you will need</h1>
      <div className="card">
        <p>We explain what is required before you proceed.</p>
        <ul>
          <li>Clear, readable document</li>
          <li>All information visible</li>
          <li>Correct document type</li>
        </ul>
      </div>

      <Link to="/journey/readiness" className="btn">I understand</Link>
    </div>
  );
}
