# Token Benchmark

## Goal

Medir si `project-memory-bridge` realmente reduce contexto leído frente a redescubrir un repo desde archivos crudos.

## What this benchmark measures

Este benchmark compara dos packs de contexto:

- **baseline**: archivos que el agente abriría sin memoria persistente
- **memory_first**: archivos baratos que debería abrir primero con este proyecto

La salida compara:

- cantidad de archivos
- líneas totales
- bytes totales
- tokens estimados

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

- si `memory_first` usa claramente menos tokens que `baseline`, la estrategia va en la dirección correcta
- si la diferencia es mínima, no vale la complejidad
- si `memory_first` gasta más, la implementación está mal y NO conviene usarla así

## What to customize

Editá `benchmarks/example-benchmark.json` para tu repo real:

- `baseline`: qué abriría el agente sin puente de memoria
- `memory_first`: qué leería primero con Graphify + Obsidian + config

## Recommended validation

Probalo al menos en 3 escenarios:

1. onboarding de repo
2. architecture review
3. planning / `sdd-init`

Si no mejora ahí, el proyecto no está cumpliendo su promesa.
