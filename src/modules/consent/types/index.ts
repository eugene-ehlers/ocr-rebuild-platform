export type ConsentType = "processing" | "disclosure";
export type ConsentStatus = "granted" | "revoked" | "expired" | "pending";

export interface ConsentRecord {
  consentId: string;
  customerId: string;
  consentType: ConsentType;
  grantedBy: string;
  timestamp: string;
  expiryDate?: string;
  status: ConsentStatus;
  standingConsent: boolean;
}

export interface CaptureConsentInput {
  customerId: string;
  consentType: ConsentType;
  grantedBy: string;
  standingConsent: boolean;
  expiryDate?: string;
}

export interface ValidateConsentInput {
  customerId: string;
  consentType: ConsentType;
  action: string;
}

export interface RevokeConsentInput {
  consentId: string;
  revokedBy: string;
  reason?: string;
}
