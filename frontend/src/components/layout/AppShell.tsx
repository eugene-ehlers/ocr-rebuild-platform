import { ReactNode } from 'react';
import { AppHeader } from './AppHeader';
import { AppFooter } from './AppFooter';

type AppShellProps = {
  children: ReactNode;
};

export function AppShell({ children }: AppShellProps) {
  return (
    <div className="app-shell">
      <AppHeader />

      <main className="app-main">
        <div className="page-container">{children}</div>
      </main>


      <AppFooter />
    </div>
  );
}
