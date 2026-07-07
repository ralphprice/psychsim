"""
interocept.py -- the one valence engine (docs/PsychSim_MASTER.md Part I, App. A & B).

The agent carries an interoceptive/homeostatic STATE VECTOR of regulated body/need
variables with set-points. Its weighted distance from set-point is DRIVE; the REDUCTION of
drive by an outcome is VALENCE:

    D    = Σ_k  w_k · deviation(H_k, H*_k)
    r    = BETA · ( D_prev − D_now )

Value is therefore COMPUTED from the agent's own state, never stipulated. The same external
event produces different r in agents with different set-points / weights / reactivities --
which is what makes "a punishment for one is a reward for another" true rather than decreed.

The honesty wall at the input: the state holds only regulated variables; threats, rewards,
people and objects are PERTURBATIONS that move them (App. A.1). The only innate event->value
links are the small, cited primary-reinforcer set in PERTURBATION_LINKS (App. B); everything
richer is learned (Phase 2, learning.py). Structure here is the grounded claim; all
magnitudes live in params.py as SCAFFOLD.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple

from .core import clamp
from . import params

# The variable names, in a stable order. Definitions (set-point/weight/polarity/allostatic)
# come from params.STATE_VARIABLES.
VARIABLES: Tuple[str, ...] = tuple(params.STATE_VARIABLES.keys())

# The innate perturbation SET: which trigger moves which variables (the grounded claim).
# Magnitudes are params.PERTURBATION_GAINS (scaffold). Derived here so the two stay in sync.
PERTURBATION_LINKS = {trig: tuple(gains.keys())
                      for trig, gains in params.PERTURBATION_GAINS.items()}


def _deviation(level: float, set_point: float, polarity: str) -> float:
    """Aversive distance from set-point (>=0). 'deficit': being below hurts; 'excess':
    being above hurts."""
    if polarity == "excess":
        return max(0.0, level - set_point)
    return max(0.0, set_point - level)


@dataclass
class StateVector:
    """The interoceptive state: a level per variable, plus per-variable set-points and
    weights (endowment; overridable). Set-points on allostatic variables may be shifted by
    development/epigenetics later (Phase 5); the structure to do so is here."""
    levels: Dict[str, float] = field(default_factory=dict)
    set_points: Dict[str, float] = field(default_factory=dict)
    weights: Dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name, spec in params.STATE_VARIABLES.items():
            self.levels.setdefault(name, spec["set_point"])
            self.set_points.setdefault(name, spec["set_point"])
            self.weights.setdefault(name, spec["weight"])

    # -- drive ------------------------------------------------------------
    def deviations(self) -> Dict[str, float]:
        out = {}
        for name in VARIABLES:
            spec = params.STATE_VARIABLES[name]
            out[name] = _deviation(self.levels[name], self.set_points[name],
                                   spec["polarity"])
        return out

    def drive(self) -> Tuple[Dict[str, float], float]:
        """Return (per-variable drive d_k = w_k·deviation_k, scalar aggregate D).
        The vector says *what to do about it*; the scalar says *how good/bad* (App. A.1)."""
        dev = self.deviations()
        per = {name: self.weights[name] * dev[name] for name in VARIABLES}
        return per, sum(per.values())

    def scalar_drive(self) -> float:
        return self.drive()[1]

    def copy(self) -> "StateVector":
        return StateVector(dict(self.levels), dict(self.set_points), dict(self.weights))


def newborn_state() -> StateVector:
    """A state at every set-point (zero drive) -- the blank homeostatic starting point."""
    return StateVector()


def reference_child_state() -> StateVector:
    """A state carrying the mild ongoing deficits a developing agent sits in, so that an
    outcome's relief or deepening of a need registers as valence (App. A / params)."""
    return StateVector(levels=dict(params.REFERENCE_CHILD_LEVELS))


# ---------------------------------------------------------------------------
# Applying events (perturbations) and computing valence
# ---------------------------------------------------------------------------

