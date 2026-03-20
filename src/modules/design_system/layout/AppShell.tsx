import React, { ReactNode } from "react";

interface AppShellProps {
  title: string;
  navigation?: ReactNode;
  actions?: ReactNode;
  children: ReactNode;
}

export function AppShell({ title, navigation, actions, children }: AppShellProps) {
  return (
    <div data-testid="app-shell">
      <header>
        <div>
          <h1>{title}</h1>
          <div>{actions}</div>
        </div>
        <nav>{navigation}</nav>
      </header>

      <main>{children}</main>

      <footer>
        <small>OCR Rebuild Control Plane</small>
      </footer>
    </div>
  );
}
