# psychsim

**A universal life-course simulation platform, with research-specific extensions
bolted on.**

The core is a general platform for simulating how people develop as they move
through a world of homes, schools and workplaces — an affect mechanism, a world,
an experiment framework, a language layer, a visualiser, and an edge-condition
explorer. Anything
specific to a particular study is an **extension** built on top. The reference
extension is the **sophropathy** research: how a fearless ("proto-psychopath /
sophropathic") disposition develops toward an adaptive or antisocial outcome.

See **`docs/ARCHITECTURE.md`** for the full design, and each package's own
`README.md` for its detail.

## Run it

```bash
python run_pipeline.py     # exercise every core layer + the extension, end to end
python run_tests.py        # the whole suite (~218 tests, 11 skipped)
```

## The live control panel (React + TypeScript)

A continuously-running town streamed to a browser: press play and watch people
move on role schedules, click anyone to inspect their emergent mind, switch
between a fast **grid** view and the designed **plan-view** ("glass-roof") floor
plans, follow a person with the camera, **save / load a whole running world**
(evolved minds and all), and run a **controlled experiment** — a fixed, grown-adult
background (from the character library) around which only the study subjects evolve.

> This box has `python3`, not `python` — activate the venv first
> (`source .venv/bin/activate`) so `python` resolves and the editable install is on
> the path.

```bash
# 1. build the UI once (Node 18+; installs into ui/node_modules)
cd ui && npm install && npm run build && cd ..

# 2. run the server — it serves the built UI AND the live sim on one port
python psychsim_server.py            # -> open http://127.0.0.1:8765/
```

Developing the UI (hot reload) — run two processes:

```bash
python psychsim_server.py            # terminal 1: the sim API on :8765
cd ui && npm run dev                 # terminal 2: Vite on :5173 (proxies the API)
#   -> open http://127.0.0.1:5173/   (edits reload instantly)
```

`ui/` is a standard Vite project; `npm run smoke` renders every component
headlessly (no browser) as a fast sanity check. See `ui/README.md` for the layout.

## Character library & controlled experiments

Minds are never scripted by attributes — the only *given* inputs are a **temperament
seed** (inherited reactivity), rearing, role, and position; the strength profile is
**grown** on the substrate. `extensions/sophropathy/library.py` grows adults to
adulthood from temperament × rearing and caches them (`library/adults.json`). In
controlled-experiment mode the sim loads that library as a **fixed, evolved background**
and lets only the **study subjects** (children by default) evolve — an identical
background across conditions being the experimental control. Toggle it on the Spawn
control; background people render faded/dashed, subjects solid.

You can **author a study subject** (the add-resident row): a fresh mind is seeded and
evolves live around the fixed background. Its disposition is **measured, never selected** —
the personality grows. (The temperament-preset picker was removed, U1; authoring falls back
to standard roles.)

> **Timescale:** PsychSim models **real human life spans** — it is a research instrument,
> not a game. Development belongs to the life-stepper (`timeline_driver.py`), on the real
> clock; the live engine runs no separate/compressed developmental clock.

```bash
python -c "from sophropathy.library import build_default_library; build_default_library().save()"
```

## A research platform (plug-in modules + data-file config)

The core is **neutral** — it names no study. A research project is a **module** dropped
under `extensions/<name>/` exposing a `MODULE = Module(...)` (seeds, world content,
category reading, params, report). It's auto-discovered and selectable at spawn — nothing
in the core is edited to add a study. Town/culture composition is **data-first**: editable
JSON under `data/towntypes/` (a new country is a file, not code), unifying demography +
household composition. `GET /modules`, `GET /report/cohort`, `GET /report/subject?cid=`
expose the modules and honest, descriptive development reports (emergent system read-outs
only — never a verdict). See handover §3.9.

## The core (universal)

| Package | Mechanism |
|---|---|
| `core/modular` | the plug-in module system — `Module` + `discover_modules` (studies plug in here) |
| `core/config` | data-file config: `TownProfile` (demography + household) loaded from `data/` |
| `core/sim_world` | places, objects, institutions, people, time, Game-Master, dialogic interaction |
| `core/affective_engine` | wraps the circuit substrate: trait seeds → development → descriptive read-out |
| `core/neuraldesigner` | offline authoring sandbox — NOT wired into the live substrate (the seed is the single source of truth) |
| `core/sim_experiment` | life-course runner + trait × environment factorials + `readout` aggregation |
| `core/speech` | two-channel language layer: speech-acts (causal) + renderer (observer), wired into the world |
| `core/sim_viz` | isometric map + compositor + tileset slot for AI art |
| `core/bifurcation` | parameter sweeps, phase diagrams, separatrix finding (binary or graded) |

## The extensions (this research)

- `extensions/sophropathy` — the family/parent model, the parent → environment
  mechanism, and the seven-stage experimental programme.
- `extensions/justice` — the criminogenic-labelling mechanism (optional): a
  sweepable ON/OFF model of how justice-system contact degrades a child's
  developmental environment.

Each depends on the core; the core does not depend on it. New research = a new
extension, core unchanged.

## Principle

Dependencies point inward. The core supplies mechanisms; extensions supply
content. Everything is computed from illustrative parameters — nothing is fitted
or invented; calibration to the human studies is a named, pending step.

## Install (optional)

```bash
pip install -e .
```
