"""
social.py (substrate) -- multi-affordance social behaviour over the live substrate (Part 6
substrate-social phase; App. F selection).

The substrate produces observable SOCIAL ACTS the same way it produces any behaviour: candidate
action tendencies compete in one basal-ganglia accumulation-to-threshold race, biased by the
circuits' own activity, dopamine gain, and the executive/STN hold. The winner is the emergent
act. There is NO social-specific arbiter -- no code reads a situation and outputs a social act by
rule; the act falls out of which circuit population wins the competition, and which population is
active depends only on what the situation drove through the substrate's own wiring.

Each candidate is grounded in a CIRCUIT POPULATION (the effector mapping -- which action tendency
a population expresses when it wins, exactly like the Panksepp BEHAVIOUR lookup; anatomy, not
meaning). The act names are the ordinary action-tendency vocabulary the world consumers already
use (approach/nurture/aggress/avoid/seek_comfort) -- NOT outcome categories.

This is the parity substrate for retiring the legacy Panksepp engine: it reproduces the social
behaviour the town sim consumes. Retirement itself is gated on that parity (invariant 6).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict

from . import params
from .engine import SubstrateEngine
from .behaviour import _mean_live, executive_hold, GO_THRESHOLD, STN_HOLD_GAIN, GO_LEAK, GO_DT, GO_MAX_STEPS

# SCAFFOLD surround inhibition among competing social affordances (winner-take-all sharpening).
SOCIAL_LATERAL = 0.20

# Candidate social acts, each grounded in a substrate CIRCUIT POPULATION (anatomy, not meaning).
# The act EMERGES from which population wins the BG competition; this map only names the winner,
# it never reads a situation to pick an act. Drives are measured PHASICALLY (activation above the
# agent's own resting level, `_phasic_drive`) so a circuit's tonic level -- e.g. CeA's high
# resting activation, or the deep net-inhibition of PAG/HYPdm -- does not bias the race; what
# competes is how much the current situation MOVED each population, exactly as phasic basal-
# ganglia selection works.
SOCIAL_AFFORDANCES: Dict[str, tuple] = {
    "nurture":      ("PVN-OT", "MPOA", "SEPT"),           # affiliation / bonding
    "approach":     ("VTA", "NAc-core", "NAc-shell"),     # appetitive approach
    "aggress":      ("CeA", "PAG", "HYPdm"),              # threat->attack (defensive aggression)
    "avoid":        ("LA", "BA", "BNST"),                 # fear / avoidance
    "seek_comfort": ("PAG-PANIC",),                      # separation distress
}

# feature read-outs over the emergent ACT (a behaviour string), engine-agnostic so both the
# substrate and the interim Panksepp path feed the same consumers. Not outcome categories.
COHESIVE_ACTS = frozenset({"approach", "nurture", "play", "court"})


def is_cohesive_act(behaviour: str) -> bool:
    """An appetitive/affiliative act that sustains a relationship (approach/nurture/play/court)."""
    return behaviour in COHESIVE_ACTS


def is_aggressive_act(behaviour: str) -> bool:
    """A RAGE/defensive-aggression act that strains a relationship."""
    return behaviour == "aggress"


@dataclass
class SocialBehaviour:
    """The emergent social act plus the per-candidate drive strengths it emerged from (a
    read-out). `behaviour` is 'restrain' if the executive held every candidate below threshold."""
    behaviour: str
    steps: int
    drives: Dict[str, float] = field(default_factory=dict)


def _pop_activation(engine: SubstrateEngine, circuits: tuple) -> float:
    """Mean throttle-adjusted OUTPUT of a circuit population (0 if none live)."""
    live = [engine.activity(c) * engine._gain(c)
            for c in circuits if engine.live_circuit.get(c, False)]
    return sum(live) / len(live) if live else 0.0


def resting_baseline(model, age_years: float = 25.0,
                     throttle: Optional[Dict[str, float]] = None) -> Dict[str, float]:
    """The per-affordance TONIC drive of an agent at rest (a throwaway engine settled with no
    input) -- the level each affordance's phasic drive is measured above. Read-only: it uses a
    fresh engine, so the real agent is never developed by this measurement."""
    e = SubstrateEngine(model, age_years=age_years)
    for cid, f in (throttle or {}).items():
        e.set_throttle(cid, f)
    e.clear_inputs()
    e.settle(30)
    return {act: _pop_activation(e, cs) for act, cs in SOCIAL_AFFORDANCES.items()}


def _phasic_drive(engine: SubstrateEngine, act: str, circuits: tuple,
                  baseline: Dict[str, float]) -> float:
    """How much the current situation moved this affordance's population ABOVE the agent's own
    resting level -- the phasic pull. Tonic activation cancels, so hub circuits do not swamp the
    race and net-inhibited outputs are not permanently frozen out."""
    return max(0.0, _pop_activation(engine, circuits) - baseline.get(act, 0.0))


def _clamp(x: float) -> float:
    return 0.0 if x < 0.0 else 1.0 if x > 1.0 else x


# how a situation (an Appraisal) presents itself to the SENSES -- the perturbation pattern it
# drives into the substrate's input channels. This is description (a threatening situation
# presents a nociceptive/threat cue), NOT a verdict and NOT a situation->act rule: the substrate
# decides what to do with it. Mirrors drives.appraisal_to_stimulus, but into substrate channels.
def appraisal_to_substrate_input(appr) -> Dict[str, float]:
    warm = max(0.0, getattr(appr, "social_valence", 0.0))
    hostile = max(0.0, -getattr(appr, "social_valence", 0.0))
    distress = getattr(appr, "other_distress", 0.0)
    return {
        "IN-SOMATO:nociception":     _clamp(getattr(appr, "threat", 0.0) + 0.3 * hostile
                                            + 0.4 * getattr(appr, "provocation", 0.0)),
        "IN-GUST:sweet":             _clamp(getattr(appr, "reward", 0.0)),
        "IN-SOMATO:affective_touch": _clamp(warm),
        "IN-INTERO:thermal_warmth":  _clamp(0.6 * warm),
        "IN-VIS:biological_motion":  _clamp(distress),
        "IN-AUD:voice":              _clamp(0.8 * distress),
        "IN-VIS:face_like":          _clamp(0.7 * distress),
        "IN-INTERO:contact_loss":    _clamp(getattr(appr, "exclusion", 0.0)),
    }


def respond_to_substrate(engine: SubstrateEngine, appr,
                         baseline: Optional[Dict[str, float]] = None,
                         ticks: int = 25) -> SocialBehaviour:
    """One behavioural moment on the substrate: the situation's perturbation pattern fires the
    agent's circuits, and the multi-affordance BG race resolves the emergent social act. The
    engine develops through the episode (as a lived moment should) -- the same substrate the
    agent's whole life runs on. Returns a SocialBehaviour (`.behaviour`) the world consumers use."""
    engine.clear_inputs()
    for ch, v in appraisal_to_substrate_input(appr).items():
        if v > 0.0:
            engine.inject_channel(ch, v)
    engine.settle(ticks)
    return select_social_behaviour(engine, baseline)


