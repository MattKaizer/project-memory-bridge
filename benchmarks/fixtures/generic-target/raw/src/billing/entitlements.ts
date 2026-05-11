export function resolveEntitlements(plan: string) {
  if (plan === "enterprise") {
    return ["analytics", "priority-support", "audit-export"];
  }

  if (plan === "pro") {
    return ["analytics", "priority-support"];
  }

  return ["basic-access"];
}
