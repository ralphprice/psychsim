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
    "aggress":      ("VMHvl", "PAG", "HYPdm"),            # provocation->attack (reactive aggression): the
                                                          # hypothalamic attack area + effectors. NOT CeA --
                                                          # CeA is GABAergic and SUPPRESSES PAG/HYPdm, so its
                                                          # activation misread as attack-drive (v9 re-grounding)
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


_REST_CACHE: Dict[tuple, Dict[str, float]] = {}


def resting_baseline(model, age_years: float = 25.0,
                     throttle: Optional[Dict[str, float]] = None) -> Dict[str, float]:
    """The per-affordance TONIC drive of an agent at rest (a throwaway engine settled with no
    input) -- the level each affordance's phasic drive is measured above. Read-only: it uses a
    fresh engine, so the real agent is never developed by this measurement.

    Memoised by (model, age, throttle-signature): the rest baseline is a deterministic function
    of those, so agents of the same temperament (same throttle) share one computed baseline
    rather than each settling 30 ticks. Pure caching -- identical values, no behaviour change."""
    key = (id(model), round(age_years, 3), frozenset((throttle or {}).items()))
    cached = _REST_CACHE.get(key)
    if cached is not None:
        return dict(cached)
    e = SubstrateEngine(model, age_years=age_years)
    for cid, f in (throttle or {}).items():
        e.set_throttle(cid, f)
    e.clear_inputs()
    e.settle(30)
    out = {act: _pop_activation(e, cs) for act, cs in SOCIAL_AFFORDANCES.items()}
    _REST_CACHE[key] = dict(out)
    return out


def _phasic_drive(engine: SubstrateEngine, act: str, circuits: tuple,
                  baseline: Dict[str, float]) -> float:
    """How much the current situation moved this affordance's population ABOVE the agent's own
    resting level -- the phasic pull. Tonic activation cancels, so hub circuits do not swamp the
    race and net-inhibited outputs are not permanently frozen out."""
    return max(0.0, _pop_activation(engine, circuits) - baseline.get(act, 0.0))


def _clamp(x: float) -> float:
    return 0.0 if x < 0.0 else 1.0 if x > 1.0 else x


# how a coarse STIMULUS bundle (the interim trigger vocabulary the matrices/development loop pass)
# presents to the substrate's input channels. Description of what a stimulus presents to the
# senses, NOT a verdict about what it should evoke. Unmapped triggers are ignored.
# each coarse trigger presents to one OR MORE input channels. thwarting/restraint are
# provocation-type stimuli: they drive the hypothalamic attack area (IN-INTERO:provocation, v9)
# AND carry a threat fraction (nociception) -- genuine competition (avoid vs aggress), not a flip.
_TRIGGER_CHANNELS = {
    "reward_cue": [("IN-GUST:sweet", 1.0)], "comfort": [("IN-GUST:sweet", 0.6)],
    "affiliation": [("IN-SOMATO:affective_touch", 1.0)], "safety": [("IN-INTERO:thermal_warmth", 0.8)],
    "vulnerable_other": [("IN-VIS:biological_motion", 1.0)], "play_signal": [("IN-VIS:biological_motion", 0.6)],
    "threat": [("IN-SOMATO:nociception", 1.0)], "pain": [("IN-SOMATO:nociception", 0.9)],
    "thwarting": [("IN-INTERO:provocation", 0.6), ("IN-SOMATO:nociception", 0.3)],
    "restraint": [("IN-INTERO:provocation", 0.5), ("IN-SOMATO:nociception", 0.25)],
    "separation": [("IN-INTERO:contact_loss", 1.0)], "loss": [("IN-INTERO:contact_loss", 0.8)],
    "novelty": [("IN-VIS", 0.6)],
}


@dataclass
class FeltResponse:
    """The emergent felt response to a stimulus: the act the substrate produced, its strength,
    and read-out flags. Whether a stimulus reads appetitive/aversive/aggressive EMERGES from the
    act the substrate chose -- no rule decides the social result."""
    behaviour: str
    strength: float

    @property
    def appetitive(self) -> bool:
        return is_cohesive_act(self.behaviour)

    @property
    def aversive(self) -> bool:
        return self.behaviour in ("avoid", "seek_comfort")

    @property
    def aggressive(self) -> bool:
        return is_aggressive_act(self.behaviour)


_FELT_FROZEN = ("weight", "theta", "mean_activity", "exp_count", "activation", "pruned",
                "eligibility", "_silent", "_step_i", "external", "channel_drive")


def felt_response(engine: SubstrateEngine, triggers: Dict[str, float],
                  age_years: Optional[float] = None,
                  baseline: Optional[Dict[str, float]] = None,
                  develop: bool = True) -> FeltResponse:
    """Live one stimulus on the substrate: its perturbation pattern fires the agent's circuits,
    the substrate DEVELOPS through the moment (the BCM plasticity in settle() IS the use-dependent
    strengthening -- the imprint equivalent), and the basal-ganglia race resolves the emergent
    act. Returns a FeltResponse whose valence is a read-out of that act. Used by the matrices and
    the development loop; nothing here arbitrates a social outcome by rule.

    `develop=False` (a fixed/background agent whose personality must not change) makes the moment
    read-only: the developed state is frozen and restored around the settle, so the act still
    emerges but nothing is learned."""
    import copy as _copy
    saved = {a: _copy.copy(getattr(engine, a)) for a in _FELT_FROZEN} if not develop else None
    if age_years is not None and age_years >= 0.5:
        engine.set_age(age_years)
    engine.clear_inputs()
    for trig, intensity in triggers.items():
        if intensity <= 0:
            continue
        for ch, scale in _TRIGGER_CHANNELS.get(trig, ()):
            engine.inject_channel(ch, _clamp(intensity * scale))
    engine.settle(18)   # converged count (affiliation settles by ~16); see convergence check
    b = select_social_behaviour(engine, baseline)
    strength = max(b.drives.values()) if b.drives else 0.0
    if saved is not None:
        for a, v in saved.items():
            setattr(engine, a, v)
    return FeltResponse(b.behaviour, strength)


# how a situation (an Appraisal) presents itself to the SENSES -- the perturbation pattern it
# drives into the substrate's input channels. This is description (a threatening situation
# presents a nociceptive/threat cue), NOT a verdict and NOT a situation->act rule: the substrate
# decides what to do with it. Maps an appraisal onto the substrate's sensory input channels.
def appraisal_to_substrate_input(appr) -> Dict[str, float]:
    warm = max(0.0, getattr(appr, "social_valence", 0.0))
    hostile = max(0.0, -getattr(appr, "social_valence", 0.0))
    distress = getattr(appr, "other_distress", 0.0)
    provocation = getattr(appr, "provocation", 0.0)
    return {
        # provocation keeps a THREAT fraction here (0.2) -- it still drives fear/avoid -- while its
        # provocation-specific part drives the attack area below (IN-INTERO:provocation). Genuine
        # competition, not a scripted flip. SCAFFOLD split (was 0.4 into nociception alone); v9.
        "IN-SOMATO:nociception":     _clamp(getattr(appr, "threat", 0.0) + 0.3 * hostile
                                            + 0.2 * provocation),
        "IN-INTERO:provocation":     _clamp(0.6 * provocation),   # v9: provocation->VMHvl attack-area drive
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
                         ticks: int = 16) -> SocialBehaviour:
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
