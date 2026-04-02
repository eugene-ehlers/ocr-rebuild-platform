import { Link } from 'react-router-dom';

export function ReadinessCheckPage() {
  return (
    <div className="page">
      <h1>Are you ready?</h1>
      <div className="card">
        <p>Please confirm before continuing.</p>
        <ul>
          <li>My document is ready</li>
          <li>The information is clear</li>
          <li>I understand the requirements</li>
        </ul>
      </div>

      <Link to="/journey/pre-upload" className="btn">Continue</Link>
    </div>
  );
}
