# PsychSim — UI redesign: ergonomic tab-based control console

**Design & implementation specification, with hand-off instructions.**
Status: ready to build. Scope: the deferred **UI-sync pass** (Part 6), plus the ergonomic restructure.
This document is the authority for the UI shell; it does **not** change the organism, the substrate,
or any honesty invariant.

---

## 0. The one-line brief

Turn a single squashed sidebar into a **lab-instrument console**: a quiet left rail carrying only the
controls that drive the simulation, and a top tab bar that opens one full screen per subsystem, each
using the same master–detail pattern (list on the left, full detail on the right).

The subject is a neural-substrate life-course simulator. The interface should read like an
**instrument**, not a SaaS dashboard: dense, precise, legible, no decoration that isn't information.

---

## 1. Honesty constraints (these bind the UI too)

The UI is a window onto the organism. It must not become a back door.

| # | Constraint | Why |
|---|---|---|
| U1 | **No outcome-named presets, anywhere.** No dropdown, preset, or button that *sets* an outcome category — the removed 8b.4 vocabulary (`strategic_prosociality`, `cool_instrumental_boldness`, `affiliative_warmth`, `reactive_aggression`, `fearful_withdrawal`) or a verdict word (`psychopath`, `callous`, `sophropath`). **A temperament seed is not an outcome.** `fearless` describes the *endowment you start with*, not what you become — a legitimate seed parameter (the temperament interface is nonetheless deprecated in favour of the throttle panel: a UI change, not an honesty one). | Outcome categories were removed as causal primitives (8b.4). A preset that *sets* an outcome re-seeds the answer. The UI exposes **circuits and parameters**; what a configuration produces is **measured**. Temperament describes initial conditions and stays settable. |
| U2 | **Neural Design is READ-ONLY, over the live v9 seed.** | The seed is the single source of truth, grounded and cited. A browser that can nudge a weight routes around the whole cited-and-reviewed discipline. Circuit changes go through a reviewed seed pass (as v9 did). |
| U3 | The current `/neural` editor edits `data/neural/library.json` — the **dead authoring sandbox**, not the live substrate. It must be repointed (read-only) or clearly relabelled. | Today a user editing "circuits" is silently editing a parallel copy that nothing runs on. Correctness-of-expectation. |
| U4 | **Report labels carry no removed outcome-category vocabulary.** | `/report/*` reads from the observer. Confirm displayed labels match current observer output. |
| U5 | **Polling must never develop an agent.** The `read_mind` round-robin cache is a staleness optimisation only. | The read-only wall (measurement never mutates). Already fixed — do not regress. |
| U6 | **The throttle panel is OUT OF SCOPE here.** It ships with the scan controller. | When it ships, it exposes **circuits** (0–100, intact = 100), never outcome-named presets. |

The existing **temperament dropdown** (`typical` / `fearless` / `fearless (calc.)`) and the
`respawn` command's `fearless_frac` are the **pre-redesign study interface**. Leave them functional
for now, but mark them `DEPRECATED — replaced by the throttle panel (scan controller)` in code, the
same way the Panksepp primitives were marked before their cut. Do not build their replacement here.

---

## 2. Current state (audited)

**Shell:** `ui/src/App.tsx` composes a pannable `Stage` (left) beside one `div.panel` (right) which
stacks *everything*: `Controls`, `Inspector`, `Development`, `MatrixEditor`, `NeuralEditor`. The panel
is resizable because "the work happens in the panel" — which is the symptom the redesign fixes.

**Components:** `Controls`, `Inspector`, `Development`, `MatrixEditor`, `NeuralEditor`, `Stage`,
`GridBackground`, `PlanBackground`, `PeopleLayer`, `Legend`. Hooks: `useSim`. Support: `api.ts`,
`types.ts`, `view.ts`, `theme.ts`, `styles.css`.

**Server surface (`psychsim_server.py`) — no new endpoints are needed except where noted.**

*GET:* `/town` · `/plan` · `/state` · `/person?cid=` · `/saves` · `/library` · `/modules` ·
`/profiles` · `/roles` · `/matrix` (kinds) · `/matrix/items?kind=` · `/neural` · `/report/cohort` ·
`/report/subject?cid=` · `/health`

