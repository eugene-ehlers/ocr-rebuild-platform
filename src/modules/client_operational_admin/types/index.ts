export interface BalanceRecord {
  customerId: string;
  balance: number;
  currency: string;
  asOf: string;
}

export interface TransactionRecord {
  transactionId: string;
  customerId: string;
  amount: number;
  currency: string;
  type: "credit" | "debit" | "simulated_payment";
  createdAt: string;
  reference: string;
}

export interface UsageRecord {
  usageId: string;
  customerId: string;
  serviceCode: string;
  requestId: string;
  metric: string;
  value: string;
  recordedAt: string;
}

export interface ActivityLogRecord {
  activityId: string;
  customerId: string;
  userId: string;
  action: string;
  module: string;
  timestamp: string;
  auditable: boolean;
}

export interface SupportQueryInput {
  customerId: string;
  subject: string;
  description: string;
}

export interface SimulatedPaymentInput {
  customerId: string;
  amount: number;
  currency: string;
  reference: string;
}
