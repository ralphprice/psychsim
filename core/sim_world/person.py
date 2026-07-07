"""
person.py -- a situated person: the affective agent given a body and a place.

The affective engine (Package 2) decides what a person feels and which
behavioural network is in charge. This module wraps that with the things a
person needs to exist in a world: an identity, an age that advances on the
developmental clock, a body/needs proxy the engine reads, and a `perceive`
method that turns the local world state into an Appraisal the engine can act on.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from affective_engine import AffectiveAgent, TraitSeed
from affective_engine.core import Appraisal

from .world import World, LifeStage, stage_for_age


@dataclass
class Body:
    """A light physiological proxy the affective engine can read and write."""
    arousal: float = 0.3
    fatigue: float = 0.0
    needs: Dict[str, float] = field(default_factory=lambda: {"safety": 0.0,
                                                             "reward": 0.0,
                                                             "belonging": 0.0})


@dataclass
class Person:
    agent_id: str
    name: str
    seed: TraitSeed
    birth_day: int = 0
    body: Body = field(default_factory=Body)
    mind: AffectiveAgent = field(init=False)

    def __post_init__(self) -> None:
        self.mind = AffectiveAgent(seed=self.seed)

    # -- age and stage -----------------------------------------------------
    def age_years(self, world: World) -> float:
        return max(0.0, (world.clock.day - self.birth_day) / 365.0)

    def life_stage(self, world: World) -> LifeStage:
        return stage_for_age(self.age_years(world))

    # -- perception --------------------------------------------------------
    def perceive(self, world: World, event: Optional["SocialEvent"] = None) -> Appraisal:
        """Build the appraisal of the current situation from the local world
        state and any social event directed at this person. The affective engine
        then activates circuits and selects a behavioural network from this."""
        here = world.location_of(self.agent_id)
        inst = world.governing_institution(self.agent_id)
        others = world.co_present(self.agent_id)

        a = Appraisal(label=(event.kind if event else "ambient"))

        # institutional climate colours the baseline social read
        if inst is not None:
            a.social_valence = (inst.warmth - 0.5) * 2.0 * 0.5
            a.controllability = 0.3 + 0.5 * inst.structure

        # body needs raise the relevant appraisal channels
        a.reward = max(a.reward, self.body.needs.get("reward", 0.0))
        a.threat = max(a.threat, self.body.needs.get("safety", 0.0))
        a.exclusion = max(a.exclusion, self.body.needs.get("belonging", 0.0))

        # a directed social event dominates the appraisal
        if event is not None:
            for dim, val in event.appraisal_overrides.items():
                setattr(a, dim, val)
        return a


@dataclass
class SocialEvent:
    """Something that happens to a person and calls for a response: a
    provocation, an offer of cooperation, another's distress, a temptation. The
    experiment layer and the world generate these; `appraisal_overrides` sets the
    appraisal dimensions the event imposes."""
    kind: str
    source_id: Optional[str] = None
    appraisal_overrides: Dict[str, float] = field(default_factory=dict)
