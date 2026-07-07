"""
floorplan.py -- the top-down "glass roof" view.

One view, seen from directly above: the normal settlement -- streets, parks,
plots -- but every building is drawn as its floor plan, as though single-storey
with a glass roof, so you look straight down into furnished rooms. Each building
is rendered from the SAME `Venue`/`Area`/`AffordanceObject` data the simulation
uses: a home shows its kitchen, lounge, bathroom and bedrooms with a table, a
sofa, a sink and beds drawn in, and the sims are placed in the room they are
using. The picture IS the model, not a separate drawing.

Flat, muted, legible -- the Smallville/Park look: soft room tints, thin walls,
simple top-down furniture glyphs, sims as small dots. It is pure SVG, so panning
and zooming for detail is trivial in any viewer.
"""

from __future__ import annotations
from typing import Dict, List, Optional, Tuple

# muted, flat palette (Park-ish)
WALL = "#6B6660"
GROUND = "#DDE4D0"
ROAD = "#B9B7AE"
ROAD_EDGE = "#A7A59C"
PARK = "#BFD8A6"
LABEL = "#5A554E"

ROOM_TINT = {
    "kitchen": "#F3E7C9", "lounge": "#EAD9C0", "living": "#EAD9C0",
    "bathroom": "#CFE4EC", "bath": "#CFE4EC",
    "bedroom": "#DED2E8", "parents_bedroom": "#D8CBE8", "shared_bedroom": "#D5E0C0",
    "classroom": "#F5EFC6", "playground": "#C7E3A8", "staff_room": "#E3E0D6",
    "work_floor": "#D6E0E6", "office": "#D6E0E6", "back_office": "#CBD5DC",
    "street": "#C9C6BE", "bar": "#E7CDA6",
}
FURNITURE_FILL = "#B6A98E"
FURNITURE_EDGE = "#8E836C"
SOFT = "#CFC4AC"
CORRIDOR = "#E7E2D6"
DOOR = "#9A8F79"

# relative room sizes -- a lounge is bigger than a bathroom
ROOM_WEIGHT = {
    "lounge": 1.5, "living": 1.5, "classroom": 1.5, "work_floor": 1.4,
    "playground": 1.4, "street": 1.4, "bar": 1.3, "kitchen": 1.25,
    "shared_bedroom": 1.15, "parents_bedroom": 1.1, "child_bedroom": 1.0,
    "back_office": 0.9, "staff_room": 0.85, "office": 1.1, "bathroom": 0.6,
}


def _weight(name: str) -> float:
    for key, w in ROOM_WEIGHT.items():
        if key in name:
            return w
    return 1.0


def _hwall(x1, x2, y, gap_c=None, gap=0.0, sw=2.0):
    a, b = min(x1, x2), max(x1, x2)
    if not gap:
        return f'<line x1="{a:.1f}" y1="{y:.1f}" x2="{b:.1f}" y2="{y:.1f}" stroke="{WALL}" stroke-width="{sw}"/>'
    g0, g1 = gap_c - gap / 2, gap_c + gap / 2
    return (f'<line x1="{a:.1f}" y1="{y:.1f}" x2="{g0:.1f}" y2="{y:.1f}" stroke="{WALL}" stroke-width="{sw}"/>'
            f'<line x1="{g1:.1f}" y1="{y:.1f}" x2="{b:.1f}" y2="{y:.1f}" stroke="{WALL}" stroke-width="{sw}"/>')


def _vwall(y1, y2, x, gap_c=None, gap=0.0, sw=2.0):
    a, b = min(y1, y2), max(y1, y2)
    if not gap:
        return f'<line x1="{x:.1f}" y1="{a:.1f}" x2="{x:.1f}" y2="{b:.1f}" stroke="{WALL}" stroke-width="{sw}"/>'
    g0, g1 = gap_c - gap / 2, gap_c + gap / 2
    return (f'<line x1="{x:.1f}" y1="{a:.1f}" x2="{x:.1f}" y2="{g0:.1f}" stroke="{WALL}" stroke-width="{sw}"/>'
            f'<line x1="{x:.1f}" y1="{g1:.1f}" x2="{x:.1f}" y2="{b:.1f}" stroke="{WALL}" stroke-width="{sw}"/>')


