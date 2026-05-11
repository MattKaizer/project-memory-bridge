# Operating Model

## Goal

Usar memoria persistente sin convertir la skill en un prompt gigante.

## State model

```text
missing_foundations -> bootstrap -> hydrate -> ready
ready -> consume
ready + durable_change -> update -> ready
```

## Mode rules

### bootstrap

Usalo cuando falta alguna base mínima:

- `.atl/memory-config.json`
- directorio de notas del proyecto
- estructura inicial para Graphify/Obsidian

### hydrate

Usalo cuando la base existe pero el conocimiento todavía no:

- notas vacías o con placeholders
- onboarding inicial
- architecture review fuerte

### consume

Modo normal para implementación cotidiana.

- leer memoria primero
- no repoblar notas
- no correr Graphify salvo necesidad real

### update

Usalo después de cambios con conocimiento durable:

- decisiones de arquitectura
- nuevas convenciones
- troubleshooting reusable
- cambios estructurales del repo

## Context routing order

1. `.atl/memory-config.json`
2. `.atl/compact-routing.json`
3. Engram compact pointer
4. `notes/00_Project_Index.md`
5. notas compactas por escenario o dominio
6. reporte completo de Graphify
7. código puntual

## Compact-first rule

Para tareas focalizadas, la skill debe intentar resolver el contexto con **1 a 3 artefactos compactos** antes de abrir `GRAPH_REPORT.md`.

El first-load genérico recomendado es:

1. manifest mínimo (`.atl/memory-config.json`)
2. puntero compacto de Engram
3. router humano (`notes/00_Project_Index.md`) o la nota de escenario/dominio más barata

Usá Graphify completo solo cuando pase al menos una de estas condiciones:

- onboarding amplio del repo
- architecture review
- relaciones cross-module
- la memoria compacta está vieja, ausente o insuficiente

Si ninguna aplica, abrir el graph completo es gastar tokens de más.

## Escalation rubric

### Compact OK

- la tarea sigue dentro de un dominio o relación ya resumida
- la nota compacta responde qué abrir después
- todavía no hace falta verificar implementación exacta

### Escalar a código crudo

- necesitás firmas, contratos, payloads o comportamiento exacto
- vas a editar o verificar código
- la memoria compacta contradice el repo actual

### Escalar a graph completo

- importan relaciones entre múltiples módulos
- el objetivo es onboarding amplio o architecture review
- el pack compacto quedó corto incluso después del first-load

## Generic compact artifact shapes

- **scenario summary**: una tarea típica completa en un área (`bugfix-auth-login`, `feature-billing-invoice-list`)
- **domain summary**: mapa compacto de un dominio (`auth`, `billing`, `frontend-shell`)
- **cross-module note**: relación entre dominios (`auth-billing`, `api-ui-contracts`)

La skill no debe hardcodear nombres de repos. Debe depender de rutas y defaults declarados en `.atl/memory-config.json`.

## Non-goals

- reemplazar Engram
- guardar documentos largos en memoria operativa
- forzar Graphify para tareas chicas
- abrir muchos archivos cuando ya existe contexto durable
