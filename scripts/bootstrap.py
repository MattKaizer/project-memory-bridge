#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def log(message: str) -> None:
    print(f"[project-memory-bridge] {message}")


def fail(message: str) -> None:
    raise SystemExit(f"[project-memory-bridge] ERROR: {message}")


def run(command: list[str], cwd: Path | None = None) -> None:
    subprocess.run(command, cwd=str(cwd) if cwd else None, check=True)


def run_shell(command: str) -> None:
    subprocess.run(command, shell=True, check=True)


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def confirm(prompt: str) -> bool:
    if not sys.stdin.isatty():
        return False
    try:
        answer = input(f"{prompt} [y/N]: ").strip().lower()
    except EOFError:
        return False
    return answer in {"y", "yes", "s", "si"}


def ensure_python_version() -> None:
    if sys.version_info < (3, 10):
        fail("bootstrap.py requiere Python 3.10+.")


def write_text_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def build_note(title: str, project_name: str, project_root: Path) -> str:
    return f"""---
project: {project_name}
source: project-memory-bridge
---

# {title}

## Purpose

Pending initial project scan.

## Current Content

Pending.

## Source Pointers

- Repository: {project_root}
- Memory config: .atl/memory-config.json
"""


def detect_graphify_installer() -> list[str] | None:
    if command_exists("uv"):
        return ["uv", "tool", "install", "graphifyy"]
    if command_exists("pipx"):
        return ["pipx", "install", "graphifyy"]
    if command_exists("python"):
        return ["python", "-m", "pip", "install", "graphifyy"]
    return [sys.executable, "-m", "pip", "install", "graphifyy"]


def ensure_graphify(install_if_missing: bool) -> bool:
    if command_exists("graphify"):
        log("Ejecutando 'graphify install' para asegurar runtime local")
        run(["graphify", "install"])
        return True

    if not install_if_missing:
        log("Graphify no está instalado. Se continúa sin instalarlo.")
        return False

    installer = detect_graphify_installer()
    if installer is None:
        fail("No encontré uv, pipx ni pip para instalar graphifyy.")

    log(f"Instalando Graphify con: {' '.join(installer)}")
    run(installer)

    if not command_exists("graphify"):
        fail("La instalación de graphifyy terminó pero el comando 'graphify' no quedó disponible.")

    log("Ejecutando 'graphify install'")
    run(["graphify", "install"])
    return True


def detect_platform() -> str:
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    if system == "windows":
        return "windows"
    if system == "linux":
        return "linux"
    return system


def install_gentle_ai(target_platform: str) -> None:
    if target_platform in {"macos", "linux"}:
        if command_exists("brew"):
            log("Instalando Gentle-AI con Homebrew...")
            run(["brew", "tap", "Gentleman-Programming/homebrew-tap"])
            run(["brew", "install", "gentle-ai"])
            return

        log("Homebrew no está disponible. Usando el script oficial de instalación de Gentle-AI...")
        run_shell("curl -fsSL https://raw.githubusercontent.com/Gentleman-Programming/gentle-ai/main/scripts/install.sh | bash")
        return

    if target_platform == "windows":
        if command_exists("scoop"):
            log("Instalando Gentle-AI con Scoop...")
            run(["scoop", "bucket", "add", "gentleman", "https://github.com/Gentleman-Programming/scoop-bucket"])
            run(["scoop", "install", "gentle-ai"])
            return

        log("Scoop no está disponible. Usando el script oficial de instalación de Gentle-AI para PowerShell...")
        run(
            [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-Command",
                "irm https://raw.githubusercontent.com/Gentleman-Programming/gentle-ai/main/scripts/install.ps1 | iex",
            ]
        )
        return

    fail(f"No tengo una ruta de instalación automática de Gentle-AI para la plataforma: {target_platform}")


def ensure_gentle_ai(install_if_missing: bool, auto_yes: bool) -> None:
    if command_exists("gentle-ai"):
        return

    target_platform = detect_platform()
    log("Project Memory Bridge depende de Gentle-AI. Engram viene dentro de ese stack.")

    if not install_if_missing:
        if auto_yes:
            fail("Gentle-AI no está instalado. Reintentá con --install-gentle-ai o instalalo manualmente.")

        wants_install = confirm("No encontré 'gentle-ai'. ¿Querés instalarlo ahora con el método recomendado para tu sistema?")
        if not wants_install:
            fail("Bootstrap cancelado porque Gentle-AI es un prerequisito obligatorio.")
    else:
        log("No encontré 'gentle-ai'. Voy a instalarlo porque pasaste --install-gentle-ai.")

    install_gentle_ai(target_platform)

    if not command_exists("gentle-ai"):
        fail("La instalación de Gentle-AI terminó pero el comando 'gentle-ai' sigue sin estar disponible.")


