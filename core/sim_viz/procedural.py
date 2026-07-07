"""
procedural.py -- draw a broad city tileset in code, as vector SVG.

The third Tileset, alongside PlaceholderTileset (bare shapes) and PngTileset
(the raster slot). Instead of loading art it *draws* each tile parametrically
to the isometric geometry contract in `iso.py`.

Coverage follows what city-builder simulations converge on -- residential,
commercial, civic and leisure buildings, green space, street dressing, and
movable agents:

  * terrain   grass, park, garden, pavement, plaza, dirt, sand, water
  * roads     straight, crossroads, footpath (kerbs + markings)
  * buildings house, terrace, apartment, office/workplace, school,
              shop, grocery, cafe, pub, bar, sports centre, civic hall
  * props     tree, bush, hedge, flowerbed, fountain, playground, bench,
              streetlight, bin, bollard, bus stop, fence
  * movable   adult, child (with behavioural-state ring), car, bike, bus

Two ideas keep it a coherent illustration rather than a pile of shapes: a
locked palette and one light direction (`PALETTE` is the "style bible" in code;
every solid is shaded top-lit / left-mid / right-shadow), and seeded per-cell
variety derived from screen position, so a street varies while rendering
identically every run. Buildings are data-driven: a new type is one entry in
`BUILDING`, not a new function.

It composes natively into the SVG compositor, scales to any resolution for
print figures, and rasterises to PNG only when a raster is wanted. No new
dependencies.
"""

from __future__ import annotations
import hashlib
from typing import Dict, List, Optional, Tuple

from .iso import TILE_W, TILE_H, HALF_W, HALF_H, diamond_points, base_bottom

# ---------------------------------------------------------------------------
# The style bible, in code
# ---------------------------------------------------------------------------

PALETTE = {
    # ground
    "grass": "#8FB56A", "park": "#6FA24E", "garden": "#93BC66",
    "pavement": "#CBC8C0", "plaza": "#D2CEC4", "dirt": "#B58A66",
    "sand": "#E4D2A6", "water": "#6FA8DC", "water_hi": "#93C1E8",
    "road": "#565656", "kerb": "#9C9C9C", "mark": "#E9E6DC",
    # walls
    "home_wall": "#E7CBA4", "terrace_wall": "#D9A78C", "apt_wall": "#C9C4BC",
    "work_wall": "#C2D4D0", "school_wall": "#CBD4E6", "shop_wall": "#E3D3B4",
    "grocery_wall": "#D8CBB0", "cafe_wall": "#E6C7A6", "pub_wall": "#C98A5A",
    "bar_wall": "#8A8592", "sports_wall": "#BFD0C8", "inst_wall": "#D8CBE8",
    # roofs
    "home_roof": "#B4552C", "terrace_roof": "#9C4A3A", "apt_roof": "#7E8894",
    "work_roof": "#2F7C73", "school_roof": "#3D6098", "shop_roof": "#6E7B8C",
    "grocery_roof": "#4E7A4A", "cafe_roof": "#8A5A3C", "pub_roof": "#7A3E2C",
    "bar_roof": "#54505E", "sports_roof": "#5E6E86", "inst_roof": "#7D5BA6",
    # details
    "window": "#F6EBC3", "window_off": "#BCC6CC", "glass": "#A8CDEA",
    "door": "#6E4B2A", "awning": "#C0553B", "awning_green": "#4E8A54",
    "sign": "#F2E4B8", "sign_dark": "#3B3B3B", "neon": "#E86FA8",
    "trunk": "#7A4B2B", "canopy": "#4E7A3F", "canopy_hi": "#5F8F4B",
    "bush": "#57843F", "hedge": "#4F7A3C", "flower_a": "#E4738A",
    "flower_b": "#E9C04E", "lamp": "#F4D35E", "metal": "#6B6B6B",
    "wood": "#9B7B4A", "play": "#E0A458", "bin": "#4E6B4E", "fountain": "#AFC6D8",
    # vehicles
    "car_a": "#C0553B", "car_b": "#3D6098", "car_c": "#4E7A4A",
    "bus": "#D6A23A", "bike": "#5B6B7B", "tyre": "#2E2E2E", "chrome": "#D6D6D6",
}

