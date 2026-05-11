export type BillingSnapshot = {
  userId: string;
  plan: string;
  active: boolean;
};

export function buildBillingSnapshot(userId: string, plan: string): BillingSnapshot {
  return {
    userId,
    plan,
    active: plan !== "free",
  };
}
