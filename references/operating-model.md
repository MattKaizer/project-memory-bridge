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

## Cheap read order

1. `.atl/memory-config.json`
2. Engram
3. índice/estado actual en Obsidian
4. reporte de Graphify
5. código puntual

## Non-goals

- reemplazar Engram
- guardar documentos largos en memoria operativa
- forzar Graphify para tareas chicas
- abrir muchos archivos cuando ya existe contexto durable