# face shading for a top-left light: top lit, left mid, right in shadow
F_TOP, F_LEFT, F_RIGHT = 1.06, 0.82, 0.63
ROOF_LIT, ROOF_DARK = 1.02, 0.72

# building catalogue -- a new type is one entry here.
#   wall/roof   : palette keys      wh : wall height px   rh : roof height px
#   roof        : "gable" | "hip" | "flat"
#   feats       : any of {chimney, shopfront, awning, awning_green, sign,
#                         hanging_sign, glass, grid, neon, steps}
BUILDING: Dict[str, dict] = {
    "building_home":        dict(wall="home_wall",    roof="home_roof",    wh=76,  rh=34, shape="gable", feats={"chimney"}),
    "building_terrace":     dict(wall="terrace_wall", roof="terrace_roof", wh=84,  rh=26, shape="gable", feats={"chimney"}),
    "building_apartment":   dict(wall="apt_wall",     roof="apt_roof",     wh=178, rh=0,  shape="flat",  feats={"grid"}),
    "building_workplace":   dict(wall="work_wall",    roof="work_roof",    wh=140, rh=0,  shape="flat",  feats={"glass"}),
    "building_school":      dict(wall="school_wall",  roof="school_roof",  wh=104, rh=30, shape="gable", feats={"sign"}),
    "building_shop":        dict(wall="shop_wall",    roof="shop_roof",    wh=86,  rh=0,  shape="flat",  feats={"shopfront", "awning", "sign"}),
    "building_grocery":     dict(wall="grocery_wall", roof="grocery_roof", wh=86,  rh=0,  shape="flat",  feats={"shopfront", "awning_green", "sign"}),
    "building_cafe":        dict(wall="cafe_wall",    roof="cafe_roof",    wh=82,  rh=26, shape="gable", feats={"shopfront", "awning"}),
    "building_pub":         dict(wall="pub_wall",     roof="pub_roof",     wh=94,  rh=30, shape="gable", feats={"hanging_sign", "chimney"}),
    "building_bar":         dict(wall="bar_wall",     roof="bar_roof",     wh=98,  rh=0,  shape="flat",  feats={"neon"}),
    "building_sports":      dict(wall="sports_wall",  roof="sports_roof",  wh=118, rh=14, shape="flat",  feats={"big"}),
    "building_institution": dict(wall="inst_wall",    roof="inst_roof",    wh=112, rh=28, shape="gable", feats={"steps"}),
}


# ---------------------------------------------------------------------------
# Colour + geometry helpers
# ---------------------------------------------------------------------------

def _shade(hex_colour: str, factor: float) -> str:
    h = hex_colour.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r, g, b = (max(0, min(255, int(c * factor))) for c in (r, g, b))
    return f"#{r:02X}{g:02X}{b:02X}"


def _P(name: str) -> str:
    return PALETTE[name]


def _variant(sx: float, sy: float) -> int:
    return int(hashlib.md5(f"{sx:.0f}:{sy:.0f}".encode()).hexdigest(), 16)


def _poly(points: List[Tuple[float, float]], fill: str,
          stroke: Optional[str] = None, sw: float = 1.0,
          opacity: Optional[float] = None) -> str:
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    s = f'<polygon points="{pts}" fill="{fill}"'
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{sw}"'
    if opacity is not None:
        s += f' opacity="{opacity}"'
    return s + "/>"


def _box_corners(sx: float, sy: float, height: float,
                 cols: int = 1, rows: int = 1) -> Dict[str, Tuple[float, float]]:
    cx = sx + HALF_W
    hw = HALF_W * max(cols, rows)
    hh = HALF_H * max(cols, rows)
    bB = (cx, sy + TILE_H)
    bL = (cx - hw, sy + TILE_H - hh)
    bR = (cx + hw, sy + TILE_H - hh)
    bT = (cx, sy + TILE_H - 2 * hh)
    up = lambda p: (p[0], p[1] - height)
    return {"bB": bB, "bL": bL, "bR": bR, "bT": bT,
            "tB": up(bB), "tL": up(bL), "tR": up(bR), "tT": up(bT)}


def _qpt(c00, c10, c01, c11, u, v):
    """Bilinear point inside a quad: u along c00->c10, v along c00->c01."""
    return (((1 - u) * (1 - v) * c00[0] + u * (1 - v) * c10[0]
             + (1 - u) * v * c01[0] + u * v * c11[0]),
            ((1 - u) * (1 - v) * c00[1] + u * (1 - v) * c10[1]
             + (1 - u) * v * c01[1] + u * v * c11[1]))


