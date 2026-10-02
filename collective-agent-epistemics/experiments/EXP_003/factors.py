"""Factor ledger: what differs between any two runs, gates or experiments.

Every run's metadata is reduced to one row of canonical factors. Comparing two rows
lists exactly which factors changed, so a difference in outcome can be attributed
(or explicitly not attributed) to a named change. EXP-002 archives are mapped onto
the same factors so the whole project sits on one ledger.

Usage:
    python -m experiments.EXP_003.factors diff <run_dir_or_metadata_a> <run_dir_or_metadata_b>
    python -m experiments.EXP_003.factors ledger <dir> [<dir> ...] [--json OUT]
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

FACTORS = (
    "experiment",
    "gate",
    "set",
    "topology",
    "regrounding",
    "root_mode",
    "probe",
    "provider",
    "model",
    "run_class",
    "fallbacks",
    "reasoning_effort",
    "rounds",
    "sensor_reliability",
    "execution_policy",
    "prompt_version",
    "schema_version",
    "conditions",
)

EXP002_RING_EDGES = [["A", "B"], ["B", "C"], ["C", "A"], ["A", "B"]]


def _load(path: Path) -> tuple[dict[str, Any], dict[str, Any] | None]:
    path = Path(path)
    if path.is_dir():
        run_meta = json.loads((path / "run_metadata.json").read_text(encoding="utf-8"))
        archive_path = path / "archive_metadata.json"
        archive = json.loads(archive_path.read_text(encoding="utf-8")) if archive_path.exists() else None
        return run_meta, archive
    run_meta = json.loads(path.read_text(encoding="utf-8"))
    archive_path = path.parent / "archive_metadata.json"
    archive = json.loads(archive_path.read_text(encoding="utf-8")) if archive_path.exists() else None
    return run_meta, archive


def factors_from_metadata(run_meta: dict[str, Any], archive: dict[str, Any] | None = None,
                          source: str | None = None) -> dict[str, Any]:
    experiment = run_meta.get("experiment")
    row: dict[str, Any] = {"source": source, "experiment": experiment}
    if archive:
        row["gate"] = archive.get("gate")
        row["set"] = archive.get("set")
    else:
        row["gate"] = run_meta.get("gate")
        row["set"] = run_meta.get("set")

    if experiment == "EXP-002":
        edges = run_meta.get("topology")
        row["topology"] = "ring" if edges == EXP002_RING_EDGES else "custom"
        row["regrounding"] = True
        row["root_mode"] = "single"
        row["probe"] = False
        row["sensor_reliability"] = 0.70
    else:
        row["topology"] = run_meta.get("topology_name")
        row["regrounding"] = run_meta.get("regrounding")
        row["root_mode"] = run_meta.get("root_mode")
        row["probe"] = run_meta.get("probe")
        row["sensor_reliability"] = run_meta.get("sensor_reliability")

    row["provider"] = run_meta.get("provider")
    row["model"] = run_meta.get("requested_model")
    row["run_class"] = run_meta.get("run_class")
    row["fallbacks"] = bool(run_meta.get("fallbacks", False))
    row["reasoning_effort"] = run_meta.get("reasoning_effort")
    row["rounds"] = run_meta.get("rounds")
    row["execution_policy"] = run_meta.get("execution_policy")
    row["prompt_version"] = run_meta.get("prompt_version")
    row["schema_version"] = run_meta.get("schema_version")
    row["conditions"] = ",".join(run_meta.get("conditions", []))
    row["seed"] = run_meta.get("seed")
    row["config_fingerprint"] = run_meta.get("config_fingerprint")
    return row


def _gate_and_set_from_path(path: Path) -> tuple[str | None, str | None]:
    """Fallback for archives without archive_metadata.json (EXP-002 pilots and replication sets)."""
    parts = [p.lower() for p in path.resolve().parts]
    for index, part in enumerate(parts):
        if part.startswith("gate_") and index + 1 < len(parts):
            return part.replace("gate_", "").upper(), parts[index + 1]
        if part == "replication_sets" and index + 1 < len(parts):
            return "2A", parts[index + 1]
        if part == "pilots" and index + 1 < len(parts):
            return "pilot", parts[index + 1]
    return None, None


def factors_for(path: Path) -> dict[str, Any]:
    path = Path(path)
    run_meta, archive = _load(path)
    row = factors_from_metadata(run_meta, archive, source=str(path))
    if row.get("gate") is None and row.get("set") is None:
        row["gate"], row["set"] = _gate_and_set_from_path(path)
    return row


def diff_factors(a: dict[str, Any], b: dict[str, Any]) -> dict[str, tuple[Any, Any]]:
    """Factors whose values differ. Seed and fingerprint are reported separately."""
    return {f: (a.get(f), b.get(f)) for f in FACTORS if a.get(f) != b.get(f)}


def ledger(paths: list[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for root in paths:
        root = Path(root)
        metas = [root] if root.is_file() or (root / "run_metadata.json").exists() else sorted(root.rglob("run_metadata.json"))
        for meta in metas:
            try:
                rows.append(factors_for(meta if meta.is_file() else meta))
            except (OSError, ValueError, KeyError) as exc:
                rows.append({"source": str(meta), "error": type(exc).__name__})
    return rows


def render_diff(a: dict[str, Any], b: dict[str, Any]) -> str:
    changed = diff_factors(a, b)
    lines = [f"A: {a.get('source')}", f"B: {b.get('source')}", ""]
    if not changed:
        lines.append("No factor differs. (Seeds: A={} B={})".format(a.get("seed"), b.get("seed")))
    else:
        lines += ["| Factor | A | B |", "|---|---|---|"]
        for f, (va, vb) in changed.items():
            lines.append(f"| {f} | {va} | {vb} |")
        lines.append("")
        lines.append(f"{len(changed)} factor(s) differ. Seeds: A={a.get('seed')} B={b.get('seed')}.")
    same_seed = a.get("seed") == b.get("seed")
    lines.append("Same world seed: " + ("yes" if same_seed else "no"))
    return "\n".join(lines)


def render_ledger(rows: list[dict[str, Any]]) -> str:
    cols = ("experiment", "gate", "set", "topology", "regrounding", "root_mode", "probe",
            "provider", "model", "run_class", "fallbacks", "reasoning_effort", "rounds", "seed")
    lines = ["| " + " | ".join(cols) + " | source |", "|" + "---|" * (len(cols) + 1)]
    for row in rows:
        if "error" in row:
            lines.append(f"| {'—'} |" * len(cols) + f" {row['source']} ({row['error']}) |")
            continue
        lines.append("| " + " | ".join(str(row.get(c)) for c in cols) + f" | {row.get('source')} |")
    # Summary of distinct values per factor across the ledger.
    lines += ["", "## Distinct values per factor", "", "| Factor | Distinct values |", "|---|---|"]
    for f in FACTORS:
        values = sorted({str(r.get(f)) for r in rows if "error" not in r})
        lines.append(f"| {f} | {', '.join(values)} |")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    d = sub.add_parser("diff", help="list factors that differ between two runs")
    d.add_argument("a", type=Path)
    d.add_argument("b", type=Path)
    l = sub.add_parser("ledger", help="one row per run under the given directories")
    l.add_argument("paths", type=Path, nargs="+")
    l.add_argument("--json", type=Path, default=None)
    args = parser.parse_args()
    if args.command == "diff":
        print(render_diff(factors_for(args.a), factors_for(args.b)))
    else:
        rows = ledger(args.paths)
        if args.json:
            args.json.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
        print(render_ledger(rows))


if __name__ == "__main__":
    main()
