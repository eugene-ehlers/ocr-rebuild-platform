import { PageScaffold } from '../PageScaffold';

export function ReportsPage() {
  return (
    <PageScaffold
      title="Reports"
      summary="View usage and processing metrics."
    >
      <div className="card">
        <h3>KPI overview</h3>
        <p>Requests, success rate, processing times.</p>
      </div>

      <div className="card">
        <h3>Recent requests</h3>
        <p>Table placeholder.</p>
      </div>
    </PageScaffold>
  );
}
