"""
sim_experiment -- Package 3 of the life-course simulation platform: the
experimental-manipulation layer. Seeds trait configurations, sets developmental
and moral environments across the life course, runs them as a factorial with
seed replication, and instruments the classified outcomes.

Built on Package 1 (the world) and Package 2 (the affective engine), both
bundled under sim_world/.
"""

from .lifecourse import StageEnv, LifeCourseSpec, LifeResult, run_life
from .conditions import seeds, conditions, SEED_FACTORY, CONDITIONS
from .batch import CellResult, FactorialResult, run_cell, run_factorial

__all__ = [
    "StageEnv", "LifeCourseSpec", "LifeResult", "run_life",
    "seeds", "conditions", "SEED_FACTORY", "CONDITIONS",
    "CellResult", "FactorialResult", "run_cell", "run_factorial",
]

__version__ = "0.1.0"
