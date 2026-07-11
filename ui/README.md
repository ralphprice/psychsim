# PsychSim UI

The live control panel for PsychSim — a **Vite + React + TypeScript** front end
that talks to `psychsim_server.py`. This replaces the old single-file
`psychsim_ui.html` proof-of-concept with a real, typed, component-structured app.

## Commands

```bash
npm install        # once
npm run dev        # hot-reload dev server on :5173 (proxies the sim API to :8765)
npm run build      # type-check + bundle to dist/ (the Python server serves this)
npm run smoke      # headless render check — renders every component with mock data
npm run typecheck  # tsc --noEmit
```

There are **two ways to view it**:

- **Production**: `npm run build`, then `python psychsim_server.py` serves `dist/`
  and the live sim on the same port — open `http://127.0.0.1:8765/`.
- **Dev**: `npm run dev` on :5173 (Vite proxies `/town`, `/plan`, `/state`,
  `/person`, `/cmd`, `/health` to the Python server on :8765). Open :5173.

Because everything uses **same-origin relative URLs**, there is no hard-coded
server address and no CORS reliance in either mode.

## Layout

```
src/
  types.ts              typed mirrors of the server JSON (town/plan/state/person)
  api.ts                thin fetch wrappers over the HTTP API
  theme.ts              drive colours, terrain/building tints, cell size, role emoji
  view.ts               ViewModel: one tile->pixel mapping shared by both views
  hooks/useSim.ts       loads geometry once, polls live state, exposes commands
  components/
    Stage.tsx           pan/zoom viewport; imperative transform; centerOn() handle
    GridBackground.tsx  the fast top-down grid (terrain, buildings, props)
    PlanBackground.tsx  the designed plan-view SVG (rendered server-side, injected)
    PeopleLayer.tsx     live people overlay: rAF-eased motion, labels, camera-follow
    Controls.tsx        transport, population, view/labels/follow, save/load, experiment
    Inspector.tsx       click-to-inspect: 7 systems, groups, memories, mind-state
    Legend.tsx          drive colour key
  App.tsx               composes the above
```

## Controlled-experiment mode

The Spawn control has a **controlled experiment (fixed background)** checkbox. When set,
the server loads the grown-adult character library (`GET /library`) as a fixed background
and evolves only the study subjects (children by default). The overlay renders background
people **faded + dashed** and subjects **solid**; the Inspector shows each person's
mind-state ("study subject (live)" vs "background (fixed)"); a status line reports the
subject/background counts; and a **library browser** lists the grown adults.

**Authoring a subject**: the add-resident row seeds a fresh **standard** person (a role) that
evolves live — never a scripted personality; its disposition is **measured, never selected**
(the temperament-preset picker was removed, U1). The Inspector still shows a subject's *given*
temperament as a read-out. Development itself runs over **real life spans** via the life-stepper
(`timeline_driver.py`), not any compressed live clock.
See the handover doc §3.8.

## Save / load

The whole running world — town, every evolved mind, positions and clock — can be
saved and reloaded. The server pickles the engine to `sims/<slug>.psychsim` with a
JSON metadata sidecar; `GET /saves` lists them, and `POST /cmd {load, slug}` swaps
the running world. In the panel: name a run and **Save**, pick one to **Load**, or
**🗑** to delete. `useSim` refreshes the saves list and re-pulls town geometry after a
load (a load replaces the town, exactly like a respawn).

## How the two views stay aligned

The plan view's SVG is produced by `sim_viz.floorplan.render_settlement_plan`
**on the server** (the picture IS the model) and injected verbatim. The live
people ride on top in a separate overlay, positioned with the SAME `cell`/`pad`
mapping the server drew the plan with (exposed by `GET /plan`). The grid view
uses its own cell size. `view.ts` captures both mappings behind one `ViewModel`
interface, so `PeopleLayer` is view-agnostic.

Smooth walking: the server reports discrete tile positions ~5×/second and a
person can jump several tiles per tick, so each dot **eases** toward its target
pixel every animation frame (decoupled from the poll rate). While a person is
followed, that same loop recentres the camera on their eased position.
