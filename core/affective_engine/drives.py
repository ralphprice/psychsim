"""
drives.py -- the neural substrate a mind is built on (crude, grounded, evolving).

INTERIM-LEGACY (deferred-retirement pointer). This Panksepp two-affect-pathway engine
(System/Brain/Drive) is the CURRENT live behaviour engine for the social layer. Its own
retirement -- replacing it with the category-free circuit substrate (core/substrate) as the
source of activation and behaviour -- is a SEPARATE, PARITY-GATED phase, NOT the "8b.4" honesty
cut. That cut removed the outcome-category NETWORK engine (the coded categories); it deliberately
did NOT touch this engine, because the substrate has not yet reproduced social behaviour
(behaviour.py yields only approach/restrain; there is no circuit observer adapter). Retiring this
engine before that parity exists would violate invariant 6. Until then this stays, flagged, and
downstream layers key on FEATURE read-outs of its emergent Response (is_cohesive/is_aggressive)
and on the emergent action (Response.behaviour) -- never on an outcome-category label.

This replaces hand-written verdicts ("a harsh place raises THREAT at rate X") with
a modelled substrate from which feeling and behaviour EMERGE. It is grounded in
Jaak Panksepp's affective neuroscience: seven primary emotional/motivational
systems, evolutionarily conserved and rooted in subcortical (brain-stem/limbic)
circuits -- SEEKING, CARE, PLAY, LUST (appetitive) and FEAR, RAGE, PANIC/GRIEF
(aversive) -- plus homeostatic drives (hunger, warmth, fatigue) and sensory
pleasure/pain (Panksepp, 1998; Montag & Panksepp, 2017). Each system fires to its
OWN triggers, as the brain's circuits do; nobody writes "this experience produces
that outcome". Which system comes to dominate a given mind is an emergent product
of what its experiences happen to activate, its temperament, and when in
development those experiences land.

Two evidence-based mechanisms drive change, both general (not outcome-directed):
  * use-dependent strengthening -- a system repeatedly activated strengthens, as
    repeated activation potentiates a circuit ("cells that fire together wire
    together"; long-term potentiation). Reliance sets behavioural patterns.
  * developmental windows -- plasticity is high in early childhood, dips, rises
    again in adolescence (late prefrontal maturation), and is low in adulthood
    (critical/sensitive-period literature: Knudsen 2004; Hensch). Impressions in
    open windows leave the deepest, most fixed marks.

Nothing here decides that a given upbringing yields a given adult. It models the
machinery and lets trajectories fall out -- which, while the machinery is this
crude, will be largely chaotic. That is expected and correct at this stage.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional
import random


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return lo if x < lo else hi if x > hi else x


class System(Enum):
    """Panksepp's seven primary emotional systems (the 'neural networks')."""
    SEEKING = "SEEKING"      # appetitive approach, expectancy, resource pursuit
    CARE = "CARE"            # nurturance toward the vulnerable
    PLAY = "PLAY"            # social joy, rough-and-tumble (needs felt safety)
    LUST = "LUST"            # sexual/mating motivation
    FEAR = "FEAR"            # danger -> flight/freeze (amygdala-anchored)
    RAGE = "RAGE"            # thwarting/restraint -> anger/defensive aggression
    PANIC = "PANIC"          # separation distress / grief


APPETITIVE = (System.SEEKING, System.CARE, System.PLAY, System.LUST)
AVERSIVE = (System.FEAR, System.RAGE, System.PANIC)

# what each system fires to. These are the systems' OWN evolved triggers (from the
# affective-neuroscience literature), not a designer's verdict about outcomes.
TRIGGER_AFFINITY: Dict[System, Dict[str, float]] = {
    System.SEEKING: {"reward_cue": 1.0, "novelty": 0.8, "comfort": 0.4},
    System.CARE:    {"vulnerable_other": 1.0, "affiliation": 0.5},
    System.PLAY:    {"play_signal": 1.0, "safety": 0.5, "affiliation": 0.4},
    System.LUST:    {"mate_cue": 1.0},
    System.FEAR:    {"threat": 1.0, "pain": 0.7, "novelty": 0.3},
    System.RAGE:    {"restraint": 1.0, "thwarting": 0.9, "pain": 0.5},
    System.PANIC:   {"separation": 1.0, "loss": 0.8},
}

