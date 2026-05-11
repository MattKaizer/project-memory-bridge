import { buildBillingSnapshot } from "./service";

export function getBillingSummary(userId: string, plan: string) {
  const snapshot = buildBillingSnapshot(userId, plan);

  return {
    userId: snapshot.userId,
    plan: snapshot.plan,
    active: snapshot.active,
    source: "billing.controller",
  };
}
