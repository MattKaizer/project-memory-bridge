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
- Use the cheapest context first: config -> Engram -> Obsidian notes -> Graphify report -> raw code.
- Store only compact Graphify/Obsidian pointers in Engram; large reports stay in files.
- Run Graphify only for init, stale structure, or architecture-heavy work.
- Treat source code as the final authority when exact implementation details matter.

## Decision Gates

| Situation | Action |
|---|---|
| `.atl/memory-config.json` missing during init/onboarding/review | Bootstrap memory config and note structure |
| Notes missing or placeholder-only | Hydrate durable notes from current repo state |
| Normal implementation task with ready memory | Consume existing memory, avoid repopulation |
| Durable architecture/process knowledge changed | Update only affected notes and pointers |

## Execution Steps

1. Read `.atl/memory-config.json`.
2. Determine mode: `bootstrap`, `hydrate`, `consume`, or `update`.
3. Follow the configured paths and respect user overrides.
4. For init/onboarding/review, ensure required memory foundations exist before claiming readiness.
5. For normal coding work, read memory before scanning many files and avoid unnecessary Graphify refreshes.
6. If durable knowledge changed, update only the relevant notes and add a compact Engram pointer.
7. Return: active mode, current state, what was created/updated, what was skipped, and why.

## Output Contract

Return:

- chosen mode and why
- readiness status: `complete`, `partial`, or `failed`
- files or notes created/updated
- Graphify status: refreshed, reused, skipped, or unavailable
- Engram pointer status
- unresolved risks or follow-up actions

## References

- `README.md` — repo overview, installation, and usage
- `assets/memory-config.schema.json` — canonical lightweight config schema
- `references/operating-model.md` — bootstrap/hydrate/consume/update behavior
- `references/obsidian-templates.md` — recommended note layout and starter templates
