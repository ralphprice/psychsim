"""
daily.py -- a functioning day (universal machinery).

Agents live by a rule-based routine (NOT autonomous planning): a timetable puts
each agent in a place doing an activity, hour by hour. The affective engine
decides HOW they act in the situation the routine puts them in; the world reads
who is co-present (who can witness whom, which role is attending), resolves each
activity into an appraisal the engine settles on and writes to memory, and
assesses the act against the local norms (see norms.py). Over many days this is
a life lived in places that offer real situations.

This module is only the machinery. It ships no routines and no venues -- what a
child's day contains, what a home or a school is, and what conduct is acceptable
where are all supplied by a study as an extension. The core provides the clock,
the placement, the observation read, the engine wiring, and the neutral
norm-assessment; nothing about any particular life.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Set, Tuple
import random

from affective_engine.core import Appraisal, clamp
from .person import Person
from .interior import Venue, Area, Affordance
from .norms import category_of, assess, observer_reaction, Norm

_HOUR_YEARS = 1.0 / (365.25 * 24.0)   # one lived hour, in developmental years (time-normalisation)


# ---------------------------------------------------------------------------
# Routines -- a rule-based timetable (the class; studies supply the content)
# ---------------------------------------------------------------------------

@dataclass
class Block:
    activity: str                 # the activity name; matches an affordance in the area
    venue: str
    area: str


@dataclass
class Routine:
    role: str
    day: Dict[int, Block] = field(default_factory=dict)      # hour -> block
    home_venue: str = ""
    home_area: str = ""

    def at(self, hour: int) -> Block:
        return self.day.get(hour, Block("idle", self.home_venue, self.home_area))


@dataclass
class Inhabitant:
    person: Person
    routine: Routine
    role: Optional[str] = None            # a role the agent occupies (gates role-affordances)


@dataclass
class ActionRecord:
    day: int
    hour: int
    agent: str
    venue: str
    area: str
    activity: str
    action: str
    behaviour: str             # the emergent action taken (Panksepp behaviour), not a category
    observed: bool
    valence: float
    category: Optional[str] = None
    norm_level: int = int(Norm.TOLERATED)
    departure: bool = False               # acted below what this place expects


@dataclass
class DayLog:
    records: List[ActionRecord] = field(default_factory=list)

    def line(self, r: ActionRecord) -> str:
        obs = "seen" if r.observed else "unseen"
        tag = "  <<norm departure>>" if r.departure else ""
        return (f"  {r.hour:02d}:00 {r.agent:10} {r.area:14} {r.activity:11} "
                f"-> {r.action:26} [{r.behaviour}, {obs}]{tag}")

    def transcript(self) -> str:
        return "\n".join(self.line(r) for r in self.records)


# ---------------------------------------------------------------------------
# Resolving an activity into a situation the engine acts on
# ---------------------------------------------------------------------------

def _valence(a: Appraisal) -> float:
    return clamp(0.6 * a.social_valence + 0.4 * a.reward - 0.5 * a.threat
                 - 0.3 * a.provocation, -1.0, 1.0)


def _importance(a: Appraisal) -> float:
    return clamp(max(a.threat, a.provocation, a.reward, a.other_distress))


def _find(area: Area, name: str) -> Optional[Affordance]:
    for aff in area.affordances():
        if aff.name == name:
            return aff
    return None


def _describe(name: str, net: str) -> str:
    word = name if name.endswith(("s", "y", "e")) else name + "s"
    return word


def _resolve_activity(inhab: Inhabitant, block: Block, venue: Venue,
                      observed: bool, roles_here: Set[str],
                      rng: random.Random,
                      categorise: Callable = category_of) -> ActionRecord:
    agent = inhab.person.mind
    area = venue.area(block.area)
    aff = _find(area, block.activity)
    role_present = aff.requires_role in roles_here if (aff and aff.requires_role) else False

    if aff is not None and not aff.available(role_present=role_present, observed=observed):
        aff = None                              # the named action is not available here/now
    appr = aff.to_appraisal() if aff is not None else Appraisal(label=block.activity or "idle")

    # TIME-NORMALISATION: one lived hour of daily life spans one hour of developmental time, so its plasticity
    # accrues on the same clock as childhood development rather than +=1 per hour -- adult daily accrual is thus
    # correctly tiny (~1.1e-4 yr) and a life that chains develop() into daily life stays on ONE clock.
    with agent.engine.developmental_dt(_HOUR_YEARS):
        _resp = agent.social_act(appr)          # the substrate's emergent act
    behaviour = _resp.behaviour                 # the emergent action, not a category
    val = _valence(appr)
    agent.memory.add(appr.label, appr, behaviour, val, _importance(appr))

    # the norm category comes from the AFFORDANCE (a study-defined attribute of the activity),
    # not from the agent's behaviour -- category_of ignores the behaviour arg.
    category = categorise(behaviour, aff)
    level, departure = assess(category, venue.area_norms(block.area))
    return ActionRecord(0, 0, inhab.person.agent_id, venue.name, area.name,
                        block.activity, _describe(block.activity, behaviour), behaviour,
                        observed, val, category=category, norm_level=int(level),
                        departure=departure)


# ---------------------------------------------------------------------------
# The day loop
# ---------------------------------------------------------------------------

def run_day(venues: Dict[str, Venue], inhabitants: Dict[str, Inhabitant],
            day: int = 0, hours: range = range(6, 22),
            rng: Optional[random.Random] = None,
            categorise: Callable = category_of) -> DayLog:
    """Advance one day hour by hour. Each hour: place everyone by routine, read
    observation and attending roles from co-presence, resolve each agent's
    activity through the engine, and assess it against the local norms. A study
    may pass its own `categorise(network, affordance)` to supply how behavioural
    networks map onto its categories; the core default reads only an affordance's
    declared category."""
    rng = rng or random.Random(20260705 + day)
    log = DayLog()
    for hour in hours:
        pos: Dict[str, Block] = {aid: inh.routine.at(hour)
                                 for aid, inh in inhabitants.items()}
        here: Dict[Tuple[str, str], List[str]] = {}
        for aid, b in pos.items():
            here.setdefault((b.venue, b.area), []).append(aid)
        for aid, b in pos.items():
            if b.activity == "idle":
                continue
            occupants = here[(b.venue, b.area)]
            observed = len(occupants) > 1
            roles_here = {inhabitants[o].role for o in occupants
                          if o != aid and inhabitants[o].role}
            rec = _resolve_activity(inhabitants[aid], b, venues[b.venue],
                                    observed, roles_here, rng, categorise)
            rec.day, rec.hour = day, hour
            log.records.append(rec)
    return log


def run_days(venues: Dict[str, Venue], inhabitants: Dict[str, Inhabitant],
             days: int = 5, hours: range = range(6, 22),
             categorise: Callable = category_of) -> List[DayLog]:
    return [run_day(venues, inhabitants, day=d, hours=hours, categorise=categorise)
            for d in range(days)]


def day_summary(logs: List[DayLog], agent_id: str) -> Dict[str, object]:
    """Aggregate one agent's experience across days: mean response valence, the
    mix of behavioural networks it ran, and how often it departed from local
    norms -- the accumulating signal, with no domain labels attached."""
    recs = [r for log in logs for r in log.records if r.agent == agent_id]
    if not recs:
        return {"episodes": 0}
    modes: Dict[str, int] = {}
    for r in recs:
        modes[r.behaviour] = modes.get(r.behaviour, 0) + 1
    return {"episodes": len(recs),
            "mean_valence": round(sum(r.valence for r in recs) / len(recs), 3),
            "norm_departures": sum(1 for r in recs if r.departure),
            "modes": dict(sorted(modes.items(), key=lambda kv: -kv[1]))}