def _tint(area_name: str) -> str:
    for key, col in ROOM_TINT.items():
        if key in area_name:
            return col
    return "#E4E0D6"


def _rect(x, y, w, h, fill, stroke=None, sw=1.0, rx=0, opacity=None):
    s = f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}"'
    if rx:
        s += f' rx="{rx}"'
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{sw}"'
    if opacity is not None:
        s += f' opacity="{opacity}"'
    return s + "/>"


def _furniture(name: str, cx: float, cy: float, s: float) -> str:
    """A simple top-down glyph for an affordance-object, centred at (cx, cy),
    scaled by room size s."""
    u = s * 0.5
    f, e = FURNITURE_FILL, FURNITURE_EDGE
    if "bunk" in name:
        return (_rect(cx - u, cy - u * 1.2, u * 0.9, u * 2.4, f, e, 1, 2)
                + _rect(cx + u * 0.1, cy - u * 1.2, u * 0.9, u * 2.4, f, e, 1, 2))
    if "bed" in name:
        return (_rect(cx - u, cy - u * 1.3, u * 2, u * 2.6, f, e, 1, 3)
                + _rect(cx - u * 0.8, cy - u * 1.1, u * 1.6, u * 0.7, SOFT, None, 0, 2))
    if "sink" in name or "kettle" in name:
        return (_rect(cx - u * 0.7, cy - u * 0.7, u * 1.4, u * 1.4, f, e, 1, 2)
                + f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{u*0.4:.1f}" fill="{SOFT}"/>')
    if "table" in name:
        return (_rect(cx - u, cy - u * 0.7, u * 2, u * 1.4, f, e, 1, 2)
                + _rect(cx - u * 1.4, cy - u * 0.4, u * 0.35, u * 0.8, SOFT, e, 0.5)
                + _rect(cx + u * 1.05, cy - u * 0.4, u * 0.35, u * 0.8, SOFT, e, 0.5))
    if "sofa" in name:
        return (_rect(cx - u * 1.2, cy - u * 0.6, u * 2.4, u * 1.2, f, e, 1, 3)
                + _rect(cx - u * 1.2, cy - u * 0.9, u * 2.4, u * 0.4, SOFT, None, 0, 2))
    if "desk" in name or "workstation" in name or "records" in name:
        return (_rect(cx - u * 1.1, cy - u * 0.5, u * 2.2, u, f, e, 1, 1)
                + f'<circle cx="{cx:.1f}" cy="{cy+u*0.9:.1f}" r="{u*0.35:.1f}" '
                  f'fill="{SOFT}" stroke="{e}" stroke-width="0.5"/>')
    if "play" in name:
        return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{u*0.9:.1f}" fill="none" '
                f'stroke="{e}" stroke-width="1.5"/>'
                + _rect(cx - u * 0.15, cy - u, u * 0.3, u * 2, e))
    if "bench" in name:
        return _rect(cx - u, cy - u * 0.25, u * 2, u * 0.5, f, e, 1, 1)
    if "shelf" in name or "bar_top" in name:
        return _rect(cx - u * 1.2, cy - u * 0.35, u * 2.4, u * 0.7, f, e, 1, 1)
    # 'floor', 'space' etc. -> open area, nothing drawn
    return ""


