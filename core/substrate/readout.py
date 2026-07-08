"""
readout.py (substrate) -- descriptive read-outs over a developed substrate (Part 6 substrate-
social phase). The substrate-native replacement for the Panksepp read_mind / dominant_profile /
profile_axis, so consumers that summarised an agent's disposition keep working once the legacy
engine is retired.

A MEASUREMENT layer: it reads the developed substrate's emergent DOMAIN activity and reports
which domain dominates and the full profile. Never fed back into behaviour; read-only (it freezes
and restores the engine's developed state around its probe, so measuring never develops the
agent). The dominant domain is an emergent read-out, not a verdict.
"""

from __future__ import annotations
import copy as _copy
from dataclasses import dataclass
from typing import Dict, Iterable, Optional

from .engine import SubstrateEngine

# the emergent domains summarised (seed circuit domains). Anatomy, not outcome categories.
_READOUT_DOMAINS = ("reward_approach", "affiliation", "defensive_threat",
                    "social_cognition", "executive")
# an appetitive/affiliative-minus-aversive contrast (a measurement axis, not a verdict)
_APPETITIVE = ("reward_approach", "affiliation")
_AVERSIVE = ("defensive_threat",)
_FROZEN = ("weight", "theta", "mean_activity", "exp_count", "activation", "pruned",
           "eligibility", "_silent", "_step_i", "external", "channel_drive")
# a neutral probe so the read-out reflects developed reactivity, not the last thing that happened
_PROBE = {"IN-VIS": 0.4}


@dataclass(frozen=True)
class _DomainLabel:
    """A dominant-domain label with a `.value`/`.name` (drop-in for the old System member)."""
    value: str

    @property
    def name(self) -> str:
        return self.value


@dataclass
class MindReadout:
    """A neutral descriptive summary of an emergent mind: the dominant emergent domain and the
    full domain profile. Whether any label applies is a separate interpretive question."""
    dominant: _DomainLabel
    profile: Dict[str, float]

    @property
    def classification(self) -> str:
        return self.dominant.value


def _domain_activity(engine: SubstrateEngine, domain: str) -> float:
    m = engine.model
    acts = [engine.activity(cid) * engine._gain(cid)
            for cid, c in m.circuits.items()
            if c.domain == domain and engine.live_circuit.get(cid, False)]
    return sum(acts) / len(acts) if acts else 0.0


def substrate_profile(engine: SubstrateEngine) -> Dict[str, float]:
    """The emergent DOMAIN profile under a neutral probe -- a normalised read-out of which
    domains are strong in this developed agent. Read-only (freeze/restore)."""
    saved = {a: _copy.copy(getattr(engine, a)) for a in _FROZEN}
    try:
        engine.clear_inputs()
        for k, v in _PROBE.items():
            engine.inject_channel(k, v)
        engine.settle(25)
        raw = {d: _domain_activity(engine, d) for d in _READOUT_DOMAINS}
    finally:
        for a, v in saved.items():
            setattr(engine, a, v)
    total = sum(raw.values()) or 1.0
    return {d: raw[d] / total for d in _READOUT_DOMAINS}


def read_mind(agent) -> MindReadout:
    """Read out a developed agent (duck-typed: an engine, or anything carrying `.engine`).
    Measurement, not a driver."""
    engine = getattr(agent, "engine", agent)
    prof = substrate_profile(engine)
    dom = max(prof, key=prof.get)
    return MindReadout(_DomainLabel(dom), prof)


def dominant_profile(engine: SubstrateEngine) -> Dict[str, float]:
    return substrate_profile(engine)


def profile_axis(profile: Dict[str, float],
                 positive: Iterable[str] = _APPETITIVE,
                 negative: Iterable[str] = _AVERSIVE) -> float:
    """A continuous appetitive/affiliative-minus-aversive score over the domain profile -- a
    measurement projection for sweeps/edge-finding, not a verdict about what the mind 'is'."""
    pos = sum(profile.get(d, 0.0) for d in positive)
    neg = sum(profile.get(d, 0.0) for d in negative)
    return pos - neg


def readout_axis(readout: MindReadout, **kw) -> float:
    return profile_axis(readout.profile, **kw)
