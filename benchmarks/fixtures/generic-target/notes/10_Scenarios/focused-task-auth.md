---
note_type: scenario-summary
token_budget: 300
---

# Focused Task: Auth

## When to open this

Use this for login bugs, token validation, or auth-only feature work.

## Key files

- raw/src/auth/routes.ts — entrypoint and payload normalization
- raw/src/auth/service.ts — session creation flow
- raw/src/shared/events.ts — audit event emission

## Escalate to graph report when

- billing entitlements or cross-domain relationships matter
