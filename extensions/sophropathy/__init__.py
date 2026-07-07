"""
sophropathy -- the research-specific extension bolted onto the core platform.

Adds the family/society model, the parent-disposition -> caregiving-environment
mechanism, and the seven-stage experimental programme for studying how a fearless
(proto-psychopath / sophropathic) disposition develops toward an adaptive or
antisocial outcome. Depends on the core platform; the core does not depend on it.
"""
from .society import (Family, Society, Environment, parent_to_environment,
                      typical_child_seed, fearless_child_seed, normal_parent_seed,
                      FAMILY_ENVIRONMENTS, CHILD_SEEDS, PARENT_SEEDS)
from .stages import (StageResult, ConditionResult, run_condition,
                     run_stage1, run_stage2, run_stage3, run_stage4,
                     run_stage5, run_stage6, run_stage7, ALL_STAGES)
from .world import (CATEGORIES, NETWORK_CATEGORY, study_category, NORMS,
                    WARM, COOPERATIVE, CONSIDERATE, SELF_DIRECTED, BOISTEROUS,
                    DISRUPTIVE, build_home, build_school, build_workplace,
                    build_community, child_routine, worker_routine)
from .lived import raise_in_world
from .viz_bridge import render_aged_town, render_watchable_town
from .townlife import render_townlife_html, simulate_townlife, build_town_space
from .timeline_driver import make_stepper, make_life_stepper
from .module import MODULE, live_spec          # the pluggable-module registration + live spec
from .report import subject_report, cohort_report, SubjectReport, CohortReport
__all__ = [
    "MODULE", "live_spec",
    "subject_report", "cohort_report", "SubjectReport", "CohortReport",
    "Family", "Society", "Environment", "parent_to_environment",
    "typical_child_seed", "fearless_child_seed", "normal_parent_seed",
    "FAMILY_ENVIRONMENTS", "CHILD_SEEDS", "PARENT_SEEDS",
    "StageResult", "ConditionResult", "run_condition",
    "run_stage1", "run_stage2", "run_stage3", "run_stage4",
    "run_stage5", "run_stage6", "run_stage7", "ALL_STAGES",
    "CATEGORIES", "NETWORK_CATEGORY", "study_category", "NORMS",
    "WARM", "COOPERATIVE", "CONSIDERATE", "SELF_DIRECTED", "BOISTEROUS",
    "DISRUPTIVE", "build_home", "build_school", "build_workplace",
    "build_community", "child_routine", "worker_routine", "raise_in_world", "make_stepper", "make_life_stepper",
]
