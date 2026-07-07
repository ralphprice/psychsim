"""
norms.py -- the local-norm mechanism (universal, opinion-free).

A universal fact about social worlds: the same conduct is acceptable in one
setting and not in another. This module is only the MACHINERY for that -- it
carries no categories of its own and no judgement about what any behaviour
means. A place holds a NORM PROFILE: a mapping from a study-defined behaviour
category to how acceptable it is there, on a neutral acceptability scale. An act
is assessed by looking up its category in the local profile; acting below what a
place expects is a NORM DEPARTURE, with a magnitude, and witnessing one colours
an observer's appraisal.

The categories, and every acceptability value, are supplied by whatever study
uses the core. The core names none of them: it does not know about cooperation
or disruption, still less about anything an application might treat as an
offence. That belongs in an extension, so the instrument stays neutral and the
same machinery serves any study -- one interested in restraint and reciprocity,
another in something else entirely.
"""

from __future__ import annotations
from enum import IntEnum
from typing import Dict, Optional, Tuple


class Norm(IntEnum):
    """A neutral, symmetric acceptability scale for a behaviour in a place."""
    UNACCEPTABLE = -2
    DISCOURAGED = -1
    TOLERATED = 0
    ACCEPTED = 1
    ENCOURAGED = 2


# A norm profile is just a mapping category -> Norm. Categories are plain strings
# defined by the study; the core ships no categories and no default profiles.
NormProfile = Dict[str, Norm]

# How far below TOLERATED a category must fall to count as a departure.
DEPARTURE_AT = Norm.DISCOURAGED


def category_of(network: str, affordance=None) -> Optional[str]:
    """The behaviour category of an act. Taken from the affordance if it declares
    one; otherwise None -- the core does not map behavioural networks to
    categories, because what a network *means* normatively is a study's decision,
    not the engine's."""
    return getattr(affordance, "category", None)


def assess(category: Optional[str], profile: Optional[NormProfile]
           ) -> Tuple[Norm, bool]:
    """Assess an act of `category` against a place's norm profile. Returns
    (acceptability_level, is_departure). A category the profile does not mention
    is TOLERATED (the core presumes nothing). `is_departure` is True when the act
    falls at or below the departure threshold -- a neutral 'acted below what this
    place expects', with no further label."""
    if category is None or not profile:
        return Norm.TOLERATED, False
    level = profile.get(category, Norm.TOLERATED)
    return level, level <= DEPARTURE_AT


def departure_magnitude(level: Norm) -> float:
    """How far below acceptable an act sits, in [0, 1] -- 0 if acceptable."""
    if level >= Norm.TOLERATED:
        return 0.0
    return min(1.0, (Norm.TOLERATED - level) / 2.0)


def observer_reaction(level: Norm) -> Dict[str, float]:
    """Appraisal dimensions a witnessed norm departure imposes on an observer --
    a neutral social-disapproval reading whose strength scales with how far below
    acceptable the act was. Not tied to any notion of offence."""
    m = departure_magnitude(level)
    if m <= 0.0:
        return {}
    return {"social_valence": -m, "provocation": 0.5 * m}
