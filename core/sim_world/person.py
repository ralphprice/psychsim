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
from affective_engine.core import Appraisal, clamp

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
    # per-agent seed for this person's PHYSICAL endowment (v10 E1), drawn by the population builder
    # from a SEPARATE rng stream (the main town-layout stream is untouched). None -> physical-neutral.
    physical_seed: Optional[int] = None
    body: Body = field(default_factory=Body)
    mind: AffectiveAgent = field(init=False)       # the substrate-backed agent (its .engine)

    def __post_init__(self) -> None:
        self.mind = AffectiveAgent(seed=self.seed, temperament_seed=self.physical_seed)

    @property
    def engine(self):
        """The person's developing substrate -- owned by its mind (one substrate per person)."""
        return self.mind.engine

    def social_act(self, appraisal: Appraisal, age_years: Optional[float] = None):
        """The person's emergent SOCIAL ACT on the substrate (delegates to its substrate-backed
        mind). Returns a SocialBehaviour (`.behaviour`) the world consumers adjudicate."""
        return self.mind.social_act(appraisal, age_years)

    # -- age and stage -----------------------------------------------------
    def age_years(self, world: World) -> float:
        return max(0.0, (world.clock.day - self.birth_day) / 365.0)

    def life_stage(self, world: World) -> LifeStage:
        return stage_for_age(self.age_years(world))

    # -- perception --------------------------------------------------------
    def perceive(self, world: World, event: Optional["SocialEvent"] = None,
                 partner_rel: Optional[object] = None) -> Appraisal:
        """Build the appraisal of the current situation from the local world
        state and any social event directed at this person. The affective engine
        then activates circuits and selects a behavioural network from this.

        `partner_rel` (duck-typed: `.familiarity`/`.affect`/`.trust`, a
        GameMaster Relationship or None) is the RECORD of this person's history
        with the specific other in the encounter. When present it COLOURS the
        read -- the same situation is appraised differently by someone who
        remembers the other -- but only colours: a directed event still
        dominates. Gains are SCAFFOLD."""
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

        # the RECORD colours the read: history with THIS other shifts the appraisal, ADDING to (not
        # overwriting) the institutional social read. Remembered warmth raises social_valence; low
        # trust raises threat (reusing GameMaster._vigilance_of's own (1 - trust) convention).
        # FAMILIARITY gates the whole read -- a barely-known other colours weakly, so a stranger
        # (familiarity 0) is NOT appraised as a low-trust threat. Gains SCAFFOLD.
        if partner_rel is not None:
            w = clamp(partner_rel.familiarity)
            a.social_valence = clamp(a.social_valence + partner_rel.affect * 0.5 * w, -1.0, 1.0)
            a.threat = clamp(a.threat + (1.0 - partner_rel.trust) * 0.3 * w)

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
