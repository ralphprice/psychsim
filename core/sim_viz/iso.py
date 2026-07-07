"""
iso.py -- the isometric geometry contract.

Implements exactly the geometry in Part II of the graphics specification, so the
compositor places tiles the way the spec promises and real art produced to the
spec drops straight in.

  * 2:1 dimetric projection
  * base tile 256 x 128 (TILE_W x TILE_H)
  * a cell at grid (gx, gy) is drawn at
        screen_x = origin_x + (gx - gy) * TILE_W/2
        screen_y = origin_y + (gx + gy) * TILE_H/2
  * non-ground sprites are anchored bottom-centre on the cell's base diamond
  * draw order is the painter's algorithm on (gx + gy)
"""

from __future__ import annotations
from typing import List, Tuple

TILE_W = 256          # base tile width  (bounding box)
TILE_H = 128          # base tile height (bounding box); 2:1 diamond
HALF_W = TILE_W // 2
HALF_H = TILE_H // 2


def cell_to_screen(gx: int, gy: int, origin_x: float, origin_y: float
                   ) -> Tuple[float, float]:
    """Top-left of the cell's bounding box in screen space."""
    return (origin_x + (gx - gy) * HALF_W,
            origin_y + (gx + gy) * HALF_H)


def diamond_points(sx: float, sy: float) -> str:
    """SVG points for the ground diamond whose bounding box top-left is (sx,sy).
    Vertices: top, right, bottom, left."""
    return (f"{sx+HALF_W},{sy} {sx+TILE_W},{sy+HALF_H} "
            f"{sx+HALF_W},{sy+TILE_H} {sx},{sy+HALF_H}")


def diamond_center(sx: float, sy: float) -> Tuple[float, float]:
    return (sx + HALF_W, sy + HALF_H)


def base_bottom(sx: float, sy: float) -> Tuple[float, float]:
    """The bottom vertex of the base diamond -- the anchor point for sprites."""
    return (sx + HALF_W, sy + TILE_H)


def z_index(gx: int, gy: int, layer: int) -> Tuple[int, int]:
    """Sort key for the painter's algorithm: farther cells first, then by layer
    within a cell. layer: 0 ground, 1 road, 2 object, 3 actor, 4 overlay."""
    return (gx + gy, layer)


def iso_box_faces(sx: float, sy: float, height: float,
                  cols: int = 1, rows: int = 1) -> dict:
    """Return the three visible faces of an isometric box sitting on the cell's
    base diamond, as SVG point strings: 'top', 'left', 'right'.

    For a multi-cell footprint the base diamond is widened by the footprint; this
    is an approximation used by the placeholder tileset (real art is a PNG sized
    per the spec)."""
    cx = sx + HALF_W
    # widen the base diamond for the footprint (approximate)
    half_w = HALF_W * max(cols, rows)
    half_h = HALF_H * max(cols, rows)
    # base diamond vertices (anchored so its bottom vertex is the cell's bottom)
    b_bottom = (cx, sy + TILE_H)
    b_left = (cx - half_w, sy + TILE_H - half_h)
    b_right = (cx + half_w, sy + TILE_H - half_h)
    b_top = (cx, sy + TILE_H - 2 * half_h)
    # top diamond is the base lifted by `height`
    def up(p): return (p[0], p[1] - height)
    t_bottom, t_left, t_right, t_top = map(up, (b_bottom, b_left, b_right, b_top))

    top = f"{t_top[0]},{t_top[1]} {t_right[0]},{t_right[1]} {t_bottom[0]},{t_bottom[1]} {t_left[0]},{t_left[1]}"
    left = f"{b_left[0]},{b_left[1]} {b_bottom[0]},{b_bottom[1]} {t_bottom[0]},{t_bottom[1]} {t_left[0]},{t_left[1]}"
    right = f"{b_bottom[0]},{b_bottom[1]} {b_right[0]},{b_right[1]} {t_right[0]},{t_right[1]} {t_bottom[0]},{t_bottom[1]}"
    return {"top": top, "left": left, "right": right}
