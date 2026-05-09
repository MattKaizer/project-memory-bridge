# Project Memory Bridge

<p align="center">
  <img src="assets/logo.svg" alt="Project Memory Bridge logo" width="180" />
</p>

<p align="center"><strong>Una skill liviana para conectar Engram, Graphify y Obsidian sin romper el flujo normal del agente.</strong></p>

<p align="center">
  <img src="https://img.shields.io/badge/version-0.1.0-22C55E" alt="Version 0.1.0" />
  <img src="https://img.shields.io/badge/license-MIT-38BDF8" alt="MIT License" />
  <img src="https://img.shields.io/badge/status-beta-F59E0B" alt="Beta status" />
</p>

---

## GitHub quick metadata

**About**

```text
Persistent-memory bridge for Gentle-AI workflows using Engram, Graphify, and Obsidian.
```

**Topics**

```text
ai llm agent memory engram obsidian graphify sdd developer-tools knowledge-management repository-analysis prompt-engineering
```

**Current version**

```text
v0.1.0
```

## Qué es

`project-memory-bridge` agrega una capa de memoria persistente para repos medianos o grandes.

Funciona **en conjunto con Gentle-AI**. No es un reemplazo del framework ni de Engram: extiende el workflow normal con memoria estructural y conocimiento durable.

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
├── scripts/
│   ├── bootstrap.py
│   ├── bootstrap.sh
│   └── bootstrap.ps1
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

## Prerrequisitos

- **Gentle-AI** ya instalado y funcionando
- **Engram** disponible dentro de ese workflow
- **Obsidian** si querés memoria durable local
- **Python 3.10+** para ejecutar el core del bootstrap
- **Graphify** si querés análisis estructural automatizado

## Arquitectura del bootstrap

El core ahora vive en:

```text
scripts/bootstrap.py
```

Pero NO me comí la curva de pensar “si no hay Python, igual va a correr”. No. Un `.py` solo depende de Python.

Por eso dejé launchers finos por plataforma:

- `scripts/bootstrap.sh` → macOS/Linux
- `scripts/bootstrap.ps1` → Windows PowerShell

Esos launchers primero resuelven Python 3.10+ y recién después invocan `bootstrap.py`.

## Instalación y bootstrap

La skill **no instala sola** Gentle-AI, Engram, Graphify ni Obsidian.

Para eso existe este bootstrap multiplataforma:

```bash
scripts/bootstrap.py
```

### Orden real del bootstrap

El flujo real respeta dependencias reales en este orden:

1. launcher detecta o instala **Python 3.10+**
2. `bootstrap.py` verifica el repo objetivo
3. crea `.atl/`
4. verifica/instala **graphifyy** con `uv`, `pipx` o `pip`
5. corre `graphify install`
6. genera `.atl/memory-config.json`
7. crea directorios y notas de Obsidian usando ese config
8. corre `graphify update .` si corresponde

Primero se resuelve Python, después Graphify, y recién después se escribe el config final con el estado real de disponibilidad. Eso evita declarar capacidades que no existen todavía.

### Uso básico

Desde el repo que querés preparar en macOS/Linux:

```bash
/ruta/a/project-memory-bridge/scripts/bootstrap.sh
```

En Windows PowerShell:

```powershell
.\scripts\bootstrap.ps1
```

### Uso recomendado

```bash
/ruta/a/project-memory-bridge/scripts/bootstrap.sh \
  --primary-agent opencode \
  --install-graphify
```

### Opciones útiles

```bash
--project-root PATH
--project-name NAME
--vault-root PATH
--project-dir PATH
--primary-agent NAME
--graphify-output-dir DIR
--install-graphify
--skip-graphify-update
--disable-obsidian
--disable-graphify
```

## Uso de la skill

1. Instalá la skill en tu runtime global o por proyecto.
2. Corré `scripts/bootstrap.sh` o `scripts/bootstrap.ps1` en el repo objetivo.
3. Activala en onboarding, architecture review o SDD init.
4. Leé primero memoria barata; abrí código crudo solo cuando haga falta.

## Roadmap sugerido

- agregar ejemplos de integración con orchestrators
- sumar plantillas de notas por tipo de proyecto
- incorporar validación automática del config
- medir ahorro real de tokens en casos de uso repetidos

## Licencia

MIT
