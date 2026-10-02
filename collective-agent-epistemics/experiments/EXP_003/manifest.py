from __future__ import annotations

import argparse
import json
from hashlib import sha256
from pathlib import Path
from typing import Any

from .topology import get_topology
from .world_generator import WorldGenerator, alignment, world_cell

MAX_SEED = 2_147_483_646


def candidate_seed(anchor: str, label: str, ordinal: int, nonce: int = 0) -> int:
    """Same derivation as Gate 2B: sha256(anchor|label|ordinal|nonce) folded into [1, MAX_SEED]."""
    payload = f"{anchor}|{label}|{ordinal}|{nonce}".encode("utf-8")
    digest = sha256(payload).digest()
    value = int.from_bytes(digest[:8], "big")
    return 1 + (value % MAX_SEED)


def order_key(anchor: str, set_id: str, seed: int) -> str:
    return sha256(f"{anchor}|ORDER|{set_id}|{seed}".encode("utf-8")).hexdigest()


def select_unfiltered(
    anchor: str, label: str, count: int, excluded: set[int]
) -> list[dict[str, Any]]:
    """Unfiltered selection: accept the first non-excluded, non-duplicate candidate per ordinal."""
    accepted: list[dict[str, Any]] = []
    seen: set[int] = set()
    for ordinal in range(1, count + 1):
        nonce = 0
        while True:
            seed = candidate_seed(anchor, label, ordinal, nonce)
            if seed in excluded or seed in seen:
                nonce += 1
                continue
            seen.add(seed)
            accepted.append({"ordinal": ordinal, "nonce": nonce, "seed": seed})
            break
    return accepted


