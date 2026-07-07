"""
conditions.py -- the two things the experiment manipulates.

Manipulation 1 (trait configuration): which disposition an agent is seeded with.
Manipulation 2 (moral / developmental environment): the life course it is raised
through.  This module names the levels of each factor so the runner (batch.py)
can cross them into a factorial design.
"""

from __future__ import annotations
from typing import Callable, Dict, List

from affective_engine import (TraitSeed, shared_root_seed,
                              shared_root_calculating_seed)

from .lifecourse import StageEnv, LifeCourseSpec


# ---------------------------------------------------------------------------
# Manipulation 1: seeded trait configurations
# ---------------------------------------------------------------------------
# The scientific comparison holds the ROOT disposition fixed and lets the
# environment (Manipulation 2) do the work -- so the two seeds below are the
# shared fearless root, differing only in cold instrumental-control temperament.
# (End-state seeds live in the engine for parameter-recovery, not used here.)

SEED_FACTORY: Dict[str, Callable[[], TraitSeed]] = {
    "shared_root": shared_root_seed,
    "shared_root_calculating": shared_root_calculating_seed,
}


def seeds() -> Dict[str, TraitSeed]:
    return {name: make() for name, make in SEED_FACTORY.items()}


# ---------------------------------------------------------------------------
# Manipulation 2: moral / developmental environments across the life course
# ---------------------------------------------------------------------------
# Each condition is a full life course: childhood (home + school), the
# transition, and adulthood.  Warmth/structure/recognition are the knobs Study 2
# and Study 5 will calibrate; here they are named, contrasting presets.

def _life(label: str, home, school, transition, adult) -> LifeCourseSpec:
    (hw, hs, hr, he), (sw, ss, sr, se) = home, school
    (tw, ts, tr, te), (aw, as_, ar, ae) = transition, adult
    return LifeCourseSpec(label, [
        StageEnv("childhood-home", hw, hs, hr, he),
        StageEnv("childhood-school", sw, ss, sr, se),
        StageEnv("transition", tw, ts, tr, te),
        StageEnv("adulthood", aw, as_, ar, ae),
    ])


# (warmth, structure, recognition, episodes) per stage
CONDITIONS: Dict[str, LifeCourseSpec] = {
    "warm_firm_throughout": _life(
        "warm_firm_throughout",
        home=(0.90, 0.85, 0.85, 30), school=(0.75, 0.80, 0.70, 20),
        transition=(0.70, 0.75, 0.60, 15), adult=(0.65, 0.70, 0.55, 15)),

    "harsh_inconsistent_throughout": _life(
        "harsh_inconsistent_throughout",
        home=(0.20, 0.25, 0.15, 30), school=(0.30, 0.35, 0.20, 20),
        transition=(0.35, 0.30, 0.20, 15), adult=(0.40, 0.35, 0.25, 15)),

    # a harsh home, then a warm, structured turn later -- does a good later
    # environment rescue the trajectory once the sensitive period has passed?
    "harsh_home_then_warm_turn": _life(
        "harsh_home_then_warm_turn",
        home=(0.20, 0.25, 0.15, 30), school=(0.35, 0.40, 0.25, 20),
        transition=(0.80, 0.85, 0.75, 15), adult=(0.80, 0.85, 0.75, 15)),

    # a warm home, then a harsh adult world -- does an early good start protect?
    "warm_home_then_harsh_world": _life(
        "warm_home_then_harsh_world",
        home=(0.90, 0.85, 0.85, 30), school=(0.70, 0.75, 0.65, 20),
        transition=(0.30, 0.30, 0.20, 15), adult=(0.25, 0.30, 0.20, 15)),
}


def conditions() -> Dict[str, LifeCourseSpec]:
    return dict(CONDITIONS)