def render_building_plan(venue, px: float, py: float, w: float, h: float,
                         occupants: Optional[Dict[str, List[str]]] = None,
                         show_labels: bool = True) -> str:
    """Draw one building as a realistic top-down floor plan in rect (px,py,w,h):
    rooms flank a central corridor, each opening onto it through a DOORWAY (a gap
    in the wall, not a solid block), with an entrance from the outside. Rooms are
    sized by type (a lounge larger than a bathroom), tinted, furnished from their
    affordance-objects, and any occupants placed inside. `occupants` maps
    area-name -> list of is_child flags."""
    areas = list(venue.areas.values())
    parts: List[str] = []

    # a garden (if any) is OUTDOOR: draw it as green space behind the house, with
    # a back door from the house; the house occupies the street-facing portion.
    garden = next((a for a in areas if a.name == "garden"), None)
    rooms = [a for a in areas if a.name != "garden"]
    hx, hy, hw, hh = px, py, w, h
    if garden is not None:
        gsize = getattr(garden, "garden_size", 0.5)
        gh = h * (0.18 + 0.20 * gsize)                    # garden depth by size
        # garden at the back (top); a couple of plants and a lawn
        parts.append(_rect(px, py, w, gh - 2, PARK, "#A7C089", 1.0, rx=3))
        parts.append(f'<text x="{px+4:.1f}" y="{py+11:.1f}" font-family="Arial" '
                     f'font-size="8.5" fill="#5f7a45">garden</text>')
        import random as _r
        rr = _r.Random(hash(venue.name) & 0xffff)
        for _ in range(1 + int(3 * gsize)):
            gx, gy = px + rr.uniform(0.15, 0.85) * w, py + rr.uniform(0.35, 0.8) * gh
            parts.append(f'<circle cx="{gx:.1f}" cy="{gy:.1f}" r="{4+6*gsize:.1f}" '
                         f'fill="#7BA05B" opacity="0.9"/>')
        hy, hh = py + gh, h - gh
    parts.append(_rect(hx, hy, hw, hh, CORRIDOR))         # house hallway underlay

    # split rooms into two columns flanking the corridor, balancing floor area
    cw = max(13.0, hw * 0.13)
    cx0, cx1 = hx + (hw - cw) / 2, hx + (hw - cw) / 2 + cw
    left: List = []
    right: List = []
    lw = rw = 0.0
    for a in sorted(rooms, key=lambda a: -_weight(a.name)):
        if lw <= rw:
            left.append(a); lw += _weight(a.name)
        else:
            right.append(a); rw += _weight(a.name)

    def _column(rooms, x0, x1, corridor_on_right):
        total = sum(_weight(a.name) for a in rooms) or 1.0
        yy = hy
        for i, a in enumerate(rooms):
            rh = hh * (_weight(a.name) / total)
            rw_ = x1 - x0
            parts.append(_rect(x0, yy, rw_, rh, _tint(a.name)))
            door_c = yy + rh / 2
            door = min(rh * 0.44, 15)
            if corridor_on_right:
                parts.append(_vwall(yy, yy + rh, x1, gap_c=door_c, gap=door))
                parts.append(_vwall(yy, yy + rh, x0))
                dx = x1 - 2
            else:
                parts.append(_vwall(yy, yy + rh, x0, gap_c=door_c, gap=door))
                parts.append(_vwall(yy, yy + rh, x1))
                dx = x0 - 1
            parts.append(f'<rect x="{dx:.1f}" y="{door_c-door/2:.1f}" width="3" '
                         f'height="{door:.1f}" fill="{DOOR}"/>')
            parts.append(_hwall(x0, x1, yy))
            for j, obj in enumerate(a.objects):
                fx = x0 + rw_ * (0.34 + 0.34 * (j % 2))
                fy = yy + rh * (0.32 + 0.32 * (j // 2))
                parts.append(_furniture(obj.name, fx, fy, min(rw_, rh) * 0.32))
            if show_labels and min(rw_, rh) > 24:
                parts.append(f'<text x="{x0+4:.1f}" y="{yy+11:.1f}" font-family="Arial" '
                             f'font-size="8.5" fill="{LABEL}">{a.name.replace("_"," ")}</text>')
            for k, occ in enumerate((occupants or {}).get(a.name, [])):
                ox = x0 + rw_ * (0.5 + 0.15 * (k - 0.5))
                oy = yy + rh * 0.72
                # an occupant may be a colour string (e.g. emergent-drive colour) or
                # a truthy is_child flag (default green child / blue adult)
                if isinstance(occ, str):
                    colour, r = occ, 3.6
                else:
                    colour = "#7BA05B" if occ else "#5B7BA0"
                    r = 3.0 if occ else 4.0
                parts.append(f'<circle cx="{ox:.1f}" cy="{oy:.1f}" r="{r:.1f}" '
                             f'fill="{colour}" stroke="#3d3d3d" stroke-width="0.6"/>')
            yy += rh
        parts.append(_hwall(x0, x1, hy + hh))

    _column(left, hx, cx0, corridor_on_right=True)
    _column(right, cx1, hx + hw, corridor_on_right=False)

    # house outer wall: FRONT door onto the street (bottom), BACK door to the
    # garden (top) if there is one
    ecx = (cx0 + cx1) / 2
    ew = min(cw * 0.7, 16)
    if garden is not None:
        parts.append(_hwall(hx, hx + hw, hy, gap_c=ecx, gap=ew))       # back door -> garden
        parts.append(f'<rect x="{ecx-ew/2:.1f}" y="{hy-1:.1f}" width="{ew:.1f}" height="3" fill="{DOOR}"/>')
    else:
        parts.append(_hwall(hx, hx + hw, hy))
    parts.append(_hwall(hx, hx + hw, hy + hh, gap_c=ecx, gap=ew))      # front door -> street
    parts.append(_vwall(hy, hy + hh, hx))
    parts.append(_vwall(hy, hy + hh, hx + hw))
    parts.append(f'<rect x="{ecx-ew/2:.1f}" y="{hy+hh-2:.1f}" width="{ew:.1f}" height="3" '
                 f'fill="{DOOR}"/>')                                    # front-door step
    return "".join(parts)


def render_settlement_plan(city, venues: Dict[str, object],
                           occupants: Optional[Dict[str, Dict]] = None,
                           cell: int = 64, pad: int = 20) -> str:
    """Render the whole settlement top-down: grass, roads and parks from the
    CityMap, and every building bound in `venues` drawn as its floor plan. Pure
    SVG with a viewBox, so it pans and zooms in any viewer."""
    W = city.cols * cell + 2 * pad
    H = city.rows * cell + 2 * pad
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}">',
           _rect(0, 0, W, H, "#EAF0F2")]

    def sx(gx): return pad + gx * cell
    def sy(gy): return pad + gy * cell

    # terrain (grass / park)
    for gy in range(city.rows):
        for gx in range(city.cols):
            t = city.terrain[gy][gx] if city.terrain and gy < len(city.terrain) else "terrain_grass"
            col = PARK if "park" in t else (ROAD if "pavement" in t else GROUND)
            out.append(_rect(sx(gx), sy(gy), cell, cell, col))
    # roads
    for p in city.roads:
        out.append(_rect(sx(p.x), sy(p.y), cell, cell, ROAD, ROAD_EDGE, 0.5))
        # a dashed centre line for legibility
        out.append(f'<line x1="{sx(p.x)+cell/2:.0f}" y1="{sy(p.y):.0f}" '
                   f'x2="{sx(p.x)+cell/2:.0f}" y2="{sy(p.y)+cell:.0f}" '
                   f'stroke="#E9E6DC" stroke-width="1.2" stroke-dasharray="5 5" opacity="0.7"/>')

    # buildings as floor plans (skip props/trees here for a clean plan)
    for p in city.objects:
        if not p.place or p.place not in venues:
            # draw trees/props lightly as green dots so parks read
            if p.tile.startswith("prop_tree"):
                out.append(f'<circle cx="{sx(p.x)+cell/2:.0f}" cy="{sy(p.y)+cell/2:.0f}" '
                           f'r="{cell*0.18:.0f}" fill="#7BA05B" opacity="0.9"/>')
            continue
        fpw, fph = p.footprint
        bx, by = sx(p.x) + cell * 0.08, sy(p.y) + cell * 0.08
        bw, bh = cell * fpw - cell * 0.16, cell * fph - cell * 0.16
        occ = (occupants or {}).get(p.place)
        out.append(render_building_plan(venues[p.place], bx, by, bw, bh, occ,
                                        show_labels=(cell >= 56)))

    out.append("</svg>")
    return "".join(out)
