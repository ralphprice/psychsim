"""
scan.py -- the scan controller's trusted PRIMITIVE (Part 4 S8): develop_and_measure.

Manual mode is primary (S8.1): set throttles by hypothesis, develop a childhood on the FIXED live
substrate, and measure the developed signatures. The auto-mode SEARCH layer is a separate, later
build that only CALLS this primitive -- it is not here.

Honesty (S8.3), held STRUCTURALLY, not by discipline:
  * FITNESS IS A MEASURED SIGNATURE. This primitive returns named, individually-grounded observer
    read-outs (`punishment_learning`, `dissociation_index`) -- scalars the study already computes,
    each grounded on its own. NO composite blend and NO distance-to-a-drawn-profile lives here; the
    search layer maximises ONE named read-out at a time (per-signature), never a weighted mixture.
  * FOUND-NOT-FITTED IS ARCHITECTURAL. The ONLY channel from this module to the substrate is
    `engine.set_throttle`. It never writes the model (the seed's weights/connections). "The
    substrate stays fixed" is therefore a property of the code, not a promise -- a test asserts the
    shared model is byte-unchanged across a run.
  * THE THROTTLE CONVENTION IS STRUCTURAL, NOT ARITHMETIC. A named `Throttle` type carries the
    researcher's panel semantics (slider 100 = intact / full function, 0 = fully attenuated); a
    bare number can never be read in the wrong convention by accident. Fixed-point tests pin both
    ends (slider 100 == no throttle applied; slider 0 == target silenced).
  * THE THROTTLEABLE SET IS SEED-DERIVED. A stated query over the seed's own domain tags (the
    affective/empathy network + PFC regulators), not a curated list -- adding a circuit to the seed
    auto-extends the set, and a reader can see the set was not hand-picked.
  * NODE-LEVEL ONLY (this cut). Connection-level throttling (S4.1, "throttle the aIns->dACC edge")
    is DEFERRED; every result records `manipulation_scope` so a null result reads as "no NODE
    throttle mattered; edges untested," never "the network doesn't matter."
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from affective_engine import TraitSeed, AffectiveAgent
from affective_engine.development import develop, Environment
from substrate.model import load_substrate, SubstrateModel
from substrate.study import (punishment_learning, empathy_response,
                             AFFECTIVE_EMPATHY, COGNITIVE_MENTALIZING)


# The affective/empathy network + PFC regulators, as a STATED QUERY over the seed's domain tags.
_THROTTLEABLE_DOMAINS = ("defensive_threat", "affiliation", "interoception_autonomic",
                         "social_cognition", "executive")

# The manipulation scope of this cut: NODES only (connection-level throttling deferred, S4.1).
MANIPULATION_SCOPE = "nodes only"

# the base temperament is FIXED and neutral -- the manipulation is the THROTTLE, not the seed
_INTACT_GAINS = {"THREAT": 0.5, "ANXIETY": 0.5, "SEEKING": 0.5, "FRUSTRATION": 0.5,
                 "CARE": 0.5, "SOCIAL_LOSS": 0.5, "CONTROL": 0.5, "INSTRUMENTAL_CONTROL": 0.5}


def _intact_seed() -> TraitSeed:
    return TraitSeed(name="scan_base", gains=dict(_INTACT_GAINS))


def _neutral_env() -> Environment:
    return Environment("scan_neutral", 0.55, 0.55, 0.55)


# ---------------------------------------------------------------------------
# The throttle -- a NAMED type so the panel convention can never be misread
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Throttle:
    """A throttle setting in the RESEARCHER'S PANEL convention: a function level `slider` in 0..100
    where 100 = intact / full function and 0 = fully attenuated / silent. It converts to the
    engine's `set_throttle` fraction (0 = normal output, 1 = silent). Named on purpose: a bare
    number can never be read as either convention by accident (an inversion here would run every
    experiment backwards while looking internally consistent)."""
    slider: float

    @property
    def fraction(self) -> float:
        """engine.set_throttle fraction: 0 (full function) .. 1 (silent) = (100 - slider)/100."""
        s = 0.0 if self.slider < 0.0 else 100.0 if self.slider > 100.0 else self.slider
        return (100.0 - s) / 100.0

    @property
    def is_intact(self) -> bool:
        return self.fraction == 0.0

    @classmethod
    def from_slider(cls, slider: float) -> "Throttle":
        return cls(float(slider))

    @classmethod
    def intact(cls) -> "Throttle":
        return cls(100.0)

    @classmethod
    def fully_attenuated(cls) -> "Throttle":
        return cls(0.0)


# a throttle CONFIG: circuit_id -> Throttle. Any circuit not present is intact (no throttle).
ThrottleConfig = Dict[str, Throttle]


def throttleable_circuits(model: Optional[SubstrateModel] = None) -> List[str]:
    """The throttleable set, DERIVED as a stated query over the seed's own domain tags -- the
    affective/empathy network + PFC regulators. Not a curated list: adding a circuit to the seed in
    one of these domains automatically extends the set. Node-level (see MANIPULATION_SCOPE)."""
    m = model or load_substrate()
    return sorted(cid for cid, c in m.circuits.items() if c.domain in _THROTTLEABLE_DOMAINS)


# ---------------------------------------------------------------------------
# The measured signatures -- named, individually-grounded scalar read-outs
# ---------------------------------------------------------------------------

# the named signatures a scan may maximise (search-for-effect) or match against (search-for-match)
# -- the exact keys measure_signatures returns. A field pattern's `signature` must be one of these.
SIGNATURE_NAMES = ("punishment_learning", "dissociation_index")


def measure_signatures(engine) -> Dict[str, float]:
    """The named scalar signatures the scan can maximise -- ONE at a time, never blended. Each is a
    single measured read-out the study already computes and grounds on its own:
      * `punishment_learning` -- how much a punished cue comes to drive the defensive output
        (low/negative = the passive-avoidance / CU inversion).
      * `dissociation_index` -- reads-but-doesn't-feel: cognitive mentalizing MINUS affective
        empathy (a difference of two measured quantities, so a legitimate scalar -- the contrast IS
        the phenomenon, not a scoring choice). DIRECTION (pinned by a fixed-point test, so "maximise
        this" is unambiguous): HIGHER = more reads-but-doesn't-feel; throttling the affective-empathy
        network RAISES it (intact ~-0.24 -> affective-throttled ~+0.07)."""
    aff, cog = empathy_response(engine)
    return {
        "punishment_learning": punishment_learning(engine),
        "dissociation_index": cog - aff,
    }


def _viable(engine, saturation_ref: float = 0.9) -> bool:
    """Coarse viability: under a neutral settle the developed agent is not driven into persistent
    saturation (a degenerate all-circuits-pinned state). 'Broken' agents are the expected
    background of the scan (S8.7) -- this flags them so phenotype is scored only on viable ones."""
    engine.clear_inputs()
    engine.settle(25)
    live = [engine.activity(c) for c in engine.model.circuits if engine.live_circuit.get(c, False)]
    if not live:
        return False
    return sum(live) / len(live) <= saturation_ref


# ---------------------------------------------------------------------------
# The primitive -- develop under a throttle config, then measure (manual mode)
# ---------------------------------------------------------------------------

@dataclass
class ProfileResult:
    """One developed-and-measured character: the throttles that were set (recorded in the panel's
    slider convention), the named measured signatures, viability, and provenance. Raw signatures --
    the intact-relative contrast is a report-layer operation over an intact baseline."""
    throttles: Dict[str, float]           # circuit -> slider value (100 = intact)
    signatures: Dict[str, float]          # named measured read-outs
    viable: bool
    seed: int
    manipulation_scope: str = MANIPULATION_SCOPE
    provenance: Dict = field(default_factory=dict)


def develop_and_measure(config: ThrottleConfig, seed: int, *, n_episodes: int = 48,
                        env: Optional[Environment] = None) -> ProfileResult:
    """MANUAL-MODE PRIMITIVE: apply a throttle config to the FIXED live substrate, develop a compressed
    childhood, and measure the developed signatures. Deterministic from `seed`. The substrate model
    is never written -- the only channel to it is `engine.set_throttle` (the agent's own engine
    holds per-instance weights; the shared seed structure is read-only)."""
    agent = AffectiveAgent(seed=_intact_seed())         # fixed neutral temperament; throttle is the manipulation
    for cid, thr in config.items():
        agent.engine.set_throttle(cid, thr.fraction)    # the ONLY channel to the substrate
    develop(agent, env or _neutral_env(), n_episodes=n_episodes, situation_seed=seed)
    result = ProfileResult(
        throttles={cid: thr.slider for cid, thr in config.items()},
        signatures=measure_signatures(agent.engine),
        viable=_viable(agent.engine),
        seed=seed,
        provenance={"substrate": agent.engine.model.meta.get("version", "unknown"),  # from the live model, never hardcoded (can't drift)
                    "base_temperament": "intact",
                    "manipulation_scope": MANIPULATION_SCOPE, "n_episodes": n_episodes},
    )
    return result


def intact_baseline(seed: int, **kw) -> ProfileResult:
    """The control arm: an intact (no-throttle) agent on the same seed. Every scan signature is
    reported RELATIVE to this -- the contrast is the result, not the raw magnitude (S8.7)."""
    return develop_and_measure({}, seed, **kw)
