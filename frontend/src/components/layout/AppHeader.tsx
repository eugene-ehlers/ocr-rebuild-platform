import { Link } from 'react-router-dom';

export function AppHeader() {
  return (
    <header className="app-header">
      <div className="page-container app-header__inner">
        <Link to="/" className="app-brand">
          OCR Intelligence Platform
        </Link>
        <nav className="app-nav" aria-label="Primary">
  <div className="app-nav__primary">
    <Link to="/submit">Submit</Link>
    <Link to="/status/sample-request">Status</Link>
    <Link to="/reports">Reports</Link>
  </div>
  <div className="app-nav__secondary">
    <Link to="/support">Support</Link>
    <Link to="/login">Login</Link>
  </div>
</nav>
      </div>
    </header>
  );
}
