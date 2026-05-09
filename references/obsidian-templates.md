# Obsidian Templates

## Suggested folders

```text
01_Projects/<project-name>/
├── 00_Project_Index.md
├── 01_Current_State.md
├── 02_Graphify/
│   ├── GRAPH_REPORT.md
│   └── last-run.md
├── 03_Architecture_Summary.md
├── 04_Conventions.md
└── 05_Active_Work.md
```

## Minimal project note template

```md
---
project: <project-name>
source: project-memory-bridge
---

# <title>

## Purpose

<why this note exists>

## Current Content

<durable project knowledge>

## Source Pointers

- Repository: <project-root>
- Memory config: .atl/memory-config.json
```

## What belongs in durable notes

- arquitectura de alto nivel
- convenciones estables
- decisiones con contexto
- troubleshooting repetible
- estado activo útil entre sesiones

## What does NOT belong

- dumps completos del grafo
- diffs gigantes
- logs efímeros
- contexto que vive mejor en Engram
