# Graph Report

## Nodes

- auth/routes.ts
- auth/service.ts
- billing/service.ts
- shared/events.ts

## Relationships

- auth/routes.ts -> auth/service.ts
- auth/service.ts -> shared/events.ts
- billing/service.ts -> shared/events.ts
- auth/service.ts -> billing/service.ts (entitlement sync)

## Expanded Notes

The auth route normalizes credentials before invoking the auth service. The auth service creates a session token and emits a shared domain event. Billing consumes identity state indirectly through entitlement synchronization paths and may subscribe to events emitted by auth-related flows. Shared event publication exists as a fan-out point across modules, which makes it structurally important during architecture review but unnecessarily expensive during focused bugfix work. The graph report is intentionally broader than a scenario summary and therefore costs more tokens while offering better repository-wide awareness.

Additional structural relationships can be listed here to simulate the cost of loading a broad graph artifact. In a real repository this file is usually much longer, which is exactly why the skill should not open it first for every task.
