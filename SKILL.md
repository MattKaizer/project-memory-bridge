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
- Use `.atl/compact-routing.json` as the truth source for scenario budgets and escalation order.
- Default to **compact-first context routing**, not Graphify-first.
- Use the context pyramid: manifest -> Engram pointer -> project router -> compact notes -> full graph -> raw code.
- Store only compact Graphify/Obsidian pointers in Engram; large reports stay in files.
- Run Graphify only for onboarding, stale structure, architecture-heavy work, or verified cross-module needs.
- Treat source code as the final authority when exact implementation details matter.

## Context Pyramid

| Level | Source | Use it for | Default token posture |
|---|---|---|---|
| L0 | `.atl/memory-config.json` | project identity, enabled layers, pointer paths | tiny |
| L1 | Engram compact pointer | decide which compact artifact to open | tiny |
| L2 | `notes/00_Project_Index.md` + compact scenario/domain notes | cheap navigation before deeper reads | cheap |
| L3 | `graphify-out/GRAPH_REPORT.md` | onboarding, architecture review, cross-module relationships | expensive |
| L4 | raw code/docs | exact implementation details, verification | variable |

Never jump to L3 if L2 can answer the task. Stop after the smallest first-read pack that explains where to go next.

## Scenario Router

| Task shape | First-read pack | Escalation default |
|---|---|---|
| Focused bugfix / feature in one domain | L0 -> L1 -> scenario/domain note | raw code |
| Planning inside one bounded area | L0 -> L1 -> project index -> domain note | raw code |
| Cross-module change | L0 -> L1 -> project index -> cross-module note | graph, then raw code |
| Repo onboarding | L0 -> L1 -> project index -> 1-2 domain notes | graph if breadth remains unclear |
| Architecture review | L0 -> L1 -> project index -> domain notes | graph, then raw code if claims need proof |

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
remaining_budget_hint: <integer>
```

The pointer should help the agent open **1-3 cheap artifacts first**.
It should not inline long note bodies or the full graph report.

## Escalation Rubric

### Compact OK

Stay in compact memory when ALL are true:

- the task remains inside one domain or one already-mapped relationship
- the compact note answers the navigation question
- exact code-level verification is not yet needed

### Escalate to raw code

Open raw code when ANY are true:

- exact implementation details, signatures, or contracts matter
- you are verifying a fix or planning an edit
- compact memory conflicts with current repository state

### Escalate to full graph

Open the full graph when ANY are true:

- the task spans multiple modules and path reasoning matters
- onboarding or architecture breadth is the goal
- compact notes are stale, missing, or insufficient after the first-read pack

## Decision Gates

| Situation | Action |
|---|---|
| `.atl/memory-config.json` or `.atl/compact-routing.json` missing during init/onboarding/review | Bootstrap memory config and note structure |
| Compact notes missing, stale, or placeholder-only | Hydrate compact scenario/domain notes before using Graphify as default |
| Normal focused implementation task with ready memory | Consume compact memory first, avoid Graphify unless proven necessary |
| Cross-module / architecture-heavy task | Reuse compact context first, then allow full Graphify |
| Durable architecture/process knowledge changed | Update only affected compact notes and pointers |

## Execution Steps

1. Read `.atl/memory-config.json`.
2. Read `.atl/compact-routing.json`.
3. Determine mode: `bootstrap`, `hydrate`, `consume`, or `update`.
4. Resolve the task scenario from routing config or task shape.
5. Open only the smallest first-read pack declared for that scenario.
6. Escalate to `graphify-out/GRAPH_REPORT.md` only if the scenario allows it and the escalation rubric is triggered.
7. Open raw code only for verification or exact implementation details.
8. If durable knowledge changed, update only the relevant compact notes and add a compact Engram pointer.
9. Return: active mode, scenario, current state, what was created/updated, what was skipped, and why.

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
- `assets/compact-routing.schema.json` — canonical routing and escalation schema
- `references/operating-model.md` — bootstrap/hydrate/consume/update behavior
- `references/obsidian-templates.md` — recommended note layout and starter templates
