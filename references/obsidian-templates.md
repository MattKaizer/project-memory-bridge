# Obsidian Templates

## Suggested folders

```text
01_Projects/<project-name>/
├── 00_Project_Index.md
├── 01_Current_State.md
├── 01_Architecture/
│   └── Architecture_Index.md
├── 02_Graphify/
│   ├── GRAPH_REPORT.md
│   └── last-run.md
├── 02_Project_Map.md
├── 03_Architecture_Summary.md
├── 04_Conventions.md
├── 05_Active_Work.md
├── 04_Decisions/
│   └── Decisions_Index.md
├── 05_Troubleshooting/
│   └── Troubleshooting_Index.md
├── 10_Scenarios/
│   └── focused-task-example.md
├── 20_Domains/
│   └── domain-example.md
└── 30_Cross_Module/
    └── relation-example.md
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
- resúmenes compactos por escenario
- resúmenes compactos por dominio
- relaciones cross-module resumidas

## What does NOT belong

- dumps completos del grafo
- diffs gigantes
- logs efímeros
- contexto que vive mejor en Engram

## Compact note frontmatter

```md
---
project: <project-name>
source: project-memory-bridge
note_type: scenario-summary | domain-summary | cross-module-summary
token_budget: 200-400
status: active
---
```

## Compact note shape

```md
# <title>

## When to open this

<task shapes where this note is the cheapest useful context>

## Key files

- path/to/file.ts — why it matters

## Constraints

- invariant or gotcha

## Escalate to graph report when

- cross-module relationships are needed
- architecture breadth matters more than token minimization
```

## Compact router note

`00_Project_Index.md` debe funcionar como router humano barato:

- dominios disponibles
- qué nota abrir primero según task shape
- cuándo alcanza compacto
- cuándo escalar a código crudo
- cuándo escalar a graph completo

Si ese router supera el costo de una nota compacta normal, se volvió demasiado verboso.

## Bootstrap alignment

El bootstrap actual crea tanto la estructura histórica (`01_Architecture`, `04_Decisions`, `05_Troubleshooting`) como las carpetas compactas (`10_Scenarios`, `20_Domains`, `30_Cross_Module`).

No son alternativas: conviven. Las carpetas compactas existen para ahorrar tokens en tareas focalizadas.

Si una nota compacta supera `max_tokens_per_artifact`, dividila por escenario, subdominio o relación antes de seguir agregando contenido.
