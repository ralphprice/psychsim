"""
sim_world -- the world and agent architecture: places, objects, institutions,
memory/history, time, the Game-Master, dialogic interaction, and the universal
spatial-interaction machinery (interiors, access, affordances, the day loop, and
the neutral local-norm mechanism). It ships no venues, routines or behaviour
categories of its own -- a study supplies those as an extension.
"""

from .world import (World, Place, WorldObject, Institution, Clock,
                    LifeStage, stage_for_age)
from .person import Person, Body, SocialEvent
from .gamemaster import (GameMaster, Relationship, Interaction,
                         Utterance, Conversation, institution_to_environment)
from .builder import build_world, WARM_FIRM_PRESET, HARSH_INCONSISTENT_PRESET
from .interior import (Affordance, AffordanceObject, Area, Door, Access, Venue)
from .norms import (Norm, NormProfile, category_of, assess, observer_reaction,
                    departure_magnitude)
from .daily import (Block, Routine, Inhabitant, DayLog, ActionRecord,
                    run_day, run_days, day_summary)
from .population import Household, Population, HouseholdProfile, populate
from .timeline import (TimeScale, Instant, Event, Period, SimClock,
                       TimeController, SCALE_NAMES)
from .relations import (RolePair, Tie, Exchange, Society, interact,
                        PARENT_CHILD, TEACHER_PUPIL, BOSS_EMPLOYEE, COLLEAGUES,
                        TEAMMATES, CAPTAIN_PLAYER, COMMUNITY, STANDARD_TIES)

__all__ = [
    "Thing", "Bond", "EnvironmentMatrix", "encounter",
    "Group", "Membership", "GroupMatrix", "group_encounter",
    "default_groups", "sample_encounter_type",
    "World", "Place", "WorldObject", "Institution", "Clock",
    "LifeStage", "stage_for_age",
    "Person", "Body", "SocialEvent",
    "GameMaster", "Relationship", "Interaction", "Utterance", "Conversation",
    "institution_to_environment",
    "build_world", "WARM_FIRM_PRESET", "HARSH_INCONSISTENT_PRESET",
    "Affordance", "AffordanceObject", "Area", "Door", "Access", "Venue",
    "Norm", "NormProfile", "category_of", "assess", "observer_reaction",
    "departure_magnitude",
    "Block", "Routine", "Inhabitant", "DayLog", "ActionRecord",
    "run_day", "run_days", "day_summary",
    "Household", "Population", "HouseholdProfile", "populate",
    "TimeScale", "Instant", "Event", "Period", "SimClock", "TimeController", "SCALE_NAMES",
    "RolePair", "Tie", "Exchange", "Society", "interact",
    "PARENT_CHILD", "TEACHER_PUPIL", "BOSS_EMPLOYEE", "COLLEAGUES",
    "TEAMMATES", "CAPTAIN_PLAYER", "COMMUNITY", "STANDARD_TIES",
]

__version__ = "0.1.0"

from .environment_matrix import (Thing, Bond, EnvironmentMatrix, encounter)
from .group_matrix import (Group, Membership, GroupMatrix, group_encounter,
                           default_groups, sample_encounter_type)
