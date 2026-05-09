# Project Memory Bridge

<p align="center">
  <img src="assets/logo.svg" alt="Project Memory Bridge logo" width="180" />
</p>

<p align="center"><strong>Una skill liviana para conectar Engram, Graphify y Obsidian sin romper el flujo normal del agente.</strong></p>

---

## Qué es

`project-memory-bridge` agrega una capa de memoria persistente para repos medianos o grandes.

La idea es simple:

- **Engram** sigue siendo la memoria operativa principal.
- **Graphify** ayuda a entender estructura y relaciones del repo.
- **Obsidian** guarda conocimiento durable: arquitectura, decisiones, troubleshooting y contexto de trabajo.

El objetivo NO es guardar todo.
El objetivo es **dejar de redescubrir el repo desde cero** cada vez que el agente vuelve a trabajar.

## Por qué existe

Sin una capa así, el agente suele gastar tokens en:

- reabrir archivos estructurales una y otra vez
- reconstruir arquitectura desde código crudo
- perder contexto entre sesiones largas
- repetir onboarding técnico

Esta skill reduce ese costo al dar un **orden de lectura más barato**:

1. config
2. Engram
3. notas de Obsidian
4. reporte de Graphify
5. código fuente puntual

## Cuándo conviene

Usala cuando:

- hacés onboarding de un repo existente
- querés correr `sdd-init` o planning serio en un repo grande
- necesitás revisar arquitectura o bounded contexts
- querés persistir contexto durable fuera del prompt runtime

No la uses para:

- cambios chicos en 1 archivo
- fixes locales ya conocidos
- preguntas conceptuales sin contexto del repo

## Qué resuelve

| Capa | Rol |
|---|---|
| Engram | Memoria operativa y continuidad de sesión |
| Graphify | Estructura del repo, relaciones y navegación |
| Obsidian | Conocimiento durable del proyecto |
| Código fuente | Fuente de verdad final |

## Filosofía

Esta skill está diseñada para ser **LLM-first**:

- `SKILL.md` corto y accionable
- detalles pesados fuera del runtime principal
- assets y references para todo lo extenso
- cero interferencia con Engram

## Estructura del repo

```text
project-memory-bridge/
├── SKILL.md
├── README.md
├── assets/
│   ├── logo.svg
│   └── memory-config.schema.json
└── references/
    ├── operating-model.md
    └── obsidian-templates.md
```

## Config mínima

La skill espera este archivo:

```text
.atl/memory-config.json
```

El esquema base vive en:

```text
assets/memory-config.schema.json
```

## Modos de operación

| Modo | Qué hace |
|---|---|
| `bootstrap` | Crea config y base mínima de memoria |
| `hydrate` | Llena notas con conocimiento real del repo |
| `consume` | Usa memoria existente sin repoblarla |
| `update` | Actualiza solo conocimiento durable afectado |

## Beneficio real

Si la skill es corta y se activa bien, **sí puede ahorrar tokens**.

Si la convertís en un documento gigante, pasa lo contrario: el costo fijo de cargar la skill supera el ahorro.

Por eso esta versión separa:

- **runtime contract** en `SKILL.md`
- **detalle operativo** en `references/`
- **schema/plantillas** en `assets/`

## Instalación y uso

1. Instalá la skill en tu runtime global o por proyecto.
2. Asegurá `.atl/memory-config.json`.
3. Activala en onboarding, architecture review o SDD init.
4. Leé primero memoria barata; abrí código crudo solo cuando haga falta.

## Roadmap sugerido

- agregar ejemplos de integración con orchestrators
- sumar plantillas de notas por tipo de proyecto
- incorporar validación automática del config
- medir ahorro real de tokens en casos de uso repetidos

## Licencia

MIT
