# PsychSim — Handover Document

**Single source of truth for the PsychSim codebase.** Written for the move to the
Claude Code extension in VS Code. Keep this file updated as the system changes.

*Last updated: this reflects the codebase in `PsychSim_Unified_Platform.zip` at handover.*

---

## 0. What PsychSim is, and why it exists

PsychSim is a **life-course and day-to-day social simulation platform**. It is the
**research instrument** for a PhD on the development of the functioning, non-offending
psychopath ("sophropath") and its childhood manifestation ("proto-psychopath"). The
PhD itself is a separate, later body of work; **PsychSim the software is the active
project.** This document is about the software.

The scientific stance is unusual and must be preserved (see §2): the simulation
contains **no hand-authored psychological effects**. Behaviour, feeling, attitudes and
personality are meant to *emerge* from an evolving neural substrate, not be scripted.

### The PhD it serves (context only — not a task in the codebase)
A four-part paper: (1) rewrite the PhD application; (2) a bias-aware review of the
literature (psychopathy, difficult children, ASPD, behavioural genetics), checking for
the field's tilt toward Hare's *criminal* construct rather than the functioning
psychopath and the childhood "proto-psychopath"; (3) research design; (4) the author's
own results. If the paper is ever worked on: **verified citations only** (never from
memory); the PCL-R is valid for its forensic branch (the critique is field-level
construct contamination, not instrument invalidation); the results are the author's
alone. None of this is code work.

---

## 1. Current state in one paragraph

The platform has: a neuroscience-grounded **emergent circuit substrate** (category-free,
~82 nucleus-level circuits — including PFC executive/regulatory circuits), **three
interface matrices** (relationships, environment, groups), a **memory-driven learning
route**, a **developmental life-stepper** (children grow up over years), a **town spawn
generator** (a tile
settlement), a **day-to-day town-life layer** (people walk between home/school/work/
leisure on role schedules, with A* pathfinding), a **plan-view ("glass-roof")
renderer**, and — newest — a **live step-loop engine + streaming server + a
Vite/React/TypeScript control panel** that runs the simulation continuously and
streams it to a browser: a fast grid view AND the designed plan-view floor plans with
live people overlaid, camera-follow, smooth motion, click-to-inspect, and
**save/load of a whole running world** (evolved minds and all). ~219 tests pass
(11 skipped are obsolete verdict-asserting tests, honestly marked). The **simulation
core is Python standard-library only** (no third-party deps). The **UI is now a proper
Vite + TypeScript project** under `ui/` (the old single-file CDN `psychsim_ui.html` is
kept as the retired proof-of-concept); building it needs Node, but the Python sim
itself still has zero third-party dependencies.

---

## 2. The governing discipline (do not violate)

1. **No encoded psychological effect.** Never hand-write directional rules like "a
   hostile setting raises threat" or "warmth builds self-control" at invented rates.
   Feeling and behaviour must emerge from the substrate. Scenario input describes what
   a situation/thing/activity *presents* (its neutral triggers), never what the person
   will feel.
2. **The substrate is a neutral stage.** Two different temperaments can respond
   oppositely to identical input, because their wiring differs.
3. **At this crude stage, chaos is correct.** The substrate is an early mock-up; it
   should NOT yet produce tidy, realistic social behaviour. Orderly outcomes that track
   the environment are a red flag that something was force-tuned — to be removed, not
   celebrated. Do not tune for realism.
4. **Crude scaffold, replaceable.** Every construct is a placeholder to be replaced,
   construct by construct, once the real neuroscience/psychology is researched.

---

## 3. System architecture

### 3.1 The internal model — the emergent substrate
`core/affective_engine/drives.py` is the heart.
- **7 primary systems** (`System`): SEEKING, CARE, PLAY, LUST (appetitive); FEAR, RAGE,
  PANIC (aversive). Each is the crude stand-in for a neural network.