# the behaviour each system, when dominant, tends toward (the 'behavioural matrix'
# lookup). A person uses different systems -- so different behaviour -- by situation.
BEHAVIOUR: Dict[System, str] = {
    System.SEEKING: "approach", System.CARE: "nurture", System.PLAY: "play",
    System.LUST: "court", System.FEAR: "avoid", System.RAGE: "aggress",
    System.PANIC: "seek_comfort",
}


@dataclass
class Drive:
    """One primary system in one individual: how readily it fires (reactivity,
    a temperament trait) and how developed/relied-upon it is (strength, which
    grows with use)."""
    reactivity: float = 0.5
    strength: float = 0.5

    def activation(self, stimulus: Dict[str, float], system: System) -> float:
        """How strongly this system fires to the present stimulus."""
        match = sum(TRIGGER_AFFINITY[system].get(k, 0.0) * v
                    for k, v in stimulus.items())
        return clamp(self.reactivity * (0.4 + 0.6 * self.strength) * match, 0.0, 3.0)


@dataclass
class Brain:
    """An individual's subcortical substrate: a Drive per primary system. Temperament
    is the pattern of reactivities; personality emerges as strengths diverge with
    experience. No system is privileged and no outcome is written in."""
    drives: Dict[System, Drive] = field(default_factory=dict)
    # an optional ALWAYS-ON executive layer (see executive.py). When attached, it is
    # consulted on every respond and may modulate the activations before the dominant
    # system is chosen. Duck-typed (Brain does not import Executive) to avoid a cycle.
    executive: Optional[object] = None

    @staticmethod
    def from_temperament(rng: random.Random,
                         reactivity_bias: Optional[Dict[System, float]] = None) -> "Brain":
        bias = reactivity_bias or {}
        d = {}
        for s in System:
            base = bias.get(s, 0.5)
            d[s] = Drive(reactivity=clamp(random_gauss(rng, base, 0.15)),
                         strength=clamp(random_gauss(rng, 0.5, 0.08)))
        return Brain(d)

    def to_dict(self) -> Dict[str, list]:
        """Serialise the substrate to plain JSON: {system: [reactivity, strength]}.
        This is the whole individual difference (given temperament) + what has been
        grown (strength). The executive layer is NOT serialised here: its learned
        registry is empty by default, and a cached/loaded brain is used either as a
        fixed background adult (no live executive needed) or re-attached a fresh one
        when it becomes a live subject."""
        return {s.value: [round(self.drives[s].reactivity, 6),
                          round(self.drives[s].strength, 6)] for s in System}

    @staticmethod
    def from_dict(data: Dict[str, list]) -> "Brain":
        """Rebuild a Brain from `to_dict` output. Missing systems fall back to
        neutral (0.5/0.5), so partial/older dicts still load."""
        drives = {}
        for s in System:
            pair = data.get(s.value) or data.get(s.name) or [0.5, 0.5]
            drives[s] = Drive(reactivity=clamp(float(pair[0])),
                              strength=clamp(float(pair[1])))
        return Brain(drives)

    def respond(self, stimulus: Dict[str, float]) -> "Response":
        """Fire all systems to the stimulus; the strongest dominates and sets the
        behaviour. Systems interact: thwarted SEEKING feeds RAGE (Panksepp)."""
        act = {s: self.drives[s].activation(stimulus, s) for s in System}
        # inter-system control: when SEEKING is engaged but thwarted, RAGE rises
        thwart = stimulus.get("thwarting", 0.0) + stimulus.get("restraint", 0.0)
        if act[System.SEEKING] > 0.3 and thwart > 0.0:
            act[System.RAGE] += 0.5 * act[System.SEEKING] * thwart
        # FEAR can recruit SEEKING (seeking safety)
        if act[System.FEAR] > 0.3:
            act[System.SEEKING] += 0.2 * act[System.FEAR]
        dominant = max(act, key=act.get)
        # the always-on executive layer is consulted on EVERY event; on the patterns
        # it has learned to monitor it modulates the activations (e.g. inhibits a
        # prepotent drive), which can change which system dominates -- the override.
        # With nothing learned to monitor, this is a no-op on the outcome.
        if self.executive is not None:
            self.executive.consult(act, dominant, stimulus)
            dominant = max(act, key=act.get)
        return Response(dominant, BEHAVIOUR[dominant], act)


@dataclass
class Response:
    dominant: System
    behaviour: str
    activations: Dict[System, float]


# ---------------------------------------------------------------------------
# development: use-dependent strengthening, gated by the developmental window
# ---------------------------------------------------------------------------

