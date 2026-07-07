"""
interior.py -- the spatial-interaction model (universal, opinion-free).

A place has an INTERIOR of areas an agent moves through; areas connect through
ACCESS rules (open, role-restricted, or closed); each area holds
AFFORDANCE-OBJECTS that offer actions; each action carries PRECONDITIONS (a role
present and attending, being observed or unobserved) and an EFFECT -- the
appraisal it imposes on the actor, which is what the affective engine then acts
on. Areas may carry a NORM PROFILE saying what conduct is acceptable there.

This is only the machinery. The core ships no venues and no affordances of its
own, and names no behaviour categories: a home, a school, a workplace -- and
whatever actions and social rules they involve -- are supplied by a study as an
extension, exactly as the sophropathy research is one extension among possible
others. The universal features here are: interiors you move through, access that
can be granted or withheld (respect for boundaries), what an action requires and
does, and that social rules are local. Any study needs these; none of them
presumes a domain.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

from affective_engine.core import Appraisal


# ---------------------------------------------------------------------------
# Access -- who may pass between areas (a generic boundary, not a lock)
# ---------------------------------------------------------------------------

@dataclass
class Access:
    """Who may pass through a connection between areas. Open to anyone by
    default; a study may restrict passage to certain roles, or close it
    entirely. A private room, a members-only area, a staff-only space and a hard
    boundary are all configurations of the one rule -- the universal feature is
    *who may enter where*, and thus respect for the boundaries one is granted."""
    roles: Optional[Set[str]] = None      # None -> anyone; otherwise only these roles
    is_open: bool = True                  # False -> closed to all

    def permits(self, role: Optional[str] = None) -> bool:
        if not self.is_open:
            return False
        if self.roles is None:
            return True
        return role in self.roles


# ---------------------------------------------------------------------------
# Affordances -- an action an object offers, with preconditions and an effect
# ---------------------------------------------------------------------------

@dataclass
class Affordance:
    """An action an object affords. `effect` is the appraisal it imposes on the
    actor (the situation the affective engine will act on); `label` is the
    engine's situation archetype; `category` is a study-defined behaviour
    category used for local-norm assessment (the core defines none). Preconditions
    gate availability."""
    name: str
    label: str
    effect: Dict[str, float] = field(default_factory=dict)
    requires_role: Optional[str] = None          # a role that must be present AND attending
    requires_observed: Optional[bool] = None     # True: needs a witness; False: needs privacy; None: either
    category: Optional[str] = None               # study-defined norm category

    def available(self, *, role_present: bool, observed: bool) -> bool:
        if self.requires_role is not None and not role_present:
            return False
        if self.requires_observed is True and not observed:
            return False
        if self.requires_observed is False and observed:
            return False
        return True

    def to_appraisal(self) -> Appraisal:
        a = Appraisal(label=self.label)
        for dim, val in self.effect.items():
            setattr(a, dim, val)
        return a


@dataclass
class AffordanceObject:
    """A thing in an area that affords one or more actions."""
    name: str
    affords: List[Affordance] = field(default_factory=list)


@dataclass
class Door:
    """A connection to another area, governed by an access rule."""
    to_area: str
    access: Access = field(default_factory=Access)

    def permits(self, role: Optional[str] = None) -> bool:
        return self.access.permits(role)


@dataclass
class Area:
    """A sub-space of a venue an agent occupies. May carry a norm profile (a
    study-supplied mapping of behaviour category -> acceptability)."""
    name: str
    objects: List[AffordanceObject] = field(default_factory=list)
    doors: List[Door] = field(default_factory=list)
    norms: Dict = field(default_factory=dict)

    def affordances(self) -> List[Affordance]:
        return [a for o in self.objects for a in o.affords]

    def door_to(self, area_name: str) -> Optional[Door]:
        for d in self.doors:
            if d.to_area == area_name:
                return d
        return None


@dataclass
class Venue:
    """A building with an interior: named areas, an entry area, a climate
    (warmth/structure) that a study may use to colour caregiving affordances, and
    an optional venue-level norm profile (areas may override it). The core
    supplies no venues; a study assembles them."""
    name: str
    kind: str
    areas: Dict[str, Area] = field(default_factory=dict)
    entry: str = ""
    warmth: float = 0.6
    structure: float = 0.6
    norms: Dict = field(default_factory=dict)

    def area(self, name: str) -> Area:
        return self.areas[name]

    def area_norms(self, area_name: str) -> Dict:
        """The norms in force in an area: its own if set, else the venue's."""
        a = self.areas.get(area_name)
        if a is not None and a.norms:
            return a.norms
        return self.norms
