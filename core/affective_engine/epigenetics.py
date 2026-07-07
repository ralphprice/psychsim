"""
epigenetics.py -- experience rewriting the endowment, early and semi-permanently
(docs/PsychSim_MASTER.md §5.2, App. A.1(3)). This is where nature and nurture meet in one
variable set, and the hook the thesis's Study 3 targets (OXTR-type effects).

Early experience (especially caregiving and adversity), accumulated within a developmental
window, shifts the ALLOSTATIC set-points and neuromodulator reactivities of the endowment and
holds them shifted. The shift is scaled by DIFFERENTIAL SUSCEPTIBILITY (Belsky & Pluess): a
low-fear child, lacking the fear that would make a harsh upbringing simply frightening, is
more malleable by the environment in BOTH directions -- so the same environment moves a
fearless child's parameters further than a typical child's. The DIRECTION of the eventual
outcome is not coded here; only the parameter shift is, and it feeds the emergent engine.

All magnitudes are SCAFFOLD (params.py).
"""

from __future__ import annotations
from typing import Optional

from .core import clamp
from . import params
from .endowment import Endowment


def susceptibility(endow: Endowment) -> float:
    """Differential susceptibility to the environment: rises as fear reactivity falls."""
    fear = endow.reactivities.get("fear", 0.5)
    return clamp(params.SUSCEPTIBILITY_BASE - fear)


def window_factor(age_years: float) -> float:
    """How open the early epigenetic window is at a given age (1 early, 0 after it closes)."""
    if age_years >= params.EPI_WINDOW_END_AGE:
        return 0.0
    return 1.0 - age_years / params.EPI_WINDOW_END_AGE


def apply_early_experience(endow: Endowment, early_valence: float,
                           age_years: float = 0.0) -> Endowment:
    """Return a NEW endowment shifted by accumulated early experience, within the window.

    `early_valence` summarises the early caregiving climate (-1 harsh .. +1 warm; e.g. the
    mean computed valence of early episodes). Adversity raises the arousal reactivity
    (allostatic load) and lowers its set-point (less tolerance -> chronic arousal drive), and
    lowers oxytocin/opioid function; a warm early climate does the reverse. Shifts are scaled
    by susceptibility and by how open the window still is; once applied they persist."""
    s = susceptibility(endow) * window_factor(age_years)
    adversity = clamp(-early_valence, -1.0, 1.0)   # +ve = harsh, -ve = warm
    step = params.EPI_RATE * s * adversity
    new = endow.copy()
    # arousal: 'excess'-polarity, allostatic. Adversity raises reactivity and LOWERS the
    # set-point so ordinary arousal reads as more deviation (allostatic load); warmth soothes.
    new.reactivities["fear"] = clamp(new.reactivities.get("fear", 0.5) + 0.5 * step)
    new.set_points["arousal"] = clamp(new.set_points.get("arousal", 0.2) - step)
    # oxytocin/opioid social-reward function is lowered by early adversity (OXTR-type; §5.2)
    new.reactivities["oxytocin"] = clamp(new.reactivities.get("oxytocin", 0.5) - step)
    new.reactivities["opioid"] = clamp(new.reactivities.get("opioid", 0.5) - step)
    # social set-points recalibrate: a socially impoverished early world lowers the
    # attachment set-point (the child expects less contact)
    new.set_points["attachment"] = clamp(new.set_points.get("attachment", 0.8) - 0.5 * step)
    return new


def environmental_swing(endow: Endowment) -> float:
    """The range across which this endowment's arousal set-point can be moved by the extremes
    of early environment (warm vs harsh) -- a measure of malleability. Larger for the more
    susceptible (low-fear) child: the differential-susceptibility signature."""
    warm = apply_early_experience(endow, +1.0).set_points["arousal"]
    harsh = apply_early_experience(endow, -1.0).set_points["arousal"]
    return abs(harsh - warm)
