import termsOfService from './terms_of_service.md?raw';
import privacyPolicy from './privacy_policy.md?raw';
import cookiePolicy from './cookie_policy.md?raw';
import acceptableUsePolicy from './acceptable_use_policy.md?raw';
import consentFrameworkStatement from './consent_framework_statement.md?raw';
import disclaimerLimitation from './disclaimer_limitation.md?raw';
import supportDisputeResolution from './support_dispute_resolution.md?raw';

export type LegalDocumentKey =
  | 'terms'
  | 'privacy'
  | 'cookies'
  | 'acceptable-use'
  | 'consent-framework'
  | 'disclaimer-limitation'
  | 'support-dispute-resolution';

type LegalDocumentDefinition = {
  title: string;
  content: string;
};

export const legalDocuments: Record<LegalDocumentKey, LegalDocumentDefinition> = {
  terms: {
    title: 'Terms of Service',
    content: termsOfService
  },
  privacy: {
    title: 'Privacy Policy',
    content: privacyPolicy
  },
  cookies: {
    title: 'Cookie Policy',
    content: cookiePolicy
  },
  'acceptable-use': {
    title: 'Acceptable Use Policy',
    content: acceptableUsePolicy
  },
  'consent-framework': {
    title: 'Consent Framework Statement',
    content: consentFrameworkStatement
  },
  'disclaimer-limitation': {
    title: 'Disclaimer & Limitation of Liability',
    content: disclaimerLimitation
  },
  'support-dispute-resolution': {
    title: 'Support & Dispute Resolution',
    content: supportDisputeResolution
  }
};
