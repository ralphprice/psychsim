"""
plasticity.py (substrate) -- the 8 seed plasticity rules as pure, MEANING-BLIND functions
(Part 2 S2.4). Every function takes only numeric activity/weight/age arguments; NOTHING here
references what a circuit is (no domain, no name, no "fear"/"threat"), and nothing references
an outcome. That is the honesty wall at the dynamics level -- verifiable at source (S2.6).

Composition order per connection per step (orchestrated by engine.py, which supplies the
live neuromodulator-circuit output for R5):

  R3-BCM      correlation term (subsumes R1-HEBB; R2-RATE = we do this at rate level)
  R5-NMOD     consolidation = eligibility_trace * modulator_scalar  (modulator = a CIRCUIT's
              live output, never a set value -- the danger point)
  R6-DEVGATE  scale by eta(age, schedule)          (age enters ONLY here, as a rate)
  R4-HOMEO    slow firing-rate homeostatic scaling of incoming weights
  R8-BOUNDS   clamp to weight bounds + competitive normalisation of incoming weights
  R7-STRUCT   slow: prune long-silent weights (adding connections is a flagged extension)
"""

from __future__ import annotations
import math
from typing import Dict, List

from . import params


def _clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return lo if x < lo else hi if x > hi else x


def _smoothstep(t: float) -> float:
    t = _clamp(t)
    return t * t * (3.0 - 2.0 * t)


# --- R3-BCM (workhorse correlation term) ------------------------------------
def bcm_term(a_pre: float, a_post: float, theta: float) -> float:
    """dw ~ a_pre * a_post * (a_post - theta). Above threshold -> potentiation, below ->
    depression; theta (the circuit's own recent activity) gives self-stabilising competition."""
    return a_pre * a_post * (a_post - theta)


def update_theta(theta: float, a_post: float, lr: float = None) -> float:
    """The BCM sliding threshold tracks the circuit's OWN recent mean activity."""
    lr = params.THETA_LR if lr is None else lr
    return theta + lr * (a_post - theta)


# --- R6-DEVGATE: eta(age, schedule) -- age enters only here, as a rate ------
def eta(schedule_ref: str, age_years: float) -> float:
    """Developmental plasticity coefficient. Keyed by the seed's plasticity schedule
    ASSIGNMENT (data); the curve SHAPES are scaffold. Shape families parsed from the ref name
    (developmental timing only -- never the circuit's meaning)."""
    s = (schedule_ref or "").lower()
    hi, lo = params.ETA_BASE_EARLY, params.ETA_ADULT_FLOOR
    if "adolescent" in s:                                   # DA system: adolescent peak
        d = (age_years - params.ADOLESCENT_PEAK_AGE) / params.ADOLESCENT_WIDTH
        return lo + (hi - lo) * math.exp(-d * d)
    if "late" in s:                                         # PFC: protracted, low early/high late
        d = (age_years - params.PFC_LATE_PEAK_AGE) / 8.0
        return lo + (hi - lo) * math.exp(-d * d)
    if "flat" in s or "lifelong" in s:
        return params.ETA_FLAT
    # default (high early -> low adult): "high_early", "childhood", "early", unspecified
    return lo + (hi - lo) * (1.0 - _smoothstep(age_years / params.MATURE_AGE))


# --- maturation(age, schedule): functional CAPACITY, not a plasticity rate (Part 3 S5.4) -----
def maturation(schedule_ref: str, age_years: float, online_age: float = 0.0) -> float:
    """The functional CAPACITY (in [0,1]) a circuit's contribution has reached by `age_years`:
    it rises monotonically from the circuit's onset to a schedule-dependent maturity. Distinct
    from eta (a plasticity RATE): this is how strongly a mature circuit CONTRIBUTES. Late/PFC
    schedules keep rising into the mid-20s; reward ('adolescent') capacities mature by
    mid-adolescence; other circuits mature in childhood. Age enters only as a rate; the schedule
    ASSIGNMENT is seed data, the curve shape is scaffold, and nothing references circuit meaning.
    Feeding this into behaviour selection lets the adolescent-risk imbalance (mature reward vs
    still-maturing control) emerge, rather than being coded."""
    s = (schedule_ref or "").lower()
    if "adolescent" in s:                 # DA/reward system: nonzero floor + mid-adolescent bump
        d = (age_years - params.REWARD_CAP_PEAK_AGE) / params.REWARD_CAP_WIDTH
        bump = math.exp(-d * d)
        return params.REWARD_CAP_FLOOR + (1.0 - params.REWARD_CAP_FLOOR) * bump
    if "late" in s:                       # PFC protracted control (low early, high late)
        mature = params.MATURE_AGE_LATE
    else:                                 # subcortical / early / childhood / flat / moderate
        mature = params.MATURE_AGE_EARLY
    span = max(1e-6, mature - online_age)
    return _smoothstep((age_years - online_age) / span)


# --- R5-NMOD consolidation (gate applied with a modulator FROM A CIRCUIT) ----
def consolidate(eligibility: float, modulator: float, eta_val: float,
                lr: float = None) -> float:
    """Weight change = rate * eta * modulator * eligibility_trace. `modulator` MUST be passed
    in from a neuromodulator circuit's live output by the engine (R5); this function cannot
    fetch or set it, so it cannot smuggle an outcome in."""
    lr = params.BCM_LR if lr is None else lr
    return lr * eta_val * modulator * eligibility


def decay_eligibility(elig: float, dt_ms: float, tau_ms: float) -> float:
    return elig * math.exp(-dt_ms / max(1.0, tau_ms))


# --- R4-HOMEO: slow firing-rate homeostatic scaling of incoming weights -----
def homeo_factor(mean_activity: float, setpoint: float, rate: float = None) -> float:
    """Multiplicative factor applied to a circuit's incoming weights to pull its mean activity
    toward its firing-rate homeostatic_setpoint (from the seed). Over-active -> <1, under -> >1."""
    rate = params.HOMEO_RATE if rate is None else rate
    return 1.0 - rate * (mean_activity - setpoint)


# --- R8-BOUNDS: clamp + competitive normalisation ---------------------------
def clamp_weight(w: float, lo: float, hi: float) -> float:
    return lo if w < lo else hi if w > hi else w


def normalise_incoming(weights: List[float]) -> List[float]:
    """Competitive normalisation: hold the total incoming drive roughly constant, so
    strengthening some connections comes at others' expense (competition is a consequence)."""
    tot = sum(abs(w) for w in weights)
    if tot <= 0:
        return weights
    target = max(1.0, len(weights) * 0.5)   # SCAFFOLD conserved-resource target
    if tot <= target:
        return weights
    scale = target / tot
    return [w * scale for w in weights]
