"""
learning.py -- RPE learning and anticipatory value (docs/PsychSim_MASTER.md App. C).

Neutral cues (a face, a name, a place, an object, a group emblem) acquire predictive value
by dopaminergic reward-prediction-error learning, bootstrapped from the ONE reward signal --
the computed drive reduction of interocept.py (r = beta*(D_prev - D_now)). This produces
ANTICIPATORY value ("wanting") that pulls behaviour before an outcome, distinct from the
consummatory value ("liking") already felt in interocept. It is what fills the three
matrices (Phase 3).

The learning IS the substrate's own neuromodulated plasticity -- a THREE-FACTOR rule
(Fremaux & Gerstner): a synapse changes as pre x post x neuromodulator, where the
neuromodulator carrying the prediction error delta is dopamine. Oxytocin/opioid are GATES
that license which primary channel's plasticity is enabled; they carry no value. The rule is
local and MEANING-BLIND -- no connection knows what it encodes. All rates are SCAFFOLD.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Optional

from .core import clamp
from . import params


# ---------------------------------------------------------------------------
# The substrate three-factor plasticity rule (the mechanism)
# ---------------------------------------------------------------------------

def three_factor(pre: float, post: float, neuromod: float, window: float = 1.0,
                 lr: Optional[float] = None) -> float:
    """Weight change for ONE connection under the three-factor rule (App. C.4):

        dw = lr * window * pre * post * neuromod

    `pre`/`post` are the co-active endpoints' activity; `neuromod` is the third factor (a
    dopamine reward-prediction-error, or an oxytocin/opioid gate). The rule sees only
    activity and a scalar neuromodulator -- never any label -- so it cannot encode an
    outcome. Developmental gating enters through `window` (window_plasticity)."""
    rate = params.THREE_FACTOR_LR if lr is None else lr
    return rate * window * pre * post * neuromod


def prepared_multiplier(cue: str) -> float:
    """The learning-rate multiplier for a cue carrying a prepared-learning bias (App. B.3).
    NOT an innate value -- a per-cue *speed* prior. Unknown cues -> 1.0."""
    c = (cue or "").lower()
    best = 1.0
    for feature, mult in params.PREPARED_LEARNING.items():
        if feature in c:
            best = max(best, mult)
    return best


# ---------------------------------------------------------------------------
# Anticipatory value: TD/RPE over cues, with a predicted drive-reduction profile
# ---------------------------------------------------------------------------

@dataclass
class CueValue:
    """The learned value of a cue: a scalar anticipatory value AND a predicted per-variable
    drive-reduction profile (App. C.5 -- so the agent can tell WHICH need a cue relieves)."""
    value: float = 0.0
    profile: Dict[str, float] = field(default_factory=dict)
    seen: int = 0


@dataclass
class ValueLearner:
    """A store of learned cue values, updated by temporal-difference RPE. Held per-agent (and
    reused per-matrix in Phase 3: each matrix entry is a CueValue for that person/thing/group,
    App. C.9)."""
    values: Dict[str, CueValue] = field(default_factory=dict)

    def value_of(self, cue: str) -> float:
        cv = self.values.get(cue)
        return cv.value if cv else 0.0

    def profile_of(self, cue: str) -> Dict[str, float]:
        cv = self.values.get(cue)
        return dict(cv.profile) if cv else {}

    def rpe(self, cue: str, r: float, next_value: float = 0.0) -> float:
        """The reward-prediction error delta = r + gamma*V(next) - V(cue) (App. C.3)."""
        return r + params.GAMMA * next_value - self.value_of(cue)

    def anticipated(self, cue: str, drive: Dict[str, float]) -> float:
        """State-dependent anticipated value (App. C.5): the cue's value weighted by how
        much its predicted profile matches the CURRENT per-variable drive `drive` -- so a
        food cue is worth pursuing when hungry, near-worthless when sated. Falls back to the
        scalar value when no profile has been learned yet."""
        cv = self.values.get(cue)
        if not cv:
            return 0.0
        if not cv.profile:
            return cv.value
        return sum(cv.profile.get(k, 0.0) * drive.get(k, 0.0) for k in drive)

    def update(self, cue: str, r: float, drive_profile: Optional[Dict[str, float]] = None,
               next_value: float = 0.0, gate: float = 1.0,
               learning_rate_mult: Optional[float] = None) -> float:
        """One TD/RPE update of a cue's value from an experienced reward `r`
        (dopamine=delta; App. C.3-C.4). Returns delta.

        - `gate` in [0,1] is the oxytocin/opioid plasticity licence (0 = plasticity not
          enabled for this channel; nothing is learned).
        - `learning_rate_mult` overrides the prepared-learning speed prior (else derived
          from the cue).
        - Aversive learning (delta<0) is faster and higher-gain; extinguishing a learned
          aversion (value<0, delta>0) is slower -- the C.8 asymmetries, in one rule."""
        cv = self.values.setdefault(cue, CueValue())
        delta = r + params.GAMMA * next_value - cv.value
        mult = prepared_multiplier(cue) if learning_rate_mult is None else learning_rate_mult
        alpha = params.ALPHA * mult * gate
        if delta < 0:
            alpha *= params.AVERSIVE_LR_MULT
        if cv.value < 0 and delta > 0:
            alpha *= params.EXTINCTION_LR_MULT
        cv.value = clamp(cv.value + alpha * delta, -1.0, 1.0)
        cv.seen += 1
        if drive_profile:
            for k, dv in drive_profile.items():
                cur = cv.profile.get(k, 0.0)
                cv.profile[k] = cur + alpha * (dv - cur)
        return delta
