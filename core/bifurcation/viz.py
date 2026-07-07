"""
viz.py -- see the edges.

render_phase_svg draws a 2-D phase map as a heatmap: one colour per outcome
basin (sophropathic / intermediate / psychopathic), with the boundary cells (the
edge conditions) outlined. render_sweep_svg draws a 1-D sweep as the continuous
score along the axis, with the classification bands beneath it, so the sharpness
of the transition is visible.
"""

from __future__ import annotations
from typing import List

from .sweep import PhaseMap, Sweep1D, boundary_cells

BASIN_COLOUR = {
    "sophropathic": "#1E8449",   # green
    "intermediate": "#E67E22",   # amber
    "psychopathic": "#C0392B",   # red
}


def render_phase_svg(pm: PhaseMap, cell: int = 26, title: str = "") -> str:
    nx, ny = len(pm.xs), len(pm.ys)
    ml, mt, mr, mb = 70, 46, 150, 54     # margins
    W = ml + nx * cell + mr
    H = mt + ny * cell + mb
    edges = set(boundary_cells(pm))
    cls = pm.classification_grid()

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'font-family="Arial, sans-serif">',
         f'<rect x="0" y="0" width="{W}" height="{H}" fill="#FFFFFF"/>']
    if title:
        p.append(f'<text x="{ml}" y="26" font-size="15" font-weight="bold" '
                 f'fill="#1F3864">{title}</text>')

    # cells (y drawn bottom-up: low y at the bottom)
    for iy in range(ny):
        for ix in range(nx):
            sx = ml + ix * cell
            sy = mt + (ny - 1 - iy) * cell
            colour = BASIN_COLOUR.get(cls[iy][ix], "#999999")
            stroke = "#111111" if (ix, iy) in edges else "none"
            sw = 1.6 if (ix, iy) in edges else 0
            p.append(f'<rect x="{sx}" y="{sy}" width="{cell}" height="{cell}" '
                     f'fill="{colour}" stroke="{stroke}" stroke-width="{sw}"/>')

    # axes
    ax0, ay1 = ml, mt + ny * cell
    p.append(f'<line x1="{ax0}" y1="{mt}" x2="{ax0}" y2="{ay1}" stroke="#333" stroke-width="1"/>')
    p.append(f'<line x1="{ax0}" y1="{ay1}" x2="{ml+nx*cell}" y2="{ay1}" stroke="#333" stroke-width="1"/>')
    p.append(f'<text x="{ml+nx*cell/2}" y="{ay1+34}" text-anchor="middle" '
             f'font-size="12" fill="#333">{pm.param_x}  ({pm.xs[0]:.2f} \u2192 {pm.xs[-1]:.2f})</text>')
    p.append(f'<text x="{ml-46}" y="{mt+ny*cell/2}" text-anchor="middle" font-size="12" '
             f'fill="#333" transform="rotate(-90 {ml-46} {mt+ny*cell/2})">'
             f'{pm.param_y}  ({pm.ys[0]:.2f} \u2192 {pm.ys[-1]:.2f})</text>')

    # legend
    lx, ly = ml + nx * cell + 18, mt + 6
    counts = pm.region_counts()
    p.append(f'<text x="{lx}" y="{ly}" font-size="12" font-weight="bold" fill="#333">basin</text>')
    for i, (name, col) in enumerate(BASIN_COLOUR.items()):
        yy = ly + 20 + i * 20
        p.append(f'<rect x="{lx}" y="{yy-11}" width="13" height="13" fill="{col}"/>')
        p.append(f'<text x="{lx+20}" y="{yy}" font-size="11" fill="#333">'
                 f'{name} ({counts.get(name,0)})</text>')
    p.append(f'<rect x="{lx}" y="{ly+92}" width="13" height="13" fill="none" '
             f'stroke="#111" stroke-width="1.6"/>')
    p.append(f'<text x="{lx+20}" y="{ly+103}" font-size="11" fill="#333">edge (separatrix)</text>')
    p.append('</svg>')
    return "\n".join(p)


def render_sweep_svg(sw: Sweep1D, width: int = 640, height: int = 300,
                     title: str = "") -> str:
    ml, mt, mr, mb = 56, 40, 20, 60
    pw, ph = width - ml - mr, height - mt - mb
    xs = sw.values
    scores = [r.score for r in sw.results]
    x0, x1 = xs[0], xs[-1]

    def px(v): return ml + pw * (v - x0) / (x1 - x0 if x1 != x0 else 1)
    def py(s): return mt + ph * (1 - (s + 1) / 2)   # score -1..1 -> bottom..top

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
         f'font-family="Arial, sans-serif">',
         f'<rect x="0" y="0" width="{width}" height="{height}" fill="#FFFFFF"/>']
    if title:
        p.append(f'<text x="{ml}" y="24" font-size="14" font-weight="bold" fill="#1F3864">{title}</text>')

    # classification band beneath the plot
    band_y = mt + ph + 10
    for i, r in enumerate(sw.results):
        sx = px(xs[i]) - (pw / (len(xs) - 1) / 2 if len(xs) > 1 else 5)
        w = pw / (len(xs) - 1) if len(xs) > 1 else 10
        p.append(f'<rect x="{sx:.1f}" y="{band_y}" width="{w:.1f}" height="12" '
                 f'fill="{BASIN_COLOUR.get(r.classification,"#999")}"/>')
    p.append(f'<text x="{ml}" y="{band_y+30}" font-size="11" fill="#333">'
             f'outcome basin along {sw.param}</text>')

    # zero line + axes
    p.append(f'<line x1="{ml}" y1="{py(0):.1f}" x2="{ml+pw}" y2="{py(0):.1f}" '
             f'stroke="#BBB" stroke-dasharray="4 4"/>')
    p.append(f'<line x1="{ml}" y1="{mt}" x2="{ml}" y2="{mt+ph}" stroke="#333"/>')
    p.append(f'<text x="{ml-8}" y="{py(1):.1f}" text-anchor="end" font-size="10" fill="#333">+1 sophro</text>')
    p.append(f'<text x="{ml-8}" y="{py(-1):.1f}" text-anchor="end" font-size="10" fill="#333">-1 psycho</text>')

    # the score curve
    pts = " ".join(f"{px(xs[i]):.1f},{py(scores[i]):.1f}" for i in range(len(xs)))
    p.append(f'<polyline points="{pts}" fill="none" stroke="#1F3864" stroke-width="2"/>')
    for i in range(len(xs)):
        p.append(f'<circle cx="{px(xs[i]):.1f}" cy="{py(scores[i]):.1f}" r="2.5" '
                 f'fill="{BASIN_COLOUR.get(sw.results[i].classification,"#999")}"/>')

    # transition markers
    for vb, va, cb, ca in sw.transitions:
        xm = px((vb + va) / 2)
        p.append(f'<line x1="{xm:.1f}" y1="{mt}" x2="{xm:.1f}" y2="{mt+ph}" '
                 f'stroke="#111" stroke-width="1" stroke-dasharray="2 3"/>')
        p.append(f'<text x="{xm:.1f}" y="{mt-4}" text-anchor="middle" font-size="9" '
                 f'fill="#111">{(vb+va)/2:.2f}</text>')

    p.append(f'<text x="{ml+pw/2}" y="{height-6}" text-anchor="middle" font-size="12" '
             f'fill="#333">{sw.param}  ({x0:.2f} \u2192 {x1:.2f})</text>')
    p.append('</svg>')
    return "\n".join(p)


def save_svg(svg: str, path: str) -> None:
    with open(path, "w") as f:
        f.write(svg)