def resolve_skill_destination(client: str, scope: str, skill_dir: str | None, project_root: Path) -> Path:
    if skill_dir:
        return Path(skill_dir).expanduser().resolve()

    if scope == "project":
        return project_root / ".agents"

    home_agents = Path.home() / ".agents"

    client_destinations = {
        "generic": home_agents,
        "opencode": home_agents,
        "codex": home_agents,
    }

    return client_destinations.get(client, home_agents)


def ensure_skill_parent(destination_root: Path, client: str, scope: str, auto_yes: bool) -> None:
    if destination_root.exists():
        return

    if destination_root.name == ".agents":
        explanation = (
            f"La carpeta {destination_root} no existe. Se usa como ubicación genérica para skills/agentes "
            f"compartidos entre clientes compatibles como {client}."
        )
        log(explanation)
        if not auto_yes and not confirm("¿Querés crearla ahora?"):
            fail("Instalación de skill cancelada porque ~/.agents no existe.")

    destination_root.mkdir(parents=True, exist_ok=True)


def install_skill(skill_repo_root: Path, destination_root: Path) -> Path:
    skill_target = destination_root / "project-memory-bridge"
    skill_target.mkdir(parents=True, exist_ok=True)

    shutil.copy2(skill_repo_root / "SKILL.md", skill_target / "SKILL.md")

    for folder_name in ("assets", "references"):
        src = skill_repo_root / folder_name
        dst = skill_target / folder_name
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

    readme_src = skill_repo_root / "README.md"
    if readme_src.exists():
        shutil.copy2(readme_src, skill_target / "README.md")

    for folder_name in ("docs", "benchmarks"):
        src = skill_repo_root / folder_name
        if not src.exists():
            continue
        dst = skill_target / folder_name
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

    benchmark_src = skill_repo_root / "scripts" / "benchmark_memory_savings.py"
    benchmark_dst_dir = skill_target / "scripts"
    benchmark_dst_dir.mkdir(parents=True, exist_ok=True)
    if benchmark_src.exists():
        shutil.copy2(benchmark_src, benchmark_dst_dir / "benchmark_memory_savings.py")

    return skill_target


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bootstrap Project Memory Bridge")
    parser.add_argument("--project-root", default=os.getcwd())
    parser.add_argument("--project-name")
    parser.add_argument("--vault-root", default="~/Obsidian/GentleAI-Vault")
    parser.add_argument("--project-dir")
    parser.add_argument("--primary-agent", default="opencode")
    parser.add_argument("--graphify-output-dir", default="graphify-out")
    parser.add_argument("--install-gentle-ai", action="store_true")
    parser.add_argument("--install-graphify", action="store_true")
    parser.add_argument("--install-skill", action="store_true")
    parser.add_argument("--client", default="generic", choices=["generic", "opencode", "codex"])
    parser.add_argument("--scope", default="global", choices=["global", "project"])
    parser.add_argument("--skill-dir")
    parser.add_argument("--skip-graphify-update", action="store_true")
    parser.add_argument("--disable-obsidian", action="store_true")
    parser.add_argument("--disable-graphify", action="store_true")
    parser.add_argument("--yes", action="store_true")
    return parser.parse_args()