def apply_event(state: StateVector, triggers: Dict[str, float]) -> StateVector:
    """Return a NEW state with the event's innate perturbations applied. `triggers` maps a
    perturbation name (App. B) to an intensity in [0,1]; each scales that trigger's scaffold
    gains. Unknown triggers are ignored (they carry no innate value -- learned only)."""
    new = state.copy()
    for trig, intensity in triggers.items():
        gains = params.PERTURBATION_GAINS.get(trig)
        if not gains or intensity == 0:
            continue
        for var, g in gains.items():
            if var in new.levels:
                new.levels[var] = clamp(new.levels[var] + g * intensity)
    return new


def valence(d_prev: float, d_now: float) -> float:
    """The one valuation: drive reduction, scaled. Positive = state moved toward set-point."""
    return params.BETA * (d_prev - d_now)


# ---------------------------------------------------------------------------
# Reading the state vector FROM the live substrate (Part 2 S2.5 -- 8b bridge)
# ---------------------------------------------------------------------------

# Each interoceptive state VARIABLE reads its activity from designated v7 substrate circuits,
# grounding the vector's structure in the substrate. The set-point MAGNITUDES stay SCAFFOLD
# (params, above) -- they are NOT read from the seed's firing-rate homeostatic_setpoint, which
# is a different quantity (S2.5). Mode 'level' = the variable level tracks the circuits' mean
# activity; 'inverse' = the level is high when those circuits are quiet (pain / a deficit
# signalled by an active afferent). The exact mapping is a functional-layer choice, flagged
# for calibration; the grounding (which circuits) is the claim.
SUBSTRATE_READOUT = {
    "arousal":          (("RVLM", "SympOut", "PVN"), "level"),    # sympathetic/HPA drive
    "tissue_integrity": (("PBN", "pIns"), "inverse"),            # pain afferents -> integrity down
    "respiratory":      (("PBN",), "inverse"),                    # air-hunger afferent (coarse)
    "attachment":       (("PVN-OT", "SEPT", "MPOA"), "level"),    # bonding / affiliation
    "belonging":        (("PVN-OT", "SEPT"), "level"),
    "energy":           (("NTS",), "level"),                      # visceral afferent hub (coarse)
    "hydration":        (("NTS",), "level"),
    "thermal":          (("PBN",), "level"),
    "rest":             (("PPTg",), "inverse"),                   # arousal-promoting -> low rest
    "uncertainty":      (("aIns",), "level"),                     # salience / prediction error
}


def state_from_substrate(engine, weights: Optional[Dict[str, float]] = None) -> StateVector:
    """Build a StateVector whose variable LEVELS are read from the live substrate engine
    (duck-typed: `.activity(cid)` + `.model.circuits`), per S2.5. Set-points/weights stay
    scaffold. This is the substrate->interoception bridge: drive and valence then compute
    over substrate activity, so the same event yields different value in different agents
    because their substrates differ."""
    sv = StateVector(weights=dict(weights or {}))
    circuits = getattr(getattr(engine, "model", None), "circuits", {})
    for var, (cids, mode) in SUBSTRATE_READOUT.items():
        acts = [engine.activity(c) for c in cids if c in circuits]
        a = sum(acts) / len(acts) if acts else 0.0
        sv.levels[var] = clamp(1.0 - a) if mode == "inverse" else clamp(a)
    return sv


def valence_of_event(state: StateVector, triggers: Dict[str, float]
                     ) -> Tuple[float, StateVector, Dict[str, float]]:
    """Compute the valence of an event from a given state: apply its perturbations, and
    return (r, new_state, per_variable_drive_reduction). The per-variable profile records
    *which* drives moved (feeds the anticipatory-value learning of Phase 2 / App. C.5)."""
    per_prev, d_prev = state.drive()
    new = apply_event(state, triggers)
    per_now, d_now = new.drive()
    reduction = {name: per_prev[name] - per_now[name] for name in VARIABLES}
    return valence(d_prev, d_now), new, reduction