*POST commands:* `play` · `pause` · `speed` · `add_person` · `respawn` · `save` · `load` ·
`delete_save` · `matrix_upsert` · `matrix_delete` · `neural_upsert` · `neural_delete`

Note `/matrix/items?kind=` already discriminates `group` / `environment` / `social` — so the three
matrix tabs need **no server change**. `MatrixEditor`'s internal `kind` selector simply becomes the
tab.

---

## 3. Design system

### 3.1 Direction

An instrument for reading a developing mind. The vernacular is the **activation trace**: graphite
chassis, hairline rules, monospace telemetry, and a single warm **phosphor** accent used only for
*live* state. Everything else is quiet. Spend the boldness in one place — the telemetry strip.

Explicitly avoided: cream/serif/terracotta, near-black-with-acid-green, and the broadsheet look.
These are defaults, not choices.

### 3.2 Tokens (add to `theme.ts`; expose as CSS custom properties in `styles.css`)

```
/* chassis */
--ink:      #0F1216   /* app ground */
--chassis:  #171B22   /* rail, tab bar */
--surface:  #1E232C   /* panels, cards */
--raised:   #262C37   /* hover, selected row */
--line:     #2E3642   /* hairlines, 1px */

/* text */
--text:     #E6E9EE   /* primary */
--muted:    #939DAD   /* secondary, labels */
--faint:    #626C7C   /* disabled, placeholders */

/* signal — used sparingly */
--phosphor: #E3A23C   /* LIVE / running / active tab underline */
--trace:    #5FD3C4   /* selection, focus ring */
--warn:     #D97C6A   /* destructive, non-viable */
```

Rules: `--phosphor` marks **running state only** (transport, live telemetry). `--trace` marks
**selection and focus only**. Never both on one element. No gradients. No shadows deeper than
`0 1px 0 var(--line)`. Radius `4px` on controls, `0` on rules and dividers.

### 3.3 Type

- **UI face:** IBM Plex Sans — an engineering family, not a default UI grotesque.
- **Data face:** IBM Plex Mono — every number, id, weight, tick, coordinate, and circuit id.
- **Tab labels / eyebrows:** IBM Plex Sans Condensed, `600`, uppercase, `letter-spacing: .08em`,
  `12px`.

Scale: `11 / 12 / 13 / 15 / 18 / 24`. Body 13. Dense tables 12/mono. Nothing above 24 —
this is an instrument; there is no hero.

### 3.4 Signature element — the telemetry strip

A full-width monospace readout pinned above the tab bar:

```
PSYCHSIM   ●LIVE   t 04:12:07   tick 15,204   pop 67   speed 1.00×   seed 4471   v9
```

`●LIVE` in `--phosphor` when running, `--faint` and `○IDLE` when paused. Everything else `--muted`
mono. This is the one memorable element and it is *true*: it tells you the sim's actual state at a
glance, which is exactly what a researcher watching a 60-year life-course needs.

---

## 4. Layout

### 4.1 Shell

```
┌──────────────────────────────────────────────────────────────────────┐
│  PSYCHSIM  ●LIVE  t 04:12:07  tick 15,204  pop 67  1.00×  seed 4471  │  telemetry strip (32px)
├──────────────────────────────────────────────────────────────────────┤
│ TOWN │ DEVELOPMENT COHORT │ SOCIAL │ ENVIRONMENT │ GROUP │ NEURAL    │  tab bar (40px)
├────────────┬─────────────────────────────────────────────────────────┤
│            │                                                         │
│  CONTROL   │                    TAB CONTENT                          │
│   RAIL     │                  (full width, own layout)               │
│  (280px)   │                                                         │
│            │                                                         │
└────────────┴─────────────────────────────────────────────────────────┘
```

- **Telemetry strip** and **tab bar** are global and always visible.
- **Control rail** is global, fixed `280px` (min 240, max 360, drag-resizable, persisted).
- **Tab content** owns the rest. Each tab defines its own internal layout.
- Active tab: `--text` label + a 2px `--phosphor` underline. Inactive: `--muted`, no underline.

### 4.2 Control rail — sections, stacked, one above the other

Only what *drives the simulation*. Each section is a labelled block separated by a hairline. No
horizontal squashing; every control gets its own line or a clean two-up row.

