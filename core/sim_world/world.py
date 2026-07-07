"""
world.py -- the physical and institutional world the agents live in.

The world is a navigable graph of Places (a home with rooms; a school with
classrooms, a playground, a staff room; workplaces; public settings), populated
by Objects with affordances, and structured by Institutions (a family, a school,
an employer, a peer group) that carry roles and incentive structures.

Two clocks run: a fine interaction clock (minutes-to-hours, the step at which
social episodes unfold) and a coarse developmental clock (months-to-years, the
step at which people age and change institutions). This module owns the world
state and time; agent cognition lives in the affective engine; the two are
joined by the Game-Master (gamemaster.py).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from enum import Enum


# ---------------------------------------------------------------------------
# Time
# ---------------------------------------------------------------------------

class LifeStage(Enum):
    EARLY_CHILDHOOD = "early_childhood"
    MIDDLE_CHILDHOOD = "middle_childhood"
    ADOLESCENCE = "adolescence"
    TRANSITION = "transition_to_adulthood"
    ADULTHOOD = "established_adulthood"


# boundaries in whole years; the developmental clock crosses these
STAGE_BOUNDARIES = [
    (0, LifeStage.EARLY_CHILDHOOD),
    (6, LifeStage.MIDDLE_CHILDHOOD),
    (12, LifeStage.ADOLESCENCE),
    (18, LifeStage.TRANSITION),
    (25, LifeStage.ADULTHOOD),
]


def stage_for_age(age_years: float) -> LifeStage:
    stage = STAGE_BOUNDARIES[0][1]
    for boundary, s in STAGE_BOUNDARIES:
        if age_years >= boundary:
            stage = s
    return stage


@dataclass
class Clock:
    """Two-rate clock. `tick` advances the interaction clock; `advance_days`
    advances wall-time and, through it, the developmental clock."""
    interaction_step: int = 0          # count of social episodes
    day: int = 0                       # simulated days elapsed

    def tick(self) -> None:
        self.interaction_step += 1

    def advance_days(self, days: int) -> None:
        self.day += days

    @property
    def years(self) -> float:
        return self.day / 365.0


# ---------------------------------------------------------------------------
# Objects and places
# ---------------------------------------------------------------------------

@dataclass
class WorldObject:
    name: str
    affordances: Set[str] = field(default_factory=set)   # e.g. {"sit", "study", "play"}
    properties: Dict[str, str] = field(default_factory=dict)


@dataclass
class Place:
    name: str
    kind: str                                            # "home" | "school" | "workplace" | "public"
    objects: List[WorldObject] = field(default_factory=list)
    connections: Set[str] = field(default_factory=set)   # names of adjacent places
    occupants: Set[str] = field(default_factory=set)     # agent ids currently here

    def affordances(self) -> Set[str]:
        aff: Set[str] = set()
        for o in self.objects:
            aff |= o.affordances
        return aff


# ---------------------------------------------------------------------------
# Institutions
# ---------------------------------------------------------------------------

@dataclass
class Institution:
    """A family, school, employer or peer group. Carries member roles and an
    incentive regime (how it rewards and sanctions conduct) that the experiment
    layer configures and the Game-Master reads when adjudicating outcomes."""
    name: str
    kind: str                                            # "family" | "school" | "employer" | "peer_group"
    roles: Dict[str, str] = field(default_factory=dict)  # agent_id -> role
    # incentive regime, 0..1 knobs the experiment sets:
    warmth: float = 0.5                                  # supportiveness of the climate
    structure: float = 0.5                               # consistency / firmness of limits
    reward_for_cooperation: float = 0.5
    sanction_for_defection: float = 0.5

    def add_member(self, agent_id: str, role: str) -> None:
        self.roles[agent_id] = role

    def members(self) -> List[str]:
        return list(self.roles)


# ---------------------------------------------------------------------------
# The world
# ---------------------------------------------------------------------------

class World:
    def __init__(self) -> None:
        self.places: Dict[str, Place] = {}
        self.institutions: Dict[str, Institution] = {}
        self.clock = Clock()
        self.agent_location: Dict[str, str] = {}         # agent id -> place name

    # -- construction ------------------------------------------------------
    def add_place(self, place: Place) -> Place:
        self.places[place.name] = place
        return place

    def connect(self, a: str, b: str) -> None:
        self.places[a].connections.add(b)
        self.places[b].connections.add(a)

    def add_institution(self, inst: Institution) -> Institution:
        self.institutions[inst.name] = inst
        return inst

    # -- agent placement ---------------------------------------------------
    def place_agent(self, agent_id: str, place_name: str) -> None:
        prev = self.agent_location.get(agent_id)
        if prev and prev in self.places:
            self.places[prev].occupants.discard(agent_id)
        self.places[place_name].occupants.add(agent_id)
        self.agent_location[agent_id] = place_name

    def move_agent(self, agent_id: str, destination: str) -> bool:
        """Move an agent to an adjacent place. Returns False if not reachable."""
        here = self.agent_location.get(agent_id)
        if here is None or destination not in self.places[here].connections:
            return False
        self.place_agent(agent_id, destination)
        return True

    # -- queries -----------------------------------------------------------
    def location_of(self, agent_id: str) -> Optional[str]:
        return self.agent_location.get(agent_id)

    def co_present(self, agent_id: str) -> Set[str]:
        """Other agents in the same place."""
        here = self.agent_location.get(agent_id)
        if here is None:
            return set()
        return self.places[here].occupants - {agent_id}

    def institutions_of(self, agent_id: str) -> List[Institution]:
        return [i for i in self.institutions.values() if agent_id in i.roles]

    def governing_institution(self, agent_id: str) -> Optional[Institution]:
        """The institution whose climate governs the agent's current place
        (the family at home, the school at school, the employer at work)."""
        here = self.agent_location.get(agent_id)
        if here is None:
            return None
        kind = self.places[here].kind
        kind_map = {"home": "family", "school": "school", "workplace": "employer"}
        want = kind_map.get(kind)
        for inst in self.institutions_of(agent_id):
            if inst.kind == want:
                return inst
        return None
