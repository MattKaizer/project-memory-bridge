---
note_type: domain-summary
token_budget: 300
---

# Auth Domain

## Responsibilities

- normalize login input
- issue session tokens
- emit session-created audit events

## Key invariants

- auth owns identity decisions
- shared only publishes events
- billing must not create auth tokens
