# Project Index

## First read order

1. `.atl/memory-config.json` for layer toggles and paths
2. `.atl/compact-routing.json` for scenario budgets and escalation rules
3. one compact note that matches the task shape

## Domains

- auth — login, session issuance, access guards
- billing — subscription state, invoices, entitlement checks
- shared — logging and event publication

## When to use compact memory first

Start with scenario and domain notes for any task that stays inside one area.

## Escalation

- escalate to raw code when exact contracts or behavior matter
- escalate to full graph when the task spans auth, billing, and shared relationships
