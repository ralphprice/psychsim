"""
mapmodel.py -- the map data the compositor reads.

This is the schema from Part V of the graphics specification, as dataclasses with
JSON round-trip. A CityMap is a grid with layers (terrain, roads, objects,
actors) plus the binding fields (`place`, `agent_id`) that tie tiles back to the
simulation's places and people.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple
import json


@dataclass
class Placement:
    """A non-terrain tile placed at a grid cell."""
    tile: str
    x: int
    y: int
    footprint: Tuple[int, int] = (1, 1)
    place: Optional[str] = None       # binds a building to a sim_world Place name


@dataclass
class Actor:
    sprite: str
    x: int
    y: int
    agent_id: Optional[str] = None    # binds a sprite to a sim_world Person


@dataclass
class CityMap:
    name: str = "town"
    cols: int = 16
    rows: int = 16
    terrain: List[List[str]] = field(default_factory=list)   # [row][col] -> tile id
    roads: List[Placement] = field(default_factory=list)
    objects: List[Placement] = field(default_factory=list)
    actors: List[Actor] = field(default_factory=list)

    def fill_terrain(self, tile_id: str) -> None:
        self.terrain = [[tile_id for _ in range(self.cols)] for _ in range(self.rows)]

    def set_terrain(self, x: int, y: int, tile_id: str) -> None:
        self.terrain[y][x] = tile_id

    # -- persistence -------------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "grid": {"cols": self.cols, "rows": self.rows, "tile": [256, 128]},
            "terrain": self.terrain,
            "roads": [asdict(p) for p in self.roads],
            "objects": [asdict(p) for p in self.objects],
            "actors": [asdict(a) for a in self.actors],
        }

    def save(self, path: str) -> None:
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def from_dict(cls, d: dict) -> "CityMap":
        grid = d.get("grid", {})
        m = cls(name=d.get("name", "town"),
                cols=grid.get("cols", 16), rows=grid.get("rows", 16))
        m.terrain = d.get("terrain", [])
        m.roads = [_placement(p) for p in d.get("roads", [])]
        m.objects = [_placement(p) for p in d.get("objects", [])]
        m.actors = [Actor(**_actor(a)) for a in d.get("actors", [])]
        return m

    @classmethod
    def load(cls, path: str) -> "CityMap":
        with open(path) as f:
            return cls.from_dict(json.load(f))


def _placement(p: dict) -> Placement:
    fp = p.get("footprint", [1, 1])
    return Placement(tile=p["tile"], x=p["x"], y=p["y"],
                     footprint=(fp[0], fp[1]), place=p.get("place"))


def _actor(a: dict) -> dict:
    return {"sprite": a["sprite"], "x": a["x"], "y": a["y"],
            "agent_id": a.get("agent_id")}