def select_stratified(
    anchor: str,
    label: str,
    per_cell: int,
    cells: list[str],
    excluded: set[int],
    topology: str,
    root_mode: str,
    reliability: float,
    max_scan: int = 10_000,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Stratified selection by truth/observation cell, as in Gate 2B's Stress Set.

    Only truth and observed states are used for classification. Returns the accepted
    worlds and the full scan (including rejections and reasons).
    """
    generator = WorldGenerator(0, topology, root_mode, reliability)
    counts = {cell: 0 for cell in cells}
    accepted: list[dict[str, Any]] = []
    scan: list[dict[str, Any]] = []
    evaluated: set[int] = set()
    for scan_index in range(1, max_scan + 1):
        seed = candidate_seed(anchor, label, scan_index, 0)
        row: dict[str, Any] = {"scan_index": scan_index, "seed": seed}
        if seed in excluded:
            row.update(accepted=False, reason="excluded")
            scan.append(row)
            continue
        if seed in evaluated:
            row.update(accepted=False, reason="duplicate")
            scan.append(row)
            continue
        evaluated.add(seed)
        world = generator.generate(seed=seed)
        cell = world_cell(world)
        row.update(truth=world.truth, cell=cell)
        if cell not in counts:
            row.update(accepted=False, reason="cell_not_targeted")
        elif counts[cell] >= per_cell:
            row.update(accepted=False, reason="cell_full")
        else:
            counts[cell] += 1
            row.update(accepted=True, reason=None)
            accepted.append({"scan_index": scan_index, "seed": seed})
        scan.append(row)
        if all(v >= per_cell for v in counts.values()):
            break
    else:
        raise RuntimeError("stratified scan did not fill every cell within max_scan")
    return accepted, scan


def describe_world(
    seed: int, set_id: str, topology: str, root_mode: str, reliability: float, anchor: str
) -> dict[str, Any]:
    world = WorldGenerator(seed, topology, root_mode, reliability).generate(seed=seed)
    return {
        "canonical_id": f"E3_{set_id}_seed_{seed}",
        "seed": seed,
        "internal_world_id": world.world_id,
        "truth": world.truth,
        "observed": [e.observed_state for e in world.evidence],
        "cell": world_cell(world),
        "alignment": alignment(world),
        "evidence": [
            {"evidence_id": e.evidence_id, "source": e.source, "reliability": e.reliability,
             "observed_state": e.observed_state, "assigned_to": list(e.assigned_to)}
            for e in world.evidence
        ],
        "order_key": order_key(anchor, set_id, seed),
    }


def build_manifest(
    anchor: str,
    set_id: str,
    topology: str,
    root_mode: str,
    count: int,
    per_cell: int | None,
    cells: list[str] | None,
    excluded: set[int],
    reliability: float = 0.70,
    seeds_from: dict[str, Any] | None = None,
) -> dict[str, Any]:
    get_topology(topology)  # validate
    if seeds_from is not None:
        # Paired set: reuse another set's seeds and execution order verbatim so that each
        # world has one execution per arm and the arms differ in topology/root mode only.
        worlds = [
            describe_world(w["seed"], set_id, topology, root_mode, reliability, anchor)
            for w in sorted(seeds_from["worlds"], key=lambda w: w["execution_order"])
        ]
        for index, world in enumerate(worlds, start=1):
            world["execution_order"] = index
            world["order_key"] = f"inherited:{seeds_from['set_id']}:{index:03d}"
        return {
            "experiment": "EXP-003",
            "set_id": set_id,
            "anchor": anchor,
            "topology": topology,
            "root_mode": root_mode,
            "sensor_reliability": reliability,
            "excluded_seeds": sorted(excluded),
            "selection": {"scheme": "inherited", "from_set_id": seeds_from["set_id"],
                          "from_anchor": seeds_from.get("anchor")},
            "worlds": worlds,
            "model_calls_made": 0,
        }
    if per_cell:
        if not cells:
            raise ValueError("stratified selection needs --cells")
        accepted, scan = select_stratified(
            anchor, set_id, per_cell, cells, excluded, topology, root_mode, reliability
        )
        selection = {"scheme": "stratified", "per_cell": per_cell, "cells": cells, "scan": scan}
    else:
        accepted = select_unfiltered(anchor, set_id, count, excluded)
        selection = {"scheme": "unfiltered", "count": count, "selection": accepted}
    worlds = [
        describe_world(row["seed"], set_id, topology, root_mode, reliability, anchor)
        for row in accepted
    ]
    worlds.sort(key=lambda w: w["order_key"])
    for index, world in enumerate(worlds, start=1):
        world["execution_order"] = index
    return {
        "experiment": "EXP-003",
        "set_id": set_id,
        "anchor": anchor,
        "topology": topology,
        "root_mode": root_mode,
        "sensor_reliability": reliability,
        "excluded_seeds": sorted(excluded),
        "selection": selection,
        "worlds": worlds,
        "model_calls_made": 0,
    }


def manifest_markdown(manifest: dict[str, Any]) -> str:
    lines = [
        f"# EXP-003 World Manifest: {manifest['set_id']}",
        "",
        "**Status:** WORLD MANIFEST FROZEN / NOT YET EXECUTED. Zero real-model calls were made to produce it.",
        "",
        f"- Anchor: `{manifest['anchor']}`",
        f"- Topology: `{manifest['topology']}`",
        f"- Root mode: `{manifest['root_mode']}`",
        f"- Sensor reliability: `{manifest['sensor_reliability']}`",
        f"- Selection scheme: `{manifest['selection']['scheme']}`",
        f"- Excluded seeds: `{manifest['excluded_seeds']}`",
        "",
        "| Order | Canonical ID | Seed | Truth | Observed | Cell | Alignment |",
        "|---:|---|---:|---|---|---|---|",
    ]
    for w in manifest["worlds"]:
        lines.append(
            f"| {w['execution_order']} | {w['canonical_id']} | {w['seed']} | {w['truth']} | "
            f"{'/'.join(w['observed'])} | {w['cell']} | {w['alignment']} |"
        )
    if manifest["selection"]["scheme"] == "inherited":
        lines += ["", f"Seeds and execution order inherited verbatim from `{manifest['selection']['from_set_id']}`."]
    if manifest["selection"]["scheme"] == "stratified":
        lines += ["", "## Selection scan", "", "| Scan | Seed | Cell | Accepted | Reason |", "|---:|---:|---|---|---|"]
        for row in manifest["selection"]["scan"]:
            lines.append(
                f"| {row['scan_index']} | {row['seed']} | {row.get('cell', '')} | "
                f"{'yes' if row['accepted'] else 'no'} | {row['reason'] or ''} |"
            )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Derive a prospective EXP-003 world manifest")
    parser.add_argument("--anchor", required=True, help="immutable derivation anchor string")
    parser.add_argument("--set-id", required=True, help="e.g. G3A_GEN001")
    parser.add_argument("--topology", default="diamond")
    parser.add_argument("--root-mode", choices=("single", "shared", "dual"), default="single")
    parser.add_argument("--count", type=int, default=12, help="unfiltered world count")
    parser.add_argument("--per-cell", type=int, default=None, help="stratified: worlds per cell")
    parser.add_argument("--cells", nargs="*", default=None, help="stratified: target cells, e.g. A/A B/B A/B B/A")
    parser.add_argument("--exclude", type=int, nargs="*", default=[], help="pre-inspected seeds to exclude")
    parser.add_argument("--reliability", type=float, default=0.70)
    parser.add_argument("--seeds-from", type=Path, default=None,
                        help="paired set: reuse this manifest's seeds and execution order")
    parser.add_argument("--out", type=Path, required=True, help="output path without extension")
    args = parser.parse_args()

    seeds_from = json.loads(args.seeds_from.read_text(encoding="utf-8")) if args.seeds_from else None
    manifest = build_manifest(
        args.anchor, args.set_id, args.topology, args.root_mode, args.count,
        args.per_cell, args.cells, set(args.exclude), args.reliability, seeds_from=seeds_from,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    # Append, never with_suffix: version strings like v0.1 contain a dot.
    json_path = Path(f"{args.out}.json")
    md_path = Path(f"{args.out}.md")
    json_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(manifest_markdown(manifest), encoding="utf-8")
    print(f"wrote {json_path} and {md_path}")


if __name__ == "__main__":
    main()
