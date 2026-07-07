"""
tileset.py -- the graphics slot.

A Tileset knows how to draw a tile id at a screen position. Two implementations:

  * PlaceholderTileset -- draws simple isometric shapes (coloured diamonds for
    ground, shaded boxes for buildings, little figures for sims) in pure SVG, so
    the whole pipeline runs and is testable *before* any art exists.

  * PngTileset -- THE SLOT. Emits <image> references to PNG files named per the
    graphics specification, positioned to the exact geometry (ground filling the
    diamond; buildings/props/actors anchored bottom-centre on the base diamond).
    Drop the AI-produced tiles into a directory, point this at it, and the real
    city renders with no other change.

Both satisfy the same interface, so the compositor swaps one for the other.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

from .iso import (TILE_W, TILE_H, HALF_W, HALF_H,
                  diamond_points, diamond_center, base_bottom, iso_box_faces)


# ---------------------------------------------------------------------------
# Interface
# ---------------------------------------------------------------------------

class Tileset:
    def render_ground(self, tile_id: str, sx: float, sy: float) -> str:
        raise NotImplementedError

    def render_object(self, tile_id: str, sx: float, sy: float,
                      footprint: Tuple[int, int] = (1, 1)) -> str:
        raise NotImplementedError

    def render_actor(self, sprite_id: str, sx: float, sy: float,
                     state_colour: Optional[str] = None) -> str:
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Placeholder tileset (runs with no art)
# ---------------------------------------------------------------------------

GROUND_COLOUR = {
    "terrain_grass": "#8CB369", "terrain_park": "#6DA34D",
    "terrain_pavement": "#C9C6BE", "terrain_dirt": "#B08968",
    "terrain_water": "#6FA8DC",
}
BUILDING = {   # (roof, wall, height_px)
    "building_home": ("#C0552B", "#E8C39E", 92),
    "building_school": ("#3D6098", "#C7D3E8", 120),
    "building_workplace": ("#2E7D74", "#BFD8D4", 150),
    "building_institution": ("#7D5BA6", "#D6C9E8", 128),
}
ROAD_ASPHALT, ROAD_MARK = "#5A5A5A", "#D9D9D9"


def _shade(hex_colour: str, factor: float) -> str:
    h = hex_colour.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r, g, b = (max(0, min(255, int(c * factor))) for c in (r, g, b))
    return f"#{r:02X}{g:02X}{b:02X}"


class PlaceholderTileset(Tileset):
    def render_ground(self, tile_id: str, sx: float, sy: float) -> str:
        if tile_id.startswith("road") or tile_id.startswith("path"):
            base = "#7C8A6B"  # grass-ish under the road
            pts = diamond_points(sx, sy)
            cx, cy = diamond_center(sx, sy)
            # asphalt diamond, slightly inset, with a centre stripe
            road = diamond_points(sx + 26, sy + 13)
            return (f'<polygon points="{pts}" fill="{base}" stroke="#6E7B5E" stroke-width="1"/>'
                    f'<polygon points="{road}" fill="{ROAD_ASPHALT}"/>'
                    f'<line x1="{sx+HALF_W}" y1="{sy+18}" x2="{sx+HALF_W}" y2="{sy+TILE_H-18}" '
                    f'stroke="{ROAD_MARK}" stroke-width="2" stroke-dasharray="8 8" opacity="0.7"/>')
        col = GROUND_COLOUR.get(tile_id, "#9AA0A6")
        pts = diamond_points(sx, sy)
        return f'<polygon points="{pts}" fill="{col}" stroke="{_shade(col,0.85)}" stroke-width="1"/>'

    def render_object(self, tile_id: str, sx: float, sy: float,
                      footprint: Tuple[int, int] = (1, 1)) -> str:
        if tile_id in BUILDING:
            roof, wall, h = BUILDING[tile_id]
            cols, rows = footprint
            faces = iso_box_faces(sx, sy, h, cols, rows)
            return (f'<polygon points="{faces["left"]}" fill="{_shade(wall,0.78)}"/>'
                    f'<polygon points="{faces["right"]}" fill="{_shade(wall,0.62)}"/>'
                    f'<polygon points="{faces["top"]}" fill="{roof}"/>')
        # props
        cx, by = base_bottom(sx, sy)
        if tile_id.startswith("prop_tree"):
            return (f'<rect x="{cx-6}" y="{by-46}" width="12" height="30" fill="#7A4B2B"/>'
                    f'<circle cx="{cx}" cy="{by-54}" r="26" fill="#4E7A3F"/>')
        if tile_id.startswith("prop_playground"):
            return (f'<rect x="{cx-30}" y="{by-48}" width="60" height="36" rx="4" '
                    f'fill="#E0A458" stroke="#B07A34"/>')
        if tile_id.startswith("prop_bench"):
            return f'<rect x="{cx-18}" y="{by-20}" width="36" height="10" fill="#9B7B4A"/>'
        if tile_id.startswith("prop_streetlight"):
            return (f'<rect x="{cx-3}" y="{by-70}" width="6" height="64" fill="#6B6B6B"/>'
                    f'<circle cx="{cx}" cy="{by-72}" r="7" fill="#F4D35E"/>')
        if tile_id.startswith("prop_fence"):
            return f'<rect x="{cx-40}" y="{by-24}" width="80" height="6" fill="#B49A6A"/>'
        # unknown prop -> a small marker
        return f'<circle cx="{cx}" cy="{by-14}" r="10" fill="#B0B0B0"/>'

    def render_actor(self, sprite_id: str, sx: float, sy: float,
                     state_colour: Optional[str] = None) -> str:
        cx, by = base_bottom(sx, sy)
        child = "child" in sprite_id
        h = 34 if child else 46
        head_r = 8 if child else 10
        parts = []
        if state_colour:  # a ring on the ground under the sim showing its state
            parts.append(f'<ellipse cx="{cx}" cy="{by-4}" rx="18" ry="9" fill="none" '
                         f'stroke="{state_colour}" stroke-width="3" opacity="0.9"/>')
        # body (a rounded triangle) + head
        parts.append(f'<path d="M{cx},{by-h} L{cx-9},{by-8} L{cx+9},{by-8} Z" '
                     f'fill="#4A4A4A"/>')
        parts.append(f'<circle cx="{cx}" cy="{by-h-head_r}" r="{head_r}" fill="#E8C39E" '
                     f'stroke="#B98C63"/>')
        return "".join(parts)


# ---------------------------------------------------------------------------
# PNG tileset (the drop-in slot for AI art)
# ---------------------------------------------------------------------------

@dataclass
class TileArt:
    filename: str
    canvas: Tuple[int, int]   # (w, h) the PNG was produced at (Part II)


class PngTileset(Tileset):
    """Renders real PNG tiles by <image> reference, positioned to the spec.

    `directory` is where the PNGs live (relative href in the SVG). `manifest`
    maps tile_id -> TileArt; if a tile is missing it is skipped (so a partial
    tileset still renders what it has). Ground tiles fill the 256x128 diamond
    box; objects and actors are anchored bottom-centre on the base diamond.
    """
    def __init__(self, directory: str, manifest: Dict[str, TileArt]):
        self.dir = directory.rstrip("/")
        self.manifest = manifest

    def _href(self, tile_id: str) -> Optional[TileArt]:
        return self.manifest.get(tile_id)

    def render_ground(self, tile_id: str, sx: float, sy: float) -> str:
        art = self._href(tile_id)
        if not art:
            return ""
        return (f'<image href="{self.dir}/{art.filename}" x="{sx}" y="{sy}" '
                f'width="{TILE_W}" height="{TILE_H}"/>')

    def render_object(self, tile_id: str, sx: float, sy: float,
                      footprint: Tuple[int, int] = (1, 1)) -> str:
        art = self._href(tile_id)
        if not art:
            return ""
        w, h = art.canvas
        cx, by = base_bottom(sx, sy)
        return (f'<image href="{self.dir}/{art.filename}" x="{cx - w/2}" '
                f'y="{by - h}" width="{w}" height="{h}"/>')

    def render_actor(self, sprite_id: str, sx: float, sy: float,
                     state_colour: Optional[str] = None) -> str:
        art = self._href(sprite_id)
        ring = ""
        cx, by = base_bottom(sx, sy)
        if state_colour:
            ring = (f'<ellipse cx="{cx}" cy="{by-4}" rx="18" ry="9" fill="none" '
                    f'stroke="{state_colour}" stroke-width="3" opacity="0.9"/>')
        if not art:
            return ring
        w, h = art.canvas
        return ring + (f'<image href="{self.dir}/{art.filename}" x="{cx - w/2}" '
                       f'y="{by - h}" width="{w}" height="{h}"/>')


def default_manifest() -> Dict[str, TileArt]:
    """A manifest matching the specification's naming and canvases, so a folder
    of correctly-named PNGs is ready to use with PngTileset."""
    m: Dict[str, TileArt] = {}
    for t in ("terrain_grass", "terrain_park", "terrain_pavement",
              "terrain_dirt", "terrain_water"):
        m[t] = TileArt(f"{t}.png", (TILE_W, TILE_H))
    for r in ("road_straight_ns", "road_straight_ew", "road_corner_ne",
              "road_corner_nw", "road_corner_se", "road_corner_sw",
              "road_cross", "path_straight", "path_corner"):
        m[r] = TileArt(f"{r}.png", (TILE_W, TILE_H))
    m["building_home"] = TileArt("building_home.png", (256, 384))
    m["building_school"] = TileArt("building_school.png", (512, 512))
    m["building_workplace"] = TileArt("building_workplace.png", (256, 384))
    m["building_institution"] = TileArt("building_institution.png", (512, 512))
    for p, c in (("prop_tree", (128, 192)), ("prop_bush", (128, 128)),
                 ("prop_playground", (256, 256)), ("prop_streetlight", (128, 224)),
                 ("prop_bench", (128, 128)), ("prop_fence", (256, 160))):
        m[p] = TileArt(f"{p}.png", c)
    for ch in ("char_adult_a", "char_adult_b", "char_child_a", "char_child_b"):
        m[ch] = TileArt(f"{ch}.png", (128, 256))
    return m
