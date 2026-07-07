"""
builder.py -- assemble a small but complete world: a home, a school, a
workplace, and public space, wired together with institutions. Environment
knobs (warmth, structure) are parameters the experiment layer will vary; here we
provide sensible defaults and named presets.
"""

from __future__ import annotations
from typing import Tuple

from .world import World, Place, WorldObject, Institution


def build_world(home_warmth: float = 0.85, home_structure: float = 0.80,
                school_warmth: float = 0.6, school_structure: float = 0.7,
                work_warmth: float = 0.5, work_structure: float = 0.6) -> World:
    w = World()

    # -- places ------------------------------------------------------------
    w.add_place(Place("home", "home", objects=[
        WorldObject("table", {"sit", "eat", "study"}),
        WorldObject("toys", {"play"}),
    ]))
    w.add_place(Place("classroom", "school", objects=[
        WorldObject("desk", {"sit", "study"}),
        WorldObject("whiteboard", {"learn"}),
    ]))
    w.add_place(Place("playground", "school", objects=[
        WorldObject("climbing_frame", {"play", "risk"}),
    ]))
    w.add_place(Place("office", "workplace", objects=[
        WorldObject("workstation", {"work"}),
    ]))
    w.add_place(Place("street", "public", objects=[]))

    # -- connections -------------------------------------------------------
    w.connect("home", "street")
    w.connect("street", "classroom")
    w.connect("classroom", "playground")
    w.connect("street", "office")

    # -- institutions ------------------------------------------------------
    w.add_institution(Institution("Family", "family",
                                  warmth=home_warmth, structure=home_structure,
                                  reward_for_cooperation=0.6, sanction_for_defection=0.5))
    w.add_institution(Institution("School", "school",
                                  warmth=school_warmth, structure=school_structure,
                                  reward_for_cooperation=0.55, sanction_for_defection=0.6))
    w.add_institution(Institution("Employer", "employer",
                                  warmth=work_warmth, structure=work_structure,
                                  reward_for_cooperation=0.5, sanction_for_defection=0.7))
    return w


WARM_FIRM_PRESET = dict(home_warmth=0.90, home_structure=0.85)
HARSH_INCONSISTENT_PRESET = dict(home_warmth=0.20, home_structure=0.25)
