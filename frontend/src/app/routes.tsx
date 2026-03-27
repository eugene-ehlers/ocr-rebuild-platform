import { Routes, Route } from 'react-router-dom';
import { HomePage } from '../pages/public/HomePage';
import { RegisterPage } from '../pages/public/RegisterPage';
import { LoginPage } from '../pages/public/LoginPage';
import { SubmitPage } from '../pages/core/SubmitPage';
import { ProcessingPage } from '../pages/core/ProcessingPage';
import { ResultPage } from '../pages/core/ResultPage';
import { BlockedPage } from '../pages/core/BlockedPage';
import { StatusPage } from '../pages/core/StatusPage';
import { AccountPage } from '../pages/platform/AccountPage';
import { BillingPage } from '../pages/platform/BillingPage';
import { SupportPage } from '../pages/platform/SupportPage';
import { ReportsPage } from '../pages/platform/ReportsPage';
import { TermsPage } from '../pages/legal/TermsPage';
import { PrivacyPage } from '../pages/legal/PrivacyPage';
import { CookiesPage } from '../pages/legal/CookiesPage';
import { AcceptableUsePage } from '../pages/legal/AcceptableUsePage';
import { ConsentFrameworkPage } from '../pages/legal/ConsentFrameworkPage';

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/login" element={<LoginPage />} />

      <Route path="/submit" element={<SubmitPage />} />
      <Route path="/processing/:request_id" element={<ProcessingPage />} />
      <Route path="/result/:request_id" element={<ResultPage />} />
      <Route path="/blocked/:request_id" element={<BlockedPage />} />
      <Route path="/status/:request_id" element={<StatusPage />} />

      <Route path="/account" element={<AccountPage />} />
      <Route path="/billing" element={<BillingPage />} />
      <Route path="/support" element={<SupportPage />} />
      <Route path="/reports" element={<ReportsPage />} />

      <Route path="/legal/terms" element={<TermsPage />} />
      <Route path="/legal/privacy" element={<PrivacyPage />} />
      <Route path="/legal/cookies" element={<CookiesPage />} />
      <Route path="/legal/acceptable-use" element={<AcceptableUsePage />} />
      <Route path="/legal/consent-framework" element={<ConsentFrameworkPage />} />
    </Routes>
  );
}
