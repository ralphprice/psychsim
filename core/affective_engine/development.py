"""
development.py -- how history builds an agent, and how outcomes are read.

Over a stream of childhood situations an agent acts, the caregiving environment
responds, each event is written to the agent's episodic memory, and three things
happen on the developmental clock:

  * Consolidation ("fire together, wire together"), gated so a network only grows
    if the environment affords its experiences.
  * Conscience-control (CONTROL) gain plasticity: an impulsive act met with a
    warm, firm, recognising response -- a teaching moment -- strengthens it.
  * Plasticity declines with developmental age (a sensitive-period effect).

Instrumental control is modelled as primarily temperamental (seeded), not built
here; developmental tuning of it is a noted future extension.

The situation stream is held identical across environments, isolating the
caregiving-response variable that Study 2 goes looking for.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict
import random

from .core import (Appraisal, clamp)
from .agent import AffectiveAgent
from .interocept import reference_child_state, valence_of_event

CTRL_LR = 0.055
ACCESS_LR = 0.060
ACCESS_DECAY = 0.004
THREAT_CREEP = 0.010
CTRL_BOUNDS = (0.20, 1.00)
THREAT_BOUNDS = (0.20, 0.90)


@dataclass
class Environment:
    name: str
    warmth: float
    structure: float
    recognition: float

    def tokens(self) -> set:
        t = set()
        t.add("warmth" if self.warmth >= 0.5 else "harshness")
        t.add("structure" if self.structure >= 0.5 else "low_structure")
        return t

    def perturbation(self) -> Dict[str, float]:
        """WHAT this environment's typical caregiving response DOES to a child's
        interoceptive state -- a pattern of innate perturbations (interocept/App. B),
        described, never a decreed valence. Warmth supplies affiliative touch / soothing
        / contact; structure supplies predictability; recognition supplies acceptance;
        their absence supplies separation / rejection. Intensities in [0,1]."""
        w, s, r = self.warmth, self.structure, self.recognition
        return {
            "affiliative_touch": w,
            "soothing": w,
            "contact_caregiver": w,
            "predictability": s,
            "acceptance": r,
            "separation": clamp(1.0 - w),
            "rejection": clamp(1.0 - w),
        }

    def response_valence(self) -> float:
        """Affective colouring of this environment's typical response -- now COMPUTED,
        not stipulated (MASTER Phase 1, honesty-critical #1): the drive reduction its
        perturbation pattern produces on a developing child's state vector. Warm/firm ->
        positive (relieves social/arousal deficits); harsh/inconsistent -> negative
        (deepens them). Clamped to the [-1,1] interface; the sign and ordering are the
        claim, the magnitude is scaffold-dependent. Because it reads a state vector, the
        SAME response yields different value in agents with different endowments."""
        r, _, _ = valence_of_event(reference_child_state(), self.perturbation())
        return clamp(r, -1.0, 1.0)



def warm_firm_home() -> Environment:
    return Environment("warm-firm-recognising", 0.90, 0.85, 0.90)


def harsh_inconsistent_home() -> Environment:
    return Environment("harsh-inconsistent", 0.20, 0.25, 0.15)


# ---------------------------------------------------------------------------
# Situation archetypes
# ---------------------------------------------------------------------------

def _jitter(rng: random.Random, x: float, s: float = 0.06) -> float:
    return clamp(x + rng.uniform(-s, s))


def situation(kind: str, rng: random.Random) -> Appraisal:
    j = lambda v: _jitter(rng, v)
    if kind == "opportunity":
        return Appraisal(reward=j(0.85), goal_relevance=j(0.7), novelty=j(0.4),
                         controllability=j(0.7), label="opportunity")
    if kind == "provocation":
        return Appraisal(provocation=j(0.85), goal_relevance=j(0.7),
                         social_valence=-j(0.7), controllability=j(0.3),
                         label="provocation")
    if kind == "vulnerable_other":
        return Appraisal(other_distress=j(0.85), social_valence=j(0.3),
                         goal_relevance=j(0.3), label="vulnerable other")
    if kind == "temptation_unobserved":
        return Appraisal(reward=j(0.8), goal_relevance=j(0.7),
                         other_distress=j(0.4), controllability=j(0.2),
                         social_valence=-j(0.2), label="temptation (unobserved)")
    if kind == "threat_event":
        return Appraisal(threat=j(0.85), controllability=j(0.3), novelty=j(0.5),
                         label="threat event")
    if kind == "cooperation":
        return Appraisal(reward=j(0.5), goal_relevance=j(0.6),
                         social_valence=j(0.6), controllability=j(0.7),
                         label="cooperation")
    raise ValueError(kind)


CHILDHOOD_CYCLE = ("opportunity", "provocation", "vulnerable_other",
                   "temptation_unobserved", "cooperation", "threat_event")


def _plasticity(age: float) -> float:
    return max(0.25, 1.0 - 0.75 * age)


def _importance(a: Appraisal) -> float:
    return clamp(max(a.threat, a.provocation, a.reward, a.other_distress))


# --- graded vs binary environmental response -------------------------------
# The default (graded=False) uses hard cutoffs at 0.5, which produce knife-edge
# bifurcations exactly at 0.5. Setting graded=True replaces the step functions
# with sigmoids, so the caregiving response varies smoothly with warmth/structure
# and the outcome boundaries become smooth surfaces -- the mode to use when
# searching for realistic edge conditions.
GRADED_STEEPNESS = 10.0


def _sigmoid(x: float, k: float = GRADED_STEEPNESS) -> float:
    import math
    return 1.0 / (1.0 + math.exp(-k * x))


def _gate(value: float, threshold: float, graded: bool, above: bool = True) -> float:
    """A gate in [0,1]. Binary: a step at `threshold`. Graded: a sigmoid across it.
    `above=True` opens as value rises past threshold; False opens as it falls."""
    d = (value - threshold) if above else (threshold - value)
    if graded:
        return _sigmoid(d)
    return 1.0 if d >= 0 else 0.0


def _token_strength(token: str, env: "Environment", graded: bool) -> float:
    if token == "warmth":
        return _gate(env.warmth, 0.5, graded, above=True)
    if token == "harshness":
        return _gate(env.warmth, 0.5, graded, above=False)
    if token == "structure":
        return _gate(env.structure, 0.5, graded, above=True)
    if token == "low_structure":
        return _gate(env.structure, 0.5, graded, above=False)
    return 1.0


def _affordance_strength(net, env: "Environment", graded: bool) -> float:
    s = 1.0
    for token in net.affordances:
        s *= _token_strength(token, env, graded)
    return s


def _env_gates(env: Environment, graded: bool):
    warm_gate = _gate(env.warmth, 0.5, graded, above=True)
    struct_gate = _gate(env.structure, 0.5, graded, above=True)
    recog_gate = _gate(env.recognition, 0.5, graded, above=True)
    harsh_gate = _gate(env.warmth, 0.5, graded, above=False)
    teach_gate = warm_gate * struct_gate * recog_gate
    return warm_gate, struct_gate, recog_gate, harsh_gate, teach_gate





def _colour_by_env(a, env):
    """Let the environment shape the SITUATIONS a child meets (their social tone),
    not the effect they have: a warmer home presents warmer situations, a harsher
    home more hostile and threatening ones. The child's systems still decide."""
    warm = 2.0 * env.warmth - 1.0
    a.social_valence = clamp(a.social_valence + 0.5 * warm, -1.0, 1.0)
    if env.warmth < 0.5:
        a.threat = clamp(a.threat + 0.6 * (0.5 - env.warmth))
    return a


def develop(agent: AffectiveAgent, env: Environment, n_episodes: int = 48,
            situation_seed: int = 20260704, graded: bool = False,
            age_window: tuple = (0.0, 1.0), cycle_offset: int = 0) -> None:
    """Grow an agent by living a childhood in an environment, ON THE SUBSTRATE.
    The environment colours WHICH situations arise; each is fed to live_moment,
    where the agent's primary systems fire, the dominant one drives behaviour, and
    the system used strengthens (use-dependent, window-gated). No outcome is
    decreed -- what the mind becomes emerges. age_window maps the run onto a slice
    of childhood (so a childhood can be lived in segments); cycle_offset shifts the
    situation cycle. `graded` is retained for signature compatibility."""
    rng = random.Random(situation_seed)
    span = 18.0
    a0, a1 = age_window
    for i in range(n_episodes):
        frac = a0 + (a1 - a0) * (i / max(1, n_episodes - 1))
        kind = CHILDHOOD_CYCLE[(cycle_offset + i) % len(CHILDHOOD_CYCLE)]
        appr = _colour_by_env(situation(kind, rng), env)
        live_moment(agent, appr, age_years=frac * span)


# ---------------------------------------------------------------------------
# Probing and outcome classification
# ---------------------------------------------------------------------------

# HONESTY MIGRATION #2 ("8b.4"): the legacy `probe()` (which ran the removed category-network
# SCORER via agent.settle) and the `Outcome` dataclass (whose fields were the outcome-category
# vocabulary -- governance_index/exploitation_index/strategic_access/... ) have been REMOVED.
# Emergent behaviour is read out by `classify` (the Panksepp MindReadout) and, for study
# constructs, by the observer read-out (observer.py) computed over lived behaviour.


def classify(agent: AffectiveAgent):
    """Read out the emergent substrate -- which primary system dominates, and the
    full profile. This is DESCRIPTIVE measurement, not a driver, and it attaches
    NO psychopathy label: whether any such label applies is a separate interpretive
    question, deliberately kept out of the mechanism."""
    from .drives import read_mind
    return read_mind(agent)


def live_moment(agent, appr, age_years: float):
    """One lived moment on the substrate from an Appraisal (a situation)."""
    from .drives import appraisal_to_stimulus
    return live_stimulus(agent, appraisal_to_stimulus(appr), age_years)


def live_stimulus(agent, stimulus: dict, age_years: float):
    """One lived moment on the substrate from a raw stimulus bundle -- the form a
    significant ACTIVITY (play, sport, learning, being driven to school, ...)
    presents. The bundle's triggers fire the agent's primary systems, the dominant
    one drives behaviour, and the system used is strengthened (use-dependent,
    window-gated). Feeling and behaviour emerge; nothing is typed in. Returns the
    drives.Response."""
    from .drives import imprint
    resp = agent.brain.respond(stimulus)
    imprint(agent.brain, resp, age_years)
    return resp
