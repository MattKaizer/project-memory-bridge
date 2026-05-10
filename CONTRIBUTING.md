# Contributing to Project Memory Bridge

Thanks for contributing. The goal is simple: keep changes reviewable, documented, and aligned with the repo's real responsibilities.

## Quick path

1. Fork or create a branch from `main`.
2. Make one focused change at a time.
3. Update docs when behavior changes.
4. Open a pull request with clear intent and verification notes.

## What to contribute

Good contributions usually improve one of these areas:

- bootstrap reliability across environments
- skill runtime installation and activation
- documentation and onboarding clarity
- Graphify or Obsidian integration guidance
- benchmarks proving memory/context value

## Ground rules

- Do not push directly to `main`.
- Prefer small PRs over broad mixed changes.
- Keep docs and code in sync.
- Verify technical claims before writing them down.
- Do not market token savings without reproducible evidence.

## Setup

Clone the repo and review the main guide first:

```bash
git clone <your-fork-or-repo-url>
cd project-memory-bridge
```

Then use the bootstrap path that matches your environment, as documented in `README.md`.

## Pull request expectations

Your PR should answer these questions clearly:

- What problem does this solve?
- Why is this the right level of change?
- How did you verify it?
- What is intentionally out of scope?

If your change affects bootstrap behavior, include:

- target OS or shell used
- exact command run
- resulting install/config path

## Commit guidance

Use conventional commits when possible.

Examples:

- `fix: prioritize existing .agents skills directory`
- `docs: clarify Windows bootstrap usage`
- `feat: add benchmark config example`

## Documentation checklist

Before opening a PR, check these:

- [ ] README is still accurate
- [ ] New flags or paths are documented
- [ ] Examples match the real script behavior
- [ ] Terminology stays consistent with Gentle-AI, Engram, Graphify, and Obsidian

## Need a safe default?

If you are unsure, choose the smaller change, explain the tradeoff in the PR, and leave the repo easier to verify than before.
