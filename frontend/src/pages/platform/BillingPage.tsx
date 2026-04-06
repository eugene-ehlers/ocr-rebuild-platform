import { PageScaffold } from '../PageScaffold';

export function BillingPage() {
  return (
    <PageScaffold
      title="Billing"
      summary="Manage billing and usage."
    >
      <div className="card">
        <p>Invoices and payment methods.</p>
      </div>
    </PageScaffold>
  );
}
