import { Link } from 'react-router-dom';

export function AppHeader() {
  return (
    <header className="app-header">
      <div className="page-container app-header__inner">
        <Link to="/" className="app-brand">
          OCR Platform
        </Link>
        <nav className="app-nav" aria-label="Primary">
          <Link to="/submit">Submit</Link>
          <Link to="/status/sample-request">Status</Link>
          <Link to="/reports">Reports</Link>
          <Link to="/support">Support</Link>
          <Link to="/login">Login</Link>
        </nav>
      </div>
    </header>
  );
}
