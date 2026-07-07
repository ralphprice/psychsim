"""
config.py -- one point in the parameter space, and how to run it.

A Config is a complete set of parameters for a single simulated life: the child's
disposition, the caregiving environment, and (optionally) a mid-life change of
environment so timing can be explored. run_config develops a child under that
Config and returns both the discrete outcome (the classification) and the
continuous measures that underlie it -- because the bifurcation is really a
transition in the continuous measures, and the classification is a thresholded
view of it.

Nothing here presupposes where the boundary is. The explorer varies these
parameters and reports whatever the mechanism does.
"""

from __future__ import annotations
from dataclasses import dataclass, replace
from typing import Dict, Optional

from affective_engine import AffectiveAgent, TraitSeed, classify
from affective_engine.development import Environment, develop

from affective_engine import shared_root_seed

AUTO = -1.0   # recognition sentinel: derive from warmth & structure


@dataclass
class Config:
    # -- child disposition (defaults: the fearless / proto-psychopath root) ----
    threat: float = 0.30            # fear level (low = fearless)
    care: float = 0.45              # affiliation / empathy
    control_start: float = 0.35     # starting conscience-control (undeveloped)
    instrumental_control: float = 0.35
    seeking: float = 0.78
    # -- caregiving environment (phase 1) -------------------------------------
    warmth: float = 0.50
    structure: float = 0.50
    recognition: float = AUTO       # AUTO -> (warmth + structure) / 2
    # -- optional phase 2 (a later change of environment; None = single phase) -
    phase1_fraction: float = 1.0    # fraction of the childhood spent in phase 1
    warmth2: Optional[float] = None
    structure2: Optional[float] = None
    recognition2: float = AUTO
    # -- development -----------------------------------------------------------
    episodes: int = 48
    situation_seed: int = 20260704
    graded: bool = False   # graded (sigmoid) affordances instead of hard 0.5 cutoffs

    def with_(self, **changes) -> "Config":
        return replace(self, **changes)


def _recognition(warmth: float, structure: float, given: float) -> float:
    return (warmth + structure) / 2.0 if given == AUTO else given


def make_seed(cfg: Config) -> TraitSeed:
    """Build a child disposition from the Config, on the fearless template's
    network accessibilities."""
    seed = shared_root_seed()
    seed.name = "explored"
    seed.gains = dict(seed.gains,
                      THREAT=cfg.threat, ANXIETY=cfg.threat,
                      CARE=cfg.care, CONTROL=cfg.control_start,
                      INSTRUMENTAL_CONTROL=cfg.instrumental_control,
                      SEEKING=cfg.seeking)
    return seed


@dataclass
class RunResult:
    classification: str            # emergent dominant primary system
    profile: dict                  # strength of each primary system (the readout)
    score: float                   # profile_axis: appetitive/affiliative minus aversive


def run_config(cfg: Config) -> RunResult:
    agent = AffectiveAgent(seed=make_seed(cfg), temperament_seed=cfg.situation_seed)
    if cfg.warmth2 is not None and cfg.phase1_fraction < 1.0:
        n1 = max(1, int(round(cfg.episodes * cfg.phase1_fraction)))
        n2 = max(1, cfg.episodes - n1)
        e1 = Environment("p1", cfg.warmth, cfg.structure,
                         _recognition(cfg.warmth, cfg.structure, cfg.recognition))
        e2 = Environment("p2", cfg.warmth2, cfg.structure2,
                         _recognition(cfg.warmth2, cfg.structure2, cfg.recognition2))
        develop(agent, e1, n_episodes=n1, situation_seed=cfg.situation_seed, graded=cfg.graded)
        develop(agent, e2, n_episodes=n2, situation_seed=cfg.situation_seed + 1000, graded=cfg.graded)
    else:
        env = Environment("env", cfg.warmth, cfg.structure,
                          _recognition(cfg.warmth, cfg.structure, cfg.recognition))
        develop(agent, env, n_episodes=cfg.episodes, situation_seed=cfg.situation_seed, graded=cfg.graded)

    o = classify(agent)                      # emergent readout
    from affective_engine.drives import profile_axis
    return RunResult(classification=o.classification, profile=dict(o.profile),
                     score=profile_axis(o.profile))
