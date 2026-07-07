# sim_viz — the visualiser (core)

**The structure and the slot for the SIM graphics.** This implements Parts V
and VI of the graphics specification: the map data model, a compositor that
renders a town to SVG, the binding to `sim_world`, the code-rendered overlays,
and — the key piece — a **tileset slot** with a placeholder renderer now and a
drop-in for the AI-produced PNG tiles later.

This is a **core** layer: a general visualiser for any `sim_world` world.

## The idea

The map is **data**; the tiles are the **paint**; the picture is composed at run
time by **code**. Nothing is a hand-drawn scene, so the map is reconfigurable,
aligned to the model, and ready for real art without touching the pipeline.

## Three tilesets, one interface

The compositor takes any `Tileset`. There are now three, and swapping them is a
one-line change:

- **`PlaceholderTileset`** — bare coloured shapes, zero dependencies, so the
  pipeline runs and is testable before any art exists.
- **`ProceduralTileset`** — draws the tiles *in code* as vector SVG: shaded
  isometric buildings with pitched or flat roofs, windows, shopfronts and
  signage, roads with kerbs and markings, layered greenery, and movable agents,
  all under one locked palette and light direction, with seeded per-cell variety.
  Buildings are data-driven — a new type is one entry in `BUILDING`. Current
  coverage: terrain (grass, park, garden, pavement, plaza, dirt, sand, water),
  roads and footpaths, buildings (house, terrace, apartment, office, school,
  shop, grocery, cafe, pub, bar, sports centre, civic hall), props (tree, bush,
  hedge, flowerbed, fountain, playground, bench, streetlight, bin, bollard, bus
  stop, fence), and movable agents (adult, child, car, bus, bike). This is a
  whole town rendered by code — no art assets, perfect style consistency by
  construction, infinite variants for free, scaling to any resolution for print
  figures. It rasterises to PNG only when a raster is wanted.
- **`PngTileset`** — the raster slot: `<image>` references to PNG files named per
  the graphics specification. Drop tiles into a folder, point this at it, and the
  raster city renders with no other change.

## The raster slot (how PNG art drops in)

The compositor takes any `Tileset`. Today it uses `PlaceholderTileset` (simple
isometric shapes) so the whole pipeline runs and is testable before any art
exists. When the AI designer delivers tiles produced to the graphics
specification, switch to `PngTileset` — **no other code changes**:

```python
from sim_viz import PngTileset, default_manifest, save_svg
tileset = PngTileset("tiles/", default_manifest())   # a folder of spec-named PNGs
save_svg(city_map, "town.svg", tileset, overlays)
```

`default_manifest()` already names every tile per the specification
(`terrain_grass.png`, `building_school.png`, `road_cross.png`, `char_child_a.png`,
…) at the exact canvas sizes and to the geometry contract (ground fills the
256×128 diamond; buildings/props/actors anchored bottom-centre). A partial
tileset still renders what it has, so tiles can be dropped in as they are made.

## Binding to sim_world

```python
from sim_viz import Layout, build_map, add_people, overlays_from_state, save_svg

layout = Layout(place_cells={"home": (2, 3), "classroom": (9, 4), "office": (5, 10)},
                cols=15, rows=14)
city = build_map(world, layout)             # places -> buildings, connections -> roads
add_people(city, world, {"alex": alex})     # persons -> actors at their location
ov = overlays_from_state(world, {"alex": alex})  # dominant network + climate
save_svg(city, "town.svg", overlays=ov)
```

- **Buildings ← places** (home/school/workplace), footprints per the spec.
- **Roads ← the place-graph** connections (the pathways between places).
- **Actors ← people**, drawn at their current `sim_world` location.
- **State overlay** ← each person's current dominant behavioural network (one
  colour per network).
- **Climate overlay** ← each place's governing institution warmth (warm/harsh
  tint).

## Code vs art (per the spec)

| Code (here) | Art (AI designer, to the spec) |
|---|---|
| map model, compositor, iso geometry, z-order | the tileset PNGs (terrain, roads, buildings, props, characters) |
| binding to sim_world | (optional) district-panel backdrops |
| overlays: sim state, climate, highlights | — |

The full production brief — geometry contract, asset manifest, style bible and
per-asset prompts — is the standalone **SIM Graphics Specification** document.
It is the brief handed to whoever produces the tiles; this module is the working
slot they drop into.


## Spawning a settlement

`settlement.py` generates a whole town from a spec -- counts of homes, offices, schools, shops and a pub, plus cars -- laying a street grid, plots, buildings (commercial central, housing outward, civic buildings given room), greenery, a park and traffic into a `CityMap` the compositor renders. `spec_for_population(N)` sizes that spec from a target population via a `DemographyProfile` of ratios (household size, workers per office, homes per shop, cars per home -- placeholders to be pinned to a real ONS area). The population itself -- households, pupils, workers and the relational ties among them -- is bound in by `sim_world.populate`, turning the generated place into a society whose lives can be run. Rough and revisable; it spawns and renders a town today.

## Layout

```
sim_viz/
  iso.py          the isometric geometry contract (transform, diamonds, z-order)
  mapmodel.py     the CityMap schema + JSON load/save
  tileset.py      Tileset interface; PlaceholderTileset + PngTileset (raster slot)
  procedural.py   ProceduralTileset: draw the tiles in code as vector SVG
  compositor.py   render a map + tileset -> SVG, with code overlays
  binding.py      sim_world World -> CityMap; live state -> overlays
```

## Status

The structure and the slot are complete and tested. The placeholder renderer
proves the whole pipeline end to end; the real city appears the moment the AI
tiles (named per the spec) are dropped into a folder and `PngTileset` is used.
See `docs/ARCHITECTURE.md`.
