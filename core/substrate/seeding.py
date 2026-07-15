"""
seeding.py (substrate) -- temperament seeding of the substrate (the substrate equivalent of the
retired brain_from_seed).

A TraitSeed's `gains` are individual-difference REACTIVITY biases (a fearless child has low
THREAT, a warm one high CARE, ...). The Panksepp engine carried these as per-system reactivities;
the substrate carries them as per-domain OUTPUT biases: a below-reference temperament gain
throttles that domain's circuits (a low-fear seed's threat circuits fire more weakly), so the
individual differences the seed encodes shape both behaviour and the observer read-out. Only
temperament enters here -- no outcome is implied; what the agent becomes still emerges from
development.

This is meaning-blind: it maps a temperament dimension to the circuit DOMAIN that dimension
biases (anatomy), and applies the existing throttle (a graded output hypofunction) -- never an
outcome-category weight.
"""

from __future__ import annotations
from typing import Dict

from .engine import SubstrateEngine

# which circuit DOMAIN each temperament dimension biases (anatomy, not meaning). FRUSTRATION maps
# to the attack circuits, which are net-inhibited in v8 (OBS-3), so it has no leverage here.
_TEMPERAMENT_DOMAIN = {
    "THREAT": "defensive_threat", "ANXIETY": "defensive_threat",
    "SEEKING": "reward_approach", "CARE": "affiliation", "SOCIAL_LOSS": "affiliation",
    "CONTROL": "executive", "INSTRUMENTAL_CONTROL": "executive",
}
_REF = 0.5   # SCAFFOLD reference temperament level; below it throttles the domain, above it does not


def seed_substrate(engine: SubstrateEngine, gains: Dict[str, float]) -> None:
    """Bias `engine` by temperament: for each dimension whose gain is BELOW the reference, throttle
    the circuits of the domain it biases, proportionally. A fearless seed (low THREAT) throttles
    the threat circuits -> it reacts less to threat and reads bolder; a low-CONTROL seed throttles
    the executive -> weaker restraint. The individual differences the seed encodes, on the
    substrate. Applied before the agent's resting baseline is captured so the baseline reflects it."""
    dom_throttle: Dict[str, float] = {}
    for dim, domain in _TEMPERAMENT_DOMAIN.items():
        g = gains.get(dim)
        if g is None:
            continue
        deficit = max(0.0, (_REF - g) / _REF)          # how far below reference (0 if at/above)
        if deficit > dom_throttle.get(domain, 0.0):
            dom_throttle[domain] = deficit
    for cid, c in engine.model.circuits.items():
        if c.structural_element:      # v14: a structural element is not a reactivity dial -- see Circuit
            continue                  # (throttling a gate DISINHIBITS its target: directionally perverse)
        frac = dom_throttle.get(c.domain, 0.0)
        if frac > 0.0:
            engine.set_throttle(cid, frac)
