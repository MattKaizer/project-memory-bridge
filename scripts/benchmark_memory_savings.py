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


def infer_escalation_tier(scenario: dict) -> str:
    full_graph_patterns = resolve_scenario_patterns(scenario, "memory_first_full_graph", "memory_first")
    if scenario.get("expected_tier") == "graph_required" and any("GRAPH_REPORT" in pattern for pattern in full_graph_patterns):
        return "graph_required"
    compact_patterns = resolve_scenario_patterns(scenario, "memory_first_compact")
    if compact_patterns:
        return "raw_code_required"
    return "compact_ok"


def percent_savings(reference: int, candidate: int) -> float:
    if reference == 0:
        return 0.0
    return ((reference - candidate) / reference) * 100


def resolve_scenario_patterns(scenario: dict, key: str, legacy_fallback: str | None = None) -> list[str]:
    values = scenario.get(key)
    if values is None and legacy_fallback is not None:
        values = scenario.get(legacy_fallback, [])
    return list(values or [])


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
        baseline_patterns = resolve_scenario_patterns(scenario, "baseline_raw_rediscovery", "baseline")
        first_load_patterns = resolve_scenario_patterns(scenario, "compact_first_load")
        compact_patterns = resolve_scenario_patterns(scenario, "memory_first_compact")
        full_graph_patterns = resolve_scenario_patterns(scenario, "memory_first_full_graph", "memory_first")

        if not baseline_patterns:
            raise SystemExit(f"[benchmark] ERROR: scenario '{name}' has no baseline_raw_rediscovery patterns")
        if not first_load_patterns:
            raise SystemExit(f"[benchmark] ERROR: scenario '{name}' has no compact_first_load patterns")
        if not compact_patterns:
            raise SystemExit(f"[benchmark] ERROR: scenario '{name}' has no memory_first_compact patterns")
        if not full_graph_patterns:
            raise SystemExit(f"[benchmark] ERROR: scenario '{name}' has no memory_first_full_graph patterns")

        first_load_files = measure_files(resolve_patterns(repo_root, first_load_patterns), repo_root)
        baseline_files = measure_files(resolve_patterns(repo_root, baseline_patterns), repo_root)
        compact_files = measure_files(resolve_patterns(repo_root, compact_patterns), repo_root)
        full_graph_files = measure_files(resolve_patterns(repo_root, full_graph_patterns), repo_root)

        first_load = summarize(first_load_files)
        baseline = summarize(baseline_files)
        compact = summarize(compact_files)
        full_graph = summarize(full_graph_files)

        first_load_saved = baseline["tokens"] - first_load["tokens"]
        compact_saved = baseline["tokens"] - compact["tokens"]
        full_graph_saved = baseline["tokens"] - full_graph["tokens"]
        first_load_percent = percent_savings(baseline["tokens"], first_load["tokens"])
        compact_percent = percent_savings(baseline["tokens"], compact["tokens"])
        full_graph_percent = percent_savings(baseline["tokens"], full_graph["tokens"])
        full_graph_overhead = full_graph["tokens"] - compact["tokens"]
        overhead_percent = percent_savings(full_graph["tokens"], compact["tokens"])
        budgets = scenario.get("budgets", {})
        expected_tier = scenario.get("expected_tier", "raw_code_required")
        observed_tier = infer_escalation_tier(scenario)

        print(f"\n## Scenario: {name}")
        if scenario.get("intent"):
            print(f"intent={scenario['intent']}")
        print_summary("compact_first_load", first_load)
        print_summary("baseline_raw_rediscovery", baseline)
        print_summary("memory_first_compact", compact)
        print_summary("memory_first_full_graph", full_graph)
        print(f"first_load_delta_tokens={first_load_saved} first_load_savings_percent={first_load_percent:.2f}")
        print(f"compact_delta_tokens={compact_saved} compact_savings_percent={compact_percent:.2f}")
        print(f"full_graph_delta_tokens={full_graph_saved} full_graph_savings_percent={full_graph_percent:.2f}")
        print(
            f"full_graph_over_compact_tokens={full_graph_overhead} compact_advantage_vs_full_graph_percent={overhead_percent:.2f}"
        )
        print(
            f"escalation_tier_check={'PASS' if observed_tier == expected_tier else 'FAIL'} expected={expected_tier} observed={observed_tier}"
        )

        first_load_budget = budgets.get("compact_first_load_max_tokens")
        compact_budget = budgets.get("compact_max_tokens")
        full_graph_budget = budgets.get("full_graph_max_tokens")
        if first_load_budget is not None:
            print(f"compact_first_load_budget_check={'PASS' if first_load['tokens'] <= first_load_budget else 'FAIL'} limit={first_load_budget}")
        if compact_budget is not None:
            print(f"compact_budget_check={'PASS' if compact['tokens'] <= compact_budget else 'FAIL'} limit={compact_budget}")
        if full_graph_budget is not None:
            print(
                f"full_graph_budget_check={'PASS' if full_graph['tokens'] <= full_graph_budget else 'FAIL'} limit={full_graph_budget}"
            )

        if args.details:
            print("\n### baseline files")
            for item in baseline_files:
                print(f"- {item.path}: {item.token_count} tokens")
            print("\n### compact first-load files")
            for item in first_load_files:
                print(f"- {item.path}: {item.token_count} tokens")
            print("\n### compact files")
            for item in compact_files:
                print(f"- {item.path}: {item.token_count} tokens")
            print("\n### full-graph files")
            for item in full_graph_files:
                print(f"- {item.path}: {item.token_count} tokens")


if __name__ == "__main__":
    main()