```
┌──────────────────────────┐
│ TRANSPORT                │
│  [ ▶ Start ]             │   ← primary, full width, --phosphor when running
│  [ « slower ][ faster » ]│
│  speed            1.00×  │   ← mono readout, right-aligned
├──────────────────────────┤
│ POPULATION               │
│  residents           67  │
│  profile   [ typical  ▾] │   ← DEPRECATED marker in code
│  role      [ adult    ▾] │
│  [ + Add person ]        │
├──────────────────────────┤
│ SPAWN                    │
│  town type [england_2021▾]│
│  population   [   200  ] │
│  ☐ controlled experiment │
│     (fixed background)   │
│  [ Spawn town ]          │
├──────────────────────────┤
│ LIBRARY                  │
│  9 grown adults          │
│  [ View library ]        │
├──────────────────────────┤
│ VIEW            (Town)   │   ← contextual: dimmed off the Town tab
│  [ grid ][ plan ]        │
│  ☑ labels   ☐ follow     │
├──────────────────────────┤
│ SESSION                  │
│  [ Save ]                │
│  no saved sims           │
│  [ Load ] [ 🗑 ]          │
└──────────────────────────┘
```

**Ergonomics:**
- The transport button is the only filled button in the rail. Everything else is outlined/ghost.
- `speed` is a mono readout, not a control — the `« »` buttons change it.
- **VIEW is contextual.** It only affects the Town stage; on other tabs render it dimmed with the
  eyebrow `VIEW (Town)` and `aria-disabled`. Do not hide it (layout stability > purity).
- Destructive actions (`🗑`) require a confirm; they use `--warn`, never as a default state.
- Empty states are directive, not apologetic: `no saved sims` → `No saved sims. Run a town, then Save.`

### 4.3 The master–detail pattern (used by every non-Town tab)

```
┌────────────────────┬────────────────────────────────────────────┐
│  LIST COLUMN       │  DETAIL PANEL                              │
│  (320px, scroll)   │  (fills, scroll)                           │
│                    │                                            │
│  [ filter…      ]  │   <selected item: full detail>             │
│  ─────────────     │                                            │
│  ▸ item            │   Nothing selected →                       │
│  ▸ item  ← selected│   "Select a <thing> to see its detail."    │
│  ▸ item            │                                            │
└────────────────────┴────────────────────────────────────────────┘
```

- Selected row: `--raised` background + 2px `--trace` left border.
- The list column has a filter box when >10 items.
- Selection persists per tab while the app is open (`useState` in the shell, keyed by tab).
- Keyboard: `↑`/`↓` moves selection, `Enter` focuses the detail panel, `/` focuses the filter.

---

## 5. Tab specifications

### 5.1 TOWN (default)

The current view, restored to full width. Stage (grid/plan background + `PeopleLayer` + `Legend`)
fills the content area; clicking a person opens the **Inspector** as a right-hand overlay panel
(`360px`, dismissible, not a modal) rather than a squashed sidebar section.

- Data: `/town`, `/plan`, `/state` (poll), `/person?cid=`.
- Empty state: `Click a person to inspect their mind, memories, role and standing.`
- The VIEW rail section is active only here.

### 5.2 DEVELOPMENT COHORT

*Assumption flagged: this tab is the cohort + per-subject developmental read-out. Confirm.*

Master–detail over the cohort.

- **List column:** every resident (cid, name, age, role). Filter by name/role. Sort by age.
- **Detail panel** for the selected subject, in three stacked cards:
  1. **Subject** — identity, age, role, standing. (`/person?cid=`)
  2. **Development** — the existing `Development` component: developmental timeline / trajectory for
     the selected cid.
  3. **Observer read-out** — `/report/subject?cid=`. Render whatever the observer returns, **labelled
     exactly as the observer names it** (constraint U4). Add a one-line footer:
     *"Measured over emergent behaviour. Never fed back."*
- **Above the list:** a cohort summary strip from `/report/cohort` — counts and distributions only.

Do **not** invent classification labels in the UI. Display what the observer emits.

### 5.3 SOCIAL MATRIX · 5.4 ENVIRONMENT MATRIX · 5.5 GROUP MATRIX

