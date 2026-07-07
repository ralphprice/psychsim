"""explore.py -- run several edge-condition explorations and render them.

Writes SVG phase diagrams and a bifurcation curve, and reports the edges the
tool locates. It does not assume where the boundaries are.
"""
from __future__ import annotations
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .config import Config
from .sweep import sweep_1d, phase_map_2d, boundary_cells, bisect_edge
from .viz import render_phase_svg, render_sweep_svg, save_svg


def report(nx: int = 21, ny: int = 21) -> str:
    L = ["#" * 82,
         "  EDGE-CONDITION EXPLORER -- where does the fearless disposition bifurcate?",
         "  (the tool reveals the boundaries; no outcome is assumed)",
         "#" * 82]

    # --- 1-D: warmth at low structure -------------------------------------
    sw = sweep_1d(Config(structure=0.30), "warmth", 0.0, 1.0, steps=25)
    save_svg(render_sweep_svg(sw, title="Bifurcation along warmth (structure=0.30)"),
             "bifurcation_warmth.svg")
    L += ["", "[1] 1-D sweep -- warmth, at low structure (0.30):", sw.summary(),
          "    -> wrote bifurcation_warmth.svg"]

    # --- 2-D: warmth x structure (the environment phase diagram) ----------
    pm1 = phase_map_2d(Config(), "warmth", 0.0, 1.0, "structure", 0.0, 1.0, nx=nx, ny=ny)
    save_svg(render_phase_svg(pm1, title="Phase diagram: warmth x structure (fearless child)"),
             "phase_warmth_structure.svg")
    L += ["", "[2] 2-D phase map -- warmth x structure:",
          f"    basins: {pm1.region_counts()}",
          f"    separatrix (edge) cells: {len(boundary_cells(pm1))}",
          "    -> wrote phase_warmth_structure.svg"]

    # --- 2-D: starting conscience x warmth --------------------------------
    pm2 = phase_map_2d(Config(structure=0.5), "control_start", 0.0, 1.0,
                       "warmth", 0.0, 1.0, nx=nx, ny=ny)
    save_svg(render_phase_svg(pm2, title="Phase diagram: starting conscience x warmth"),
             "phase_control_warmth.svg")
    L += ["", "[3] 2-D phase map -- starting conscience (control_start) x warmth:",
          f"    basins: {pm2.region_counts()}",
          f"    separatrix (edge) cells: {len(boundary_cells(pm2))}",
          "    -> wrote phase_control_warmth.svg"]

    # --- precise edges via bisection --------------------------------------
    L += ["", "[4] Precise tipping points (bisection):"]
    for struct in (0.2, 0.5, 0.8):
        e = bisect_edge(Config(structure=struct), "warmth", 0.0, 1.0)
        if e:
            L.append(f"    at structure={struct:.1f}: warmth boundary "
                     f"{e['boundary']:.3f}  ({e['below'][1]} below -> {e['above'][1]} above)")
        else:
            L.append(f"    at structure={struct:.1f}: no transition across warmth 0..1")

    L += ["", "#" * 82,
          "  NOTE: these are the boundaries of the CURRENT illustrative model. The",
          "  explorer is the instrument; run it on any calibration or a richer model",
          "  to find that model's edge conditions. Nothing here is fitted or assumed.",
          "#" * 82]
    return "\n".join(L)


if __name__ == "__main__":
    print(report())
