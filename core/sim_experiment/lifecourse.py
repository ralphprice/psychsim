"""
lifecourse.py -- run one whole life, end to end.

The experiment's unit of observation is a single life course: a seeded
disposition, raised through a sequence of life stages in a configured moral
environment, ending in a classified outcome. This module assembles the three
stages the design specifies -- childhood (home + classroom), the transition
(further education / first job), and adulthood (an occupational role with a risk
profile) -- carrying the SAME person across all of them so the trajectory is
continuous, and reading the outcome from behaviour at the end.

It reuses the affective engine's validated development rule at each stage; the
only thing that changes stage to stage is the environment the person is embedded
in, so the moral environment can differ across the life course (a harsh home
followed by a structured first job, say).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from affective_engine import AffectiveAgent, TraitSeed, classify, Outcome
from affective_engine.development import Environment, develop


# ---------------------------------------------------------------------------
# Environment specification per life stage
# ---------------------------------------------------------------------------

@dataclass
class StageEnv:
    """The moral environment for one life stage, as warmth/structure/recognition
    knobs plus the number of developmental episodes spent in it."""
    name: str
    warmth: float
    structure: float
    recognition: float
    episodes: int

    def to_environment(self) -> Environment:
        return Environment(self.name, self.warmth, self.structure, self.recognition)


@dataclass
class LifeCourseSpec:
    """A full life course: an ordered list of stage environments. Later studies
    vary these; presets are provided in conditions.py."""
    label: str
    stages: List[StageEnv]


# ---------------------------------------------------------------------------
# Result
# ---------------------------------------------------------------------------

@dataclass
class LifeResult:
    seed_name: str
    condition_label: str
    outcome: Outcome
    control_gain: float
    instrumental_control_gain: float
    strategic_access: float
    exploitation_access: float
    classification: str
    psychopathy_subtype: str
    stage_trace: List[str] = field(default_factory=list)   # classification after each stage


def run_life(seed: TraitSeed, spec: LifeCourseSpec,
             situation_seed: int = 20260704, trace: bool = False) -> LifeResult:
    """Raise one agent from `seed` through the stages of `spec`."""
    agent = AffectiveAgent(seed=seed, temperament_seed=situation_seed)
    stage_trace: List[str] = []
    for i, stage in enumerate(spec.stages):
        # a distinct situation stream per stage, but reproducible
        develop(agent, stage.to_environment(), n_episodes=stage.episodes,
                situation_seed=situation_seed + i * 1000)
        if trace:
            stage_trace.append(f"{stage.name}: {classify(agent).classification}")

    o = classify(agent)
    return LifeResult(
        seed_name=seed.name,
        condition_label=spec.label,
        outcome=o,
        control_gain=0.0, instrumental_control_gain=0.0,
        strategic_access=0.0, exploitation_access=0.0,
        classification=o.classification,
        psychopathy_subtype="",
        stage_trace=stage_trace,
    )
