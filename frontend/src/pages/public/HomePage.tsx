import { Link } from 'react-router-dom';

export function HomePage() {
  return (
    <div className="home-page">

      <section className="home-hero">
        <div className="home-hero__content">
          <p className="home-kicker section-label">Secure document intelligence</p>
          <h1>
            Client-ready OCR workflows with clear guidance, trusted handling, and premium usability.
          </h1>
          <p className="home-hero__summary">
            Submit document requests confidently, understand what is required before upload, and follow each stage
            from preparation through result with a guided, client-facing experience.
          </p>

          <div className="home-hero__actions">
            <Link to="/entry" className="btn-primary">Start request</Link>
            <Link to="/how-it-works" className="btn-secondary">How it works</Link>
          </div>
        </div>

        <aside className="home-hero__panel">
          <h3>Sampling capability</h3>
          <ul className="home-list">
            <li>Structured intake for individual and business journeys</li>
            <li>Document readiness checks before upload</li>
            <li>Clear review, status, and result visibility</li>
            <li>Support, trust, and governance surfaces already visible</li>
          </ul>
        </aside>
      </section>

      <section className="home-section">
        <div className="home-section__header">
          <p className="home-kicker section-label">Choose your role</p>
          <h2>Start your journey</h2>
        </div>

        <div className="home-grid home-grid--3">
          <article className="card card--primary">
            <span className="card-badge">Recommended</span>
            <div className="icon">👤</div>
            <h3>Individual applicant</h3>
            <p>Provide personal details and proceed through a guided request flow.</p>
            <Link to="/entry" className="btn-primary">Continue</Link>
          </article>

          <article className="card">
            <div className="icon">🏢</div>
            <h3>Business representative</h3>
            <p>Prepare organisation details and supporting files.</p>
            <Link to="/entry" className="btn-primary">Continue</Link>
          </article>

          <article className="card">
            <div className="icon">📊</div>
            <h3>Operations</h3>
            <p>Access reporting and support surfaces.</p>
            <Link to="/reports" className="btn-admin">Open</Link>
          </article>
        </div>
      </section>

      <section className="home-section home-section--process">
        <div className="home-section__header">
          <p className="home-kicker section-label">Process</p>
          <h2>How it works</h2>
        </div>

        <div className="home-grid home-grid--4">
          <article className="card card--primary">
            <h4>1. Choose path</h4>
            <p>Select the right journey.</p>
          </article>

          <article className="card step--complete">
            <h4>2. Prepare</h4>
            <p>Complete required details.</p>
          </article>

          <article className="card step--complete">
            <h4>3. Review</h4>
            <p>Confirm before submission.</p>
          </article>

          <article className="card">
            <h4>4. Track</h4>
            <p>Follow progress and results.</p>
          </article>
        </div>
      </section>

      <section className="trust-band-strong">
        <div className="trust-grid">
          <div className="trust-item-strong">
            <span className="icon icon--green">🛡</span>
            <span>Secure handling</span>
          </div>
          <div className="trust-item-strong">
            <span className="icon icon--green">✔</span>
            <span>Verified workflows</span>
          </div>
          <div className="trust-item-strong">
            <span className="icon icon--green">⚖</span>
            <span>Audit-ready outputs</span>
          </div>
          <div className="trust-item-strong">
            <span className="icon icon--green">💬</span>
            <span>Support available</span>
          </div>
        </div>
      </section>

    </div>
  );
}
