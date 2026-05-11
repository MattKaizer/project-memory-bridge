---
name: project-memory-bridge
description: "Trigger: Graphify, Obsidian, project memory, token optimization, repo onboarding, architecture review, sdd-init. Add a lightweight persistent-memory bridge without replacing Engram."
license: MIT
metadata:
  author: MBMJ
  version: "0.1.0"
---

# Skill: project-memory-bridge

## Activation Contract

Use this skill when the task needs project memory beyond normal Engram flow:

- repository onboarding or architecture review
- SDD init or planning on a medium/large repo
- reducing repeated repo rediscovery
- wiring Graphify and Obsidian as optional memory layers

Do not use it for tiny edits, one-file fixes, formatting, or conceptual questions detached from the repo.

## Hard Rules

- Preserve normal Engram behavior. Never replace, suppress, or redefine it.
- Read `.atl/memory-config.json` first when the skill activates.
- Default to **compact-first context routing**, not Graphify-first.
- Use the context pyramid: config -> Engram pointer -> compact notes -> full graph -> raw code.
- Store only compact Graphify/Obsidian pointers in Engram; large reports stay in files.
- Run Graphify only for onboarding, stale structure, architecture-heavy work, or verified cross-module needs.
- Treat source code as the final authority when exact implementation details matter.

## Context Pyramid

| Level | Source | Use it for | Default token posture |
|---|---|---|---|
| L0 | `.atl/memory-config.json` | routing, paths, scenario defaults, budgets | tiny |
| L1 | Engram compact pointer | decide which compact artifact to open | tiny |
| L2 | compact scenario/domain notes | focused tasks, localized debugging, targeted edits | cheap |
| L3 | `graphify-out/GRAPH_REPORT.md` | onboarding, architecture review, cross-module relationships | expensive |
| L4 | raw code/docs | exact implementation details, verification | variable |

Never jump to L3 if L2 can answer the task.

## Scenario Router

| Task shape | Preferred route | Graph report allowed? |
|---|---|---|
| Focused bugfix / feature in one domain | L0 -> L1 -> L2 -> L4 | No by default |
| Planning inside one bounded area | L0 -> L1 -> L2 -> L4 | Only if compact context is stale or insufficient |
| Cross-module change | L0 -> L1 -> L2 -> L3 -> L4 | Yes |
| Repo onboarding | L0 -> L1 -> L2 -> L3 | Yes |
| Architecture review | L0 -> L1 -> L2 -> L3 -> L4 | Yes |

## Compact Pointer Contract

When Engram points to durable context, keep it compact and scenario-aware.

```text
scenario: focused-task | cross-module | onboarding | architecture-review
domains: [auth, billing, ui-shell]
recommended_notes:
  - notes/10_Scenarios/<scenario>.md
  - notes/20_Domains/<domain>.md
cross_module_note: notes/30_Cross_Module/<relationship>.md
graph_report: graphify-out/GRAPH_REPORT.md
graph_report_required: true|false
```

The pointer should help the agent open **1-3 cheap artifacts first**.
It should not inline long note bodies or the full graph report.

## Decision Gates

| Situation | Action |
|---|---|
| `.atl/memory-config.json` missing during init/onboarding/review | Bootstrap memory config and note structure |
| Compact notes missing, stale, or placeholder-only | Hydrate compact scenario/domain notes before using Graphify as default |
| Normal focused implementation task with ready memory | Consume compact memory first, avoid Graphify unless proven necessary |
| Cross-module / architecture-heavy task | Reuse compact context first, then allow full Graphify |
| Durable architecture/process knowledge changed | Update only affected compact notes and pointers |

## Execution Steps

1. Read `.atl/memory-config.json`.
2. Determine mode: `bootstrap`, `hydrate`, `consume`, or `update`.
3. Resolve the task scenario from config or task shape.
4. Open the cheapest viable artifacts first: config -> Engram pointer -> compact scenario/domain notes.
5. Escalate to `graphify-out/GRAPH_REPORT.md` only if the scenario explicitly allows it or compact context proves insufficient.
6. Open raw code only for verification or exact implementation details.
7. If durable knowledge changed, update only the relevant compact notes and add a compact Engram pointer.
8. Return: active mode, scenario, current state, what was created/updated, what was skipped, and why.

## Output Contract

Return:

- chosen mode and why
- chosen scenario and why
- readiness status: `complete`, `partial`, or `failed`
- compact-context status: reused, refreshed, missing, or skipped
- files or notes created/updated
- Graphify status: refreshed, reused, skipped, or unavailable
- Engram pointer status
- unresolved risks or follow-up actions

## References

- `README.md` — repo overview, installation, and usage
- `assets/memory-config.schema.json` — canonical lightweight config schema
- `references/operating-model.md` — bootstrap/hydrate/consume/update behavior
- `references/obsidian-templates.md` — recommended note layout and starter templates
