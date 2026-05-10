#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


def try_tokenizer():
    try:
        import tiktoken  # type: ignore

        return tiktoken.get_encoding("cl100k_base")
    except Exception:
        return None


ENCODER = try_tokenizer()


@dataclass
class FileMeasure:
    path: str
    bytes_count: int
    line_count: int
    token_count: int


def estimate_tokens(text: str) -> int:
    if ENCODER is not None:
        return len(ENCODER.encode(text))
    return max(1, round(len(text) / 4))


def resolve_patterns(repo_root: Path, patterns: Iterable[str]) -> list[Path]:
    paths: set[Path] = set()
    for pattern in patterns:
        matches = list(repo_root.glob(pattern))
        if not matches:
            print(f"[benchmark] warning: pattern matched nothing: {pattern}")
        for match in matches:
            if match.is_file():
                paths.add(match.resolve())
    return sorted(paths)


def measure_files(paths: Iterable[Path], repo_root: Path) -> list[FileMeasure]:
    result: list[FileMeasure] = []
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="ignore")
        result.append(
            FileMeasure(
                path=str(path.relative_to(repo_root)),
                bytes_count=len(text.encode("utf-8")),
                line_count=text.count("\n") + (1 if text and not text.endswith("\n") else 0),
                token_count=estimate_tokens(text),
            )
        )
    return result


def summarize(items: list[FileMeasure]) -> dict[str, int]:
    return {
        "files": len(items),
        "bytes": sum(item.bytes_count for item in items),
        "lines": sum(item.line_count for item in items),
        "tokens": sum(item.token_count for item in items),
    }


def print_summary(name: str, summary: dict[str, int]) -> None:
    print(
        f"{name}: files={summary['files']} lines={summary['lines']} bytes={summary['bytes']} tokens={summary['tokens']}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark Project Memory Bridge token savings")
    parser.add_argument("--repo-root", required=True, help="Repository to benchmark")
    parser.add_argument("--config", required=True, help="JSON benchmark config")
    parser.add_argument("--details", action="store_true", help="Print per-file details")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).expanduser().resolve()
    config_path = Path(args.config).expanduser().resolve()

    config = json.loads(config_path.read_text(encoding="utf-8"))
    scenarios = config.get("scenarios", [])
    if not scenarios:
        raise SystemExit("[benchmark] ERROR: config has no scenarios")

    print(f"[benchmark] repo: {repo_root}")
    print(f"[benchmark] tokenizer: {'cl100k_base' if ENCODER else 'char/4 estimate'}")

    for scenario in scenarios:
        name = scenario["name"]
        baseline_patterns = scenario.get("baseline", [])
        memory_patterns = scenario.get("memory_first", [])

        baseline_files = measure_files(resolve_patterns(repo_root, baseline_patterns), repo_root)
        memory_files = measure_files(resolve_patterns(repo_root, memory_patterns), repo_root)

        baseline = summarize(baseline_files)
        memory = summarize(memory_files)

        saved = baseline["tokens"] - memory["tokens"]
        percent = 0.0 if baseline["tokens"] == 0 else (saved / baseline["tokens"]) * 100

        print(f"\n## Scenario: {name}")
        print_summary("baseline", baseline)
        print_summary("memory_first", memory)
        print(f"delta_tokens={saved} savings_percent={percent:.2f}")

        if args.details:
            print("\n### baseline files")
            for item in baseline_files:
                print(f"- {item.path}: {item.token_count} tokens")
            print("\n### memory-first files")
            for item in memory_files:
                print(f"- {item.path}: {item.token_count} tokens")


if __name__ == "__main__":
    main()
