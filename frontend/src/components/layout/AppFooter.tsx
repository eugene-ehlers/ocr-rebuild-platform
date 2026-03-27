import { Link } from 'react-router-dom';

export function AppFooter() {
  return (
    <footer className="app-footer">
      <div className="page-container app-footer__inner">
        <div className="app-footer__meta">
          <p>Governed OCR frontend shell baseline.</p>
        </div>
        <nav className="app-footer__nav" aria-label="Legal and support">
          <Link to="/legal/terms">Terms</Link>
          <Link to="/legal/privacy">Privacy</Link>
          <Link to="/legal/cookies">Cookies</Link>
          <Link to="/legal/acceptable-use">Acceptable Use</Link>
          <Link to="/legal/consent-framework">Consent Framework</Link>
          <Link to="/support">Support</Link>
        </nav>
      </div>
    </footer>
  );
}
