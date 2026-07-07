"""
phenomena.py (substrate) -- core-validation phenomena over the live substrate (8b.6).

Runnable probes for the universal-organism validation targets that live at the substrate level:
the ADOLESCENT-RISK imbalance (Part 3 S5.4 mechanism-gap 1) and DA/SATIETY state-dependence
(Part 7 S15 / S5.4 mechanism-gap 2). Both are read out over EMERGENT circuit activity; neither
is coded. These are core phenomena of any developing organism -- not psychopathy findings.

Honesty:
  * Adolescent risk EMERGES from the seed's schedule shapes fed into behaviour selection as
    CAPACITY (plasticity.maturation): mature reward vs still-maturing control. No 'adolescent
    risk' rule; age enters only as a rate.
  * DA/satiety is CIRCUIT MODULATION, never DA scaled by a computed value: the energy deficit
    drives the interoceptive nutritive_state channel -> LH -> VTA (the seed's own chain), so a
    hungry agent's food-reward DA is amplified and a sated agent's attenuated. The modulator is
    LH activity (a circuit output), which is R5-clean.
"""

from __future__ import annotations
from typing import Dict, Iterable, Tuple

from .engine import SubstrateEngine
from .model import load_substrate
from .behaviour import go_drive, executive_hold, GO_THRESHOLD, STN_HOLD_GAIN

# neutral perturbation patterns (not stipulated valences)
_REWARD_CUE = {"IN-GUST:sweet": 0.8}       # a primary appetitive cue (sweet -> VTA/NAc, seed link)
_NUTRITIVE = "IN-INTERO:nutritive_state"   # the energy-deficit interoceptive channel (-> LH -> VTA)


# ---------------------------------------------------------------------------
# Mechanism-gap 1: adolescent-risk imbalance (mature reward vs immature control)
# ---------------------------------------------------------------------------

def risk_index(engine: SubstrateEngine) -> float:
    """How strongly the reward pull wins over the raised decision threshold RIGHT NOW: the ratio
    of the Go drive to the executive-raised threshold. Higher = more impulsive/risky. A read-out
    over emergent activity + the maturing capacities; nothing codes 'risk'."""
    go = go_drive(engine)
    hold = executive_hold(engine)
    return go / (GO_THRESHOLD + STN_HOLD_GAIN * hold)


def _reward_primed(model, age: float) -> SubstrateEngine:
    e = SubstrateEngine(model, age_years=age)
    e.clear_inputs()
    for k, v in _REWARD_CUE.items():
        e.inject_channel(k, v)
    e.settle(30)
    return e


def adolescent_risk_curve(model=None, ages: Iterable[float] = (6, 10, 14, 16, 18, 22, 30)
                          ) -> Dict[float, float]:
    """The risk index across development, under a fixed reward cue. If it PEAKS in adolescence
    (higher than both childhood and adulthood), the dual-systems imbalance emerged; if it is
    monotone or flat, that is the honest read-out (report, don't force)."""
    m = model or load_substrate()
    return {a: risk_index(_reward_primed(m, a)) for a in ages}


# ---------------------------------------------------------------------------
# Mechanism-gap 2: DA/satiety state-dependence (circuit modulation, not DA x r)
# ---------------------------------------------------------------------------

def couple_energy_to_nutritive(engine: SubstrateEngine, energy_level: float) -> None:
    """Close the homeostatic loop (Part 7 S15): the agent's ENERGY state drives the interoceptive
    nutritive_state channel. nutritive_state is an energy-DEFICIT signal, so a LOW energy level
    (hunger) drives it high; a sated agent drives it low. This is the body signalling its own
    state through interoception -- the modulator downstream is LH activity, never a computed r."""
    deficit = max(0.0, min(1.0, 1.0 - energy_level))
    engine.inject_channel(_NUTRITIVE, deficit)


def food_reward_da(model, energy_level: float, age: float = 25.0) -> float:
    """The dopaminergic response to a food cue at a given energy state. The energy deficit drives
    nutritive_state -> LH -> VTA (amplifying), while the sweet cue drives VTA directly; the DA
    read-out is the VTA/SNc output. Hungrier -> more LH drive -> larger food-reward DA."""
    e = SubstrateEngine(model or load_substrate(), age_years=age)
    e.clear_inputs()
    couple_energy_to_nutritive(e, energy_level)
    for k, v in _REWARD_CUE.items():
        e.inject_channel(k, v)
    e.settle(30)
    return e.neuromod_output("DA")


def satiety_modulates_reward(model=None, hungry: float = 0.15, sated: float = 0.95
                             ) -> Tuple[float, float]:
    """Return (food-reward DA when hungry, when sated). Deficit should AMPLIFY and satiety
    ATTENUATE the food-reward DA -- the motivational-modulation signature, via LH->VTA."""
    m = model or load_substrate()
    return food_reward_da(m, hungry), food_reward_da(m, sated)
