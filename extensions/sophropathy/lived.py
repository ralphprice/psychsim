"""
lived.py -- a childhood LIVED IN THE WORLD, driving the development rule.

This closes the loop. Until now the world drove behaviour and relational strain,
but development was run over an abstract situation cycle. Here a child lives days
in an actual home and school -- meeting the situations those places afford and
the caregiving of the parent-child relationship -- and each lived situation is
fed to the SAME validated `develop_step`. The environment that gates plasticity
is not stipulated: it is derived from the home the child actually lives in and
how the parent-child tie is going. At the end, the standard classifier reads the
outcome.

The point is a test-bed: the outcome is now PRODUCED by a life in the world, so
every later refinement to homes, schools, relationships or norms becomes
observable as a change in what comes out. It is rough by design and will be
improved; what matters is that the loop is closed and the effect of upgrades can
be seen.

No new developmental mechanism is invented: the world supplies the experience,
and the existing rule consumes it.
"""

from __future__ import annotations
import random
from typing import List, Optional

from affective_engine.core import Appraisal, clamp
from substrate.readout import read_mind
from affective_engine.development import (live_moment, Environment,
                                          situation, CHILDHOOD_CYCLE)
from sim_world import Person, Society, PARENT_CHILD, Venue


def _home_environment(home: Venue, tie_standing: float) -> Environment:
    """The developmental environment IS the home the child lives in: its warmth
    and structure, with recognition read from how the parent-child relationship
    is going (a well-held tie is felt as being recognised)."""
    recognition = clamp(0.5 * home.warmth + 0.5 * tie_standing)
    return Environment(home.name, home.warmth, home.structure, recognition)


def _lived_situations(home: Venue, school: Optional[Venue],
                      rng: random.Random) -> List[Appraisal]:
    """The stream of situations a child meets moving through the world: home
    self-care and family life, school work, and the playground's rough-and-tumble
    and occasional provocation. Drawn from the venues' own affordances, so the
    situations are those the world actually affords -- enriching the world
    changes this stream, and hence development."""
    sits: List[Appraisal] = []
    for area in ("kitchen", "lounge", "bathroom"):
        if area in home.areas:
            sits += [a.to_appraisal() for a in home.area(area).affordances()]
    if school is not None:
        for area in ("classroom", "playground"):
            if area in school.areas:
                sits += [a.to_appraisal() for a in school.area(area).affordances()]
    return sits


def raise_in_world(seed, home: Venue, school: Optional[Venue] = None,
                   graded: bool = True, years: int = 6,
                   situation_seed: int = 20260705) -> Outcome:
    """Raise one seeded child by living a childhood in `home` (and `school`), and
    return the classified adult outcome. Plasticity declines with age across the
    childhood, so WHEN experience lands matters, exactly as in the abstract rule
    -- but the experience and the environment now come from the world."""
    child = Person("child", "Child", seed)
    mind = child.mind

    soc = Society()
    tie = soc.add("parent", "child", PARENT_CHILD,
                  standing=clamp(home.warmth),
                  strain=clamp(0.4 * (1.0 - home.structure)))
    rng = random.Random(situation_seed)
    world_sits = _lived_situations(home, school, rng)
    episodes = max(24, years * 8)
    childhood_span = 18.0
    for i in range(episodes):
        age = i / max(1, episodes - 1)
        # the home shapes WHICH situations arise (their stimulus content); the
        # child's own systems decide the response. The lived world colours every
        # third moment; the rest are the testing diet.
        if i % 3 == 2 and world_sits:
            appr = rng.choice(world_sits)
        else:
            appr = situation(CHILDHOOD_CYCLE[i % len(CHILDHOOD_CYCLE)], rng)
        live_moment(mind, appr, age_years=age * childhood_span)
    return read_mind(mind)