def window_plasticity(age_years: float) -> float:
    """Openness of the developmental window by age (0..1). High in early childhood,
    a dip in middle childhood, a resurgence in adolescence (late prefrontal
    maturation), low in adulthood. Grounded in the critical/sensitive-period
    literature; the exact shape is crude and a calibration target."""
    if age_years < 5:
        return 0.9 - 0.04 * age_years          # ~0.9 -> ~0.7, very open
    if age_years < 11:
        return 0.6 - 0.03 * (age_years - 5)    # ~0.6 -> ~0.4, narrowing
    if age_years < 18:
        return 0.55 - 0.02 * (age_years - 11)  # adolescent resurgence ~0.55 -> ~0.4
    return max(0.1, 0.35 - 0.01 * (age_years - 18))  # adult: low, settling to ~0.1


USE_LR = 0.06          # how much a used system strengthens per activation
DISUSE_DECAY = 0.004   # gentle drift of unused systems


def imprint(brain: Brain, response: Response, age_years: float,
            neuromod: float = 1.0) -> None:
    """Use-dependent plasticity, expressed as the substrate's THREE-FACTOR rule
    (Fremaux & Gerstner / App. C.4): the system that drove behaviour strengthens as
    pre (it was engaged) x post (its activation) x a NEUROMODULATOR, gated by the
    developmental window; the rest drift gently. `neuromod` defaults to 1.0 -- the
    legacy use-dependent path where reliance alone sets patterns -- and is set to a
    dopamine reward-prediction-error (delta) by the value-learning system so that
    reliance consolidates in proportion to how rewarding it was. Local and
    meaning-blind: this is a general learning mechanism, NOT a rule about which
    upbringing yields which adult -- outcomes emerge from which systems a life
    engages."""
    plast = window_plasticity(age_years)
    used = response.dominant
    for s, drive in brain.drives.items():
        if s is used:
            drive.strength = clamp(drive.strength
                                   + USE_LR * plast * response.activations[s] * neuromod)
        else:
            drive.strength = clamp(drive.strength - DISUSE_DECAY * plast)


def random_gauss(rng: random.Random, mu: float, sigma: float) -> float:
    return rng.gauss(mu, sigma)


def dominant_profile(brain: Brain) -> Dict[str, float]:
    """A descriptive READOUT of the emergent substrate -- which systems are strong.
    This is measurement applied to the mind, not a driver of it; any label a
    researcher attaches (and whether it is apt) is a separate, later question."""
    total = sum(d.strength for d in brain.drives.values()) or 1.0
    return {s.value: brain.drives[s].strength / total for s in System}


# ---------------------------------------------------------------------------
# bridges into the existing world: situations -> stimuli, temperament -> a brain
# ---------------------------------------------------------------------------

# how a seed's temperament (reactivities of the OLD circuits) carries into the
# primary systems. This is individual difference (temperament), not an outcome.
_SEED_TO_SYSTEM = {
    System.FEAR: ("THREAT", "ANXIETY"),
    System.SEEKING: ("SEEKING",),
    System.RAGE: ("FRUSTRATION",),
    System.CARE: ("CARE",),
    System.PANIC: ("SOCIAL_LOSS",),
    # PLAY, LUST: no seed equivalent -> default reactivity
}


def brain_from_seed(seed, rng: random.Random) -> "Brain":
    """Build a Brain whose reactivities reflect a disposition seed's temperament
    (a fearless seed -> low FEAR reactivity, and so on). Only temperament is
    carried; no outcome is implied -- what the mind becomes still emerges."""
    bias = {}
    for system, keys in _SEED_TO_SYSTEM.items():
        vals = [seed.gains[k] for k in keys if k in getattr(seed, "gains", {})]
        if vals:
            bias[system] = sum(vals) / len(vals)
    return Brain.from_temperament(rng, reactivity_bias=bias)


