import { buildBillingSnapshot } from "./service";
import { publishDomainEvent } from "../shared/events";

export function syncSubscription(userId: string, plan: string) {
  const snapshot = buildBillingSnapshot(userId, plan);

  return publishDomainEvent({
    type: "billing.subscription.synced",
    userId,
    payload: {
      plan: snapshot.plan,
      active: snapshot.active,
    },
  });
}
