"""
core.py -- primitives for the affective-circuit engine.

Defines: Appraisal, the primary circuits and how a situation drives them,
Network (a behavioural network), and TraitSeed (a disposition as circuit gains
plus initial network accessibilities).

Two regulatory circuits, and the distinction is the point of the model:

  * CONTROL              -- conscience-linked self-command: deliberate regulation
                            in service of a considered, other-regarding end. It
                            boosts governed/prosocial modes and suppresses
                            exploitative ones. It is the sophropathic
                            differentiator, and it is largely BUILT by warm,
                            firm, recognising development.
  * INSTRUMENTAL_CONTROL -- cold, strategic self-regulation with no conscience
                            brake: the calm calculation of the "successful"
                            offender. It suppresses reactive (impulsive)
                            aggression but ENABLES calculated exploitation. It is
                            largely temperamental (seeded) in this model.

Same boldness + weak conscience-control + strong instrumental-control -> the
cool, calculated, community "successful" psychopath. Same boldness + strong
conscience-control -> the sophropath. Same boldness + both weak -> the reckless,
reactive, criminal-tending psychopath. This lets the engine represent the very
distinction the forensic (Hare) tradition collapses.

Nothing here is biophysical: these are functional primitives, validated
behaviourally, not a simulation of neurons.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Set


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


# ---------------------------------------------------------------------------
# Appraisal
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
# Circuits
# ---------------------------------------------------------------------------

CIRCUITS = ("THREAT", "ANXIETY", "SEEKING", "FRUSTRATION",
            "CARE", "SOCIAL_LOSS", "CONTROL", "INSTRUMENTAL_CONTROL")

# Prepotent, bottom-up impulses that both regulatory circuits respond to.
IMPULSIVE = ("SEEKING", "FRUSTRATION", "THREAT")

DECAY = 0.5  # leaky-integrator smoothing


def stimulus_drives(a: Appraisal) -> Dict[str, float]:
    """Bottom-up drive in [0,1] for each stimulus-driven circuit. The two
    regulatory circuits are computed from impulse pressure in agent.tick()."""
    rejection = max(0.0, -a.social_valence)
    warmth = max(0.0, a.social_valence)
    return {
        "THREAT":      clamp(0.90 * a.threat + 0.10 * (1 - a.controllability)),
        "ANXIETY":     clamp(0.35 * a.threat + 0.35 * (1 - a.controllability)
                             + 0.30 * a.novelty),
        "SEEKING":     clamp(0.60 * a.reward + 0.30 * a.goal_relevance
                             + 0.10 * a.novelty),
        "FRUSTRATION": clamp(0.60 * a.provocation
                             + 0.60 * a.goal_relevance * (1 - a.controllability)),
        "CARE":        clamp(0.70 * a.other_distress + 0.30 * warmth),
        "SOCIAL_LOSS": clamp(0.60 * a.exclusion + 0.40 * rejection),
    }


# ---------------------------------------------------------------------------
# Behavioural networks
# ---------------------------------------------------------------------------

@dataclass
class Network:
    name: str
    weights: Dict[str, float]
    governance: str                  # "governed" | "ungoverned" | "neutral"
    affordances: Set[str]
    policy: str
    instr: float = 0.0               # response to INSTRUMENTAL_CONTROL:
                                     #   <0 suppressed (reactive), >0 enabled
                                     #   (calculated exploitation / cool competence)


# DEPRECATED (MASTER Phase 8 -- honesty-critical #2). These behavioural networks are named
# after OUTCOME CATEGORIES ("callous_exploitation", "strategic_prosociality",
# "cool_instrumental_boldness", ...) and are arbitrated over as selectable PRIMITIVES by the
# legacy engine (agent.network_score) -- the encoded-answer the discipline forbids. They
# cannot be removed piecemeal (the seeds' `access` weights and agent scoring depend on them);
# they retire together with the whole legacy network engine at Phase 8, after which these
# categories exist ONLY as observer read-outs (see observer.py / App. D). Kept, working, and
# parity-preserved until then, per invariant 6.
def default_catalogue() -> Dict[str, Network]:
    nets = [
        Network(
            "cool_instrumental_boldness",
            {"SEEKING": 0.7, "CONTROL": 0.6, "THREAT": -0.5, "ANXIETY": -0.4},
            "governed", {"structure"},
            "calm, goal-directed action under pressure; risk taken for a purpose",
            instr=0.45,
        ),
        Network(
            "strategic_prosociality",
            {"CARE": 0.4, "CONTROL": 0.8, "SEEKING": 0.3},
            "governed", {"warmth", "structure"},
            "cooperation chosen on reflective grounds and kept when unobserved",
            instr=0.0,
        ),
        Network(
            "affiliative_warmth",
            {"CARE": 0.9, "SOCIAL_LOSS": 0.4, "SEEKING": 0.2},
            "governed", {"warmth"},
            "nurturant, cooperative, emotionally attuned conduct",
            instr=0.0,
        ),
        Network(
            "reactive_aggression",
            {"FRUSTRATION": 0.9, "THREAT": 0.5, "CONTROL": -0.6},
            "ungoverned", {"harshness"},
            "explosive, retaliatory, poorly-governed hostility",
            instr=-1.1,  # cold calculation strongly suppresses impulsive rage
        ),
        Network(
            "callous_exploitation",
            {"SEEKING": 0.8, "CARE": -0.7, "SOCIAL_LOSS": -0.5},
            "ungoverned", {"low_structure"},
            "instrumental manipulation without an affective brake",
            instr=0.7,   # cold calculation enables strategic exploitation
        ),
        Network(
            "fearful_withdrawal",
            {"THREAT": 0.8, "ANXIETY": 0.7, "SEEKING": -0.5},
            "neutral", set(),
            "avoidance, submission, retreat",
            instr=0.0,
        ),
    ]
    return {n.name: n for n in nets}


# DEPRECATED (MASTER Phase 8): these sets group the legacy category-named networks above;
# they are the observer's job (App. D), not the mechanism's. Retire with the legacy engine.
GOVERNED = {"cool_instrumental_boldness", "strategic_prosociality",
            "affiliative_warmth"}
EXPLOITATIVE = {"callous_exploitation", "reactive_aggression"}


# ---------------------------------------------------------------------------
# Trait seeds
# ---------------------------------------------------------------------------

@dataclass
class TraitSeed:
    name: str
    gains: Dict[str, float]
    # DEPRECATED (MASTER Phase 8): `access` keys are the OUTCOME-CATEGORY network names and
    # double as the legacy engine's per-network reachability (agent.network_score:106). It is
    # thus both an honesty violation (a seed carrying `callous_exploitation=0.78` is close to
    # encoding the answer) AND load-bearing legacy state -- so it is removed together with the
    # legacy network engine at Phase 8, not before (invariant 6). The seed's temperament now
    # lives in the endowment fields below; the categories move to observer.py.
    access: Dict[str, float]
    # --- valence-engine endowment (MASTER Phase 5) -- the ONLY legitimate place a seed
    # differs (doc §5.1). Optional and empty by default: when unset, endowment.endowment_of()
    # derives them from the legacy `gains` so every existing seed still constructs and behaves.
    set_points: Dict[str, float] = field(default_factory=dict)          # state-vector set-points
    weights: Dict[str, float] = field(default_factory=dict)             # drive weights w_k
    reactivities: Dict[str, float] = field(default_factory=dict)        # neuromodulator gains
    perturbation_gains: Dict[str, float] = field(default_factory=dict)  # innate-perturbation gains
    physical: Dict[str, float] = field(default_factory=dict)            # attractiveness/health/...


def _access(**overrides) -> Dict[str, float]:
    base = {name: 0.20 for name in default_catalogue()}
    base.update(overrides)
    return base


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
        access=_access(reactive_aggression=0.30, cool_instrumental_boldness=0.25,
                       affiliative_warmth=0.25, strategic_prosociality=0.10,
                       callous_exploitation=0.22, fearful_withdrawal=0.20),
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
        access=_access(cool_instrumental_boldness=0.75, strategic_prosociality=0.75,
                       affiliative_warmth=0.55, reactive_aggression=0.15,
                       callous_exploitation=0.15, fearful_withdrawal=0.15),
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
        access=_access(callous_exploitation=0.78, reactive_aggression=0.60,
                       cool_instrumental_boldness=0.35, strategic_prosociality=0.10,
                       affiliative_warmth=0.12, fearful_withdrawal=0.15),
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
        access=_access(callous_exploitation=0.80, reactive_aggression=0.25,
                       cool_instrumental_boldness=0.55, strategic_prosociality=0.10,
                       affiliative_warmth=0.12, fearful_withdrawal=0.12),
    )


# ---------------------------------------------------------------------------
# Language actuator (the LLM integration point, stubbed)
# ---------------------------------------------------------------------------

class LanguageActuator:
    """Interface between the affective engine and the language model. The engine
    decides the mode; the actuator realises the situated action in that mode.
    Default is a deterministic stub so the engine runs with no model key; swap in
    a real gateway behind the same `act` signature."""

    def act(self, appraisal: "Appraisal", network: Network) -> str:
        return (f"[{network.name}] in '{appraisal.label or 'situation'}': "
                f"{network.policy}.")