def select_social_behaviour(engine: SubstrateEngine,
                            baseline: Optional[Dict[str, float]] = None) -> SocialBehaviour:
    """Run the multi-affordance basal-ganglia race: each candidate social act accumulates from
    its population's PHASIC drive (above rest; dopamine sets the gain), with surround inhibition
    between candidates and the executive/STN hold raising the threshold. The first to cross wins
    and IS the emergent act; if the hold keeps them all below threshold, the agent RESTRAINS.
    Emergent -- no coded rule maps the situation to an act. `baseline` is the agent's resting
    drives (computed once via resting_baseline if not supplied)."""
    if baseline is None:
        baseline = resting_baseline(engine.model, engine.age_years, engine.throttle)
    drives = {act: _phasic_drive(engine, act, cs, baseline)
              for act, cs in SOCIAL_AFFORDANCES.items()}
    da = engine.neuromod_output("DA")                # dopamine sets the Go gain (F.4)
    threshold = GO_THRESHOLD + STN_HOLD_GAIN * executive_hold(engine)
    acc = {act: 0.0 for act in drives}
    for step in range(1, GO_MAX_STEPS + 1):
        total = sum(acc.values())
        for act, d in drives.items():
            go = d * (0.5 + da)
            lateral = SOCIAL_LATERAL * (total - acc[act])   # surround inhibition
            acc[act] = max(0.0, acc[act] + GO_DT * (go - GO_LEAK * acc[act] - lateral))
        winner = max(acc, key=acc.get)
        if acc[winner] >= threshold:
            return SocialBehaviour(winner, step, drives)
    return SocialBehaviour("restrain", GO_MAX_STEPS, drives)
