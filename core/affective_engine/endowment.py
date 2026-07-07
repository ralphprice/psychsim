"""
endowment.py -- the newborn's parameters (docs/PsychSim_MASTER.md §5.1, App. A/B).

Genetic endowment is not behaviours but the PARAMETERS of the valence engine: homeostatic
set-points, drive weights w_k, the reactivities of the neuromodulator systems (fear/opioid/
oxytocin/dopamine), the innate-perturbation gains, and the physical traits. This is the only
legitimate place a seed differs; nothing here is an outcome.

A TraitSeed may carry these explicitly; when it does not, they are DERIVED from the legacy
`gains` here, so every existing seed constructs and behaves unchanged (parity), while new
seeds can specify the engine parameters directly. All magnitudes are SCAFFOLD (params.py).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict

from .core import clamp
from . import params

# How the legacy temperament `gains` map onto neuromodulator-system reactivities. A fearless
# seed (low THREAT/ANXIETY gain) -> low fear reactivity; a warm seed (high CARE) -> high
# oxytocin/opioid reactivity; a strong SEEKING seed -> high dopamine reactivity. SCAFFOLD map.
_GAIN_TO_REACTIVITY = {
    "fear":     (("THREAT", 0.6), ("ANXIETY", 0.4)),
    "dopamine": (("SEEKING", 1.0),),
    "oxytocin": (("CARE", 0.7), ("SOCIAL_LOSS", 0.3)),
    "opioid":   (("CARE", 0.5), ("SOCIAL_LOSS", 0.5)),
}
_NEUTRAL_REACTIVITY = 0.5


@dataclass
class Endowment:
    """The resolved newborn parameter set the valence engine reads."""
    set_points: Dict[str, float] = field(default_factory=dict)
    weights: Dict[str, float] = field(default_factory=dict)
    reactivities: Dict[str, float] = field(default_factory=dict)
    perturbation_gains: Dict[str, float] = field(default_factory=dict)
    physical: Dict[str, float] = field(default_factory=dict)

    def copy(self) -> "Endowment":
        return Endowment(dict(self.set_points), dict(self.weights),
                         dict(self.reactivities), dict(self.perturbation_gains),
                         dict(self.physical))


def _reactivity_from_gains(gains: Dict[str, float]) -> Dict[str, float]:
    out = {}
    for system, terms in _GAIN_TO_REACTIVITY.items():
        vals = [w * gains[g] for g, w in terms if g in gains]
        wsum = sum(w for g, w in terms if g in gains)
        out[system] = clamp(sum(vals) / wsum) if wsum else _NEUTRAL_REACTIVITY
    return out


def _weights_from_gains(gains: Dict[str, float]) -> Dict[str, float]:
    """Derive the drive weights from temperament: a low-affiliation seed weights the social
    needs less; an anxious/threat-reactive seed weights arousal more. Others neutral."""
    w = {name: spec["weight"] for name, spec in params.STATE_VARIABLES.items()}
    care = gains.get("CARE", 0.5)
    social_loss = gains.get("SOCIAL_LOSS", 0.5)
    threat = gains.get("THREAT", 0.5)
    anxiety = gains.get("ANXIETY", 0.5)
    w["attachment"] = clamp(w["attachment"] * (0.5 + care))
    w["belonging"] = clamp(w["belonging"] * (0.5 + 0.5 * (care + social_loss)))
    w["arousal"] = clamp(w["arousal"] * (0.5 + 0.5 * (threat + anxiety)))
    return w


def endowment_of(seed) -> Endowment:
    """Resolve a seed's endowment: explicit fields where given, else derived from `gains`."""
    gains = getattr(seed, "gains", {}) or {}
    set_points = dict({n: s["set_point"] for n, s in params.STATE_VARIABLES.items()})
    set_points.update(getattr(seed, "set_points", {}) or {})
    weights = _weights_from_gains(gains)
    weights.update(getattr(seed, "weights", {}) or {})
    reactivities = _reactivity_from_gains(gains)
    reactivities.update(getattr(seed, "reactivities", {}) or {})
    return Endowment(
        set_points=set_points, weights=weights, reactivities=reactivities,
        perturbation_gains=dict(getattr(seed, "perturbation_gains", {}) or {}),
        physical=dict(getattr(seed, "physical", {}) or {}),
    )


def state_vector_from_endowment(endow: Endowment):
    """Build an interocept StateVector seeded with this endowment's set-points and weights."""
    from .interocept import StateVector
    return StateVector(set_points=dict(endow.set_points), weights=dict(endow.weights))