Three tabs, one component, parameterised by `kind` (`social` | `environment` | `group`). This
replaces `MatrixEditor`'s internal `kind` selector.

- **List column:** items from `/matrix/items?kind=<kind>`. Filter box. A `+ New` row at the bottom.
- **Detail panel:** the item's full definition — every field, one per line, labelled, mono values.
  Actions: `Save changes` (→ `matrix_upsert`), `Delete` (→ `matrix_delete`, confirm, `--warn`).
- **Header of the detail panel:** the kind's description from `/matrix` (kinds metadata), so a user
  reading the Social tab is told what a social role-pair *is*.
- Copy: these are **definition items** (the interface matrices' vocabulary), not runtime traces. Say
  so in a one-line eyebrow: `Definition items — the runtime traces live on each person.`

Per-kind list labels: Social → role-pair; Environment → thing; Group → group.

### 5.6 NEURAL DESIGN — read-only (constraints U2, U3)

**This tab changes behaviour, not just layout.** Today it edits the dead sandbox.

- **Repoint** `/neural` at the **live v9 seed** (`docs/neuralnetworks/psychsim_substrate_seed_v9.json`
  via the substrate loader — the same single source `core/substrate/model.py` reads). Serve it
  **read-only**.
- **Remove** the `neural_upsert` and `neural_delete` POST commands, and every write control in
  `NeuralEditor` (rename it `NeuralView`).
- **List column:** circuits, from the live seed. Filter by id/name. Group by `domain`
  (`defensive_threat`, `affiliation`, `interoception_autonomic`, `social_cognition`, executive…).
- **Detail panel** for a selected circuit:
  - identity: `id`, `name`, `domain`, `transmitters`
  - dynamics: `baseline_activation`, `activation_bounds`, `time_constant_tau_ms`,
    `homeostatic_setpoint`, `developmental_online_age`, `plasticity_coeff_schedule_ref`
  - **provenance:** `confidence`, `evidence_base`, `sources` — rendered prominently
  - **incoming / outgoing connections**, each with target, `default_weight`,
    `gating_neuromodulator`, `is_innate_reinforcer_link`; clicking one selects that circuit
- **Banner, always visible:**
  `Read-only. The seed is the single source of truth — grounded, cited, and versioned. Circuit changes go through a reviewed seed pass.`
- **Scaffold marking:** every number that is scaffold renders with a `SCAFFOLD` chip. Do not let a
  reader mistake a placeholder for a measured constant.

If `neuraldesigner`'s sandbox is still wanted for authoring, it becomes a *separate, clearly labelled*
route (`/sandbox`) — **not** this tab. Default: drop it from the UI.

---

## 6. File & component map

```
ui/src/
  App.tsx                     → shell only: telemetry + tabs + rail + <Outlet/>
  shell/
    TelemetryStrip.tsx        NEW  (live/idle, clock, tick, pop, speed, seed, seed-version)
    TabBar.tsx                NEW
    ControlRail.tsx           NEW  (composes the rail sections below)
    rail/
      TransportSection.tsx    NEW  ← from Controls.tsx
      PopulationSection.tsx   NEW  ← from Controls.tsx (mark temperament DEPRECATED)
      SpawnSection.tsx        NEW  ← from Controls.tsx
      LibrarySection.tsx      NEW  ← from Controls.tsx
      ViewSection.tsx         NEW  ← from App.tsx (mode/labels/follow), contextual
      SessionSection.tsx      NEW  ← from Controls.tsx (save/load/delete)
  layout/
    MasterDetail.tsx          NEW  (list column + detail panel + filter + kbd nav)
  tabs/
    TownTab.tsx               NEW  (Stage + backgrounds + PeopleLayer + Legend + Inspector overlay)
    DevelopmentCohortTab.tsx  NEW  (cohort strip + subject master-detail + <Development/>)
    MatrixTab.tsx             NEW  (parameterised by kind; replaces MatrixEditor)
    NeuralTab.tsx             NEW  (read-only; replaces NeuralEditor)
  components/                 (unchanged, now consumed by tabs)
    Stage, GridBackground, PlanBackground, PeopleLayer, Legend, Inspector, Development
  components/Controls.tsx     DELETE once its sections are extracted
  components/MatrixEditor.tsx DELETE (superseded by MatrixTab)
  components/NeuralEditor.tsx DELETE (superseded by NeuralTab)
```

State: keep `useSim` as-is. Add a shell-level `activeTab` (persisted to `localStorage`, key
`psychsim.tab`) and a per-tab `selectedId` map. No router dependency — a discriminated union and a
switch is enough for six tabs.

---

## 7. Server changes (small, and only these)

1. **`/neural` → read-only view of the live v9 seed.** Read through the substrate loader so the UI and
   the engine cannot diverge. Return circuits + connections + meta (including `version`, so the
   telemetry strip can show `v9`).
2. **Remove `neural_upsert` and `neural_delete`.** Return `400 unknown command` if received.
3. **Optional (telemetry):** if `/state` doesn't already expose `tick`, `clock`, `speed`, `seed`, and
   the seed `version`, add them. One extra field each; no new endpoint.
4. Leave `/matrix`, `/matrix/items`, `/report/*` exactly as they are.

Nothing else. The redesign is a client-side restructure plus the honesty repoint.

---

## 8. Implementation phases (build in order; each lands green)

**Phase 0 — tokens & scaffold.** Add tokens to `theme.ts` / `styles.css`. Add `TelemetryStrip`,
`TabBar`, empty `ControlRail`. Render the existing panel inside the `TOWN` tab unchanged.
*Accept:* app builds (`tsc --noEmit`, `vite build`); nothing visually broken; tabs switch and persist.

**Phase 1 — control rail.** Extract the six rail sections from `Controls.tsx` / `App.tsx`. Delete
`Controls.tsx`. Mark the temperament dropdown `DEPRECATED — replaced by the throttle panel`.
*Accept:* every control still works (play/pause/speed/add/respawn/save/load/delete); VIEW dims off the
Town tab; rail width persists.

**Phase 2 — Town tab.** Stage full-width; Inspector becomes a dismissible right overlay.
*Accept:* pan/zoom, person pick, inspector open/close, follow mode all work; empty state copy present.

**Phase 3 — `MasterDetail`.** Build the shared layout primitive with filter + keyboard nav.
*Accept:* unit-tested selection, filtering, `↑/↓/Enter//` keys, empty state.

**Phase 4 — three matrix tabs.** `MatrixTab` parameterised by kind; delete `MatrixEditor`.
*Accept:* items list per kind; upsert/delete work; delete confirms; kind description shown.

**Phase 5 — Development Cohort tab.** Cohort strip + subject master-detail + `Development` + observer
read-out with the "measured, never fed back" footer.
*Accept:* selecting a resident populates all three cards; labels match observer output verbatim (U4).

**Phase 6 — Neural Design (read-only).** Server repoint + command removal + `NeuralTab`.
*Accept:* the tab renders the **live v9 seed** (circuit count matches `core/substrate/model.py`); no
write control exists; `neural_upsert`/`neural_delete` are gone; banner present; SCAFFOLD chips render;
a test asserts the UI has no neural write path.

**Phase 7 — polish.** Loading skeletons, error copy ("what happened, how to fix"), focus rings
(`--trace`), `prefers-reduced-motion`, responsive down to 1024px, `aria` roles on tabs
(`role="tablist"` / `tab` / `tabpanel`).
*Accept:* keyboard-only navigation of the whole console; visible focus; no motion when reduced.

---

## 9. Definition of done — honesty checklist

- [ ] No outcome-named preset, dropdown, or button anywhere in `ui/src` — **zero hits outside
      comments** for the removed 8b.4 outcome vocabulary:
      `grep -riE "psychopath|callous|sophropath|strategic_prosociality|cool_instrumental_boldness|affiliative_warmth|reactive_aggression|fearful_withdrawal" ui/src`.
      (`fearless` is a *temperament seed*, not an outcome — excluded by ruling. `strategic`/`boldness`
      use their full category names so the pattern doesn't false-positive on ordinary English.
      Retirement/provenance comments that name a category to say it was *removed* are fine.)
- [ ] Temperament dropdown marked `DEPRECATED` in code, replacement deferred to the scan controller.
- [ ] `NeuralTab` is read-only over the **live v9 seed**; `neural_upsert` / `neural_delete` deleted;
      no write path exists (asserted by test).
- [ ] `/report/*` labels rendered verbatim from the observer; no removed category vocabulary.
- [ ] The `/state` poll still does not develop agents (read-only wall intact).
- [ ] SCAFFOLD values visibly marked in the Neural tab.
- [ ] Full suite green; `tsc --noEmit` and `vite build` exit 0.

## 10. Out of scope (deliberately)

- **The throttle panel** — ships with the scan controller; exposes circuits (0–100, intact = 100),
  never outcome-named presets.
- **Arena / bank / scan UI** — later, once those instruments are exercised from the CLI.
- ~~The stale Panksepp docstrings in `core/sim_world/group_matrix.py` and `core/sim_world/README.md`~~
  — **checked (2026-07 audit): neither file actually contains a Panksepp reference; nothing to fix here.**
- **Numeric age / distinct resident names in the cohort list.** The sim exposes neither (`name === cid`,
  and only a life-stage `role_name`, no `age_years`). The Development Cohort list therefore shows
  cid + life-stage + role and sorts by cid — it displays what exists rather than inventing an age
  from a life-stage bucket or synthesising names. A real age column/sort is a **server field**
  (`/person` or `/state` exposing `age_years`), authorised as its own small change if wanted. Ruled
  deferred (Phase 5) — not faked in the view.

---

## 11. Hand-off note — paste this to the Claude Code session

> **Task: the UI-sync pass + ergonomic tab redesign.** Spec: `docs/PsychSim_UI_Redesign.md`. Build it
> in the phases given (0→7), landing each green (`tsc --noEmit`, `vite build`, full suite).
>
> This is a **client-side restructure plus one honesty repoint**. It does not touch the organism, the
> substrate, the matrices' mechanics, or any invariant. Do not take on adjacent work.
>
> **The shape:** replace the single squashed sidebar with (a) a fixed left **control rail** carrying
> only the controls that drive the sim — transport, population, spawn, library, view, session —
> stacked one above the other in labelled sections; and (b) a **top tab bar**: `TOWN ·
> DEVELOPMENT COHORT · SOCIAL · ENVIRONMENT · GROUP · NEURAL`. Every non-Town tab uses one shared
> **master–detail** primitive: a filterable list column on the left, full detail on the right.
>
> **Three things are honesty-critical, not cosmetic:**
> 1. **Neural Design becomes READ-ONLY over the live v9 seed.** Today `/neural` reads
>    `data/neural/library.json` — the dead authoring sandbox nothing runs on. Repoint it through the
>    substrate loader (`core/substrate/model.py`'s single source), serve it read-only, **delete the
>    `neural_upsert` and `neural_delete` commands**, and remove every write control. Add a test
>    asserting the UI has no neural write path. The seed is the single source of truth — grounded,
>    cited, versioned — and circuit changes go through a reviewed seed pass, not a browser.
> 2. **No outcome-named presets, anywhere.** The UI exposes circuits and parameters; what a
>    configuration produces is measured, never named in advance. Mark the existing temperament
>    dropdown (`typical`/`fearless`/`fearless (calc.)`) and `respawn`'s `fearless_frac`
>    `DEPRECATED — replaced by the throttle panel (scan controller)`. **Do not build the throttle
>    panel here.**
> 3. **Render observer labels verbatim.** The Development Cohort tab shows `/report/subject` output as
>    the observer names it. Don't invent classification labels in the UI. Footer:
>    *"Measured over emergent behaviour. Never fed back."*
>
> **Server changes are only these:** repoint `/neural` (read-only, live seed, include `meta.version`);
> remove `neural_upsert`/`neural_delete`; optionally add `tick`/`clock`/`speed`/`seed`/`version` to
> `/state` for the telemetry strip. Leave `/matrix`, `/matrix/items`, `/report/*` untouched —
> `/matrix/items?kind=` already discriminates the three matrices, so the tab split needs no backend
> work.
>
> **Don't regress the read-only wall:** the `/state` poll's `read_mind` round-robin is a staleness
> cache; measuring must never develop an agent.
>
> Sync per phase. Flag anything that looks like it wants to reach past the UI into the organism.
