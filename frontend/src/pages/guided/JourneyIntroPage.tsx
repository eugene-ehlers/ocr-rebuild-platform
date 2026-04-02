import { Link } from 'react-router-dom';

export function JourneyIntroPage() {
  return (
    <div className="page">
      <h1>Before we begin</h1>

      <div className="card">
        <p>We will guide you step by step.</p>
        <p>You will need your documents ready.</p>
      </div>

      <Link to="/journey/service-context" className="btn">Start journey</Link>
    </div>
  );
}
