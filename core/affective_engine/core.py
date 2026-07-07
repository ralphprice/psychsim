"""
core.py -- primitives for the affective engine.

Defines: the Appraisal (a situation vector) and TraitSeed (a disposition as
temperament gains plus the valence-engine endowment).

HONESTY MIGRATION #2 done (MASTER Phase 6 / "8b.4"): the outcome-category network
engine that used to live here -- the `Network` catalogue named after OUTCOME
CATEGORIES (`callous_exploitation`, `strategic_prosociality`, ...), the
`TraitSeed.access` per-category reachability weights, and the `GOVERNED`/
`EXPLOITATIVE` groupings -- has been REMOVED. Those were the encoded-answer the
discipline forbids (a seed carrying `callous_exploitation=0.78` is close to
seeding the outcome). The outcome categories now exist ONLY as observer read-outs
(observer.py, App. D): computed over emergent behaviour, never fed back, never a
seed input and never a causal branch.

The live behaviour engine is the Panksepp substrate in drives.py (interim-legacy;
its own retirement onto the circuit substrate is a separate, parity-gated phase).
Behaviour there emerges from the primary-system dynamics; downstream layers key on
FEATURE read-outs of the emergent response (`is_cohesive`/`is_aggressive`) and on
the emergent action itself, not on any outcome-category label.

Nothing here is biophysical: these are functional primitives, validated
behaviourally, not a simulation of neurons.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


# ---------------------------------------------------------------------------
# Appraisal -- the situation vector the engine reads
# ---------------------------------------------------------------------------

APPRAISAL_DIMS = (
    "threat", "reward", "social_valence", "goal_relevance", "novelty",
    "agency", "controllability", "other_distress", "provocation", "exclusion",
)


@dataclass
class Appraisal:
    threat: float = 0.0
    reward: float = 0.0
    social_valence: float = 0.0       # hostile (-1) .. warm (+1)
    goal_relevance: float = 0.0
    novelty: float = 0.0
    agency: float = 0.5
    controllability: float = 0.5
    other_distress: float = 0.0
    provocation: float = 0.0
    exclusion: float = 0.0
    label: str = ""


# ---------------------------------------------------------------------------
# Trait seeds -- a disposition as temperament gains + valence-engine endowment
# ---------------------------------------------------------------------------

# the temperament circuits a seed carries reactivity gains over. These are
# individual-difference dimensions (temperament), NOT outcome categories.
GAIN_DIMS = ("THREAT", "ANXIETY", "SEEKING", "FRUSTRATION",
             "CARE", "SOCIAL_LOSS", "CONTROL", "INSTRUMENTAL_CONTROL")


@dataclass
class TraitSeed:
    name: str
    gains: Dict[str, float]
    # --- valence-engine endowment (MASTER Phase 5) -- the ONLY legitimate place a seed
    # differs (doc S5.1). Optional and empty by default: when unset, endowment.endowment_of()
    # derives them from `gains` so every existing seed still constructs and behaves.
    set_points: Dict[str, float] = field(default_factory=dict)          # state-vector set-points
    weights: Dict[str, float] = field(default_factory=dict)             # drive weights w_k
    reactivities: Dict[str, float] = field(default_factory=dict)        # neuromodulator gains
    perturbation_gains: Dict[str, float] = field(default_factory=dict)  # innate-perturbation gains
    physical: Dict[str, float] = field(default_factory=dict)            # attractiveness/health/...


def shared_root_seed() -> TraitSeed:
    """The disposition both a sophropath and a criminal psychopath begin from:
    attenuated threat/anxiety (fearless, resilient boldness), partly attenuated
    affiliation, a weak/undeveloped conscience-control circuit, low instrumental
    control, and a strong seeking drive. Development decides the rest."""
    return TraitSeed(
        "shared_root",
        gains={"THREAT": 0.30, "ANXIETY": 0.30, "SEEKING": 0.78,
               "FRUSTRATION": 0.62, "CARE": 0.45, "SOCIAL_LOSS": 0.45,
               "CONTROL": 0.35, "INSTRUMENTAL_CONTROL": 0.35},
    )


def shared_root_calculating_seed() -> TraitSeed:
    """The same shared root disposition, but temperamentally high in cold
    instrumental control. Raised harshly, this becomes the cool, calculated
    'successful' psychopath rather than the reckless, reactive one."""
    s = shared_root_seed()
    s.name = "shared_root_calculating"
    s.gains = dict(s.gains, INSTRUMENTAL_CONTROL=0.80)
    return s


def sophropathic_seed() -> TraitSeed:
    """A developed sophropathic end-state (for parameter-recovery tests): shared
    boldness, bounded (not absent) affiliation, a strong conscience-control
    circuit, and a well-developed strategic-prosociality repertoire."""
    return TraitSeed(
        "sophropathic",
        gains={"THREAT": 0.28, "ANXIETY": 0.30, "SEEKING": 0.70,
               "FRUSTRATION": 0.45, "CARE": 0.45, "SOCIAL_LOSS": 0.50,
               "CONTROL": 0.85, "INSTRUMENTAL_CONTROL": 0.50},
    )


def psychopathic_seed() -> TraitSeed:
    """A developed criminal-psychopathic end-state, reactive/unsuccessful subtype:
    the same boldness, deep affiliation attenuation, weak conscience control AND
    weak instrumental control -- reckless, reactive, prone to getting caught."""
    return TraitSeed(
        "psychopathic",
        gains={"THREAT": 0.28, "ANXIETY": 0.28, "SEEKING": 0.80,
               "FRUSTRATION": 0.70, "CARE": 0.20, "SOCIAL_LOSS": 0.20,
               "CONTROL": 0.32, "INSTRUMENTAL_CONTROL": 0.30},
    )


def psychopathic_successful_seed() -> TraitSeed:
    """A developed 'successful' psychopathic end-state, calculated subtype: same
    boldness and deep affiliation attenuation, weak conscience control but STRONG
    instrumental control -- calm, calculated, manipulative, rarely reactive."""
    return TraitSeed(
        "psychopathic_successful",
        gains={"THREAT": 0.26, "ANXIETY": 0.26, "SEEKING": 0.80,
               "FRUSTRATION": 0.55, "CARE": 0.20, "SOCIAL_LOSS": 0.22,
               "CONTROL": 0.30, "INSTRUMENTAL_CONTROL": 0.85},
    )
