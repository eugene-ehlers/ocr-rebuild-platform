import { PageScaffold } from '../PageScaffold';

export function AccountPage() {
  return (
    <PageScaffold
      title="Account"
      summary="Manage your account settings."
    >
      <div className="card">
        <p>User details and preferences.</p>
      </div>
    </PageScaffold>
  );
}
