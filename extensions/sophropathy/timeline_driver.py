"""
timeline_driver.py -- driving a spawned universe through time (study extension).

Supplies the `world_step(clock, minutes)` the core TimeController needs: over a
span of simulated minutes it runs relational exchanges across the society and
emits EVENTS on state transitions -- a tie strains, ruptures or repairs -- plus a
cohesion snapshot as days roll over and a milestone each year. Emitting on
transition (not on every interaction) keeps the stream meaningful whether you are
watching in real time or fast-forwarding by the year.

This is study-specific event semantics; the core clock and controller are neutral.
"""

from __future__ import annotations
import random
from typing import Callable, List

from sim_world import Event, interact
from sim_world.timeline import MIN_PER_DAY, DAYS_PER_YEAR


def make_stepper(universe, seed: int = 0) -> Callable:
    """Build a world_step over `universe` for a TimeController. Interactions scale
    with the span; events fire on relational state transitions."""
    persons = universe.population.persons
    ties = universe.population.society.ties
    rng = random.Random(seed)
    prev_state = {id(t): t.state() for t in ties}
    last_year = [0]

    def world_step(clock, minutes: int) -> List[Event]:
        evs: List[Event] = []
        start = clock.total_minutes
        n = min(400, max(1, minutes // 45))          # ~an exchange per 45 sim-minutes
        for _ in range(n):
            t = rng.choice(ties)
            hi, lo = persons.get(t.higher), persons.get(t.lower)
            if not hi or not lo:
                continue
            ex = interact(t, hi.mind, lo.mind)
            at = start + rng.randint(0, max(1, minutes))
            # always emit the interaction itself, so real-time shows activity
            evs.append(Event(at, "interaction", t.higher,
                             f"{t.higher} & {t.lower}: {t.pair.kind} ({ex.state})"))
            was = prev_state[id(t)]
            now = ex.state
            if now != was:                           # and flag state transitions
                if now == "ruptured":
                    evs.append(Event(at, "rupture", t.higher,
                                     f"{t.pair.kind} {t.higher}->{t.lower} ruptured"))
                elif now in ("warm", "working") and was in ("strained", "ruptured"):
                    evs.append(Event(at, "repair", t.higher,
                                     f"{t.pair.kind} {t.higher}->{t.lower} repaired"))
                elif now == "strained":
                    evs.append(Event(at, "strain", t.higher,
                                     f"{t.pair.kind} {t.higher}->{t.lower} strained"))
                prev_state[id(t)] = now
        clock.advance(minutes)
        # a cohesion snapshot at the end of the span; a milestone each year
        evs.append(Event(clock.total_minutes, "cohesion",
                         text=f"cohesion {universe.population.society.cohesion():.0%}"))
        yr = (clock.total_minutes // MIN_PER_DAY) // DAYS_PER_YEAR
        if yr > last_year[0]:
            last_year[0] = yr
            evs.append(Event(clock.total_minutes, "milestone",
                             text=f"year {yr}: cohesion {universe.population.society.cohesion():.0%}, "
                                  f"{len(universe.population.society.strained())} ties strained"))
        return evs

    return world_step


def make_life_stepper(universe, venues=None, seed: int = 0,
                      childhood_years: float = 18.0, episodes_per_year: float = 3.0,
                      graded: bool = True):
    """Build a world_step in which ADVANCING THE CLOCK AGES THE POPULATION.

    Each child lives developmental episodes through their days -- situations from
    their own home and school -- fed to the substrate via live_moment, with the
    plasticity-gating environment derived from their home's parenting climate and
    the parent-child tie. As simulated years pass, children age through the life
    stages and, at the end of childhood, reach a CLASSIFIED OUTCOME. The society's
    relational dynamics tick alongside. Events surface at whatever scale the clock
    is run: interactions and stage transitions close up, outcomes and cohesion as
    milestones when fast-forwarding.

    This connects the three layers -- the clock, the day/situation stream, and the
    development rule -- into one running instrument. It is a test-bed: the outcomes
    are produced by the mechanism as it runs, illustrative of the model, not
    evidence about people.
    """
    from affective_engine.core import clamp
    from affective_engine.development import (live_moment, live_stimulus,
                                              Environment, situation, CHILDHOOD_CYCLE)
    from affective_engine.activities import sample_activity
    from affective_engine.executive import (Executive, monitor_executive,
                                            install_monitors_from_memory)
    from affective_engine.core import Appraisal
    from substrate.readout import read_mind
    from sim_world.timeline import MIN_PER_DAY, DAYS_PER_YEAR
    from sim_world.environment_matrix import (default_things, birth_matrix, encounter)
    from sim_world.group_matrix import (default_groups, GroupMatrix,
                                        group_encounter, sample_encounter_type)
    from .world import venues_for, build_school

    pop = universe.population
    if venues is None:
        venues = venues_for(universe.city, pop)
    school = next((v for k, v in venues.items() if k.startswith("school")), build_school())

    home_of = {c: hh.home for hh in pop.households for c in hh.children}
    tie_standing = {t.lower: t.standing for t in pop.society.ties
                    if t.pair.kind == "parent-child"}

    rng = random.Random(seed)
    total_ep = max(6.0, childhood_years * episodes_per_year)
    world_things = default_things()      # the ordinary things a child meets
    world_groups = default_groups()      # the groups a child belongs to
    DELIBERATIVE = {"learning", "achievement", "independence", "exploration"}

    def _episode(d):
        """One developmental step at the child's current age: a lived situation on
        the substrate, AND an encounter with one of the world's things -- so the
        child's inventory of attractions and aversions builds and evolves over the
        childhood alongside their development, from inherited birth leans outward."""
        age = min(1.0, d["age"])
        age_years = d["age"] * childhood_years
        idx = int(d["age"] * total_ep)
        if idx % 3 == 2 and d["sits"]:
            # the home/school's own situations -- environmental grounding
            appr = rng.choice(d["sits"])
            live_moment(d["mind"], appr, age_years=age_years)
        else:
            # a significant, age-appropriate life-activity -- the rich diet that
            # fills a life (play, learning, sport, friends, being driven to school,
            # and from adolescence intimacy). Which system it engages emerges.
            act = sample_activity(age_years, rng)
            live_stimulus(d["mind"], act.stimulus, age_years=age_years)
            d["deliberative"] = act.id in DELIBERATIVE
        # meet a thing from the world, weighted by how often it is really met (food
        # and screens often, a snake almost never), run through the substrate; the
        # bond emerges and any inherited lean evolves with exposure
        thing = rng.choices(world_things,
                            weights=[t.frequency for t in world_things], k=1)[0]
        encounter(d["mind"].brain, thing, d["env_matrix"], age_years=age_years)
        # a moment in one of the child's groups -- standing and belonging accrue,
        # by dominance or prestige, from the emergent response
        grp = rng.choice(world_groups)
        mem = d["group_matrix"].membership(grp.id, grp.kind)
        pre = mem.standing + mem.belonging
        gresp = group_encounter(d["mind"].brain, grp, mem, sample_encounter_type(rng),
                                age_years=age_years)
        post = mem.standing + mem.belonging
        # remember the outcome: the drive that was run, and whether it bettered or
        # worsened the person's social position (emergent valence, not a per-drive rule)
        d["mind"].memory.add(label=grp.kind, appraisal=Appraisal(label=grp.kind),
                             dominant=gresp.dominant.value,
                             valence=max(-1.0, min(1.0, post - pre)), importance=0.5)
        # monitor the executive-function layer (self-awareness) -- READ, not applied:
        # it matures with age, reads moral orientation off the substrate, and accrues
        # purpose on deliberative steps. It does NOT change behaviour.
        monitor_executive(d["executive"], d["mind"].brain, age_years,
                          deliberative=d.get("deliberative", False))
        if d.get("deliberative", False):
            install_monitors_from_memory(d["executive"], d["mind"].memory)
        d["deliberative"] = False
        d["age"] = min(1.0, d["age"] + 1.0 / total_ep)

    dev = {}
    for cid in pop.pupils:
        home = venues.get(home_of.get(cid))
        if home is None:
            continue
        warmth = getattr(home, "warmth", 0.75)
        structure = getattr(home, "structure", 0.70)
        recog = clamp(0.5 * warmth + 0.5 * tie_standing.get(cid, 0.6))
        env = Environment(home.name, warmth, structure, recog)
        sits = [a.to_appraisal() for area in ("kitchen", "lounge", "bathroom")
                if area in home.areas for a in home.area(area).affordances()]
        sits += [a.to_appraisal() for area in ("classroom", "playground")
                 if area in school.areas for a in school.area(area).affordances()]
        d = {"mind": pop.persons[cid].mind, "env": env,
             "age": 0.0, "sits": sits, "env_matrix": birth_matrix(world_things),
             "group_matrix": GroupMatrix(), "executive": Executive(),
             "deliberative": False,
             "done": False, "outcome": None, "stage": "early_childhood",
             "carry": 0.0, "warmth": warmth}
        # make the executive ALWAYS-ON for this child: attach it to the brain so it is
        # consulted on every respond (every brain event), not just when we sample its
        # state. With nothing learned to monitor yet, the loop runs but does not act.
        d["mind"].brain.executive = d["executive"]
        # a child already part-grown at t=0 has LIVED those years: run the
        # episodes up to their current age so early development counts
        start_age = rng.uniform(0.0, 0.92)
        while d["age"] < start_age:
            _episode(d)
        yrs = d["age"] * childhood_years
        d["stage"] = ("adolescence" if yrs >= 12 else
                      "middle_childhood" if yrs >= 6 else "early_childhood")
        dev[cid] = d

    ties = pop.society.ties
    prev_state = {id(t): t.state() for t in ties}

    def world_step(clock, minutes):
        evs = []
        start = clock.total_minutes
        years = minutes / (MIN_PER_DAY * DAYS_PER_YEAR)

        # 1. age children through lived developmental episodes
        for cid, d in dev.items():
            if d["done"]:
                continue
            d["carry"] += years * episodes_per_year
            whole = int(d["carry"]); d["carry"] -= whole
            for _ in range(whole):
                _episode(d)
                yrs = d["age"] * childhood_years
                ns = ("adolescence" if yrs >= 12 else
                      "middle_childhood" if yrs >= 6 else "early_childhood")
                if ns != d["stage"]:
                    d["stage"] = ns
                    evs.append(Event(start, "stage", cid,
                                     f"{cid} enters {ns.replace('_', ' ')}"))
            if d["age"] >= 1.0 and not d["done"]:
                d["done"] = True
                d["outcome"] = read_mind(d["mind"]).classification
                evs.append(Event(clock.total_minutes, "milestone", cid,
                                 f"{cid} reaches adulthood: {d['outcome']}"))

        # 2. the society's relational dynamics tick alongside
        n_int = min(200, max(1, minutes // 90))
        for _ in range(n_int):
            t = rng.choice(ties)
            hi, lo = pop.persons.get(t.higher), pop.persons.get(t.lower)
            if not hi or not lo:
                continue
            ex = interact(t, hi.mind, lo.mind)
            was, now = prev_state[id(t)], ex.state
            if now != was:
                if now == "ruptured":
                    evs.append(Event(start, "rupture", t.higher,
                                     f"{t.pair.kind} {t.higher}->{t.lower} ruptured"))
                prev_state[id(t)] = now

        clock.advance(minutes)
        evs.append(Event(clock.total_minutes, "cohesion",
                         text=f"cohesion {pop.society.cohesion():.0%}"))
        return evs

    world_step.dev = dev          # expose developmental state for inspection
    return world_step
