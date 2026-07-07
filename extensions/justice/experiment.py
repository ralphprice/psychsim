"""
experiment.py -- does the system manufacture its own subjects?

The comparison the module exists for: identical children (same trait seed,
same situation streams, same seeded randomness) grown in the same base
environment, once with the justice module OFF and once ON. Any difference in
the outcome distribution is attributable to the labelling mechanism alone.

Read the output as a hypothesis generator: 'under these assumed detection and
labelling parameters, the mechanism moves N% of borderline children from
intermediate into the psychopathic basin'. It is a claim about the model, and
a target for the empirical studies -- never a finding about people.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Tuple

from affective_engine.agent import AffectiveAgent
from affective_engine.core import TraitSeed, shared_root_seed
from affective_engine.development import Environment, classify
from .system import JusticeParams, JusticeSystem, develop_with_justice


@dataclass
class CohortResult:
    condition: str                       # "justice_off" | "justice_on"
    outcomes: List = field(default_factory=list)     # drives.MindReadout per child (emergent)
    contacts: List[int] = field(default_factory=list)

    def shares(self) -> Dict[str, float]:
        n = max(1, len(self.outcomes))
        labels = [o.classification for o in self.outcomes]
        return {k: labels.count(k) / n
                for k in ("sophropathic", "intermediate", "psychopathic")}


def _grow(seed_fn: Callable[[], TraitSeed], base_env: Environment,
          child_seed: int, justice: JusticeSystem | None) -> Outcome:
    agent = AffectiveAgent(seed=seed_fn(), temperament_seed=child_seed)
    develop_with_justice(agent, base_env, justice=justice,
                         seed=child_seed, graded=True)
    return classify(agent)


def run_comparison(n_children: int = 40,
                   base_env: Environment | None = None,
                   params: JusticeParams | None = None,
                   seed_fn: Callable[[], TraitSeed] = shared_root_seed,
                   master_seed: int = 20260705
                   ) -> Tuple[CohortResult, CohortResult]:
    """Grow the SAME cohort twice. Child i lives the same situation stream in
    both conditions (situation seed = master_seed + 17*i); the ON condition
    additionally fits a justice system whose detection rolls use their own
    seeded stream (master_seed + 31*i), so OFF/ON differ in the mechanism and
    in nothing else."""
    base_env = base_env or Environment("borderline-adversity", 0.42, 0.45, 0.40)
    params = params or JusticeParams()

    off = CohortResult("justice_off")
    on = CohortResult("justice_on")
    for i in range(n_children):
        child_seed = master_seed + 17 * i

        off.outcomes.append(_grow(seed_fn, base_env, child_seed, None))
        off.contacts.append(0)

        js = JusticeSystem(params=params, seed=master_seed + 31 * i)
        on.outcomes.append(_grow(seed_fn, base_env, child_seed, js))
        on.contacts.append(js.contacts)

    return off, on


def report(off: CohortResult, on: CohortResult) -> str:
    so, sn = off.shares(), on.shares()
    lines = [
        "CRIMINOGENIC-JUSTICE COMPARISON (mechanism, not magnitude)",
        f"  n = {len(off.outcomes)} identical children; base env shared; "
        "only the labelling mechanism differs.",
        "",
        f"  {'outcome':<15}{'justice OFF':>12}{'justice ON':>12}{'delta':>9}",
    ]
    for k in ("sophropathic", "intermediate", "psychopathic"):
        lines.append(f"  {k:<15}{so[k]:>11.1%}{sn[k]:>12.1%}"
                     f"{sn[k]-so[k]:>+9.1%}")
    mean_contacts = sum(on.contacts) / max(1, len(on.contacts))
    labelled = sum(1 for c in on.contacts if c > 0) / max(1, len(on.contacts))
    lines += [
        "",
        f"  mean contacts (ON): {mean_contacts:.2f}; "
        f"children ever labelled: {labelled:.1%}",
        "  Interpretation: any rightward shift in the psychopathic share is",
        "  produced by the labelling mechanism alone under the assumed",
        "  parameters. A hypothesis about the mechanism -- not evidence",
        "  about people.",
    ]
    return "\n".join(lines)