def _panel(face, u0, u1, v0, v1, fill, stroke=None, sw=0.7, opacity=None):
    """A rectangular panel in face-space (face = (c00,c10,c01,c11))."""
    p = [_qpt(*face, u0, v0), _qpt(*face, u1, v0),
         _qpt(*face, u1, v1), _qpt(*face, u0, v1)]
    return _poly(p, fill, stroke=stroke, sw=sw, opacity=opacity)


# ---------------------------------------------------------------------------
# The tileset
# ---------------------------------------------------------------------------

class ProceduralTileset:
    """Vector procedural tiles satisfying the compositor's Tileset interface."""

    # -- ground ------------------------------------------------------------
    def render_ground(self, tile_id: str, sx: float, sy: float) -> str:
        if tile_id.startswith("road") or tile_id.startswith("path"):
            return self._road(tile_id, sx, sy)
        return self._terrain(tile_id, sx, sy)

    def _terrain(self, tile_id: str, sx: float, sy: float) -> str:
        base = {"terrain_grass": "grass", "terrain_park": "park",
                "terrain_garden": "garden", "terrain_pavement": "pavement",
                "terrain_plaza": "plaza", "terrain_dirt": "dirt",
                "terrain_sand": "sand", "terrain_water": "water"}.get(tile_id, "grass")
        col = _P(base)
        pts = diamond_points(sx, sy)
        out = [f'<polygon points="{pts}" fill="{col}" '
               f'stroke="{_shade(col, 0.9)}" stroke-width="1"/>']
        cx, cy = sx + HALF_W, sy + HALF_H
        rng = _variant(sx, sy)
        if base in ("grass", "park", "garden"):
            for k in range(3):
                r2 = (rng >> (k * 5)) % 100
                tx, ty = cx + (r2 % 7 - 3) * 12, cy + ((r2 // 7) % 5 - 2) * 7
                out.append(_poly([(tx, ty - 5), (tx + 4, ty), (tx, ty + 3),
                                  (tx - 4, ty)], _shade(col, 0.86)))
            if base == "garden":
                for k in range(4):
                    r2 = (rng >> (k * 6 + 2)) % 100
                    fx, fy = cx + (r2 % 9 - 4) * 11, cy + ((r2 // 9) % 5 - 2) * 6
                    out.append(f'<circle cx="{fx:.0f}" cy="{fy:.0f}" r="2.5" '
                               f'fill="{_P("flower_a") if k % 2 else _P("flower_b")}"/>')
        elif base in ("pavement", "plaza"):
            for (x1, y1, x2, y2) in (
                (sx + HALF_W, sy + 8, sx + TILE_W - 8, sy + HALF_H),
                (sx + 8, sy + HALF_H, sx + HALF_W, sy + TILE_H - 8)):
                out.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" '
                           f'y2="{y2:.0f}" stroke="{_shade(col, 0.9)}" '
                           f'stroke-width="1" opacity="0.6"/>')
        elif base == "water":
            out.append(_poly([(cx - 26, cy), (cx - 10, cy - 5), (cx + 6, cy),
                              (cx - 10, cy + 5)], _P("water_hi"), opacity=0.7))
        return "".join(out)

    def _road(self, tile_id: str, sx: float, sy: float) -> str:
        path = tile_id.startswith("path")
        grass = _shade(_P("grass"), 0.94)
        inset = 40 if path else 24
        pts = diamond_points(sx, sy)
        asphalt = diamond_points(sx + inset, sy + inset // 2)
        out = [f'<polygon points="{pts}" fill="{grass}"/>']
        if not path:
            out.append(f'<polygon points="{diamond_points(sx + 18, sy + 9)}" '
                       f'fill="{_P("kerb")}"/>')
        out.append(f'<polygon points="{asphalt}" '
                   f'fill="{_P("wood") if path else _P("road")}"/>')
        cx = sx + HALF_W
        if not path:
            if "cross" in tile_id or "_t" in tile_id:
                out.append(f'<line x1="{sx+30}" y1="{sy+HALF_H}" x2="{sx+TILE_W-30}" '
                           f'y2="{sy+HALF_H}" stroke="{_P("mark")}" stroke-width="2" '
                           f'stroke-dasharray="7 7" opacity="0.75"/>')
            out.append(f'<line x1="{cx}" y1="{sy+18}" x2="{cx}" y2="{sy+TILE_H-18}" '
                       f'stroke="{_P("mark")}" stroke-width="2" '
                       f'stroke-dasharray="8 8" opacity="0.75"/>')
        return "".join(out)

    # -- objects -----------------------------------------------------------
    def render_object(self, tile_id: str, sx: float, sy: float,
                      footprint: Tuple[int, int] = (1, 1)) -> str:
        if tile_id in BUILDING:
            return self._building(tile_id, sx, sy, footprint)
        return self._prop(tile_id, sx, sy)

    def _building(self, tile_id: str, sx: float, sy: float,
                  footprint: Tuple[int, int]) -> str:
        spec = BUILDING[tile_id]
        cols, rows = footprint
        rng = _variant(sx, sy)
        wall = _P(spec["wall"])
        roof = _shade(_P(spec["roof"]), 0.92 + (rng % 16) / 100.0)
        feats = spec["feats"]
        c = _box_corners(sx, sy, spec["wh"], cols, rows)

        left = (c["bL"], c["bB"], c["tL"], c["tB"])    # left wall face
        right = (c["bB"], c["bR"], c["tB"], c["tR"])   # right (viewer-facing) wall

        out = [_poly([c["bL"], c["bB"], c["tB"], c["tL"]], _shade(wall, F_LEFT)),
               _poly([c["bB"], c["bR"], c["tR"], c["tB"]], _shade(wall, F_RIGHT))]

        # glass frontage (offices): translucent panels instead of small windows
        if "glass" in feats:
            for face, fac in ((left, F_LEFT), (right, F_RIGHT)):
                out.append(_panel(face, 0.12, 0.88, 0.10, 0.92,
                                  _shade(_P("glass"), fac), opacity=0.9))
                for u in (0.30, 0.50, 0.70):
                    out.append(_panel(face, u, u + 0.006, 0.10, 0.92,
                                      _shade(wall, fac * 0.9)))
        else:
            # window grid; density from wall height (denser if "grid")
            levels = max(1, int((spec["wh"] - 22) / (26 if "grid" in feats else 34)))
            gap = 0.62 / levels
            ground_shop = "shopfront" in feats
            for lvl in range(levels):
                v0 = 0.18 + lvl * gap
                # leave the ground floor for a shopfront if present
                if ground_shop and lvl == 0:
                    continue
                for (u0, u1) in ((0.18, 0.36), (0.44, 0.62), (0.70, 0.88)):
                    for face, fac, bit in ((left, F_LEFT, lvl * 6 + 0),
                                           (right, F_RIGHT, lvl * 6 + 3)):
                        lit = ((rng >> (bit + int(u0 * 10))) & 1) == 1
                        out.append(_panel(face, u0, u1, v0, v0 + gap * 0.5,
                                          _shade(_P("window") if lit
                                                 else _P("window_off"), fac),
                                          stroke=_shade(_P("window_off"), fac * 0.7)))

        # shopfront: a big display window + door on the ground floor (right wall)
        if "shopfront" in feats:
            out.append(_panel(right, 0.14, 0.62, 0.02, 0.24,
                              _shade(_P("glass"), F_RIGHT), opacity=0.92,
                              stroke=_shade(wall, 0.6)))
            out.append(_panel(right, 0.68, 0.86, 0.02, 0.30, _P("door")))
            if "awning" in feats or "awning_green" in feats:
                aw = _P("awning_green" if "awning_green" in feats else "awning")
                out.append(_panel(right, 0.10, 0.90, 0.26, 0.30, _shade(aw, F_RIGHT)))
                out.append(_panel(right, 0.10, 0.90, 0.24, 0.26, _shade(aw, 1.0)))
        else:
            # a plain door low on the right wall
            out.append(_panel(right, 0.44, 0.60, 0.0, 0.28, _P("door")))

        # signage
        if "sign" in feats:
            out.append(_panel(right, 0.16, 0.60, 0.66, 0.80, _P("sign"),
                              stroke=_P("sign_dark")))
        if "neon" in feats:
            out.append(_panel(right, 0.20, 0.64, 0.60, 0.72, _P("neon"), opacity=0.85))
        if "hanging_sign" in feats:
            hx, hy = _qpt(*right, 0.30, 0.66)
            out.append(f'<rect x="{hx-14:.0f}" y="{hy:.0f}" width="24" height="16" '
                       f'rx="2" fill="{_P("sign")}" stroke="{_P("sign_dark")}"/>')
        if "steps" in feats:
            sx2, sy2 = _qpt(*right, 0.36, 0.0)
            out.append(f'<rect x="{sx2-6:.0f}" y="{sy2:.0f}" width="44" height="6" '
                       f'fill="{_shade(_P("plaza"),0.9)}"/>')

        # roof
        if spec["shape"] == "gable":
            out.append(self._roof_gable(c, roof, spec["rh"]))
            if "chimney" in feats:
                out.append(self._chimney(c, rng))
        elif spec["shape"] == "hip":
            out.append(self._roof_hip(c, roof, spec["rh"]))
        else:  # flat parapet
            out.append(_poly([c["tT"], c["tR"], c["tB"], c["tL"]], _shade(roof, 1.0)))
            out.append(_poly([c["tL"], c["tT"], c["tR"], c["tB"]],
                             _shade(roof, 1.0), stroke=_shade(roof, 0.7), sw=2))
        return "".join(out)

    def _roof_gable(self, c, roof, rh):
        tT, tR, tB, tL = c["tT"], c["tR"], c["tB"], c["tL"]
        mid = lambda a, b: ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        up = lambda p: (p[0], p[1] - rh)
        p1, p2 = up(mid(tL, tT)), up(mid(tR, tB))
        return (_poly([p1, tL, tB, p2], _shade(roof, ROOF_DARK))
                + _poly([p1, tT, tR, p2], _shade(roof, ROOF_LIT))
                + f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" '
                  f'y2="{p2[1]:.1f}" stroke="{_shade(roof,0.6)}" stroke-width="1.5"/>')

    def _roof_hip(self, c, roof, rh):
        tT, tR, tB, tL = c["tT"], c["tR"], c["tB"], c["tL"]
        apex = ((tT[0] + tB[0]) / 2, (tT[1] + tB[1]) / 2 - rh)
        return (_poly([tL, tT, apex], _shade(roof, ROOF_LIT))
                + _poly([tT, tR, apex], _shade(roof, ROOF_LIT * 0.9))
                + _poly([tB, tL, apex], _shade(roof, ROOF_DARK * 1.05))
                + _poly([tR, tB, apex], _shade(roof, ROOF_DARK)))

    def _chimney(self, c, rng):
        bx, by = _qpt(c["tL"], c["tT"], c["tB"], c["tR"], 0.7, 0.35)
        return (f'<rect x="{bx-4:.0f}" y="{by-30:.0f}" width="9" height="24" '
                f'fill="{_shade(_P("terrace_roof"),0.8)}"/>')

    def _prop(self, tile_id: str, sx: float, sy: float) -> str:
        cx, by = base_bottom(sx, sy)
        rng = _variant(sx, sy)
        if tile_id.startswith("prop_tree"):
            h, r = 30 + rng % 12, 22 + rng % 8
            return (f'<rect x="{cx-5:.1f}" y="{by-h-14:.1f}" width="10" '
                    f'height="{h+14:.0f}" rx="3" fill="{_P("trunk")}"/>'
                    + _poly([(cx, by - h - r - 6), (cx + r, by - h - 4),
                             (cx, by - h + r - 8), (cx - r, by - h - 4)], _P("canopy"))
                    + _poly([(cx, by - h - r - 6), (cx + r * 0.5, by - h - r * 0.5 - 5),
                             (cx, by - h - 2), (cx - r * 0.5, by - h - r * 0.5 - 5)],
                            _P("canopy_hi"), opacity=0.75))
        if tile_id.startswith("prop_bush"):
            return (_poly([(cx, by - 26), (cx + 16, by - 8), (cx, by - 2),
                          (cx - 16, by - 8)], _P("bush"))
                    + f'<circle cx="{cx:.1f}" cy="{by-16:.1f}" r="5" '
                      f'fill="{_shade(_P("bush"),1.15)}" opacity="0.6"/>')
        if tile_id.startswith("prop_hedge"):
            return (_poly([(cx - 44, by - 8), (cx, by - 20), (cx + 44, by - 8),
                          (cx, by + 4)], _P("hedge"))
                    + _poly([(cx - 44, by - 12), (cx, by - 24), (cx + 44, by - 12),
                            (cx, by - 8)], _shade(_P("hedge"), 1.12), opacity=0.7))
        if tile_id.startswith("prop_flowerbed"):
            out = [_poly([(cx - 26, by - 6), (cx, by - 15), (cx + 26, by - 6),
                         (cx, by + 3)], _shade(_P("dirt"), 1.05))]
            for k in range(6):
                r2 = (rng >> (k * 4)) % 100
                fx, fy = cx + (r2 % 9 - 4) * 5, by - 6 - (r2 // 9) % 6
                out.append(f'<circle cx="{fx:.0f}" cy="{fy:.0f}" r="2.5" '
                           f'fill="{_P("flower_a") if k%2 else _P("flower_b")}"/>')
            return "".join(out)
        if tile_id.startswith("prop_fountain"):
            return (_poly([(cx - 26, by - 8), (cx, by - 18), (cx + 26, by - 8),
                          (cx, by + 2)], _shade(_P("plaza"), 0.9))
                    + _poly([(cx - 16, by - 10), (cx, by - 16), (cx + 16, by - 10),
                            (cx, by - 4)], _P("fountain"))
                    + f'<rect x="{cx-2:.0f}" y="{by-30:.0f}" width="4" height="16" '
                      f'fill="{_shade(_P("fountain"),0.85)}"/>'
                    + f'<circle cx="{cx:.0f}" cy="{by-32:.0f}" r="4" '
                      f'fill="{_P("water_hi")}" opacity="0.8"/>')
        if tile_id.startswith("prop_playground"):
            return (f'<rect x="{cx-30:.1f}" y="{by-42:.1f}" width="60" height="30" '
                    f'rx="4" fill="{_P("play")}" stroke="{_shade(_P("play"),0.75)}"/>'
                    f'<line x1="{cx-30:.1f}" y1="{by-42:.1f}" x2="{cx+30:.1f}" '
                    f'y2="{by-12:.1f}" stroke="{_shade(_P("play"),0.7)}"/>')
        if tile_id.startswith("prop_bench"):
            return (f'<rect x="{cx-18:.1f}" y="{by-18:.1f}" width="36" height="6" '
                    f'fill="{_P("wood")}"/><rect x="{cx-18:.1f}" y="{by-12:.1f}" '
                    f'width="36" height="4" fill="{_shade(_P("wood"),0.8)}"/>')
        if tile_id.startswith("prop_streetlight"):
            return (f'<rect x="{cx-3:.1f}" y="{by-66:.1f}" width="6" height="60" '
                    f'fill="{_P("metal")}"/><circle cx="{cx:.1f}" cy="{by-70:.1f}" '
                    f'r="7" fill="{_P("lamp")}"/><circle cx="{cx:.1f}" cy="{by-70:.1f}"'
                    f' r="12" fill="{_P("lamp")}" opacity="0.25"/>')
        if tile_id.startswith("prop_bin"):
            return (f'<rect x="{cx-7:.0f}" y="{by-22:.0f}" width="14" height="20" '
                    f'rx="2" fill="{_P("bin")}"/><rect x="{cx-8:.0f}" y="{by-24:.0f}" '
                    f'width="16" height="4" rx="2" fill="{_shade(_P("bin"),0.8)}"/>')
        if tile_id.startswith("prop_bollard"):
            return (f'<rect x="{cx-2:.0f}" y="{by-16:.0f}" width="5" height="14" '
                    f'rx="2" fill="{_P("metal")}"/>')
        if tile_id.startswith("prop_bus_stop"):
            return (f'<rect x="{cx-2:.0f}" y="{by-40:.0f}" width="4" height="38" '
                    f'fill="{_P("metal")}"/><rect x="{cx-2:.0f}" y="{by-40:.0f}" '
                    f'width="22" height="12" fill="{_P("glass")}" opacity="0.8" '
                    f'stroke="{_P("metal")}"/>')
        if tile_id.startswith("prop_fence"):
            return (f'<rect x="{cx-40:.1f}" y="{by-22:.1f}" width="80" height="5" '
                    f'fill="{_P("wood")}"/><rect x="{cx-40:.1f}" y="{by-16:.1f}" '
                    f'width="80" height="10" fill="{_shade(_P("wood"),0.82)}" '
                    f'opacity="0.7"/>')
        return f'<circle cx="{cx:.1f}" cy="{by-12:.1f}" r="9" fill="#B0B0B0"/>'

    # -- movable agents (actor layer): people and vehicles -----------------
    def render_actor(self, sprite_id: str, sx: float, sy: float,
                     state_colour: Optional[str] = None) -> str:
        if sprite_id.startswith("vehicle") or sprite_id in ("car", "bike", "bus"):
            return self._vehicle(sprite_id, sx, sy)
        return self._person(sprite_id, sx, sy, state_colour)

    def _person(self, sprite_id, sx, sy, state_colour):
        cx, by = base_bottom(sx, sy)
        child = "child" in sprite_id
        h, head_r = (32, 7) if child else (44, 9)
        body = "#7B8B6B" if child else "#5B6B7B"
        out = []
        if state_colour:
            out.append(f'<ellipse cx="{cx:.1f}" cy="{by-3:.1f}" rx="16" ry="8" '
                       f'fill="none" stroke="{state_colour}" stroke-width="3" '
                       f'opacity="0.9"/>')
        out.append(f'<ellipse cx="{cx:.1f}" cy="{by-2:.1f}" rx="11" ry="5" '
                   f'fill="#000000" opacity="0.12"/>')
        out.append(f'<rect x="{cx-6:.1f}" y="{by-h+head_r:.1f}" width="12" '
                   f'height="{h-head_r-2:.0f}" rx="5" fill="{body}"/>')
        out.append(f'<circle cx="{cx:.1f}" cy="{by-h+head_r-2:.1f}" r="{head_r}" '
                   f'fill="#E8C9A0"/>')
        return "".join(out)

    def _vehicle(self, sprite_id, sx, sy):
        cx, by = base_bottom(sx, sy)
        out = [f'<ellipse cx="{cx:.0f}" cy="{by-2:.0f}" rx="26" ry="8" '
               f'fill="#000000" opacity="0.12"/>']
        if "bike" in sprite_id:
            out.append(f'<circle cx="{cx-12:.0f}" cy="{by-8:.0f}" r="7" fill="none" '
                       f'stroke="{_P("tyre")}" stroke-width="2.5"/>')
            out.append(f'<circle cx="{cx+12:.0f}" cy="{by-8:.0f}" r="7" fill="none" '
                       f'stroke="{_P("tyre")}" stroke-width="2.5"/>')
            out.append(f'<path d="M{cx-12},{by-8} L{cx},{by-20} L{cx+12},{by-8} '
                       f'M{cx},{by-20} L{cx-2},{by-8}" stroke="{_P("bike")}" '
                       f'stroke-width="2" fill="none"/>')
            return "".join(out)
        # car / bus: an isometric body with a lighter cabin and dark wheels
        col = {"vehicle_car_b": "car_b", "vehicle_car_c": "car_c"}.get(sprite_id, "car_a")
        if "bus" in sprite_id:
            col = "bus"
        body = _P(col)
        w = 40 if "bus" in sprite_id else 30
        # lower body (parallelogram, iso 3/4)
        out.append(_poly([(cx - w, by - 10), (cx, by - 4), (cx + w, by - 10),
                          (cx, by - 16)], _shade(body, 0.8)))
        out.append(_poly([(cx - w, by - 10), (cx - w, by - 20), (cx, by - 26),
                          (cx, by - 16)], _shade(body, F_LEFT)))
        out.append(_poly([(cx, by - 16), (cx, by - 26), (cx + w, by - 20),
                          (cx + w, by - 10)], _shade(body, F_RIGHT)))
        out.append(_poly([(cx - w, by - 20), (cx, by - 26), (cx + w, by - 20),
                          (cx, by - 14)], _shade(body, 1.05)))
        # windows
        out.append(_poly([(cx - w * 0.6, by - 19), (cx, by - 23),
                          (cx + w * 0.6, by - 19), (cx, by - 16)],
                         _shade(_P("glass"), 0.95), opacity=0.9))
        # wheels
        for wx in (cx - w * 0.6, cx + w * 0.6):
            out.append(f'<ellipse cx="{wx:.0f}" cy="{by-7:.0f}" rx="4" ry="3" '
                       f'fill="{_P("tyre")}"/>')
        return "".join(out)
