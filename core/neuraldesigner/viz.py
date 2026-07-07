"""
viz.py -- draw a library as a wiring diagram (SVG).

Circuits are nodes, laid out on a circle and coloured by category; pathways are
directed edges, green for excitatory and red for inhibitory; a legend lists the
behavioural networks. This is the designer's view of the neural substrate -- a
picture of what has been wired together. It writes a standalone .svg file that
opens in any browser.
"""

from __future__ import annotations
import math
from typing import Dict

from .library import NeuralLibrary

CAT_COLOUR = {"affective": "#C0392B", "motivational": "#2E86C1",
              "regulatory": "#1E8449", "other": "#7D3C98"}


def to_svg(lib: NeuralLibrary, width: int = 760, height: int = 620) -> str:
    circuits = list(lib.circuits.values())
    n = max(1, len(circuits))
    cx, cy, r = width / 2, height / 2 - 20, min(width, height) * 0.34
    pos: Dict[str, tuple] = {}
    for i, c in enumerate(circuits):
        ang = -math.pi / 2 + 2 * math.pi * i / n
        pos[c.id] = (cx + r * math.cos(ang), cy + r * math.sin(ang))

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
             f'font-family="Arial, sans-serif">']
    parts.append('<defs>'
                 '<marker id="exc" markerWidth="9" markerHeight="9" refX="8" refY="3" '
                 'orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#1E8449"/></marker>'
                 '<marker id="inh" markerWidth="9" markerHeight="9" refX="8" refY="3" '
                 'orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#C0392B"/></marker>'
                 '</defs>')
    parts.append(f'<rect x="0" y="0" width="{width}" height="{height}" fill="#FFFFFF"/>')
    parts.append(f'<text x="{width/2}" y="30" text-anchor="middle" font-size="18" '
                 f'font-weight="bold" fill="#1F3864">{lib.name}</text>')

    # edges (pathways)
    for p in lib.pathways.values():
        if p.source not in pos or p.target not in pos:
            continue
        x1, y1 = pos[p.source]; x2, y2 = pos[p.target]
        dx, dy = x2 - x1, y2 - y1
        dist = math.hypot(dx, dy) or 1
        # trim to node radius so arrows land on the rim
        ux, uy = dx / dist, dy / dist
        x1t, y1t = x1 + ux * 26, y1 + uy * 26
        x2t, y2t = x2 - ux * 30, y2 - uy * 30
        # curve slightly so reciprocal edges (loops) don't overlap
        mx, my = (x1t + x2t) / 2 - uy * 22, (y1t + y2t) / 2 + ux * 22
        exc = p.weight >= 0
        colour = "#1E8449" if exc else "#C0392B"
        marker = "exc" if exc else "inh"
        parts.append(f'<path d="M{x1t:.1f},{y1t:.1f} Q{mx:.1f},{my:.1f} '
                     f'{x2t:.1f},{y2t:.1f}" fill="none" stroke="{colour}" '
                     f'stroke-width="{1 + 2.2 * abs(p.weight):.1f}" opacity="0.75" '
                     f'marker-end="url(#{marker})"/>')

    # nodes (circuits)
    for c in circuits:
        x, y = pos[c.id]
        col = CAT_COLOUR.get(c.category, CAT_COLOUR["other"])
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="24" fill="{col}" '
                     f'fill-opacity="0.16" stroke="{col}" stroke-width="2"/>')
        label = c.id if len(c.id) <= 9 else c.id[:8] + "\u2026"
        parts.append(f'<text x="{x:.1f}" y="{y+4:.1f}" text-anchor="middle" '
                     f'font-size="10" fill="#222">{label}</text>')

    # legend
    ly = height - 96
    parts.append(f'<text x="24" y="{ly}" font-size="12" font-weight="bold" '
                 f'fill="#333">networks ({len(lib.networks)}):</text>')
    for i, net in enumerate(lib.networks.values()):
        parts.append(f'<text x="24" y="{ly + 18 + i*15:.0f}" font-size="11" '
                     f'fill="#444">\u2022 {net.name or net.id} ({net.category})</text>')
    parts.append(f'<text x="{width-24}" y="{height-40}" text-anchor="end" '
                 f'font-size="10" fill="#1E8449">\u2192 excitatory</text>')
    parts.append(f'<text x="{width-24}" y="{height-24}" text-anchor="end" '
                 f'font-size="10" fill="#C0392B">\u2192 inhibitory</text>')
    parts.append('</svg>')
    return "\n".join(parts)


def save_svg(lib: NeuralLibrary, path: str) -> None:
    with open(path, "w") as f:
        f.write(to_svg(lib))
