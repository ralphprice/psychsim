"""
scan_search.py -- the scan controller's AUTO mode (Part 4 S8): the coarse-to-fine search over
throttle configurations, built ON the trusted primitive (scan.develop_and_measure). It is an
automated caller of the primitive; the substrate is reached ONLY through it, so this layer has no
handle to write the model either.

The objective is the honesty core (S8.3), held STRUCTURALLY:
  * FITNESS IS ONE NAMED MEASURED READ-OUT, recorded BY NAME. An `Objective` names a single key of
    `measure_signatures` and an orientation (+1 if higher = stronger signature, -1 if lower). There
    is NO weighting of read-outs anywhere -- a scan maximises ONE signature; convergence of
    separate single-signature scans on the same configuration is the FINDING, never an assumption
    baked into a blend. (Negative test: no summation over signatures. Positive record: the
    objective name and orientation travel on the result.)
  * IT IS A CONTRAST FROM THE INTACT CONTROL, never a distance to a drawn target. The value is
    `orientation * (config_signature - intact_signature)`: "more of a MEASURED signature than the
    intact control shows." Which configuration does that is the discovery.
  * COARSE-TO-FINE (S8.4): Phase 1 screens single throttles at 0/100 (binary) to find which
    circuits matter at all; Phase 2 grades (25/50/75) ONLY the handful that survived. Never a
    continuous high-dimensional grid.
  * VIABLE-FIRST, PHENOTYPE-SECOND (S8.7): a config that yields a non-viable agent is the expected
    'broken' background -- recorded, never scored on the objective.
  * EVERY FLAGGED 'BEST' IS A HYPOTHESIS, NOT A FINDING (S8.7). Results carry
    status='candidate_hypothesis' and a robustness probe is available: does the signature survive
    perturbing the scaffold? A candidate is promoted only by passing it -- the scan generates
    candidates, it does not validate them.
  * THE TRAJECTORY IS LOGGED, not just the winner -- which circuits mattered, how many configs were
    non-viable, whether the landscape is smooth or knife-edge. Provenance for after-the-fact
    robustness checks.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from scan import (Throttle, throttleable_circuits, develop_and_measure, intact_baseline,
                  ProfileResult, MANIPULATION_SCOPE)


# ---------------------------------------------------------------------------
# The objective -- ONE named read-out, oriented; recorded by name; never blended
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Objective:
    """Fitness = a single named measured read-out, oriented so higher = a stronger signature. NO
    blend of read-outs exists -- this holds exactly one signature key. The orientation is grounded
    and pinned by the primitive's fixed-point tests (dissociation_index rises toward CU -> +1;
    punishment_learning falls toward the CU inversion -> -1)."""
    name: str            # the objective's own name (recorded on the result)
    signature: str       # exactly ONE key of measure_signatures
    orientation: int     # +1 higher = stronger, -1 lower = stronger

    def value(self, result: ProfileResult, baseline: ProfileResult) -> float:
        """The signature's CONTRAST from the intact baseline, oriented so higher = stronger. Never a
        distance to a drawn profile: the reference is the MEASURED intact control, and the target is
        'more signature than intact'."""
        return self.orientation * (result.signatures[self.signature]
                                   - baseline.signatures[self.signature])


# the named objectives a scan may maximise -- each a SINGLE grounded read-out, never a mixture
OBJECTIVES: Dict[str, Objective] = {
    "dissociation": Objective("dissociation", "dissociation_index", +1),
    "punishment_inversion": Objective("punishment_inversion", "punishment_learning", -1),
}

# a config that shifts the objective at least this far above the intact control (averaged over
# seeds) is a Phase-1 SURVIVOR worth grading. SCAFFOLD threshold; recorded on the result.
_SCREEN_DELTA = 0.02


# ---------------------------------------------------------------------------
# One evaluated configuration (a node in the trajectory)
# ---------------------------------------------------------------------------

@dataclass
class Evaluated:
    config: Dict[str, float]        # circuit -> slider (100 = intact)
    objective: Optional[float]      # contrast vs intact (None if not scored because non-viable)
    viable: bool
    phase: int
    signatures_mean: Dict[str, float] = field(default_factory=dict)


@dataclass
class ScanResult:
    """The scan's full record -- the landscape, not just the winner. Carries the objective BY NAME,
    the intact baseline, every evaluated config (the trajectory), the Phase-1 survivors, the best
    VIABLE candidate, and the honesty status."""
    objective: str                  # recorded BY NAME
    signature: str
    orientation: int
    manipulation_scope: str
    baseline: Dict[str, float]      # intact control-arm mean signatures
    survivors: List[str]
    trajectory: List[Evaluated]
    best: Optional[Evaluated]
    status: str = "candidate_hypothesis"   # NEVER "finding" -- promotion needs the robustness probe
    provenance: Dict = field(default_factory=dict)

    def n_non_viable(self) -> int:
        return sum(1 for e in self.trajectory if not e.viable)


# ---------------------------------------------------------------------------
# Evaluation helpers (viable-first, intact-relative, seed-averaged)
# ---------------------------------------------------------------------------

def _mean(xs: List[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def _evaluate(config: Dict[str, Throttle], obj: Objective, seeds: List[int],
              baselines: Dict[int, ProfileResult], phase: int) -> Evaluated:
    """Develop the config across seeds; VIABLE-FIRST -- if any seed is non-viable the config is
    'broken' background and is NOT scored on the objective (S8.7). Otherwise score the objective as
    the mean intact-relative contrast."""
    results = [develop_and_measure(config, s) for s in seeds]
    viable = all(r.viable for r in results)
    sig_mean = {k: _mean([r.signatures[k] for r in results]) for k in results[0].signatures}
    if not viable:
        return Evaluated({c: t.slider for c, t in config.items()}, None, False, phase, sig_mean)
    score = _mean([obj.value(r, baselines[s]) for r, s in zip(results, seeds)])
    return Evaluated({c: t.slider for c, t in config.items()}, score, True, phase, sig_mean)


# ---------------------------------------------------------------------------
# The coarse-to-fine search
# ---------------------------------------------------------------------------

def scan(objective, seeds: List[int], *, circuits: Optional[List[str]] = None,
         screen_delta: float = _SCREEN_DELTA, top_k: int = 3,
         graded_levels: Tuple[float, ...] = (75.0, 50.0, 25.0)) -> ScanResult:
    """Coarse-to-fine search for the throttle configuration that maximises ONE objective, relative
    to the intact control. Phase 1 binary-screens single circuits; Phase 2 grades only the
    survivors. Deterministic from `seeds`. Reaches the substrate only via develop_and_measure ->
    set_throttle (no model handle here).

    `objective` is either the NAME of a built-in search-for-effect objective (a key of OBJECTIVES)
    or any objective INSTANCE exposing `.name`, `.signature`, `.orientation`, and
    `.value(result, baseline)` -- e.g. a search-for-match MatchObjective (scan_match)."""
    if isinstance(objective, str):
        if objective not in OBJECTIVES:
            raise ValueError(f"unknown objective '{objective}'; choose one of {sorted(OBJECTIVES)}")
        obj = OBJECTIVES[objective]
    else:
        obj = objective        # an objective instance (search-for-match, etc.); no model handle either way
    circuits = circuits if circuits is not None else throttleable_circuits()

    # the intact control arm -- every score is relative to this (the contrast IS the result)
    baselines = {s: intact_baseline(s) for s in seeds}
    baseline_mean = {k: _mean([baselines[s].signatures[k] for s in seeds])
                     for k in next(iter(baselines.values())).signatures}

    trajectory: List[Evaluated] = []

    # -- Phase 1: binary screen -- each single circuit fully attenuated (0) vs intact (100) --------
    survivors: List[str] = []
    for cid in circuits:
        e = _evaluate({cid: Throttle.fully_attenuated()}, obj, seeds, baselines, phase=1)
        trajectory.append(e)
        if e.viable and e.objective is not None and e.objective >= screen_delta:
            survivors.append(cid)
    # keep only the strongest few survivors for the graded phase (never grade the whole set)
    def _phase1_score(cid: str) -> float:
        return next((e.objective for e in trajectory
                     if e.phase == 1 and list(e.config) == [cid] and e.objective is not None), 0.0)
    survivors = sorted(survivors, key=_phase1_score, reverse=True)[:top_k]

    # -- Phase 2: graded search -- only the survivors, at graded levels (never a continuous grid) ---
    for cid in survivors:
        for lvl in graded_levels:
            trajectory.append(_evaluate({cid: Throttle.from_slider(lvl)}, obj, seeds, baselines, 2))
    # low-order combinations of survivors, still graded/binary (small, bounded set)
    for i in range(len(survivors)):
        for j in range(i + 1, len(survivors)):
            trajectory.append(_evaluate(
                {survivors[i]: Throttle.fully_attenuated(),
                 survivors[j]: Throttle.fully_attenuated()}, obj, seeds, baselines, 2))

    scored = [e for e in trajectory if e.viable and e.objective is not None]
    best = max(scored, key=lambda e: e.objective) if scored else None

    return ScanResult(
        objective=obj.name, signature=obj.signature, orientation=obj.orientation,
        manipulation_scope=MANIPULATION_SCOPE, baseline=baseline_mean, survivors=survivors,
        trajectory=trajectory, best=best, status="candidate_hypothesis",
        provenance={"seeds": list(seeds), "screen_delta": screen_delta, "top_k": top_k,
                    "graded_levels": list(graded_levels), "n_circuits": len(circuits)},
    )


# ---------------------------------------------------------------------------
# Robustness probe -- what promotes a candidate toward a finding (never automatic)
# ---------------------------------------------------------------------------

def robustness_across_seeds(config: Dict[str, Throttle], objective: str,
                            seeds: List[int]) -> Dict[str, float]:
    """A candidate's first robustness question (S8.7): does the objective contrast hold ACROSS
    developmental streams, or is it an artifact of one seed's random childhood? Returns the
    per-seed objective values so the caller can see spread vs central tendency. This is a
    seed-robustness check; deeper SCAFFOLD-perturbation robustness (does it survive changing an
    uncalibrated constant?) is the further gate a candidate must pass to be reported as a finding --
    the scan generates candidates, it does not validate them."""
    obj = OBJECTIVES[objective]
    out = {}
    for s in seeds:
        r = develop_and_measure(config, s)
        b = intact_baseline(s)
        out[str(s)] = obj.value(r, b) if r.viable else float("nan")
    return out
