from __future__ import annotations

import re
from typing import Any

from .models import Evidence

# Words that mark the content as relayed rather than directly observed.
INDIRECTION_PATTERN = re.compile(
    r"\b(relay(?:ed|s|ing)?|report(?:ed|s|ing)?(?!\s+reliability)|indirect(?:ly)?|via|"
    r"forward(?:ed|s|ing)?|pass(?:ed|es|ing)? (?:along|on)|second-?hand|hearsay|upstream|"
    r"downstream|chain|inference steps?|hops?|received from|from agent)\b",
    re.IGNORECASE,
)

# Broad: evidence is attributed through an agent at all ("Agent A reports Sensor 1 ...").
# This is ordinary relay language and is not by itself a provenance error.
AGENT_ATTRIBUTION_PATTERN = re.compile(
    r"\bAgent\s+[A-Z]\d?(?:'s|’s)?\s+(?:separately\s+|independently\s+|own\s+)?"
    r"(?:report(?:ed|s)?|relay(?:ed|s)?|evidence|observation|sensor|reading|data|source)\b",
    re.IGNORECASE,
)

# Strict: the agent is presented as the owner of the evidence ("Agent B's evidence",
# "B's separately reported evidence", "Agent C's observation"). This is the wording
# that preceded the one EXP-002 inflation event.
AGENT_POSSESSIVE_PATTERN = re.compile(
    r"\b(?:Agent\s+)?[A-Z]\d?(?:'s|’s)\s+(?:separately\s+|independently\s+|own\s+)?"
    r"(?:report(?:ed)?\s+)?(?:evidence|observation|sensor|reading|data|source)\b",
)

PRESERVATION_FIELDS = ("source_named", "reliability_named", "observed_state_named")


def _source_regex(source: str) -> re.Pattern[str]:
    # sensor_1 -> matches "sensor_1", "sensor 1", "Sensor-1", "sensor1"
    parts = re.split(r"[_\s-]+", source.strip())
    body = r"[\s_-]*".join(re.escape(p) for p in parts if p)
    return re.compile(rf"\b{body}\b", re.IGNORECASE)


def _reliability_regex(reliability: float) -> re.Pattern[str]:
    # 0.70 -> "0.70", "0.7", ".70", ".7", "70%"
    pct = int(round(reliability * 100))
    dec = f"{reliability:.2f}"
    short = dec.rstrip("0").rstrip(".") if "." in dec else dec
    alternatives = {
        re.escape(dec),
        re.escape(short),
        re.escape(dec.lstrip("0")),
        re.escape(short.lstrip("0")),
        rf"{pct}\s?%",
        rf"{pct}\s?percent",
    }
    return re.compile(r"(?<![\d.])(?:" + "|".join(sorted(alternatives)) + r")(?![\d])")


def score_message(text: str, roots: tuple[Evidence, ...]) -> dict[str, Any]:
    """Mechanical provenance marks for one message given the roots actually in its lineage.

    These are regex checks on the visible message only. They are deliberately
    conservative and literal; they do not infer meaning. `observed_state_named` is
    weak (it fires whenever the observed-state letter appears near an evidence word)
    and is retained only for completeness.
    """
    source_named = any(_source_regex(e.source).search(text) for e in roots)
    reliability_named = any(_reliability_regex(e.reliability).search(text) for e in roots)
    observed_state_named = any(
        re.search(
            rf"\b(?:observ\w*|sensor\w*|evidence|reading|report\w*|favor\w*|indicat\w*|show\w*)\b[^.;\n]{{0,40}}\b{e.observed_state}\b",
            text,
            re.IGNORECASE,
        )
        or re.search(
            rf"\b{e.observed_state}\b[^.;\n]{{0,40}}\b(?:observ\w*|sensor\w*|evidence|reading|report\w*)\b",
            text,
            re.IGNORECASE,
        )
        for e in roots
    )
    agent_attribution = bool(AGENT_ATTRIBUTION_PATTERN.search(text))
    agent_possessive = bool(AGENT_POSSESSIVE_PATTERN.search(text))
    # agent_as_source: the evidence is owned by an agent in the wording, or it is
    # attributed through an agent while the original sensor is no longer named.
    agent_as_source = agent_possessive or (agent_attribution and not source_named)
    return {
        "source_named": bool(source_named),
        "reliability_named": bool(reliability_named),
        "observed_state_named": bool(observed_state_named),
        "indirection_marked": bool(INDIRECTION_PATTERN.search(text)),
        "agent_attribution": agent_attribution,
        "agent_as_source": agent_as_source,
    }


def erosion(parent_marks: list[dict[str, Any]], child_marks: dict[str, Any]) -> dict[str, Any]:
    """Facts present in at least one inbound message and absent in the outgoing message."""
    lost: list[str] = []
    for field in PRESERVATION_FIELDS:
        available = any(bool(m.get(field)) for m in parent_marks)
        if available and not child_marks.get(field):
            lost.append(field)
    return {"erosion_count": len(lost), "eroded_fields": lost}


def provenance_record(
    text: str, roots: tuple[Evidence, ...], parent_marks: list[dict[str, Any]]
) -> dict[str, Any]:
    marks = score_message(text, roots)
    record = dict(marks)
    record.update(erosion(parent_marks, marks))
    record["inbound_agent_as_source"] = any(bool(m.get("agent_as_source")) for m in parent_marks)
    return record
