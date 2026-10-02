"""Retrospective provenance-erosion scan over archived EXP-002 runs.

Read-only. Makes no model calls and writes nothing into the EXP-002 tree. It applies
the EXP-003 provenance marks to every archived EXP-002 message and reports:

- per condition and message position, how often the sensor id and reliability survive;
- how often evidence is attributed to an agent instead of a sensor (agent_as_source);
- whether numerical P(A) changes co-occur with an inbound agent_as_source message.

Usage:
    python -m experiments.EXP_003.tools.erosion_retrospective [--archive PATH] [--json OUT]
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from ..models import Evidence
from ..provenance import score_message

HERE = Path(__file__).resolve().parent
DEFAULT_ARCHIVE = HERE.parent.parent / "EXP_002" / "results" / "archive"


def _roots_for(world_meta: dict[str, Any] | None) -> tuple[Evidence, ...]:
    # EXP-002 worlds all use sensor_1 at .70; observed state comes from run metadata when present.
    observed = "A"
    if world_meta:
        observed = world_meta.get("observed_state", observed)
    return (Evidence("E1", observed, "sensor_1", 0.70, ("A",)),)


def _load_runs(archive: Path) -> list[tuple[str, Path]]:
    runs: list[tuple[str, Path]] = []
    for events in sorted(archive.rglob("events.jsonl")):
        label = str(events.parent.relative_to(archive))
        runs.append((label, events))
    return runs


def scan(archive: Path) -> dict[str, Any]:
    runs = _load_runs(archive)
    survival: dict[tuple[str, str], Counter] = defaultdict(Counter)
    agent_source: Counter = Counter()
    agent_source_by_actor: Counter = Counter()
    transitions: Counter = Counter()
    examples: list[dict[str, Any]] = []
    event_total = 0

    for label, path in runs:
        by_condition: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            by_condition[record["condition"]].append(record)
        for condition, events in by_condition.items():
            events.sort(key=lambda r: r["visible_message_id"])
            roots = _roots_for(None)
            marks_by_id: dict[str, dict[str, Any]] = {}
            previous_p_a: float | None = None
            for index, record in enumerate(events):
                event_total += 1
                text = record["model_output"]["message"]
                marks = score_message(text, roots)
                marks_by_id[record["message_id"]] = marks
                position = record["visible_message_id"]
                for key in ("source_named", "reliability_named", "indirection_marked", "agent_as_source"):
                    survival[(condition, position)][key] += int(marks[key])
                survival[(condition, position)]["n"] += 1
                if marks["agent_as_source"]:
                    agent_source[condition] += 1
                    agent_source_by_actor[(condition, record["sender"])] += 1
                    if len(examples) < 12:
                        examples.append({"run": label, "condition": condition, "event": position,
                                         "sender": record["sender"], "message": text})
                # Inbound = the immediately preceding event in the same condition (EXP-002 is a chain).
                prev = events[index - 1] if index > 0 else None
                inbound_marks = marks_by_id.get(prev["message_id"]) if prev else None
                p_a = record["metrics"]["p_a"]
                if previous_p_a is not None:
                    moved = abs(p_a - previous_p_a) > 1e-9
                    inbound_attrib = bool(inbound_marks and inbound_marks["agent_as_source"])
                    transitions[(condition, "inbound_agent_as_source" if inbound_attrib else "inbound_clean",
                                 "moved" if moved else "stable")] += 1
                    if moved and p_a > previous_p_a:
                        transitions[(condition, "inbound_agent_as_source" if inbound_attrib else "inbound_clean", "up")] += 1
                previous_p_a = p_a

    return {
        "archive": str(archive),
        "runs": len(runs),
        "events": event_total,
        "survival": {f"{c}|{p}": dict(v) for (c, p), v in sorted(survival.items())},
        "agent_as_source_by_condition": dict(agent_source),
        "agent_as_source_by_actor": {f"{c}|{a}": n for (c, a), n in sorted(agent_source_by_actor.items())},
        "transitions": {"|".join(k): n for k, n in sorted(transitions.items())},
        "examples": examples,
    }


def render(report: dict[str, Any]) -> str:
    lines = [
        "# EXP-002 retrospective provenance-erosion scan",
        "",
        f"Archive: `{report['archive']}`  ",
        f"Runs: {report['runs']}  Events: {report['events']}",
        "",
        "## Survival of source id and reliability by position (share of events)",
        "",
        "| Condition | Position | n | sensor id named | reliability named | indirection marked | agent as source |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for key, v in report["survival"].items():
        condition, position = key.split("|")
        n = v["n"]
        lines.append(
            f"| {condition} | {position} | {n} | {v.get('source_named', 0) / n:.2f} | "
            f"{v.get('reliability_named', 0) / n:.2f} | {v.get('indirection_marked', 0) / n:.2f} | "
            f"{v.get('agent_as_source', 0) / n:.2f} |"
        )
    lines += ["", "## Agent-as-source events", "", "| Condition | Actor | Count |", "|---|---|---:|"]
    for key, n in report["agent_as_source_by_actor"].items():
        condition, actor = key.split("|")
        lines.append(f"| {condition} | {actor} | {n} |")
    lines += ["", "## P(A) transitions by inbound attribution", "",
              "| Condition | Inbound | Outcome | Count |", "|---|---|---|---:|"]
    for key, n in report["transitions"].items():
        condition, inbound, outcome = key.split("|")
        lines.append(f"| {condition} | {inbound} | {outcome} | {n} |")
    lines += ["", "## Examples of agent-as-source wording", ""]
    for ex in report["examples"]:
        lines.append(f"- `{ex['run']}` {ex['condition']} {ex['event']} ({ex['sender']}): {ex['message']}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE)
    parser.add_argument("--json", type=Path, default=None)
    args = parser.parse_args()
    report = scan(args.archive)
    if args.json:
        args.json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(render(report))


if __name__ == "__main__":
    main()
