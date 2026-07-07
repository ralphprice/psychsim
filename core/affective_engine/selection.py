"""
selection.py -- behaviour selection as basal-ganglia action selection (App. F).

Several incompatible action tendencies are active at once; only one reaches the effectors.
Selection turns the parallel pulls into a single action WITHOUT a coded arbiter: candidate
values accumulate to a threshold via striatum->pallidum disinhibition (Go release / NoGo
suppression / STN global hold); dopamine sets the gain; the executive BIASES the
competition's parameters but never picks the winner (App. F.5). Internal conflict,
approach-avoidance paralysis, impulsivity and the adolescent risk gradient all EMERGE.

The honesty wall at the effector bottleneck: the outcome is a property of which channel
accumulates fastest given its value, the current drive, the dopaminergic gain and the
executive's parameter settings -- not a rule that reads the situation and outputs a
behaviour. All rates/thresholds are SCAFFOLD (params.py).
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .core import clamp
from . import params


def _smoothstep(t: float) -> float:
    t = 0.0 if t < 0 else 1.0 if t > 1 else t
    return t * t * (3.0 - 2.0 * t)


def reward_gain(age_years: float) -> float:
    """The reward / sensation-seeking system (App. F.7; Steinberg): CURVILINEAR -- rises
    through childhood, peaks in mid-adolescence, declines toward an adult floor."""
    d = (age_years - params.SEL_REWARD_PEAK_AGE) / params.SEL_REWARD_WIDTH
    return 0.2 + 0.8 * math.exp(-(d * d))


def brake_capacity(age_years: float) -> float:
    """The prefrontal->STN control brake (App. F.7): rises monotonically from a late onset
    into the mid/late-20s."""
    span = params.SEL_BRAKE_MATURE_AGE - params.SEL_BRAKE_ONSET_AGE
    return _smoothstep((age_years - params.SEL_BRAKE_ONSET_AGE) / span)


def dopamine_gain(dopamine: float) -> float:
    """Tonic-dopamine -> Go gain, as an inverted-U (Cools): too little or too much impairs
    selection; the peak is the operating point."""
    d = dopamine - params.SEL_DOPAMINE_PEAK
    inverted_u = 1.0 - (d / max(1e-6, params.SEL_DOPAMINE_PEAK)) ** 2 if dopamine < 2 * params.SEL_DOPAMINE_PEAK else 0.0
    return params.SEL_GO_BASE + params.SEL_DOPAMINE_GAIN * clamp(inverted_u)


@dataclass
class Candidate:
    """A potential action competing for the effector bottleneck (App. F.2)."""
    name: str
    anticipated_value: float = 0.0                       # learned value of its outcome (+/-)
    drive_profile: Dict[str, float] = field(default_factory=dict)  # which drives it predicts relieving
    prepotent: float = 0.0                               # reflexive/habitual base strength

    def matched(self, drive: Dict[str, float]) -> float:
        """Anticipated value read AGAINST the current drive (App. F.2 / C.5): a food-seeking
        candidate is strong when hungry, weak when sated. This is the goal-directed
        component; the reflexive/reward `prepotent` component is added by select() scaled by
        the maturing reward system."""
        if self.drive_profile:
            return sum(self.drive_profile.get(k, 0.0) * drive.get(k, 0.0) for k in drive)
        return self.anticipated_value


@dataclass
class ExecutiveBias:
    """The executive sets PARAMETERS of the competition, never the outcome (App. F.5).
    Populated from executive maturation/monitoring; a parameter-setter, not a decider."""
    threshold_add: float = 0.0                           # proactive: raise the bar
    nogo: Dict[str, float] = field(default_factory=dict)  # per-candidate NoGo pre-load
    stn_hold: float = 0.0                                # reactive global hold (0..1)


def bias_from_maturation(age_years: float, monitors: Optional[Dict[str, float]] = None
                         ) -> ExecutiveBias:
    """Derive the executive's parameter settings from its maturation (a weak brake in
    childhood; App. F.7) plus any learned inhibitory monitors (which candidates to hold)."""
    cap = brake_capacity(age_years)
    return ExecutiveBias(threshold_add=0.0, stn_hold=cap,
                         nogo={k: cap * v for k, v in (monitors or {}).items()})


@dataclass
class SelectionOutcome:
    winner: Optional[str]
    steps: int                          # accumulation steps to commit (many = high conflict)
    conflict: float                     # 0..1 closeness of the leading candidates
    committed: bool                     # did anything cross threshold within the cap
    accumulators: Dict[str, float]


def select(candidates: List[Candidate], drive: Dict[str, float], dopamine: float = 0.6,
           bias: Optional[ExecutiveBias] = None, age_years: float = 30.0) -> SelectionOutcome:
    """Run the accumulation-to-threshold competition and return the winner. Close values ->
    slow, effortful, high-conflict decisions; a dominant value -> fast commitment
    (Bogacz & Gurney)."""
    bias = bias or ExecutiveBias()
    gain = dopamine_gain(dopamine)
    rgain = reward_gain(age_years)   # the reward/impulse system matures early (App. F.7)
    acc = {c.name: 0.0 for c in candidates}
    # channel input = dopaminergic gain x (goal-directed value + matured reward/impulse
    # drive) minus the executive's NoGo pre-load. Reward maturation lifts the prepotent
    # (impulse) component specifically -- so an immature child is not yet impulse-driven.
    inputs = {c.name: gain * (c.matched(drive) + rgain * c.prepotent)
              - bias.nogo.get(c.name, 0.0)
              for c in candidates}
    # STN global hold scales the threshold with the executive's reactive hold AND the number
    # of near-equal competitors (the hyperdirect "hold your horses"; Frank).
    n_active = sum(1 for v in inputs.values() if v > 0)
    stn = params.SEL_STN_HOLD_GAIN * bias.stn_hold * max(0, n_active - 1)
    threshold = params.SEL_THRESHOLD + bias.threshold_add + stn

    dt, leak, lat = params.SEL_DT, params.SEL_LEAK, params.SEL_LATERAL
    for step in range(1, params.SEL_MAX_STEPS + 1):
        total = sum(max(0.0, a) for a in acc.values())
        for name in acc:
            surround = lat * (total - max(0.0, acc[name]))
            acc[name] = acc[name] + dt * (inputs[name] - leak * acc[name] - surround)
        ranked = sorted(acc.values(), reverse=True)
        top = ranked[0]
        if top >= threshold:
            winner = max(acc, key=acc.get)
            second = ranked[1] if len(ranked) > 1 else 0.0
            conflict = clamp(1.0 - (top - second) / max(1e-6, top))
            return SelectionOutcome(winner, step, conflict, True, dict(acc))
    # no commitment within the cap -> deadlocked conflict (approach-avoidance paralysis)
    ranked = sorted(acc.values(), reverse=True)
    top = ranked[0] if ranked else 0.0
    second = ranked[1] if len(ranked) > 1 else 0.0
    conflict = clamp(1.0 - (top - second) / max(1e-6, abs(top) + 1e-6))
    winner = max(acc, key=acc.get) if acc else None
    return SelectionOutcome(winner, params.SEL_MAX_STEPS, conflict, False, dict(acc))


def bis_arousal(outcome: SelectionOutcome) -> float:
    """The behavioural-inhibition-system feedback (App. F.6): an unresolved approach/avoid
    near-tie holds arousal elevated. Returns an arousal increment for interocept, largest
    when the decision was high-conflict and/or failed to commit."""
    unresolved = 1.0 if not outcome.committed else 0.0
    return params.SEL_BIS_AROUSAL_GAIN * outcome.conflict * (0.5 + 0.5 * unresolved)
