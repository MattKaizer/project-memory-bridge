# Token Benchmark

## Goal

Medir si `project-memory-bridge` realmente reduce contexto leído frente a redescubrir un repo desde archivos crudos.

## What this benchmark measures

Este benchmark compara tres packs de contexto:

- **baseline_raw_rediscovery**: archivos que el agente abriría sin memoria persistente
- **memory_first_compact**: contexto barato y focalizado que debería abrir primero
- **memory_first_full_graph**: contexto barato + Graphify completo cuando la tarea realmente necesita amplitud

La salida compara:

- cantidad de archivos
- líneas totales
- bytes totales
- tokens estimados
- ahorro porcentual contra baseline
- overhead de full graph contra compacto

## Important limitation

Esto NO mide tokens facturados por un proveedor real.

Mide una **proxy reproducible de contexto potencialmente cargado**.

Eso alcanza para decidir si la estrategia tiene sentido o no.

## Run it

```bash
python3 scripts/benchmark_memory_savings.py \
  --repo-root /ruta/al/repo-objetivo \
  --config benchmarks/example-benchmark.json \
  --details
```

## How to interpret it

- si `memory_first_compact` usa claramente menos tokens que `baseline`, la estrategia va en la dirección correcta para tareas focalizadas
- si `memory_first_full_graph` sigue siendo menor que `baseline`, Graphify completo sigue teniendo lugar para onboarding/review
- si `memory_first_full_graph` pierde contra `memory_first_compact` en tareas focalizadas, NO es un bug: es la evidencia de que conviene arrancar compacto

## What to customize

Editá `benchmarks/example-benchmark.json` para tu repo real:

- `baseline_raw_rediscovery`: qué abriría el agente sin puente de memoria
- `memory_first_compact`: qué leería primero con contexto compacto
- `memory_first_full_graph`: qué leería cuando además necesita amplitud estructural

## Recommended validation

Probalo al menos en 3 escenarios:

1. tarea focalizada en un dominio
2. onboarding de repo
3. architecture review
4. cambio cross-module

Si no mejora ahí, el proyecto no está cumpliendo su promesa.
