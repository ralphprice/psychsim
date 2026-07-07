"""
binding.py -- join the visualiser to sim_world.

The graphics specification (Part V) says buildings bind to places, roads express
the place-graph connections, and actors bind to people. This module builds a
CityMap from a sim_world World given a layout (a screen position for each place),
and reads live simulation state -- each person's dominant behavioural network and
each institution's climate -- into the compositor's Overlays.

Positions are supplied as a layout rather than invented, because where the
buildings sit on the grid is a presentation choice, not a fact about the model.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from .mapmodel import CityMap, Placement, Actor
from .compositor import Overlays

# map a sim_world place kind to a building tile and footprint
PLACE_TILE = {
    "home": ("building_home", (1, 1)),
    "school": ("building_school", (2, 2)),
    "workplace": ("building_workplace", (1, 1)),
    "public": (None, (1, 1)),
}


@dataclass
class Layout:
    """Where each sim_world place sits on the grid, and the base terrain."""
    place_cells: Dict[str, Tuple[int, int]]
    cols: int = 16
    rows: int = 16
    base_terrain: str = "terrain_grass"


def build_map(world, layout: Layout, name: str = "town") -> CityMap:
    """Construct a CityMap from a sim_world World and a layout."""
    m = CityMap(name=name, cols=layout.cols, rows=layout.rows)
    m.fill_terrain(layout.base_terrain)

    # pave the cells that hold places, and place buildings
    for place_name, (gx, gy) in layout.place_cells.items():
        place = world.places.get(place_name)
        if place is None:
            continue
        tile, fp = PLACE_TILE.get(place.kind, (None, (1, 1)))
        # give buildings a pavement pad
        if 0 <= gy < m.rows and 0 <= gx < m.cols:
            m.set_terrain(gx, gy, "terrain_pavement")
        if tile:
            m.objects.append(Placement(tile=tile, x=gx, y=gy, footprint=fp,
                                       place=place_name))

    # roads: lay a road tile along the straight route between connected places
    for a in world.places.values():
        if a.name not in layout.place_cells:
            continue
        ax, ay = layout.place_cells[a.name]
        for b_name in a.connections:
            if b_name not in layout.place_cells:
                continue
            bx, by = layout.place_cells[b_name]
            for (cx, cy) in _line(ax, ay, bx, by):
                if (cx, cy) in layout.place_cells.values():
                    continue
                m.roads.append(Placement(tile="road_straight_ns", x=cx, y=cy))
    return m


def add_people(m: CityMap, world, people: Dict[str, object]) -> None:
    """Place people onto the map at their current sim_world location."""
    for agent_id, person in people.items():
        loc = world.location_of(agent_id)
        if loc is None or loc not in _cells_by_place(m):
            continue
        gx, gy = _cells_by_place(m)[loc]
        sprite = "char_child_a" if _is_child(person, world) else "char_adult_a"
        m.actors.append(Actor(sprite=sprite, x=gx, y=gy, agent_id=agent_id))


def overlays_from_state(world, people: Dict[str, object]) -> Overlays:
    """Read live state into compositor overlays: each person's dominant network,
    and each governed place's institution climate."""
    ov = Overlays()
    for agent_id, person in people.items():
        dominant = getattr(getattr(person, "mind", None), "dominant", None)
        if dominant:
            ov.actor_state[agent_id] = dominant
    # climate: mark each place by the warmth of the institution that governs it
    for inst in world.institutions.values():
        warm = inst.warmth >= 0.5
        for place_name, place in world.places.items():
            kind_ok = {"family": "home", "school": "school",
                       "employer": "workplace"}.get(inst.kind)
            if place.kind == kind_ok:
                ov.place_climate[place_name] = "warm" if warm else "harsh"
    return ov


# -- helpers ---------------------------------------------------------------

def _cells_by_place(m: CityMap) -> Dict[str, Tuple[int, int]]:
    return {p.place: (p.x, p.y) for p in m.objects if p.place}


def _is_child(person, world) -> bool:
    try:
        return person.life_stage(world).value in ("early_childhood",
                                                   "middle_childhood", "adolescence")
    except Exception:
        return False


def _line(x0: int, y0: int, x1: int, y1: int) -> List[Tuple[int, int]]:
    """Integer points on the straight line between two cells (Bresenham)."""
    pts = []
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    x, y = x0, y0
    while True:
        pts.append((x, y))
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy; x += sx
        if e2 < dx:
            err += dx; y += sy
    return pts