def main() -> None:
    ensure_python_version()
    args = parse_args()

    project_root = Path(args.project_root).expanduser().resolve()
    skill_repo_root = Path(__file__).resolve().parent.parent
    if not project_root.is_dir():
        fail(f"Project root no existe: {project_root}")

    project_name = args.project_name or project_root.name
    vault_root = Path(args.vault_root).expanduser()
    project_dir = Path(args.project_dir).expanduser() if args.project_dir else vault_root / "01_Projects" / project_name

    obsidian_enabled = not args.disable_obsidian
    graphify_enabled = not args.disable_graphify
    run_graphify_update = not args.skip_graphify_update

    atl_dir = project_root / ".atl"
    config_path = atl_dir / "memory-config.json"
    graphify_output_path = project_root / args.graphify_output_dir
    last_run_note = project_dir / "02_Graphify" / "last-run.md"
    skill_install_path: Path | None = None

    log("Step 1: ensuring Gentle-AI dependency")
    ensure_gentle_ai(install_if_missing=args.install_gentle_ai, auto_yes=args.yes)

    log("Step 2: creating .atl foundation")
    atl_dir.mkdir(parents=True, exist_ok=True)

    log("Step 3: ensuring Graphify runtime prerequisites")
    graphify_available = False
    if graphify_enabled:
        graphify_available = ensure_graphify(install_if_missing=args.install_graphify)
    else:
        log("Graphify deshabilitado por flag")

    log("Step 4: writing memory-config.json")
    config = {
        "project": {
            "name": project_name,
            "root": str(project_root),
            "managed_by": "gentle-ai",
            "primary_agent": args.primary_agent,
            "platform": platform.system().lower(),
        },
        "memory": {
            "engram": {
                "enabled": True,
                "pointer_mode": "compact",
            },
            "obsidian": {
                "enabled": obsidian_enabled,
                "vault_root": str(vault_root),
                "project_dir": str(project_dir),
            },
            "graphify": {
                "enabled": graphify_enabled,
                "available": graphify_available,
                "local_output_dir": args.graphify_output_dir,
                "install_if_missing": args.install_graphify,
                "force_graphify_on_init": run_graphify_update,
            },
            "compact": {
                "enabled": True,
                "default_strategy": "compact-first",
                "scenario_default": "focused-task",
                "max_tokens_per_artifact": 400,
                "max_artifacts_per_request": 3,
                "auto_refresh_days": 7,
                "scenarios": {
                    "focused-task": {
                        "preferred_sources": ["engram", "obsidian_compact", "raw_code"],
                        "allow_graph_report": False,
                        "target_token_budget": 1200,
                    },
                    "cross-module": {
                        "preferred_sources": ["engram", "obsidian_compact", "graph_report", "raw_code"],
                        "allow_graph_report": True,
                        "target_token_budget": 2600,
                    },
                    "architecture-review": {
                        "preferred_sources": ["engram", "obsidian_compact", "graph_report"],
                        "allow_graph_report": True,
                        "target_token_budget": 3200,
                    },
                    "repo-onboarding": {
                        "preferred_sources": ["engram", "obsidian_compact", "graph_report"],
                        "allow_graph_report": True,
                        "target_token_budget": 3200,
                    },
                },
            },
        },
    }
    config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")

    if obsidian_enabled:
        log("Step 5: creating Obsidian directories and seed notes from config")
        for path in [
            project_dir,
            project_dir / "01_Architecture",
            project_dir / "02_Graphify",
            project_dir / "10_Scenarios",
            project_dir / "20_Domains",
            project_dir / "30_Cross_Module",
            project_dir / "04_Decisions",
            project_dir / "05_Troubleshooting",
        ]:
            path.mkdir(parents=True, exist_ok=True)

        notes = {
            project_dir / "00_Project_Index.md": "Project Index",
            project_dir / "01_Current_State.md": "Current State",
            project_dir / "02_Project_Map.md": "Project Map",
            project_dir / "03_Architecture_Summary.md": "Architecture Summary",
            project_dir / "04_Conventions.md": "Conventions",
            project_dir / "05_Active_Work.md": "Active Work",
            project_dir / "10_Scenarios" / "focused-task-example.md": "Focused Task Example",
            project_dir / "20_Domains" / "domain-example.md": "Domain Example",
            project_dir / "30_Cross_Module" / "relation-example.md": "Cross Module Relation Example",
            project_dir / "01_Architecture" / "Architecture_Index.md": "Architecture Index",
            project_dir / "04_Decisions" / "Decisions_Index.md": "Decisions Index",
            project_dir / "05_Troubleshooting" / "Troubleshooting_Index.md": "Troubleshooting Index",
        }
        for path, title in notes.items():
            write_text_if_missing(path, build_note(title, project_name, project_root))

        write_text_if_missing(
            last_run_note,
            f"""---
project: {project_name}
source: project-memory-bridge
---

# Graphify Last Run

Status: pending

Graphify has not run yet, or no successful run has been recorded.
""",
        )
    else:
        log("Step 5: skipping Obsidian setup because it was disabled")

    log("Step 6: refreshing graph if available and enabled")
    if graphify_enabled and graphify_available:
        graphify_output_path.mkdir(parents=True, exist_ok=True)
        if run_graphify_update:
            run(["graphify", "update", "."], cwd=project_root)
            if obsidian_enabled:
                last_run_note.write_text(
                    f"""---
project: {project_name}
source: project-memory-bridge
---

# Graphify Last Run

Status: success

Graphify update completed successfully during bootstrap.
""",
                    encoding="utf-8",
                )
        else:
            log("Graphify update omitido por flag")
    elif graphify_enabled:
        log("Graphify sigue no disponible; config escrito con available=false")

    if args.install_skill:
        log("Step 7: installing skill files for agent runtime")
        destination_root = resolve_skill_destination(args.client, args.scope, args.skill_dir, project_root)
        ensure_skill_parent(destination_root, args.client, args.scope, args.yes)
        skill_install_path = install_skill(skill_repo_root, destination_root)
        log(f"Skill instalada en: {skill_install_path}")

    log(f"Config: {config_path}")
    if obsidian_enabled:
        log(f"Obsidian project dir: {project_dir}")
    if graphify_enabled:
        log(f"Graphify output dir: {graphify_output_path}")
    if skill_install_path:
        log(f"Skill runtime path: {skill_install_path}")
    log("Done")


if __name__ == "__main__":
    main()
