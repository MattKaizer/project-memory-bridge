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


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bootstrap Project Memory Bridge")
    parser.add_argument("--project-root", default=os.getcwd())
    parser.add_argument("--project-name")
    parser.add_argument("--vault-root", default="~/Obsidian/GentleAI-Vault")
    parser.add_argument("--project-dir")
    parser.add_argument("--primary-agent", default="opencode")
    parser.add_argument("--graphify-output-dir", default="graphify-out")
    parser.add_argument("--install-graphify", action="store_true")
    parser.add_argument("--skip-graphify-update", action="store_true")
    parser.add_argument("--disable-obsidian", action="store_true")
    parser.add_argument("--disable-graphify", action="store_true")
    return parser.parse_args()


def main() -> None:
    ensure_python_version()
    args = parse_args()

    project_root = Path(args.project_root).expanduser().resolve()
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

    log("Step 1/6: verifying Gentle-AI-oriented target repository")

    log("Step 2/6: creating .atl foundation")
    atl_dir.mkdir(parents=True, exist_ok=True)

    log("Step 3/6: ensuring Graphify runtime prerequisites")
    graphify_available = False
    if graphify_enabled:
        graphify_available = ensure_graphify(install_if_missing=args.install_graphify)
    else:
        log("Graphify deshabilitado por flag")

    log("Step 4/6: writing memory-config.json")
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
        },
    }
    config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")

    if obsidian_enabled:
        log("Step 5/6: creating Obsidian directories and seed notes from config")
        for path in [
            project_dir,
            project_dir / "01_Architecture",
            project_dir / "02_Graphify",
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
        log("Step 5/6: skipping Obsidian setup because it was disabled")

    log("Step 6/6: refreshing graph if available and enabled")
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

    log(f"Config: {config_path}")
    if obsidian_enabled:
        log(f"Obsidian project dir: {project_dir}")
    if graphify_enabled:
        log(f"Graphify output dir: {graphify_output_path}")
    log("Done")


if __name__ == "__main__":
    main()
