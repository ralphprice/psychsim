"""
divergence.py (substrate) -- the executive-control development arm + the 2x2 divergence test
(docs/PsychSim_MASTER_Part4.md S7). This completes the causal chain the observer reads at its
END: a circuit throttle sets the affective ROOT; a developmental environment (perturbation
patterns only) drives circuit activity; meaning-blind plasticity sculpts the developed
executive control; the OUTCOME is measured.

THE HONESTY LINE (S7.3 -- the whole game). Environments are ONLY perturbation patterns
(sensory/social input-channel drives); NOTHING here maps an environment to an outcome. There
is no "warm -> control" or "harsh -> disinhibition" line: whether warm-firm and harsh
development diverge is left to the substrate's own wiring + plasticity, and MEASURED. If you
can find the line where an environment is mapped to an outcome, it is a bug -- rip it out.

THE FINDING IS THE INTERACTION (S7.4), not the main effect: the claim is that the fearless
(throttled) child's outcome is MORE environment-dependent than the intact child's -- the
differential-susceptibility structure. A 2x2: {throttled, intact} x {warm-firm, harsh}.

HONEST RESULT (surfaced, not forced -- Part IV robustness / S5.6): the interaction is
KNIFE-EDGE. It flips sign across the (arbitrary, scaffold) development duration -- negative at
short/medium durations, briefly positive around ~450-500 ticks, ~zero at long ones -- driven
by an UNSTABLE intact+warm cell whose developed executive control oscillates between ~0.17 and
~1.0 rather than settling. Per Part IV a knife-edge phenomenon is flagged, NOT reported as a
finding: so the divergence does NOT robustly emerge here. The proximate cause is a stability
problem in the developmental dynamics (extended development oscillates rather than converging
to an attractor), which must be resolved before the divergence can be fairly tested -- OR it
is the earned negative. That is the design-session's call at the phenomena review.
"""

from __future__ import annotations
from typing import Dict, Iterable, Tuple

from .engine import SubstrateEngine
from .model import load_substrate
from .study import throttled_newborn, AFFECTIVE_EMPATHY

# Developmental environments as PERTURBATION PATTERNS (input-channel drives only). These
# describe what a caregiving world PRESENTS to the senses -- contact/warmth/nurturance vs
# separation/pain -- NOT what it should produce. No outcome, no valence, no control target.
ENVIRONMENTS: Dict[str, Dict[str, float]] = {
    "warm_firm": {"IN-SOMATO:affective_touch": 0.7, "IN-SOMATO:touch": 0.5,
                  "IN-INTERO:thermal_warmth": 0.5, "IN-GUST:sweet": 0.4},
    "harsh_inconsistent": {"IN-INTERO:contact_loss": 0.7, "IN-SOMATO:nociception": 0.5},
}

# The executive circuits that actually receive projections (vlPFC/vmPFC are near-isolated in
# v8 and sit at baseline -- excluded so they do not dilute the read-out). Anatomy, not meaning.
EXECUTIVE = ("dlPFC", "OFC", "dACC")

DEVELOP_YEARS = 18.0
DEVELOP_TICKS = 400          # SCAFFOLD developmental resolution
_PROBE = {"IN-VIS": 0.5}     # a neutral probe for reading developed control


def develop(engine: SubstrateEngine, environment: Dict[str, float],
            years: float = DEVELOP_YEARS, ticks: int = DEVELOP_TICKS) -> None:
    """Run a childhood: inject the environment's perturbation pattern across developmental age;
    the substrate's meaning-blind plasticity sculpts it forward. Nothing steers the outcome."""
    for i in range(ticks):
        engine.set_age(0.2 + years * i / ticks)
        engine.clear_inputs()
        for k, v in environment.items():
            engine.inject_channel(k, v)
        engine.settle(3)
    engine.set_age(25.0)


def developed_executive_control(engine: SubstrateEngine) -> float:
    """Read the developed executive control: the engaged PFC circuits' response to a neutral
    probe after development. A measurement over emergent activity -- the observer's end-point."""
    engine.clear_inputs()
    for k, v in _PROBE.items():
        engine.inject_channel(k, v)
    engine.settle(30)
    val = sum(engine.activity(c) for c in EXECUTIVE) / len(EXECUTIVE)
    engine.clear_inputs()
    engine.settle(10)
    return val


def _cell(throttle: float, environment: Dict[str, float], model,
          ticks: int = DEVELOP_TICKS) -> float:
    eng = throttled_newborn(throttle, AFFECTIVE_EMPATHY, model=model)
    develop(eng, environment, ticks=ticks)
    return developed_executive_control(eng)


def interaction_at(model, ticks: int) -> float:
    """The 2x2 interaction (throttled_swing - intact_swing) at a given development duration."""
    W, H = ENVIRONMENTS["warm_firm"], ENVIRONMENTS["harsh_inconsistent"]
    iw, ih = _cell(0.0, W, model, ticks), _cell(0.0, H, model, ticks)
    tw, th = _cell(0.7, W, model, ticks), _cell(0.7, H, model, ticks)
    return abs(tw - th) - abs(iw - ih)


def interaction_across_durations(model=None,
                                 durations: Iterable[int] = (350, 450, 600)) -> Dict[int, float]:
    """The interaction at several development durations. If the SIGN is not stable across them,
    the interaction is knife-edge -- NOT a robust finding (Part IV)."""
    m = model or load_substrate()
    return {t: interaction_at(m, t) for t in durations}


def divergence_2x2(model=None) -> Dict[str, float]:
    """Run the 2x2 {throttled, intact} x {warm-firm, harsh} and return the cell outcomes plus
    the two environment-swings and their INTERACTION (throttled_swing - intact_swing). A
    positive interaction = the differential-susceptibility structure (S7.4)."""
    m = model or load_substrate()
    iw = _cell(0.0, ENVIRONMENTS["warm_firm"], m)
    ih = _cell(0.0, ENVIRONMENTS["harsh_inconsistent"], m)
    tw = _cell(0.7, ENVIRONMENTS["warm_firm"], m)
    th = _cell(0.7, ENVIRONMENTS["harsh_inconsistent"], m)
    intact_swing = abs(iw - ih)
    throttled_swing = abs(tw - th)
    return {
        "intact_warm": iw, "intact_harsh": ih,
        "throttled_warm": tw, "throttled_harsh": th,
        "intact_swing": intact_swing, "throttled_swing": throttled_swing,
        "interaction": throttled_swing - intact_swing,
    }