- Each person's `Brain` holds a `Drive` per system with **reactivity** (temperament,
  inherited) and **strength** (grows with use, LTP-style).
- A stimulus (bundle of triggers) is presented; each system computes an activation to
  its own triggers; systems interact (thwarted SEEKING→RAGE; FEAR→SEEKING); the
  **dominant** system drives behaviour via a fixed `BEHAVIOUR` lookup.
- `imprint()` strengthens the system used, gated by `window_plasticity(age)` (a crude
  4-phase developmental curve — high early childhood, dip, adolescent resurgence, low
  adult). **Target for replacement: a proper 5–7 stage developmental model.**
- `read_mind()` gives a **descriptive** readout (dominant system + profile) — **no
  "psychopath/sophropath" label** (the old hand-coded classifier was deleted).

### 3.2 The executive layer (always-on, monitored)
`core/affective_engine/executive.py`.
- An `Executive` state (inhibitory capacity, deliberation, moral orientation, purpose),
  maturing toward a mid-20s ceiling; moral orientation is a **read-out** of the CARE
  system (Blair's affective conscience), not imposed.
- **Always-on**: attached to a `Brain`, consulted on *every* `respond`. It fires only on
  patterns it has **learned to monitor**, and when it fires it inhibits the prepotent
  drive (gated by maturation) — the override.
- **Memory installs what it monitors** (`install_monitors_from_memory`): reversal-
  learning — where a drive's remembered outcomes are net-costly, it installs an
  inhibitory monitor for that drive. Honest state: the current environment mostly
  rewards, so little is learned live; the mechanism is proven. Grounded in Diamond
  (executive function) and Blair (amygdala–vmPFC moral circuit).

### 3.3 The three interface matrices (all on the substrate)
- **Relationship matrix** (`core/sim_world/relations.py`): Park-style `Tie`/`Society`
  (standing, reciprocity, strain), driven by emergent behaviour.
- **Environment matrix** (`core/sim_world/environment_matrix.py`): `Thing`/`Bond` —
  emergent attractions/aversions to things, with inherited (epigenetic) leans that
  evolve. Inventory is evidence-based (traffic/water as real hazards, not folk
  predators; the inherited-fear-vs-modern-hazard mismatch).
- **Group matrix** (`core/sim_world/group_matrix.py`): `Group`/`Membership` — standing,
  belonging, contribution, conformity, and a **dominance-vs-prestige** status route that
  emerges from temperament (Henrich & Gil-White; social identity; need-to-belong;
  ostracism).

### 3.4 The human-interior diet
`core/affective_engine/activities.py`: significant life-activities as age-gated stimulus
bundles (play, learning, sport, friends, being driven to school, intimacy — strictly
age-gated 14+, plus adverse ones: failure, rejection, loss).

### 3.5 The developmental life-stepper (grow up over years)
`extensions/sophropathy/timeline_driver.py` (`make_life_stepper`): ages a population
through developmental episodes on the substrate + matrices, over the clock.

### 3.6 The town + day-to-day life (Park-modelled)
- **Town generator** (`core/sim_viz/` — `generate_settlement`, `spec_for_population`):
  a tile `CityMap` with homes, school, workplaces, shop, pub, roads, greenery. Each
  building has a `place` name and footprint.
- **Town-life layer** (`extensions/sophropathy/townlife.py`): a spatial address layer
  (walkable tiles, building entrances, rooms), **A\* pathfinding** (`astar`), **role
  daily schedules** (`scheduled_block` — child/adult, weekday/weekend), and a batch
  day-cycle stepper (`simulate_townlife`) + a plan-view animated HTML player
  (`render_townlife_html`).
- **Plan-view renderer** (`core/sim_viz/floorplan.py` — `render_settlement_plan`): the
  top-down "glass-roof" view (houses as floor plans, rooms, doorways, gardens,
  furniture). *This is the designed look — not the isometric one.*

### 3.7 The LIVE engine + server + React UI (newest, the current frontier)
- **`extensions/sophropathy/engine.py` — `SimEngine`**: refactors the batch stepper into
  a genuine continuous loop. `step()` advances one tick; `snapshot()` returns JSON live
  state (positions, drives, clock); `town()` returns geometry; `person_detail(cid)`
  returns full inspectable state; live controls: `set_tick_minutes`, `add_person`,
  `respawn`.
- **`engine.py` also has `plan()`** (the plan-view "glass-roof" SVG rendered
  server-side via `render_settlement_plan` — the picture IS the model — plus the
  grid→pixel mapping so a frontend overlays live people at `pad + x*cell + cell/2`) and
  **`save()`/`load()`/`list_saves()`/`delete_save()`** (pickle the whole engine — evolved
  minds, memories, positions, clock — to `sims/<slug>.psychsim` + a JSON metadata
  sidecar; reloads into a fresh runnable engine).
- **`psychsim_server.py`** (repo root): a **stdlib** HTTP server that runs the engine
  step loop on a background thread while "playing", with CORS. Endpoints: `GET /town`,
  `GET /plan[?cell=]`, `GET /state`, `GET /person?cid=`, `GET /saves`, `GET /health`,
  `POST /cmd` ({play|pause|speed|add_person|respawn|save|load|delete_save}). On `load` it
  swaps the running engine under the lock. If a built UI exists at `ui/dist` it also
  **serves that SPA** at `/` (with SPA fallback) — so one command serves both the app and
  the live sim. Verified in Claude Code: `play` advances the clock; `/plan` returns the
  SVG + mapping; save→list→load restores the exact clock/minds; `ui/dist` served with
  correct content-types.
- **`ui/` — the Vite + React + TypeScript control panel** (replaces the retired
  single-file `psychsim_ui.html`): typed components (`Stage` pan/zoom, `GridBackground`,
  `PlanBackground`, `PeopleLayer`, `Controls`, `Inspector`, `Legend`), a `useSim` polling
  hook, same-origin relative API (Vite proxies in dev; the Python server answers in prod).
  Feature parity with the old UI **plus**: a **grid ⇄ plan-view toggle** (plan draws the
  floor plans with people overlaid), **name/emoji labels**, **camera-follow**, **rAF-eased
  smooth motion**, and a **Save / Load** panel (name a run, reload it, delete it).
  `npm run smoke` renders every component headlessly (no browser) as a fast check. See
  `ui/README.md`.

### 3.8 The character library + controlled-experiment mode (newest)

Authoring people is done **with the discipline**, not by scripting personalities via
attributes. The only *given* attributes are the scenario setup — **temperament seed**
(inherited reactivity), rearing, role, position; the strength profile is **grown** on
the substrate. Two modes, one model:

- **Controlled-experiment mode (mode A)** — a fixed, evolved **background** population,
  identical across conditions, around which only the **study subjects** evolve live.
  This is the correct experimental control, and it is built.
- **Open-ended mode (mode B)** — every mind evolves live (the "watch-the-town" sim).

Built:
- **`core/affective_engine/drives.py` — `Brain.to_dict()/from_dict()`**: the substrate
  serialises to plain JSON `{system: [reactivity, strength]}` (exact round-trip).
- **`extensions/sophropathy/library.py`**: `grow_adult(temperament_seed, rearing)` grows
  ONE mind to adulthood on the substrate via the *same* developmental primitives the
  life-stepper composes per episode (activities → `live_stimulus`, world things →
  `encounter`, groups → `group_encounter`, executive monitored) — it mirrors
  `timeline_driver._episode`, decoupled so temperament and rearing can be set per adult.
  `CharacterLibrary` grows/caches/loads a set to JSON; `build_default_library()` grows
  3 temperaments × 3 rearings; a deterministic set ships in **`library/adults.json`**.
- **`SimEngine(experiment=True, study_subjects=None)`**: loads the library as a fixed
  background, **freezes** non-subject brains (gates use-dependent strengthening off in
  `step`'s group encounters), and evolves only the subjects (children by default; an
  explicit `study_subjects` list overrides). `snapshot()`/`person_detail()` expose a
  `subject` flag + `mind_state`; the server has `GET /library` and
  `respawn {experiment, study_subjects}`; the React UI has a **controlled-experiment
  toggle** on Spawn, a **faded/dashed** rendering for fixed background people, a
  subjects/background status line, and a **library browser** (name · temperament/rearing
  → dominant).
- **Authoring a study subject by temperament**: `SimEngine.add_person(role, temperament=)`
  builds a **fresh mind from the chosen temperament seed** (`brain_from_seed` — typical /
  fearless / fearless_calculating), NOT a clone of a grown resident; the mind's reactivities
  are seeded from the engine rng so authoring is **reproducible**; the authored person is
  always a **live subject**. The UI has a temperament picker on the +child/+adult buttons;
  the Inspector shows the given temperament. Disciplined authoring: only temperament is
  given; the personality grows.

Honest caveat (design doc §4): at this crude stage the substrate funnels most grown adults
to **SEEKING-dominant**, so the library is weakly differentiated — fine as background
scenery (inherited temperament still varies by seed) and it gets richer as the substrate
matures. Verified: background brains stay fixed across a live run while subjects evolve.

> **Timescale discipline (important):** PsychSim models **real human life spans** — it is a
> research instrument, not a game. Development belongs to the **life-stepper**
> (`timeline_driver.py`), which ages the population on the **real clock**. The live engine
> does **not** run any separate or compressed developmental clock. (An earlier attempt to
> compress developmental time so children were "watchable" as they grew up was a mistake —
> exactly the "make it look successful" corruption the discipline forbids — and was removed.)
> The library's `grow_adult` runs a *full* childhood offline to cache a grown adult; that is
> a batch life-grow (the sanctioned developmental resolution), not a real-time compression.

### 3.9 The plug-in module system + data-file config + reports (newest — platform Phase 1)

PsychSim is now a **neutral research platform**: a study is a **module** plugged into a
core that names no psychology. (Substrate *tuning* is a separate effort; here we refine
the platform.)

- **Modules** (`core/modular/registry.py`): a `Module` dataclass with optional hooks
  (`child_source`, `adult_source`, `world_content`, `categorise`, `report`, `default_params`).
  `discover_modules(extensions_dir)` **lazily** scans `extensions/*/` for a top-level
  `MODULE` symbol — a researcher adds a study by dropping a package with a `MODULE`; nothing
  in `project.py` is edited. The old hand-written `EXTENSION_REGISTRY` is gone.
- **Data-file-first config** (`core/config/`, `data/`): town/culture profiles unify the two
  previously-disconnected demography data points (`DemographyProfile` sized buildings;
  `HouseholdProfile` composed families but was never threaded into the spawn) into a
  `TownProfile`, shipped as editable JSON (`data/towntypes/*.json`) — a new country/culture
  is a JSON file, no code. Built-in profiles resolve to their Python constants (identity, so
  existing spawns are byte-identical); `spawn_universe` now threads `household_profile`
  through `populate` (family-size/tenure finally take effect). Per-module params live in
  `data/modules/*.json`.
- **`project.py`**: `spawn_universe` resolves modules + a `TownProfile`, layers params
  (module defaults ← `data/modules/*.json` ← `spec.module_params`, + a deprecated
  `spec.fearless_frac` alias), and collects each module's `world_content` onto
  `Universe.content`. `available_modules()`/`available_extensions()`/`available_profiles()`
  feed the UI. The live engine (`SimEngine`) and batch both spawn through the SAME
  `sophropathy.live_spec()` — no drift.
- **Reports** (`core/sim_experiment/readout.py` — neutral aggregation;
  `extensions/sophropathy/report.py` — `SubjectReport`/`CohortReport`): descriptive
  read-outs only (dominant = emergent Panksepp system, **never** a psychopath/sophropath
  verdict; chaotic crude-stage output expected). The live engine samples each subject's
  trajectory **on in-sim day rollover** (real time, never compressed). Server:
  `GET /modules`, `GET /report/cohort`, `GET /report/subject?cid=`; the UI has a read-only
  **Development** panel (cohort distribution + a subject's trajectory).
- **`sys.path` bootstrap**: `project.py` and `psychsim_server.py` put `core/` and
  `extensions/` on the path as roots, so any core package and any dropped-in module resolves
  without reinstalling — this is what makes the plug-in system work.

Verified: 242 tests (10 new) pass; the built-in town JSONs round-trip to the constants;
the deprecated `fearless_frac` alias selects the identical fearless children as
`module_params`; the new platform infra (`core/modular`, `core/config`) names no study.

### 3.10 The researcher's world + mind editors (data-driven, view/add/edit/delete)

Everything a study configures is now **data-file-first and editable**, so a researcher
curates their world without touching code. All served by `psychsim_server.py`; the React
UI panel has a collapsible editor for each.

- **Town types / culture** (`core/sim_viz/settlement.py`, `data/towntypes/*.json`):
  building types are a `BUILDING_TYPES` registry (added hospital / clinic / place-of-worship
  / market); a `TownProfile` unifies demography + household composition; ratios by culture
  spawn a convincing town (civic buildings only at real sizes). `GET /profiles`, UI town-type
  selector. An illustrative `traditional_town` ships (labelled illustrative — replace with
  real country data).
- **Roles** (`extensions/sophropathy/townlife.py`, `data/roles/*.json`): the schedule tables
  are a role library — built-in child/adult (byte-identical) + preschooler / teenager /
  retired / teacher; `role_block(role, hour, weekend)` is role-driven; the engine assigns
  varied roles deterministically. `GET /roles`, UI role picker; `add_person(role=)`.
- **Environment things** (`core/sim_world/environment_matrix.py`, `data/things/*.json`):
  `default_things()` is data-driven (14 evidence-based + ordinary additions = 19).
- **Matrix CRUD** (`core/config/matrixstore.py`, `data/{things,groups,social}/`): one generic
  view/add/edit/delete over the three matrices' DEFINITION items (Things, Groups, RolePairs);
  the emergent traces (Bonds/Memberships/Ties) are read-only. `GET /matrix`, `/matrix/items`,
  `POST /cmd {matrix_upsert|matrix_delete}`; UI MatrixEditor. Edits apply on next Spawn
  (social role-pairs on restart).
- **Neural pathway/network editor** (`core/neuraldesigner/store.py`, `data/neural/library.json`):
  on the existing `neuraldesigner` sandbox (JSON-serialisable, SVG wiring diagram, `validate`,
  loop-detection). Added `remove_*`/cascade. View/add/edit/delete circuits, pathways, and
  networks (aggregate pathways into a weighted network). `GET /neural`,
  `POST /cmd {neural_upsert|neural_delete}`; UI NeuralEditor (SVG + integrity). **Authoring
  sandbox only — NOT wired into the live substrate** (that is the separate substrate overhaul).
- **Executive-function editor** — *RETIRED (see `PsychSim_CORE_RECORD.md`, Reduction A).* The
  Panksepp learned-monitor Executive (`exec_store.py`, `data/executive/monitors.json`, the
  `/executive` endpoint + `executive_upsert|delete` commands, the ExecutiveEditor UI) was
  **deleted**; executive/regulatory function now lives in the substrate's PFC circuits.

All additive: existing spawns/behaviour are byte-identical (built-in defaults preserved,
civic ratios ~0 for small towns, empty executive registry). ~264 tests pass. `sys.path` is
bootstrapped so a new extension/data file is picked up without reinstalling.

**Roadmap (later):** wire authored neural networks into the live `drives.Brain` (with the
substrate overhaul); make teachers live residents so the teacher role auto-assigns; place
overlaid people in rooms; import real per-country demography; richer inline (non-JSON)
matrix editors; HTML reports.

---

## 4. Repository map

```
psychsim_x/
├── core/
│   ├── affective_engine/   drives.py (substrate), executive.py, activities.py,
│   │                       development.py, agent.py, memory.py, core.py
│   ├── sim_world/          relations.py, environment_matrix.py, group_matrix.py,
│   │                       world.py, population.py, timeline.py, daily.py,
│   │                       gamemaster.py, builder.py
│   ├── sim_viz/            floorplan.py (PLAN VIEW), procedural.py, compositor.py,
│   │                       binding.py, settlement.py (DemographyProfile), mapmodel.py
│   ├── modular/            registry.py — Module + discover_modules (PLUG-IN SYSTEM)
│   ├── config/             townprofile.py + loader.py (data-file config: TownProfile)
│   ├── bifurcation/  sim_experiment/ (+ readout.py)  speech/  neuraldesigner/
├── extensions/
│   ├── sophropathy/        module.py (MODULE + live_spec), report.py, engine.py (LIVE),
│   │                       library.py, timeline_driver.py, townlife.py, world.py, ...
│   └── justice/            (secondary study; also a MODULE)
├── data/                   EDITABLE config: towntypes/ modules/ roles/ things/ groups/
│                           social/ neural/ executive/ (the researcher's world + mind)
├── tests/                  ~27 test files
├── library/                adults.json — shipped grown-adult background (deterministic)
├── ui/                     Vite + React + TypeScript control panel (the live UI)
│   ├── src/                types.ts, api.ts, view.ts, hooks/, components/, App.tsx
│   ├── scripts/smoke.mjs   headless render check (no browser)
│   └── package.json        npm install && npm run build  ->  ui/dist (served by the server)
├── sims/                   saved simulations (<slug>.psychsim + <slug>.json); created on first save
├── psychsim_server.py      LIVE streaming server (run this; serves ui/dist if built)
├── psychsim_ui.html        RETIRED single-file CDN-React proof-of-concept (superseded by ui/)
├── run_pipeline.py         end-to-end batch demo
├── run_tests.py            whole test suite
├── run_townlife_demo.py    batch day-of-life -> town_life.html
├── project.py              spawn_universe / ProjectSpec (main API)
└── pyproject.toml          zero deps for the sim core, python >=3.9 (UI build needs Node)
```

---

## 5. How to run everything

Setup (WSL2/Ubuntu, VS Code — see the separate VSCode setup guide):
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e .          # zero third-party deps; this just puts core/ + extensions/ on the path
```

Run:
```bash
python run_tests.py                     # or: python -m pytest -q   (expect ~206 pass, 11 skip)
python run_pipeline.py                  # batch end-to-end demo

# STATIC day-of-life clip (pre-computed, plays in browser):
python run_townlife_demo.py             # -> town_life.html

# LIVE, continuously-running sim streamed to the React/TS UI (the frontier):
#   build the UI once (needs Node 18+):
cd ui && npm install && npm run build && cd ..
python psychsim_server.py               # serves the UI + live sim on :8765
#   -> open http://127.0.0.1:8765/ in a browser
#   press Start; toggle grid/plan view; click a person; turn on 'follow'; Spawn a town;
#   add a child/adult; name a run and Save it, then Load it back later.

# Developing the UI with hot reload (two processes):
python psychsim_server.py               # terminal 1: sim API on :8765
cd ui && npm run dev                     # terminal 2: Vite on :5173 (proxies the API)
#   -> open http://127.0.0.1:5173/       (edits reload instantly)
cd ui && npm run smoke                    # optional: headless render check of every component
```

> Note: this box has `python3`, not `python`. Activate the venv first
> (`source .venv/bin/activate`) so `python` resolves and the editable install is on
> the path; `.venv/bin/python psychsim_server.py` also works.

---

## 6. Development goals / roadmap

**Done:** substrate + 3 matrices + executive (with memory-learning) + developmental
life-stepper + town generator + day-to-day town-life + plan-view render + **live engine,
streaming server, and a working React UI**.

**Done since handover:** the UI is now a **proper Vite + TypeScript project** (`ui/`);
the **richer live view** landed (plan-view floor plans drawn live with a people overlay,
grid⇄plan toggle, name/emoji labels, camera-follow, rAF-eased motion); **save/load of a
whole running world** (pickle + JSON sidecar, from the UI); the **character library +
controlled-experiment mode** (§3.8); **authoring study subjects by temperament**
(reproducible fresh minds from a seed); and the **plug-in module system + data-file config
+ development reports** (§3.9 — the core is now a neutral platform; sophropathy is one
discoverable module; town/culture profiles are editable JSON; cohort/subject reports).

**Next (in rough priority):**
0. **Platform Phase 2+ (see §3.9 roadmap):** matrix CRUD editors; the neural pathway/network
   editor (on `core/neuraldesigner/`) and executive-function editor; promoting
   roles/things/groups to data-files; more country/culture town-types; HTML reports.
1. **Development over real life spans (needs discussion first).** Subjects must develop over
   a *real* human timescale, on the real clock — via the life-stepper, not any compressed
   live loop. How the live "watch-the-town" engine and the life-stepper relate (and whether/
   how a subject's rearing enters live development) is a **design decision for the author**,
   not to be made unilaterally. The substrate itself is due a major overhaul (neuroscience
   research, live-brain-scan-derived networks); expect highly chaotic social evolution
   meanwhile, and do **not** tune detail to make it look successful.
2. **Grow the library richer / from the UI**: a *grow-new-adults* button; assign specific
   library adults to specific homes (not just a deterministic cycle). Then **expand an
   existing town** (add streets/buildings) rather than only respawning.
3. **Deepen the live plan view**: place each overlaid person in the *room* they are
   actually using (the batch renderer already does this via `occupants`; the live engine
   currently only tracks a building tile), and expose per-person paths so walking is
   truly tile-by-tile rather than eased.
4. **Richer on-arrival interactions**: when people co-locate, run *situated* activities
   through the substrate (not just a generic group encounter), so days have texture.
5. **Deepen the substrate dynamics** so structure emerges from a rich diet (currently
   most people stay SEEKING — honest crude-stage behaviour). Part of the coming substrate
   overhaul (neuroscience / live brain scans).
6. **The 5–7 stage developmental model** to replace the crude 4-phase `window_plasticity`.
7. **An environment that also punishes** (retaliation/sanction) so the executive's
   memory-learning route actually learns inhibition live.
8. Tie activities/things/groups to specific places/homes/ages (not one shared diet).

---

## 7. The Park sim — reference and lessons (IMPORTANT)

**Source (fork used):** `https://github.com/ralphprice/generative_agents_sociopathy`
(fork of Park et al. 2023, "Generative Agents: Interactive Simulacra of Human
Behavior"; upstream: `https://github.com/joonspk-research/generative_agents`).

**Its architecture (what we learned from and modelled the live layer on):**
- A simple **step loop**: `curr_time += sec_per_step`; backend↔frontend handshake via
  JSON files (`environment/{step}.json` = where each agent *is*; `movement/{step}.json`
  = where each should move *next*). Our live engine/server is the modern analogue
  (WebSocket-less: stdlib HTTP + polling).
- A tiled **maze** with a *world→sector→arena→object* address hierarchy + **A\***
  pathfinding. We built a light version (`townlife.py`: entrances, rooms, `astar`).
- Agent **memory stream** (`associative_memory.py`), **scratch** (state + **daily
  schedule** `f_daily_schedule` — the thing that makes agents "exist" day-to-day),
  **spatial memory**; cognition = **perceive → retrieve → plan → reflect → execute**.
- A Phaser frontend that tweens sprites and ticks a clock.

**The crucial difference we keep:** Park's cognition (schedule, choices, dialogue, and
*effects of actions*) is **LLM-driven** — the exact hand-authored-effect pattern
PsychSim rejects. We take Park's **spatial/loop skeleton** and replace its **cognition
with our emergent substrate**: schedules from **role + age** (not GPT), interactions
when co-located run through our **matrices** (emergent), effects **emerge**. Park's
watchable town life, on PsychSim's emergent mind. (See `PsychSim_Park_Review.md` for the
full review.)

---

## 8. Honest limitations / known issues

- **The live UI now has the plan-view, the richer live view, and save/load**, but is
  still not the finished control panel: no add/edit-people-with-attributes and no
  expand-town yet (that is roadmap #1).
- In the live plan view, an overlaid person sits on their **building tile**, not yet in
  the specific **room** they are using (the batch renderer does place them in rooms).
- **Movement is eased** toward the polled position (smooth, but not true tile-by-tile
  walking — the engine would need to expose each person's path).
- **Saves are Python pickles** (complete and faithful, stdlib-only), so they are
  code-version-bound: a save may not reload after large refactors of the engine/mind
  classes. Fine for a local research tool; not a long-term archive format.
- **Colours barely change** in short runs: the crude substrate keeps most people in
  SEEKING. This is correct crude-stage behaviour, not a bug — do not tune it away.
- **On-arrival interactions are lightweight** (a generic group encounter + a memory).
- The developmental model is a **crude 4-phase** placeholder.
- **Verified in Claude Code**: the Python engine + every server endpoint (incl. `/plan`,
  `/saves`, save/load, and `ui/dist` static serving), the full test suite (~219 pass),
  the UI type-check + production build, a **headless render of every UI component**
  (`npm run smoke`), the dev proxy (Vite :5173 → server :8765), and an end-to-end
  save→load→delete cycle through the running server. **Not yet verified by human eyes**:
  the actual in-browser look/feel (plan-view overlay alignment, easing, camera-follow) —
  a browser is still needed for that final visual check.

---

## 9. A note on process (why this document exists)

This conversation suffered from repeated confusion — the assistant kept conflating the
PhD *paper* with the PsychSim *software*, and re-derived components instead of tracking
state. This handover is the remedy: **one source of truth** for what exists, how to run
it, and where it's going. In Claude Code / VS Code, work against this document and the
tests, update this file when the system changes, and keep the PhD paper and the software
strictly separate (the paper is not code work).

---

## 10. Key references (for grounding; cite properly if used in the paper)

- **Park et al. 2023**, Generative Agents (fork: github.com/ralphprice/generative_agents_sociopathy).
- **Panksepp** (1998), Affective Neuroscience; **Montag & Panksepp** — the 7 primary systems.
- **Knudsen 2004; Hensch** — critical/sensitive developmental periods.
- **Diamond 2013** — executive function (inhibitory control, working memory, flexibility).
- **Blair** — amygdala–vmPFC model of care-based morality; its dysfunction in psychopathy.
- **Tajfel & Turner 1979** (social identity); **Baumeister & Leary 1995** (need to
  belong); **Williams** (ostracism / need-threat); **Henrich & Gil-White 2001; Cheng,
  Tracy & Henrich 2013** (dominance-prestige status).
- Companion docs in this package: `PsychSim_Design_Document.md`, `PsychSim_Park_Review.md`,
  `PsychSim_ARCHITECTURE.md`, `PsychSim_VSCode_WSL2_Setup.md`.
