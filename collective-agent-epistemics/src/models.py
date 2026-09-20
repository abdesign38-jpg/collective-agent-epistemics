from dataclasses import dataclass, field
from typing import FrozenSet, Optional

@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    supports_state: str   # "A" or "B"
    reliability: float    # >0.5 means informative
    source: str

@dataclass
class Claim:
    claim_id: str
    sender: str
    supports_state: str
    confidence: float
    actual_roots: FrozenSet[str]
    perceived_roots: FrozenSet[str]
    inference_depth: int
    derived_from: Optional[str] = None

@dataclass
class AgentState:
    name: str
    evidence: list[Evidence] = field(default_factory=list)
    received: list[Claim] = field(default_factory=list)
    counted_root_ids: set[str] = field(default_factory=set)
    naive_social_units: list[float] = field(default_factory=list)
