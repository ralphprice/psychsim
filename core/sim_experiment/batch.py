"""
batch.py -- the factorial runner.

Crosses the seed factor (trait configuration) with the condition factor (moral
life course), runs each cell across many random seeds, and aggregates the
classified outcomes. Between-seed variation is reported as a quantity in its own
right (the proportion of seeds giving each outcome), following the design's
insistence that seed and model variation are first-class uncertainty rather than
noise to average away.

Everything here is deterministic given the seed range, so a run reproduces.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Tuple
from collections import Counter
import statistics

from affective_engine import TraitSeed

from .lifecourse import LifeCourseSpec, LifeResult, run_life
from .conditions import seeds as default_seeds, conditions as default_conditions


@dataclass
class CellResult:
    seed_name: str
    condition_label: str
    n_runs: int
    classification_counts: Dict[str, int]         # emergent dominant system counts, e.g. {"SEEKING": 27, ...}
    modal_classification: str
    modal_fraction: float                         # share of seeds in the modal outcome

    def summary(self) -> str:
        dist = ", ".join(f"{k} {v}/{self.n_runs}"
                         for k, v in sorted(self.classification_counts.items(),
                                            key=lambda kv: -kv[1]))
        return (f"{self.seed_name:24} x {self.condition_label:30} "
                f"-> {self.modal_classification} ({self.modal_fraction:.0%})  [{dist}]")


def run_cell(seed: TraitSeed, spec: LifeCourseSpec, n_runs: int = 30,
             base_situation_seed: int = 1000) -> CellResult:
    results: List[LifeResult] = [
        run_life(seed, spec, situation_seed=base_situation_seed + r)
        for r in range(n_runs)
    ]
    cls = Counter(r.classification for r in results)
    modal, modal_n = cls.most_common(1)[0]
    return CellResult(
        seed_name=seed.name,
        condition_label=spec.label,
        n_runs=n_runs,
        classification_counts=dict(cls),
        modal_classification=modal,
        modal_fraction=modal_n / n_runs,
    )


@dataclass
class FactorialResult:
    cells: List[CellResult] = field(default_factory=list)

    def table(self) -> str:
        lines = ["FACTORIAL RESULT  (trait configuration x moral life course)",
                 "=" * 92]
        for c in self.cells:
            lines.append("  " + c.summary())
        lines.append("=" * 92)
        return "\n".join(lines)


def run_factorial(n_runs: int = 30, seeds=None, conditions=None) -> FactorialResult:
    """Cross every seed with every condition and run each cell."""
    seeds = seeds if seeds is not None else default_seeds()
    conditions = conditions if conditions is not None else default_conditions()
    fr = FactorialResult()
    for seed_name, seed in seeds.items():
        for cond_label, spec in conditions.items():
            fr.cells.append(run_cell(seed, spec, n_runs=n_runs))
    return fr
