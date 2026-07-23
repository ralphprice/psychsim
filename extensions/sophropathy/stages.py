"""
stages.py -- the seven-stage experimental programme.

Each stage is a runnable configuration that builds on the one before, following
the design:

  Stage 1  Perfect condition   -- a balanced, functioning society (the reference).
  Stage 2  Imbalance           -- a mix of caring and dysfunctional family types.
  Stage 3  Control             -- typical children developed across those families.
  Stage 4  The manipulation    -- fearless (proto-psychopath/sophropathic)
                                  children across those families.
  Stage 5  Faithful modelling  -- the same, with family and child parameters
                                  CALIBRATED to the human studies (placeholder
                                  calibration until Study 2 / Study 5 provide it).
  Stage 6  Parent effect       -- psychopathic / sophropathic PARENTS (whose
                                  disposition shapes the environment) raising
                                  typical children.
  Stage 7  Full interaction    -- those parents raising fearless children.

Outcomes are read from behaviour by the engine's classifier. Everything is
computed from the stated illustrative parameters; nothing is fitted or invented.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from collections import Counter

from affective_engine import AffectiveAgent, classify, TraitSeed
from affective_engine.development import Environment, develop

from .society import (Family, Society, FAMILY_ENVIRONMENTS, CHILD_SEEDS,
                      PARENT_SEEDS, typical_child_seed, fearless_child_seed,
                      parent_to_environment, normal_parent_seed)

N_DEFAULT = 20          # children per condition
EPISODES = 48


# ---------------------------------------------------------------------------
# Running one condition
# ---------------------------------------------------------------------------

@dataclass
class ConditionResult:
    label: str
    n: int
    distribution: Dict[str, int]       # counts of emergent dominant systems
    modal: str                         # most common dominant system
    mean_profile: Dict[str, float]     # mean strength of each primary system
    mean_axis: float                   # mean appetitive-minus-aversive projection

    def line(self) -> str:
        dist = ", ".join(f"{k} {v}/{self.n}" for k, v in
                         sorted(self.distribution.items(), key=lambda kv: -kv[1]))
        return f"{self.label:42} -> {self.modal:12} ({dist})  axis {self.mean_axis:+.2f}"


def run_condition(label: str, child_seed_fn, env: Environment,
                  n: int = N_DEFAULT, base_seed: int = 1000) -> ConditionResult:
    from substrate.readout import profile_axis
    outs = []
    for i in range(n):
        agent = AffectiveAgent(seed=child_seed_fn(), temperament_seed=base_seed + i)
        develop(agent, env, n_episodes=EPISODES, situation_seed=base_seed + i)
        outs.append(classify(agent))
    dist = Counter(o.classification for o in outs)
    modal = dist.most_common(1)[0][0]
    keys = list(outs[0].profile) if outs else []
    mean_profile = {k: sum(o.profile.get(k, 0.0) for o in outs) / n for k in keys}
    mean_axis = sum(profile_axis(o.profile) for o in outs) / n
    return ConditionResult(label=label, n=n, distribution=dict(dist), modal=modal,
                           mean_profile=mean_profile, mean_axis=mean_axis)


# ---------------------------------------------------------------------------
# Stage 1 -- perfect condition
# ---------------------------------------------------------------------------

@dataclass
class StageResult:
    stage: int
    title: str
    society: Optional[Society] = None
    conditions: List[ConditionResult] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)


def run_stage1(n_families: int = 30) -> StageResult:
    """A balanced, functioning society: ordinary parents, caring homes. The
    reference against which imbalance is later introduced."""
    fams = [Family("caring", FAMILY_ENVIRONMENTS["caring"],
                   parent_seed=normal_parent_seed()) for _ in range(n_families)]
    soc = Society("perfect_condition", fams)
    prof = soc.environment_profile()
    return StageResult(1, "Perfect condition (balanced society)", society=soc,
                       notes=[f"{prof['families']} families, all caring/balanced",
                              f"mean warmth {prof['mean_warmth']:.2f}, "
                              f"mean structure {prof['mean_structure']:.2f}",
                              "no children developing yet; this fixes the reference environment"])


# ---------------------------------------------------------------------------
# Stage 2 -- introduce imbalance
# ---------------------------------------------------------------------------

def run_stage2(counts=None) -> StageResult:
    """Introduce conflict and imbalance: a mix of caring, balanced and
    dysfunctional family types."""
    counts = counts or {"caring": 12, "balanced": 8, "dysfunctional": 10}
    fams = []
    for ftype, k in counts.items():
        fams += [Family(ftype, FAMILY_ENVIRONMENTS[ftype]) for _ in range(k)]
    soc = Society("imbalanced_society", fams)
    prof = soc.environment_profile()
    return StageResult(2, "Introduce imbalance (mixed family types)", society=soc,
                       notes=[f"family mix: {counts}",
                              f"mean warmth {prof['mean_warmth']:.2f}, "
                              f"mean structure {prof['mean_structure']:.2f}",
                              "the environmental landscape children will develop in"])


# ---------------------------------------------------------------------------
# Stage 3 -- control: typical children across family types
# ---------------------------------------------------------------------------

def run_stage3(n: int = N_DEFAULT) -> StageResult:
    conds = [run_condition(f"typical child / {ftype} family", typical_child_seed,
                           env, n=n)
             for ftype, env in FAMILY_ENVIRONMENTS.items()]
    return StageResult(3, "Control: typical children across family types",
                       conditions=conds,
                       notes=["the control: how ordinary children fare by family type",
                              "expect robustness -- ordinary fear tends to yield anxiety/"
                              "withdrawal in harsh homes, not callousness"])


# ---------------------------------------------------------------------------
# Stage 4 -- fearless (proto-psychopath/sophropathic) children across family types
# ---------------------------------------------------------------------------

def run_stage4(n: int = N_DEFAULT) -> StageResult:
    conds = [run_condition(f"fearless child / {ftype} family", fearless_child_seed,
                           env, n=n)
             for ftype, env in FAMILY_ENVIRONMENTS.items()]
    return StageResult(4, "Manipulation: fearless children across family types",
                       conditions=conds,
                       notes=["the core manipulation: same fearless disposition, different homes",
                              "expect divergence -- caring -> sophropathic, dysfunctional -> "
                              "psychopathic -- and greater sensitivity than the typical child"])


# ---------------------------------------------------------------------------
# Stage 5 -- faithful modelling (calibrated; placeholder until real data)
# ---------------------------------------------------------------------------

# PLACEHOLDER calibration. These are NOT empirical values. They stand in until
# Study 2 (family environments) and Study 5 (child profiles) provide real
# distributions, at which point this dict is replaced with the fitted values.
CALIBRATION_PLACEHOLDER = {
    "family_type_prevalence": {"caring": 0.45, "balanced": 0.35, "dysfunctional": 0.20},
    "source": "PLACEHOLDER -- replace with Study 2 / Study 5 findings before use",
}


def run_stage5(n: int = N_DEFAULT, calibration: Optional[dict] = None) -> StageResult:
    cal = calibration or CALIBRATION_PLACEHOLDER
    prev = cal["family_type_prevalence"]
    # weight each family type's contribution by its (placeholder) prevalence
    conds = []
    for ftype, env in FAMILY_ENVIRONMENTS.items():
        weight = prev.get(ftype, 0.0)
        k = max(1, round(n * weight / max(prev.values())))
        conds.append(run_condition(
            f"fearless child / {ftype} (prev {weight:.2f})",
            fearless_child_seed, env, n=k))
    return StageResult(5, "Faithful modelling (calibrated distribution)",
                       conditions=conds,
                       notes=[f"family-type prevalence: {prev}",
                              f"calibration source: {cal['source']}",
                              "structure is ready; parameters await the human studies"])


# ---------------------------------------------------------------------------
# Stage 6 -- psychopathic/sophropathic PARENTS raising typical children
# ---------------------------------------------------------------------------

def run_stage6(n: int = N_DEFAULT) -> StageResult:
    conds = []
    for ptype, seed_fn in PARENT_SEEDS.items():
        env = parent_to_environment(seed_fn())
        conds.append(run_condition(
            f"typical child / {ptype} parent "
            f"(w{env.warmth:.2f} s{env.structure:.2f})",
            typical_child_seed, env, n=n))
    return StageResult(6, "Parent effect: dispositional parents, typical children",
                       conditions=conds,
                       notes=["the parent's disposition shapes the environment "
                              "(warmth from CARE, structure from CONTROL)",
                              "tests the parent -> environment -> child pathway",
                              "★ TRANSMISSION CLAIM WITHDRAWN (prototype item 2b): parent_to_environment is a hand-authored scaffold (invented coeffs; parent never an agent; PARENT_SEEDS uses developed end-states as inputs). This stage RUNS as a scaffold demo; no grounded transmission claim rests on it until parent-as-agent is built."])


# ---------------------------------------------------------------------------
# Stage 7 -- dispositional parents raising fearless children
# ---------------------------------------------------------------------------

def run_stage7(n: int = N_DEFAULT) -> StageResult:
    conds = []
    for ptype, seed_fn in PARENT_SEEDS.items():
        env = parent_to_environment(seed_fn())
        conds.append(run_condition(
            f"fearless child / {ptype} parent "
            f"(w{env.warmth:.2f} s{env.structure:.2f})",
            fearless_child_seed, env, n=n))
    return StageResult(7, "Full interaction: dispositional parents, fearless children",
                       conditions=conds,
                       notes=["heritable disposition AND parent-shaped environment together",
                              "fearless child + sophropathic parent vs + psychopathic parent: "
                              "same disposition, opposite outcome -- transmission via environment",
                              "★ TRANSMISSION CLAIM WITHDRAWN (prototype item 2b): the 'opposite outcome via "
                              "environment' claim rests on the hand-authored parent_to_environment scaffold "
                              "(invented coeffs; parent never an agent; PARENT_SEEDS feeds developed end-states "
                              "as inputs). Scaffold demo only; no grounded transmission claim rests on it until "
                              "parent-as-agent is built."])


ALL_STAGES = [run_stage1, run_stage2, run_stage3, run_stage4,
              run_stage5, run_stage6, run_stage7]
