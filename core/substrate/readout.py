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


# Below this normalised-profile margin, the top two domains are effectively a tie -- the point at
# which a bare-argmax classification would flip on a perturbation. NOT used to alter the label (D6
# ruling: the core read-out reports WHAT the substrate is -- a domain -- and the STUDY layer decides
# what it MEANS; grading the label would push interpretation into the core, blurring that boundary).
# It is the threshold at which `margin` is worth attending to.
_BLEND_MARGIN = 0.05


@dataclass
class MindReadout:
    """A neutral descriptive summary of an emergent mind: the dominant emergent domain, the full
    domain profile, and the MARGIN to the runner-up. Whether any label applies is a separate
    interpretive question -- owned by the study layer (which speaks outcomes: sophropathic/
    psychopathic/intermediate), not by this core read-out (which speaks domains)."""
    dominant: _DomainLabel
    profile: Dict[str, float]

    @property
    def classification(self) -> str:
        """The BARE dominant domain (a member of _READOUT_DOMAINS). The read-out audit's knife-edge
        -- a 0.05 race rendered as a confident single label -- is exposed by the `margin` FIELD, not
        by grading this label: the margin is the diagnostic (read it when you care / assert it is
        recorded), the domain stays the label every consumer parses, and the study layer owns the
        verdict. That is the correct three-way split (D6, reversing the earlier graded-label call)."""
        return self.dominant.value

    @property
    def runner_up(self) -> str:
        """The second-strongest domain (empty if there is only one)."""
        rest = {d: v for d, v in self.profile.items() if d != self.dominant.value}
        return max(rest, key=rest.get) if rest else ""

    @property
    def margin(self) -> float:
        """The normalised-profile gap dominant - runner-up. A near-tie (< _BLEND_MARGIN) means the
        classification is a close race that would flip on a small perturbation -- captured here (and
        in the golden) so a future flip is visible as a margin-shift, not a silent label change."""
        ru = self.runner_up
        top = self.profile.get(self.dominant.value, 0.0)
        return round(top - self.profile.get(ru, 0.0), 6) if ru else round(top, 6)


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
