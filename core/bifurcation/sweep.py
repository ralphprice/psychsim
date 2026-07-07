"""
sweep.py -- explore the parameter space and locate the edges.

Four tools, none of which assume where the boundary lies:

  sweep_1d      -- vary one parameter across a range; report the outcome and the
                   continuous score at each step, and the value(s) where the
                   classification changes (the bifurcation point along that axis).
  phase_map_2d  -- vary two parameters over a grid; classify every cell. The
                   result is a phase diagram of the outcome basins.
  boundary_cells-- the cells of a phase map that sit next to a different outcome:
                   the separatrix, i.e. the edge conditions.
  bisect_edge   -- between two Configs with different outcomes, bisect to locate
                   the transition to a chosen precision -- the exact tipping point.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple

from .config import Config, run_config, RunResult


def _frange(lo: float, hi: float, steps: int) -> List[float]:
    if steps <= 1:
        return [lo]
    return [lo + (hi - lo) * i / (steps - 1) for i in range(steps)]


# ---------------------------------------------------------------------------
# 1-D sweep
# ---------------------------------------------------------------------------

@dataclass
class Sweep1D:
    param: str
    values: List[float]
    results: List[RunResult]
    transitions: List[Tuple[float, float, str, str]]  # (v_before, v_after, cls_before, cls_after)

    def summary(self) -> str:
        lines = [f"1-D sweep over '{self.param}'  ({len(self.values)} points)"]
        # compact strip of the classification along the axis
        strip = "".join({"sophropathic": "S", "intermediate": ".",
                         "psychopathic": "P"}.get(r.classification, "?")
                        for r in self.results)
        lines.append(f"  {self.values[0]:.2f} |{strip}| {self.values[-1]:.2f}   (S=sophro . =inter P=psycho)")
        if self.transitions:
            for vb, va, cb, ca in self.transitions:
                lines.append(f"  transition {cb} -> {ca} between {self.param}="
                             f"{vb:.3f} and {va:.3f}")
        else:
            lines.append("  no classification change across this range")
        return "\n".join(lines)


def sweep_1d(base: Config, param: str, lo: float, hi: float, steps: int = 21) -> Sweep1D:
    values = _frange(lo, hi, steps)
    results = [run_config(base.with_(**{param: v})) for v in values]
    transitions = []
    for i in range(1, len(results)):
        if results[i].classification != results[i - 1].classification:
            transitions.append((values[i - 1], values[i],
                                results[i - 1].classification, results[i].classification))
    return Sweep1D(param, values, results, transitions)


# ---------------------------------------------------------------------------
# 2-D phase map
# ---------------------------------------------------------------------------

@dataclass
class PhaseMap:
    param_x: str
    param_y: str
    xs: List[float]
    ys: List[float]
    grid: List[List[RunResult]]   # grid[y][x]

    def classification_grid(self) -> List[List[str]]:
        return [[cell.classification for cell in row] for row in self.grid]

    def region_counts(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for row in self.grid:
            for cell in row:
                counts[cell.classification] = counts.get(cell.classification, 0) + 1
        return counts


def phase_map_2d(base: Config, param_x: str, x_lo: float, x_hi: float,
                 param_y: str, y_lo: float, y_hi: float,
                 nx: int = 21, ny: int = 21) -> PhaseMap:
    xs, ys = _frange(x_lo, x_hi, nx), _frange(y_lo, y_hi, ny)
    grid = [[run_config(base.with_(**{param_x: x, param_y: y})) for x in xs]
            for y in ys]
    return PhaseMap(param_x, param_y, xs, ys, grid)


def boundary_cells(pm: PhaseMap) -> List[Tuple[int, int]]:
    """Grid indices (ix, iy) whose classification differs from a 4-neighbour --
    the separatrix / edge conditions."""
    cls = pm.classification_grid()
    ny, nx = len(cls), len(cls[0])
    edges = []
    for iy in range(ny):
        for ix in range(nx):
            here = cls[iy][ix]
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                jx, jy = ix + dx, iy + dy
                if 0 <= jx < nx and 0 <= jy < ny and cls[jy][jx] != here:
                    edges.append((ix, iy)); break
    return edges


# ---------------------------------------------------------------------------
# Bisection edge-finder
# ---------------------------------------------------------------------------

def bisect_edge(base: Config, param: str, lo: float, hi: float,
                tol: float = 1e-3, max_iter: int = 40) -> Optional[Dict[str, object]]:
    """Between param=lo and param=hi, if the classification differs, bisect to
    locate the transition to precision `tol`. Returns the boundary value and the
    outcomes either side, or None if both ends share a classification."""
    r_lo, r_hi = run_config(base.with_(**{param: lo})), run_config(base.with_(**{param: hi}))
    if r_lo.classification == r_hi.classification:
        return None
    a, b = lo, hi
    ca = r_lo.classification
    for _ in range(max_iter):
        if (b - a) <= tol:
            break
        mid = (a + b) / 2
        cm = run_config(base.with_(**{param: mid})).classification
        if cm == ca:
            a = mid
        else:
            b = mid
    return {"param": param, "boundary": (a + b) / 2, "tol": b - a,
            "below": (a, run_config(base.with_(**{param: a})).classification),
            "above": (b, run_config(base.with_(**{param: b})).classification)}