def appraisal_to_stimulus(a) -> Dict[str, float]:
    """Translate a situation (an Appraisal) into the triggers it PRESENTS. This
    is description, not verdict: a threatening situation presents a threat
    trigger; the FEAR system, given the sim's wiring, decides what to do with it."""
    warmth = max(0.0, getattr(a, "social_valence", 0.0))
    hostile = max(0.0, -getattr(a, "social_valence", 0.0))
    ctrl = getattr(a, "controllability", 0.5)
    return {
        "threat": clamp(getattr(a, "threat", 0.0) + 0.3 * hostile),
        "reward_cue": clamp(getattr(a, "reward", 0.0)),
        "novelty": clamp(getattr(a, "novelty", 0.0)),
        "thwarting": clamp(getattr(a, "provocation", 0.0)
                           + 0.4 * getattr(a, "goal_relevance", 0.0) * (1 - ctrl)),
        "restraint": clamp(0.6 * (1 - ctrl) * hostile),
        "vulnerable_other": clamp(getattr(a, "other_distress", 0.0)),
        "separation": clamp(getattr(a, "exclusion", 0.0)),
        "affiliation": clamp(warmth),
        "safety": clamp(warmth * ctrl),
        "comfort": clamp(0.5 * getattr(a, "reward", 0.0) + 0.3 * warmth),
    }


@dataclass
class MindReadout:
    """A neutral, descriptive summary of an emergent mind: which primary system
    dominates and the full profile of strengths. Whether any psychopathy label
    applies is a SEPARATE interpretive question, not decided here."""
    dominant: System
    profile: Dict[str, float]

    @property
    def classification(self) -> str:      # back-compat: the emergent dominant system
        return self.dominant.value

    @property
    def probe_map(self) -> Dict[str, str]:
        return {}


def read_mind(agent) -> MindReadout:
    """Read out the emergent substrate -- measurement, not a driver."""
    prof = dominant_profile(agent.brain)
    dom = max(agent.brain.drives, key=lambda s: agent.brain.drives[s].strength)
    return MindReadout(dom, prof)


# a NEUTRAL measurement axis over the emergent profile, for sweeps and edge-finding.
# This is a projection of the profile onto a chosen contrast -- a way to read the
# substrate as one continuous number -- NOT a verdict about what the mind "is".
def profile_axis(profile: Dict[str, float],
                 positive=(System.SEEKING, System.CARE, System.PLAY, System.LUST),
                 negative=(System.FEAR, System.RAGE, System.PANIC)) -> float:
    """Continuous score in ~[-1, 1]: appetitive/affiliative strength minus
    aversive/defensive strength. A measurement choice; other projections are
    equally valid for asking other questions."""
    pos = sum(profile.get(s.value, 0.0) for s in positive)
    neg = sum(profile.get(s.value, 0.0) for s in negative)
    return pos - neg


def readout_axis(readout, **kw) -> float:
    return profile_axis(readout.profile, **kw)


# ---------------------------------------------------------------------------
# unifying behaviour + relationships onto the substrate
# ---------------------------------------------------------------------------

def respond_to_appraisal(agent, appr):
    """One behavioural moment on the substrate: the situation's triggers fire the
    agent's primary systems and the dominant one drives behaviour. This is how a
    mind ACTS in an interaction -- the same substrate that development runs on."""
    return agent.brain.respond(appraisal_to_stimulus(appr))


# the appetitive/affiliative acts that sustain a relationship, as emergent BEHAVIOUR strings.
# Engine-agnostic on purpose (Part 6 substrate-social phase): both the Panksepp Response and the
# substrate SocialBehaviour expose `.behaviour`, so these feature read-outs feed the same
# consumers whichever engine produced the act -- the seam that lets the town sim run on either.
_COHESIVE_BEHAVIOURS = frozenset({"approach", "nurture", "play", "court"})


def is_cohesive(resp) -> bool:
    """A response that SUSTAINS a relationship: an appetitive/affiliative engagement (approach,
    nurture, play, court) rather than aggression, withdrawal or distress. Keyed on the emergent
    behaviour, so it reads a substrate SocialBehaviour or a Panksepp Response identically."""
    return getattr(resp, "behaviour", None) in _COHESIVE_BEHAVIOURS


def is_aggressive(resp) -> bool:
    """A response that ESCALATES strain: an aggressive act."""
    return getattr(resp, "behaviour", None) == "aggress"


# HONESTY MIGRATION #2 ("8b.4"): the `_BEHAVIOUR_TO_NETWORK` / `response_to_network` layer that
# translated an emergent behaviour into an outcome-category label has been REMOVED. Downstream
# layers now key on the emergent action itself (`Response.behaviour`: approach/nurture/play/court/
# avoid/aggress/seek_comfort -- action tendencies, not categories) and on the feature read-outs
# is_cohesive/is_aggressive. The outcome categories are computed only as observer read-outs
# (observer.py); see core.py for the full record of what was removed.
