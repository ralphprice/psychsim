"""
compositor.py -- draw a map with a tileset into an SVG.

Reads a CityMap and a Tileset and produces a complete SVG document, drawing in
painter's-algorithm order (Part II of the spec): terrain, then roads, then
objects, then actors, then the code-rendered overlays. The overlays -- a sim's
behavioural-network state and an institution's climate -- are drawn here in code,
not baked into art, so they can change every tick.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .iso import TILE_W, TILE_H, HALF_W, HALF_H, cell_to_screen, diamond_points
from .mapmodel import CityMap
from .tileset import Tileset, PlaceholderTileset

# one colour per EMERGENT ACTION / dominant drive, for the sim state overlay. Honesty
# migration #2: keyed on the emergent Panksepp action (approach/nurture/...) and the seven
# primary systems -- never on an outcome-category label (those live only in observer.py).
NETWORK_COLOUR = {
    # the emergent Panksepp behaviours the world loop records
    "approach": "#2E86C1",      # exploratory blue
    "nurture":  "#28B463",      # warm green
    "play":     "#F1C40F",      # bright yellow
    "court":    "#E91E8C",      # magenta
    "avoid":    "#7F8C8D",      # grey
    "aggress":  "#C0392B",      # red
    "seek_comfort": "#5D6D7E",  # slate
    # the seven emergent primary systems (Panksepp), so the visualiser can colour a
    # person by their EMERGENT dominant drive
    "SEEKING": "#2E86C1",   # exploratory blue
    "CARE":    "#28B463",   # warm green
    "PLAY":    "#F1C40F",   # bright yellow
    "LUST":    "#E91E8C",   # magenta
    "FEAR":    "#7F8C8D",   # grey
    "RAGE":    "#C0392B",   # red
    "PANIC":   "#5D6D7E",   # slate
}
# climate tint colours
WARM_TINT, HARSH_TINT = "#F5B041", "#5DADE2"


@dataclass
class Overlays:
    """Optional per-render overlay data the compositor draws on top."""
    actor_state: Dict[str, str] = field(default_factory=dict)     # agent_id -> network name
    place_climate: Dict[str, str] = field(default_factory=dict)   # place -> "warm"|"harsh"
    highlight_cells: List[Tuple[int, int]] = field(default_factory=list)


def _bounds(m: CityMap) -> Tuple[float, float, float, float]:
    """Screen bounding box for the whole grid, to size the SVG and set origin."""
    xs, ys = [], []
    for gy in range(m.rows):
        for gx in range(m.cols):
            sx, sy = cell_to_screen(gx, gy, 0, 0)
            xs += [sx, sx + TILE_W]; ys += [sy, sy + TILE_H]
    # extra headroom at the top for tall buildings
    return min(xs), min(ys) - 180, max(xs), max(ys)


def render_svg(m: CityMap, tileset: Optional[Tileset] = None,
               overlays: Optional[Overlays] = None, pad: int = 24) -> str:
    ts = tileset or PlaceholderTileset()
    ov = overlays or Overlays()
    minx, miny, maxx, maxy = _bounds(m)
    ox, oy = -minx + pad, -miny + pad
    width = (maxx - minx) + 2 * pad
    height = (maxy - miny) + 2 * pad

    # collect (zkey, svg) so we can paint back to front
    items: List[Tuple[Tuple[int, int, int], str]] = []

    def add(gx, gy, layer, svg, sub=0):
        if svg:
            items.append(((gx + gy, layer, sub), svg))

    # ground terrain
    for gy in range(m.rows):
        for gx in range(m.cols):
            if gy < len(m.terrain) and gx < len(m.terrain[gy]):
                sx, sy = cell_to_screen(gx, gy, ox, oy)
                add(gx, gy, 0, ts.render_ground(m.terrain[gy][gx], sx, sy))

    # roads (on ground)
    for p in m.roads:
        sx, sy = cell_to_screen(p.x, p.y, ox, oy)
        add(p.x, p.y, 1, ts.render_ground(p.tile, sx, sy))

    # objects (buildings, props) + climate tint overlay under buildings
    for p in m.objects:
        sx, sy = cell_to_screen(p.x, p.y, ox, oy)
        if p.place and p.place in ov.place_climate:
            tint = WARM_TINT if ov.place_climate[p.place] == "warm" else HARSH_TINT
            add(p.x, p.y, 1, f'<polygon points="{diamond_points(sx, sy)}" '
                             f'fill="{tint}" opacity="0.28"/>', sub=1)
        add(p.x, p.y, 2, ts.render_object(p.tile, sx, sy, p.footprint))

    # actors (sims) with state overlay
    for a in m.actors:
        sx, sy = cell_to_screen(a.x, a.y, ox, oy)
        colour = None
        if a.agent_id and a.agent_id in ov.actor_state:
            colour = NETWORK_COLOUR.get(ov.actor_state[a.agent_id], "#333333")
        add(a.x, a.y, 3, ts.render_actor(a.sprite, sx, sy, colour))

    # highlights (top overlay)
    for (gx, gy) in ov.highlight_cells:
        sx, sy = cell_to_screen(gx, gy, ox, oy)
        add(gx, gy, 4, f'<polygon points="{diamond_points(sx, sy)}" fill="none" '
                       f'stroke="#F1C40F" stroke-width="4" opacity="0.95"/>')

    items.sort(key=lambda it: it[0])
    body = "\n".join(svg for _, svg in items)

    legend = _legend(ov, width, height)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.0f} '
            f'{height:.0f}" font-family="Arial, sans-serif">\n'
            f'<rect x="0" y="0" width="{width:.0f}" height="{height:.0f}" fill="#EAF2F8"/>\n'
            f'{body}\n{legend}\n</svg>')


def _legend(ov: Overlays, width: float, height: float) -> str:
    if not ov.actor_state:
        return ""
    used = []
    seen = set()
    for net in ov.actor_state.values():
        if net not in seen:
            seen.add(net); used.append(net)
    parts = [f'<text x="16" y="24" font-size="14" font-weight="bold" '
             f'fill="#1F3864">sim state (dominant network)</text>']
    for i, net in enumerate(used):
        y = 44 + i * 18
        parts.append(f'<circle cx="24" cy="{y-4}" r="6" fill="{NETWORK_COLOUR.get(net,"#333")}"/>')
        parts.append(f'<text x="38" y="{y}" font-size="12" fill="#333">{net.replace("_"," ")}</text>')
    return "".join(parts)


def save_svg(m: CityMap, path: str, tileset: Optional[Tileset] = None,
             overlays: Optional[Overlays] = None) -> None:
    with open(path, "w") as f:
        f.write(render_svg(m, tileset, overlays))
