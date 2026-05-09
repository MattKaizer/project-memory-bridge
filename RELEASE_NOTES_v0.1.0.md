# Release v0.1.0

## About

First public release of **Project Memory Bridge**.

This version establishes the base skill contract for combining **Gentle-AI**, **Engram**, **Graphify**, and **Obsidian** as a lightweight persistent-memory strategy.

## Highlights

- Introduces a compact, LLM-first `SKILL.md`
- Adds a visual project identity with `assets/logo.svg`
- Documents purpose, usage, and operating model in `README.md`
- Provides a lightweight config schema in `assets/memory-config.schema.json`
- Moves detailed guidance into `references/` to reduce runtime token cost

## Why this release matters

The original draft had strong ideas but was too large for efficient runtime use.

`v0.1.0` turns the repository into a publishable base with:

- a shorter skill contract
- clearer boundaries between runtime instructions and supporting docs
- a better chance of actually saving tokens in medium and large repositories

## Included files

- `SKILL.md`
- `README.md`
- `assets/logo.svg`
- `assets/memory-config.schema.json`
- `references/operating-model.md`
- `references/obsidian-templates.md`

## Suggested GitHub release title

```text
v0.1.0 — First public beta
```

## Suggested GitHub release description

```md
First public beta of Project Memory Bridge.

This release introduces a lightweight runtime skill for Gentle-AI workflows, bridging Engram, Graphify, and Obsidian, plus the supporting docs and config schema needed to start using it in real repositories.
```
