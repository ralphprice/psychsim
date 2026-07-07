"""
study.py (substrate) -- the proto-psychopath THROTTLE study over the live substrate
(docs/PsychSim_MASTER_Part3.md S4). This is the make-or-break test of the thesis's core claim,
built to the honesty line (S5.5): the manipulation is a graded HYPOFUNCTION on affective-
empathy circuitry of an ORDINARY newborn -- NOT an outcome-category weight, no seeded
disposition. What it produces (the callous-unemotional profile) is MEASURED by read-outs over
emergent activity, never read from a coded category. If a signature does not emerge, that is a
finding to surface, not to force (S5.6).

v8 carries both empathy systems, so the affective side can be throttled while the cognitive
mentalizing network is left structurally intact -- the "reads but doesn't feel" manipulation.
"""

from __future__ import annotations
from typing import Dict, Iterable, List, Optional, Tuple

from .engine import SubstrateEngine
from .model import load_substrate

# The affective-empathy network (the throttle set, S4.1) and the cognitive mentalizing network
# (left intact). Circuit ids only -- anatomy, not meaning.
AFFECTIVE_EMPATHY = ("LA", "BA", "CeA", "MeA", "aIns")
COGNITIVE_MENTALIZING = ("rSMG-TPJ", "pSTS", "PCun-PCC", "ATL-TP")
DEFENSIVE_OUTPUT = ("CeA", "PAG", "BA")

# neutral, described input patterns (S5.5: perturbation patterns, not stipulated valences)
_CUE = {"IN-VIS": 0.6}
_PUNISH = {"IN-SOMATO:nociception": 0.9}
_DISTRESS = {"IN-VIS:biological_motion": 0.8, "IN-AUD:voice": 0.7, "IN-VIS:face_like": 0.7}


def throttled_newborn(fraction: float = 0.0,
                      targets: Iterable[str] = AFFECTIVE_EMPATHY,
                      age_years: float = 4.0,
                      model=None) -> SubstrateEngine:
    """An ordinary newborn substrate with a throttle applied to `targets` from birth."""
    eng = SubstrateEngine(model or load_substrate(), age_years=age_years)
    for cid in targets:
        if cid in eng.model.circuits:
            eng.set_throttle(cid, fraction)
    return eng


def _defensive_to_cue(eng: SubstrateEngine, ticks: int = 25) -> float:
    eng.clear_inputs()
    for k, v in _CUE.items():
        eng.inject_channel(k, v)
    eng.settle(ticks)
    val = sum(eng.activity(c) for c in DEFENSIVE_OUTPUT) / len(DEFENSIVE_OUTPUT)
    eng.clear_inputs()
    eng.settle(15)
    return val


def punishment_learning(eng: SubstrateEngine, trials: int = 60) -> float:
    """The passive-avoidance / punishment-learning probe (S4.2 -- the sharpest CU signature):
    pair a neutral cue with a punishment (nociception), then measure how much the cue alone
    now drives the defensive output. Positive = the aversion was learned; ~0 or negative = the
    child fails to learn from punishment (the CU inversion). MUTATES the engine (it develops)."""
    before = _defensive_to_cue(eng)
    for _ in range(trials):
        eng.clear_inputs()
        for k, v in {**_CUE, **_PUNISH}.items():
            eng.inject_channel(k, v)
        eng.settle(12)
    after = _defensive_to_cue(eng)
    return after - before


def empathy_response(eng: SubstrateEngine, ticks: int = 35) -> Tuple[float, float]:
    """Present another's distress and read the AFFECTIVE (feel) and COGNITIVE (read) responses.
    Returns (affective, cognitive). Transient -- restores the engine to rest after."""
    eng.clear_inputs()
    for k, v in _DISTRESS.items():
        eng.inject_channel(k, v)
    eng.settle(ticks)
    aff = sum(eng.activity(c) for c in AFFECTIVE_EMPATHY) / len(AFFECTIVE_EMPATHY)
    cog = sum(eng.activity(c) for c in COGNITIVE_MENTALIZING) / len(COGNITIVE_MENTALIZING)
    eng.clear_inputs()
    eng.settle(15)
    return aff, cog


def cu_profile(fraction: float = 0.0, targets: Iterable[str] = AFFECTIVE_EMPATHY,
               model=None) -> Dict[str, float]:
    """Measure the CU profile a given throttle produces on a developed newborn (S4.2). All
    fields are OBSERVER read-outs over emergent activity; none is seeded. Each measurement runs
    on a fresh throttled newborn (punishment_learning develops the substrate)."""
    m = model or load_substrate()
    aff, cog = empathy_response(throttled_newborn(fraction, targets, model=m))
    return {
        "throttle": fraction,
        "punishment_learning": punishment_learning(throttled_newborn(fraction, targets, model=m)),
        "affective_empathy": aff,
        "cognitive_mentalizing": cog,
        # the dissociation index: high when the cognitive read is spared relative to the
        # affective feel -- the "reads but doesn't feel" signature (measured, not defined).
        "affective_minus_cognitive": aff - cog,
    }
