# Project Memory Bridge

<p align="center">
  <img src="assets/logo.svg" alt="Project Memory Bridge logo" width="180" />
</p>

<p align="center"><strong>Persistent-memory bridge for Gentle-AI workflows using Engram, Graphify, and Obsidian.</strong></p>

<p align="center">
  <img src="https://img.shields.io/badge/version-0.1.0-22C55E" alt="Version 0.1.0" />
  <img src="https://img.shields.io/badge/license-MIT-38BDF8" alt="MIT License" />
  <img src="https://img.shields.io/badge/status-beta-F59E0B" alt="Beta status" />
</p>

> `project-memory-bridge` is a **companion layer for Gentle-AI**. It does not replace Gentle-AI or Engram. It adds structured project memory, durable notes, and Graphify-powered repository discovery on top of the normal workflow.

## Table of Contents

- [What is this?](#what-is-this)
- [Quick Start](#quick-start)
- [What lives where](#what-lives-where)
- [Supported bootstrap paths](#supported-bootstrap-paths)
- [Bootstrap architecture](#bootstrap-architecture)
- [Repository structure](#repository-structure)
- [Configuration](#configuration)
- [Operation modes](#operation-modes)
- [Token benchmark](#token-benchmark)
- [When to use it](#when-to-use-it)
- [Credits](#credits)
- [Documentation](#documentation)
- [GitHub metadata](#github-metadata)
- [License](#license)

---

## What is this?

Project Memory Bridge exists to stop agents from **rediscovering the same large repository from scratch** every time they return.

It combines four layers with clear responsibilities:

| Layer | Role |
|---|---|
| **Gentle-AI** | Main workflow, orchestration, skills, SDD behavior |
| **Engram** | Operational memory and session continuity |
| **Graphify** | Repository structure, relationships, discovery |
| **Obsidian** | Durable project knowledge, notes, architecture history |

The goal is NOT “store everything”.
The goal is **spend tokens on reasoning, not on repeated repo reconstruction**.

---

## Quick Start

### 1. Prerequisites

- **Python 3.10+** for the bootstrap core
- **Graphify** if you want structural repository analysis
- **Obsidian** if you want local durable notes

> **Important:** this project depends on **Gentle-AI**. The bootstrap now checks that dependency interactively. If `gentle-ai` is missing, it explains why it is required and can install it with the recommended method for your operating system. **Engram comes with Gentle-AI**, so you do not need to install Engram separately in the normal path.

> **Obsidian note:** the bootstrap can create the project note structure and configured vault paths, but it does **not** install the Obsidian application itself. If you want the Obsidian layer, install Obsidian first and then run the bootstrap.

### 2. Run bootstrap

Choose the launcher that matches your environment.

#### macOS / Linux / Git Bash / MSYS / Cygwin

```bash
/ruta/a/project-memory-bridge/scripts/bootstrap
```

This launcher auto-detects the OS and delegates to the right wrapper.

Recommended example:

```bash
/ruta/a/project-memory-bridge/scripts/bootstrap \
  --primary-agent opencode \
  --install-gentle-ai \
  --install-graphify \
  --install-skill \
  --client opencode
```

#### Windows PowerShell

```powershell
.\scripts\bootstrap.ps1 `
  --primary-agent opencode `
  --install-gentle-ai `
  --install-graphify `
  --install-skill `
  --client opencode
```

#### Windows CMD

```bat
scripts\bootstrap.cmd --primary-agent opencode --install-gentle-ai --install-graphify --install-skill --client opencode
```

#### Delegation flow

- POSIX shells → `bootstrap`
- Windows PowerShell → `bootstrap.ps1`
- Windows CMD / double-click style entry → `bootstrap.cmd`

- macOS / Linux → `bootstrap` → `bootstrap.sh` → `bootstrap.py`
- Git Bash / MSYS / Cygwin → `bootstrap` → `bootstrap.ps1` → `bootstrap.py`
- Windows PowerShell → `bootstrap.ps1` → `bootstrap.py`
- Windows CMD → `bootstrap.cmd` → `bootstrap.ps1` → `bootstrap.py`

### 3. Use the skill

1. Run the bootstrap launcher for your environment.
2. Let it install or verify **Gentle-AI** if needed.
3. Let it install or verify **Graphify** if you requested it.
4. Let it copy the skill into the runtime if you passed `--install-skill`.
5. Open your target repo in your AI client.
6. Activate the skill during onboarding, architecture review, or `sdd-init`.
7. Read cheap memory first, prefer compact scenario/domain notes, and open raw code only when needed.

### 4. Route context by task shape

Use this default routing strategy:

| Task shape | First context | Escalation |
|---|---|---|
| Focused bugfix / targeted feature | config + Engram pointer + compact scenario/domain notes | raw code |
| Cross-module change | compact notes | full Graphify report |
| Repo onboarding | compact notes | full Graphify report |
| Architecture review | compact notes | full Graphify report |

The important shift is simple: **Graphify full report is not the default starting point anymore**.
It is the escalation path for broad structural work.

---

## Token benchmark

If you are not sure the project saves context, do not trust it blindly. Measure it.

Run the benchmark script against a real target repository:

```bash
python3 scripts/benchmark_memory_savings.py \
  --repo-root /ruta/al/repo-objetivo \
  --config benchmarks/example-benchmark.json \
  --details
```

What it compares:

- **baseline_raw_rediscovery** → raw files opened without memory
- **memory_first_compact** → config + Engram pointer targets + compact notes
- **memory_first_full_graph** → compact context plus full Graphify when breadth is needed

What it reports:

- number of files
- total lines
- total bytes
- estimated tokens

Interpretation:

- if `memory_first_compact` is much smaller for focused tasks, the bridge is doing its main job
- if `memory_first_full_graph` is still smaller than baseline for onboarding/review, Graphify remains justified for broad work
- if full graph is used for focused tasks and loses badly to compact memory, that is expected and should be avoided

Important limitation:

- this does **not** measure billed provider tokens directly
- it measures a **reproducible proxy of loaded context**
- that is enough to decide whether the strategy is directionally good or bad

Recommended validation scenarios:

1. focused task in one domain
2. repo onboarding
3. architecture review / cross-module planning

If it does not improve those scenarios, the project is not delivering on its promise.

Full guide:

- `docs/token-benchmark.md`

---

## What lives where

| Component | Responsibility |
|---|---|
| **This repo** | Skill contract, bootstrap scripts, config schema, note templates |
| **Gentle-AI** | Agent behavior, persona, SDD orchestration, normal Engram usage |
| **Target repo** | `.atl/memory-config.json`, `graphify-out/`, local project state |
| **Obsidian vault** | Durable notes, architecture summaries, project memory |

This repo is a **bridge layer**, not a standalone assistant framework.

---

## Credits

Project Memory Bridge builds on top of the work and ideas behind these tools and projects:

| Project | Role in this workflow |
|---|---|
| **[Gentle-AI](https://github.com/Gentleman-Programming/gentle-ai)** | Base workflow, agent behavior, persona, SDD, and orchestration |
| **[Graphify](https://github.com/safishamsi/graphify)** | Repository graph generation and structural discovery |
| **[Engram](https://github.com/Gentleman-Programming/engram)** | Operational memory and continuity across sessions |
| **[Obsidian](https://obsidian.md/)** | Durable local project knowledge and notes |

This repository is meant to **extend** those workflows, not to replace or erase their contribution.

---

## Supported bootstrap paths

| Platform | Entry point | Python handling |
|---|---|---|
| Main launcher (POSIX) | `scripts/bootstrap` | Detects OS and delegates to the right wrapper |
| macOS | `scripts/bootstrap.sh` | Detects Python 3.10+, installs via Homebrew if missing |
| Linux | `scripts/bootstrap.sh` | Detects Python 3.10+, asks for manual install if missing |
| Windows PowerShell | `scripts/bootstrap.ps1` | Detects Python 3.10+, installs via `winget` or `scoop` if possible |
| Windows CMD | `scripts/bootstrap.cmd` | Delegates to PowerShell launcher |
| Core logic | `scripts/bootstrap.py` | Shared bootstrap behavior across platforms |

---

## Bootstrap architecture

The bootstrap is intentionally split in two layers:

- **platform launcher** → obtains Python 3.10+
- **Python core** → performs the real bootstrap

The **central logic entrypoint** is still `scripts/bootstrap.py`.

The shell and PowerShell launchers exist only to make sure the Python runtime is available before delegating to that core.

For everyday usage, the launcher layer is now complete enough to present a clear main path on both POSIX and Windows environments.

### Why this split matters

A single `.py` file is cleaner and more maintainable for shared logic.

But a pure Python entrypoint fails immediately if Python is missing.

So the launchers solve the runtime dependency first, then call the core.

### Real dependency order

1. launcher resolves **Python 3.10+**
2. `bootstrap.py` checks **Gentle-AI**
3. if missing, it explains the dependency and can install it interactively
4. creates `.atl/`
5. ensures **graphifyy** via `uv`, `pipx`, or `pip`
6. runs `graphify install`
7. writes `.atl/memory-config.json`
8. creates Obsidian folders and seed notes
9. runs `graphify update .` if enabled
10. optionally installs the skill into the agent runtime

This order matters because the final config should reflect **real available capabilities**, not wishful ones.

### Gentle-AI installation path

If `gentle-ai` is missing, the bootstrap can suggest or run the official installation path:

| Platform | Preferred path |
|---|---|
| macOS | `brew tap Gentleman-Programming/homebrew-tap && brew install gentle-ai` |
| Linux | Homebrew if available, otherwise official install script |
| Windows | `scoop install gentle-ai`, otherwise official PowerShell installer |

If you want it to install without asking, pass:

```bash
--install-gentle-ai --yes
```

### Skill installation targets

If you pass `--install-skill`, the bootstrap can also copy the skill runtime files.

Resolution order:

1. `--skill-dir` if you provide it
2. `~/.agents/skills` if that folder already exists
3. client-aware destination if supported
4. `~/.agents` as generic global fallback
5. `<target-repo>/.agents` when `--scope project`

Today the generic fallback is the safest default for clients like **OpenCode** and **Codex**.

If `~/.agents` does not exist, the script becomes **interactive by default**:

- it explains what `~/.agents` is for
- asks whether you want to create it
- creates it only if you confirm

If you want non-interactive behavior, pass:

```bash
--yes
```

---

## Repository structure

```text
project-memory-bridge/
├── SKILL.md
├── README.md
├── RELEASE_NOTES_v0.1.0.md
├── assets/
│   ├── logo.svg
│   └── memory-config.schema.json
├── scripts/
│   ├── bootstrap
│   ├── bootstrap.cmd
│   ├── bootstrap.py
│   ├── bootstrap.sh
│   └── bootstrap.ps1
└── references/
    ├── operating-model.md
    └── obsidian-templates.md
```

---

## Configuration

The expected config file is:

```text
.atl/memory-config.json
```

The lightweight schema lives in:

```text
assets/memory-config.schema.json
```

### Common options

```bash
--project-root PATH
--project-name NAME
--vault-root PATH
--project-dir PATH
--primary-agent NAME
--graphify-output-dir DIR
--install-gentle-ai
--install-graphify
--install-skill
--client generic|opencode|codex
--scope global|project
--skill-dir PATH
--skip-graphify-update
--disable-obsidian
--disable-graphify
--yes
```

---

## Operation modes

| Mode | What it does |
|---|---|
| `bootstrap` | Creates config and minimum memory foundations |
| `hydrate` | Fills notes with real project knowledge |
| `consume` | Uses existing memory without repopulating it |
| `update` | Refreshes only durable knowledge affected by a change |

The skill is designed to stay **LLM-first**:

- short runtime contract in `SKILL.md`
- heavier detail moved to `references/`
- schema and install artifacts moved to `assets/` and `scripts/`

---

## When to use it

Use it when:

- onboarding an existing repository
- running `sdd-init` or planning on a medium/large repo
- reviewing architecture or bounded contexts
- reducing repeated context rebuilds across sessions

Do **not** use it for:

- tiny one-file edits
- already-known local fixes
- conceptual questions detached from the repository

---

## Documentation

| Document | Purpose |
|---|---|
| `SKILL.md` | Runtime contract for the skill |
| `references/operating-model.md` | Bootstrap, hydrate, consume, update model |
| `references/obsidian-templates.md` | Suggested durable note structure |
| `RELEASE_NOTES_v0.1.0.md` | First public beta release notes |
| `docs/token-benchmark.md` | How to validate real context savings |

---

## GitHub metadata

**About**

```text
Persistent-memory bridge for Gentle-AI workflows using Engram, Graphify, and Obsidian.
```

**Topics**

```text
ai llm agent memory engram obsidian graphify sdd developer-tools knowledge-management repository-analysis prompt-engineering gentle-ai
```

**Current version**

```text
v0.1.0
```

---

## License

MIT
