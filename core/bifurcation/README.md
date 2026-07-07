# bifurcation — the edge explorer (core)

**Parameter sweeps, phase diagrams, separatrix extraction and a bisection
edge-finder.** Where the affect engine tells you what *one* configuration does,
this layer maps the *boundaries* between outcomes across a whole parameter
space — the developmental knife-edges where a small change in warmth or
structure flips a child from one adult outcome to another.

This is a **core** layer and presupposes no result: it finds the outcome
boundaries of *any* configuration or model, in binary or graded mode. The
sophropathy research uses it to locate the divergence conditions, but the
mechanism is general.

## What it provides

- **1-D sweeps (`sweep_1d`).** Vary one parameter and record the outcome along
  it — the simplest cut through the space.
- **2-D phase maps (`phase_map_2d`).** Vary two parameters on a grid and classify
  the outcome in each cell, giving the basins of attraction (sophropathic /
  intermediate / psychopathic) as regions.
- **Separatrix extraction (`boundary_cells`).** Pull out the cells that sit on a
  basin boundary — the developmental separatrix itself.
- **Bisection edge-finding (`bisect_edge`).** Home in on a boundary crossing to
  arbitrary precision along a line through the space.
- **Binary vs graded.** In binary mode the developmental rule uses hard 0.5
  cutoffs, which produce knife-edge artefacts exactly at 0.5; in graded mode the
  affordances are smooth (sigmoid), so the separatrix is a smooth surface. The
  key finding it makes legible: the psychopathic basin requires *both* low warmth
  *and* low structure — neither alone is sufficient.

## Use it

```python
from bifurcation import Config, phase_map_2d, boundary_cells

pm = phase_map_2d(Config(graded=True),
                  "warmth", 0.0, 1.0, "structure", 0.0, 1.0, nx=11, ny=11)
print(pm.region_counts())          # size of each outcome basin
print(len(boundary_cells(pm)), "separatrix cells")
```

## Honest scope

A boundary the explorer locates is a *prediction* about the model — a
hypothesis for the human studies to test — until the model is calibrated. It is
not evidence about people. The parameters are illustrative; the geometry it
reports is a property of the mechanism given those parameters.

## Layout

```
bifurcation/
  config.py     a run configuration + single-run driver
  sweep.py      1-D sweeps, 2-D phase maps, separatrix, bisection edge-finder
  explore.py    higher-level exploration helpers
  viz.py        text/plot rendering of sweeps and maps
```

Depends only on the core affect engine; nothing depends on it. See
`docs/ARCHITECTURE.md`.
