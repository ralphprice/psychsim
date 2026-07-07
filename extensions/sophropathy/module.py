"""
module.py -- the sophropath study as a pluggable PsychSim module.

This is the reference plug-in: it declares to the neutral core how the study perturbs
the baseline spawn (a fearless minority among the children), what world content it
supplies, how it reads behaviour into its categories, and how it reports. `project.py`
no longer names this study -- it discovers this `MODULE` object.
"""

from __future__ import annotations

from modular import Module

from .society import fearless_child_seed, typical_child_seed
from .world import venues_for, study_category
from .report import report as _cohort_report_hook


def child_source(rng, params):
    """Seed a `fearless_frac` minority as fearless (the proto-psychopath the study
    follows), the rest ordinary. GIVEN temperament only; the outcome emerges."""
    frac = float(params.get("fearless_frac", 0.15))

    def draw():
        return fearless_child_seed() if rng.random() < frac else typical_child_seed()
    return draw


def world_content(city, population, params):
    """The study's world content: its venues (drawn as floor plans) and its reading of
    a settled network into a social category."""
    return {"venues": venues_for(city, population) if population is not None else None,
            "categorise": study_category}


def live_spec(name: str, population: int, seed: int, fearless_frac: float = 0.4,
              profile: str = "england_2021"):
    """The canonical live-engine ProjectSpec for this study -- the SINGLE source of the
    live config, shared by SimEngine and demos so the live and batch spawn paths cannot
    drift. (project imported lazily so this module stays import-cheap.)"""
    from project import ProjectSpec
    return ProjectSpec(name=name, target_population=population, profile=profile,
                       extensions=["sophropathy"],
                       module_params={"sophropathy": {"fearless_frac": fearless_frac}},
                       seed=seed)


MODULE = Module(
    name="sophropathy",
    title="Sophropathy (adaptive / proto-psychopathy)",
    description="Seeds a minority of children with the fearless (proto-psychopath) "
                "disposition and follows how it develops toward an adaptive or antisocial "
                "outcome. Descriptive read-outs only; no verdict.",
    child_source=child_source,
    adult_source=None,                          # keep core default -> no behaviour change
    world_content=world_content,
    categorise=study_category,
    report=_cohort_report_hook,
    default_params={"fearless_frac": 0.15},
)
