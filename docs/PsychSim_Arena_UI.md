# PsychSim — the Arena tab: a UI for the fine-detail testing instrument

**Design & implementation spec, with a hand-off note for the implementation session.**
Status: ready to build after design-session review. Scope: a deliberate promotion of the Arena UI
from the register's parking-lot to an active build (by explicit researcher decision — not drift).

---

## 0. What the Arena is, and why it's in the UI

The Arena is the **fine-detail lens** on the substrate. Where the Town spawns many agents into an open
world (coarse per-agent detail, slow), the Arena spawns **a few agents into a confined
micro-environment** (deep per-agent detail, fast). It is how a researcher runs a study at high
resolution: make a manipulation — a new neural pathway, a throttled circuit, a family composition — and
watch, in detail, how each subject develops and behaves under repeated close-range interaction. A
"study" is any manipulation-and-observation; the Arena is the place it happens at the finest grain.

The capability is **already built and tested** (`core/arena.py`, `tests/test_arena.py`). What is
missing is only the **server endpoint** and the **UI tab**. This spec wires those, reusing the Town
tab's live-view and inspector machinery. It is "a more specific spawn type," in its own tab.

---

## 1. The honesty constraint that shapes everything (read first)

The Arena already embodies the honesty wall in its structure, and the UI must **preserve, not bypass**
it. Two points are load-bearing:

- **A micro-environment is a defined set of present `Thing`s, each carrying a stimulus dict in the
  trigger vocabulary** (`{"reward_cue":0.7, ...}`) — never a valence, never a "stressful" tag.
  Confinement is *structural*: `escape = len(present)` — the count of non-social affordances to divert
  to — not a stress multiplier. So "one room" is aversive (if it is) because *few things are present*,
  and that scarcity is *perceived* by the agent's own circuits — it is never labelled aversive.
- **The roster agents ARE the social presence.** Relationships are not coded feelings; a relationship
  is a *history of encounters*, and what each agent feels about another **emerges** from living those
  encounters through its own substrate.

**The consequence for the UI — this is the critical design point:** the UI must NOT let a researcher
type a free-text environment ("classroom") or a coded relationship ("hostile colleagues") that has no
defined stimulus/matrix content behind it. **A hollow label is a lie** — it would present an
environment or relationship the substrate can't actually instantiate. So:

> **The Arena UI exposes the environments and relationship-configurations that are DEFINED in the
> matrices. Adding a new environment (classroom, office, 2-houses) or relationship type
> (colleagues, schoolmates) is grounded matrix work — defining the present `Thing`s and their
> stimulus dicts, or the matrix relationships — and only once defined does it appear in the UI.**

This is not a limitation to apologize for — it is the Arena's *purpose*. The researcher said the Arena
is the tool that helps *build the matrices*. So the loop is: define environment/relationship content
(grounded) → it appears in the Arena UI → spawn and test it → refine. The UI is the front end to
defined content, and the content set grows deliberately.

**Two different axes — do not conflate them:**
- **Roster SIZE is a fixed instrument bound: 2–5 agents** (S12.2; `run_arena` raises `ValueError`
  outside it). This is NOT an arbitrary limit — it is the Arena's *defining scale*: few subjects, high
  detail. 2 is the minimum for social interaction; 5 is the ceiling past which the per-agent detail
  that is the whole point is lost. A 50-agent "arena" would just be a small Town — that's the other
  instrument. **The UI enforces min 2 / max 5.** Lifting the core guard is out of scope (it would
  change `run_arena`, i.e. not wiring the existing).
- **Content — environments and relationship-configurations — has no arbitrary limit**: it grows as
  *defined* matrix content (§5, §6). The cap there is "is this content defined?", never a number.

So: roster size is bounded (instrument design); content variety is open-ended (grounded, growable).

---

## 2. What exists in core (build the UI on this — do not reinvent it)

`core/arena.py` provides the real interface. Use it directly.

- **`MicroEnv`** — a named environment: `present` (tuple of `Thing`s with stimulus dicts) + a
  documentary `note`. `escape` is `len(present)` (structural). **`MICRO_ENVS` currently defines FOUR:**
  `one_room` (screen, food — little present, no escape), `one_house` (food, screen, toys, music,
  fire_stove, height — an ordinary home), `house_garden` (adds pet_dog, greenspace, water_play — home
  plus garden), `office` (screen, music, electrical — an adult workspace). *(Note: office already
  exists — the UI exposes all four from day one.)*
- **`Slot`** — one roster agent, with a **source** (S12.2): `"newborn"` (fresh, with a `TraitSeed`
  temperament, defaults to intact), `"grown"` (developed `grow_years` before the Arena), or `"banked"`
  (restored from an `AgentBank`, never edited). Plus `age` (spawn age) and per-slot temperament seed.
- **`ArenaSpec`** — `micro_env` + `slots` (the roster) + `seed` (determinism) + `shared_hours`
  (co-located hours/day — the proximity dial).
- **`run_arena(spec, childhood_years=..., ...)`** — runs the closed-system development and returns an
  **`ArenaTrace`**: per-episode `records` (emergent `acts`, `max_act`, `drift` per agent; `strain`
  **per tie-pair** — strain is a property of a *relationship* between two agents, not of one agent, so
  the UI renders it on the pair, not the individual),
  plus `act_counts()`, a deterministic `signature()` (for regression diff), `peak_activation()` (the
  saturation signal), and `viable()` (no agent driven into persistent saturation).

So the UI's job: **compose an `ArenaSpec` from user choices, call `run_arena`, and render the
`ArenaTrace` live + inspectably.** The behaviour, the acts, the drift — all already computed and
emergent; the UI displays them.

---

## 3. Server changes

Add Arena endpoints (mirroring how Town spawn/state work). Minimum:

- **`GET /arena/environments`** — the defined `MICRO_ENVS` (id, note, the present `Thing` ids +
  `escape` count), so the UI lists real environments, not typed labels.
- **`GET /arena/sources`** — what a slot can be: `newborn` (+ available temperament seeds),
  `grown` (+ grow-years), `banked` (+ the available banked agent ids from the `AgentBank`).
- **`GET /arena/relationships`** — the defined relationship-configurations available (see §5). If the
  matrices currently define relationships only structurally (via encounter history), this returns the
  *composition presets* that are defined; it must not offer undefined ones.
- **`POST arena_run`** — accepts an `ArenaSpec` (micro_env, slots with sources/ages/temperaments,
  seed, shared_hours, childhood_years), calls `run_arena`, and streams/returns the `ArenaTrace`.
- **Live streaming:** the Arena runs episodes to `childhood_years`; the researcher wants to watch it
  evolve. Either stream trace records as episodes complete (preferred — the "watch live" requirement),
  or run and return the full trace with a scrubber. Live streaming is the better fit for "see the
  evolving behaviours all the way through."

Determinism is preserved (the `seed` field) — an Arena run reproduces exactly, which the regression
`signature()` depends on. Do not add an unseeded path.

## 4. The Arena tab — layout

A new tab **ARENA** in the tab bar, alongside TOWN. It reuses the Town's live-view + inspector
machinery, pointed at the small roster.

```
┌──────────────────────────────────────────────────────────────────────┐
│  telemetry strip (global)                                             │
├──────────────────────────────────────────────────────────────────────┤
│ TOWN │ ARENA │ DEVELOPMENT COHORT │ SOCIAL │ ENVIRONMENT │ GROUP │ …  │
├────────────┬─────────────────────────────────────────────────────────┤
│  ARENA     │                                                         │
│  SETUP     │              THE ARENA STAGE (live)                     │
│  (rail)    │        the confined space + the roster agents,          │
│            │        interacting live — same view primitives          │
│  environment│       as Town, at small scale + high detail            │
│  [one_house▾]│                                                         │
│            │        [click an agent → inspector overlay,             │
│  ROSTER    │         full mind/memory/standing, live]                │
│  ▸ slot 1  │                                                         │
│  ▸ slot 2  ├─────────────────────────────────────────────────────────┤
│  ▸ slot 3  │   INTERACTION TRACE (below or side)                     │
│  [+ add]   │   per-episode emergent acts, drift, strain — evolving   │
│            │   as it runs; scrub/replay; viable/saturation indicator │
│  shared hrs│                                                         │
│  [ 3.0 ]   │                                                         │
│  seed [ 0 ]│                                                         │
│  [ ▶ Run ] │                                                         │
└────────────┴─────────────────────────────────────────────────────────┘
```

### 4.1 The Arena setup rail
- **Environment** — a dropdown of the **defined** `MICRO_ENVS` (one_room / one_house / house_garden /
  office today; more as defined). Selecting one shows its present `Thing`s and `escape` count (so the
  researcher sees *what's in the space*, structurally).
- **Roster** — a list of **2–5 slots**, each configurable (§4.2). `+ add slot` (enabled up to 5);
  the roster must have at least 2. The 2–5 bound is the instrument's design scale (§1), UI-enforced —
  `run_arena` rejects rosters outside it.
- **shared_hours** — the co-located-hours/day dial (proximity).
- **seed** — determinism (default 0; a run reproduces exactly).
- **childhood_years** — how far to run the development (default 18).
- **▶ Run** — composes the `ArenaSpec`, calls `arena_run`, starts the live stream.

### 4.2 A roster slot (per agent — the composition)
Each slot configures one agent (2–5 slots total, per §1). The slot controls are exactly what `Slot`
supports today — **do not expose capabilities the wired instrument lacks:**
- **source:** newborn / grown / banked.
- **age:** spawn age.
- **temperament seed:** for newborn/grown (defaults to intact).
- **grow_years:** if grown.
- **bank id:** if banked (from the available banked agents).
- **sex + physical:** sampled per-agent from the v10 endowment — **displayed, not settable in this
  build** (`Slot` has no sex/physical field; they are sampled inside the agent). Per-slot *setting* of
  sex/physical is a real future extension (extend `Slot` + `_build_agent`), flagged in §7, not smuggled
  into this wiring build.
- **relationship:** **NOT a per-slot dropdown.** Relationships are not a slot property you set — they
  emerge from shared encounter history through the matrices (see §5). How agents relate is governed by
  `shared_hours` (proximity), seeded shared history, and the co-presence model; *named* relationship
  configurations are defined matrix content (§5), not a control on the slot.

### 4.3 The stage + inspector (reuse Town's machinery)
- The confined space rendered with the Town's view primitives, at small scale — the roster agents
  present and interacting.
- **Live:** as `run_arena` streams episodes, the stage updates — behaviours evolve visibly.
- **Inspect any subject, any time:** click an agent → the inspector overlay (the same one the Town
  uses) showing its mind, memories, standing — *live, all the way through the run*. This is the
  "see a lot of detail about each subject" requirement: the small space makes deep per-agent
  inspection tractable.

### 4.4 The interaction trace
- The `ArenaTrace` rendered as it accrues: per-episode emergent `acts` per agent, `drift`, `strain`,
  the running `act_counts`.
- **viable/saturation indicator** — surface `trace.viable()` and `peak_activation()`: if an agent is
  driven into persistent saturation, show it (this is the closed-loop failure signal, and it's exactly
  what a researcher testing a new pathway needs to see — "did my change blow something up?").
- **Scrub/replay** — step through episodes; the deterministic trace makes replay exact.

## 5. Relationships — the honest treatment (the open-ended part)

The researcher wants any relationship: family, friends, colleagues, schoolmates, any mix. The honest
implementation, per §1:

- A relationship in the Arena is instantiated through the **social/group matrices** and the **shared
  encounter history** — it is not a coded feeling. Two agents who are "family" differ from "strangers"
  by the *matrix relationship* and the *history* they're seeded with, and what they come to feel
  **emerges**.
- So the UI offers the relationship-configurations that are **defined** in the matrices. Where the
  matrices define a relationship type (kin, peer, co-worker, classmate), it appears. Where they don't,
  it is **defined first** (grounded matrix work — the relationship's initial matrix state) and *then*
  appears.
- **This is the matrix-building the Arena supports.** The build should expose whatever is defined now,
  and make *adding* a relationship configuration a clear, grounded step (define the matrix
  relationship → it becomes available in the Arena roster). Do not offer relationship labels with no
  matrix content behind them.

If the current matrices define relationships only via encounter history (no named presets), then Phase
1 exposes **co-presence + shared_hours + seeded shared history** as the relationship substrate, and
named configurations (family/colleagues/classmates) are added as defined matrix content. **Flag to the
design session** what relationship content currently exists vs. needs defining — this determines how
much of §5 is "wire the existing" vs. "define new."

## 6. Environments — expanding the set (grounded, not typed)

Beyond the four defined (`one_room`, `one_house`, `house_garden`, `office`), the researcher wants
outdoor space, 2-houses, classroom, and more. Each is a **defined `MicroEnv`**: a named set of present
`Thing`s with stimulus dicts + the structural `escape` count. Adding one is:
1. Define the present `Thing`s (each with its stimulus dict in the trigger vocabulary — grounded, the
   same way the existing four are).
2. Add the `MicroEnv` to `MICRO_ENVS`.
3. It appears in the Arena environment dropdown automatically (the UI lists `MICRO_ENVS`).

So the environment set grows by *defining content*, and the UI surfaces it. The build should make this
addition-path clean, and may define the researcher's requested set (outdoor space, 2-houses, classroom)
as grounded `MicroEnv`s as part of the work — but each is defined content, never a hollow label.
**Flag which new environments to define, and their present `Thing`s, to the design session** —
defining an environment is a substrate/matrix decision, reviewed like the others.

## 7. What this build is, and is not

**Is:** wire the existing `core/arena.py` to a server endpoint and an ARENA tab; reuse the Town's
live-view + inspector; expose the defined environments/sources/relationships; compose an `ArenaSpec`
from user choices; run it live; render the `ArenaTrace` with inspection all the way through; surface
the viability/saturation signal.

**Is not:** a free-text environment/relationship builder (hollow labels); a new development engine (it
reuses `run_arena`); a study module (it's general instrumentation — a study is any manipulation, run
here at high detail); an unseeded/non-deterministic path (determinism is preserved); an
unlimited-roster tool (2–5 is the instrument's design bound, §1).

**Flagged future extensions (deliberate, not this build):** per-slot *setting* of sex/physical (extend
`Slot` + `_build_agent` — useful for controlled studies, e.g. spawn a high-formidability male beside a
low-formidability female); named relationship configurations as defined matrix content (§5); new
environments as defined `MicroEnv`s (§6). Each is a grounded, reviewed addition, not part of the wiring
build.

## 8. Honesty checklist (definition of done)

- [ ] The environment dropdown lists only **defined** `MICRO_ENVS`; no free-text environment.
- [ ] The relationship options are only **defined** matrix configurations; no hollow relationship
      labels. What's defined vs. needs-defining is flagged to the design session.
- [ ] A micro-environment's aversiveness (if any) is **structural** (few present `Things`) and
      **perceived** by the agent's circuits — never a coded "stressful" tag anywhere in the UI or the
      new endpoints.
- [ ] Relationships instantiate through matrices + encounter history; no coded feeling. The behaviour
      and the bonds **emerge** and are displayed, never assigned.
- [ ] Banked agents in a slot are **restored, never edited** (the bank invariant).
- [ ] The run is **deterministic** (the `seed` field); no unseeded path; the regression `signature()`
      still reproduces.
- [ ] Roster is **2–5 agents, UI-enforced** (min 2 / max 5, matching `run_arena`'s guard — the
      instrument's design scale, not an arbitrary limit). Content variety (environments, relationships)
      is open-ended within *defined* content.
- [ ] The viability/saturation signal (`viable()`, `peak_activation()`) is surfaced — a researcher
      testing a pathway can see if it destabilized an agent.
- [ ] `tsc --noEmit` 0 · `vite build` 0 · Arena core tests still green · new endpoint tests.

## 9. Sequencing note

This is a **deliberate promotion** from the register's parking-lot (Arena/bank/scan UI), by explicit
researcher decision. It does **not** touch the frozen organism. The environment/relationship *content*
additions (§5, §6) are grounded matrix work and go through design-session review like any substrate
change — the UI wiring is bounded, the content growth is the ongoing matrix-building the Arena exists
to support. The CU surface (2.2) remains separate and still awaits the CU-spec §9 answers; the Arena is
general instrumentation, independent of it.

---

## 10. Hand-off note — for the implementation session

> **Task: the ARENA tab** — a UI for the fine-detail testing instrument. Spec:
> `docs/PsychSim_Arena_UI.md`. The Arena (`core/arena.py`) is **already built and tested** — this
> wires it to a server endpoint and a new ARENA tab, reusing the Town tab's live-view + inspector.
>
> **The Arena is the high-detail lens:** a few agents in a confined micro-environment (room / house /
> house+garden / office — all four already defined in `MICRO_ENVS`), developed and watched live with
> full per-agent inspection all the way through. It's "a more specific spawn type," in its own tab.
>
> **The one critical constraint — do not build a hollow-label builder.** The UI exposes the
> environments and relationship-configurations that are **DEFINED** (in `MICRO_ENVS` and the matrices).
> It must NOT offer a free-text "classroom" or a coded "hostile colleagues" with no stimulus/matrix
> content behind it — a hollow label is a lie about what the substrate can instantiate. A
> micro-environment is a defined set of present `Thing`s with stimulus dicts (aversiveness is
> *structural* — few things present — and *perceived*, never tagged). A relationship instantiates
> through the matrices + encounter history — the bonds **emerge**, never assigned. Expose what's
> defined; adding new environments/relationships is grounded content work (flag to the design session
> what exists vs. needs defining).
>
> **Build:** `GET /arena/environments|sources|relationships` (list the defined content),
> `POST arena_run` (compose an `ArenaSpec` — micro_env + roster slots with sources/ages/sex/physical/
> temperament/relationship + seed + shared_hours + childhood_years — call `run_arena`, stream the
> `ArenaTrace`). The ARENA tab: a setup rail (environment dropdown, **2–5-slot roster** — UI-enforced
> min 2 / max 5, the instrument's design bound, NOT unlimited; slot controls are source/age/temperament/
> bank-id, with sex/physical sampled-and-displayed not set, and NO per-slot relationship dropdown —
> relationships emerge from shared history per §5), shared_hours, seed, Run), the confined stage (Town's
> view primitives, small scale), the inspector
> overlay (live, any agent, any time), and the interaction trace (per-episode emergent acts/drift/
> strain, the `viable()`/`peak_activation()` saturation signal, scrub/replay). Determinism preserved
> (the `seed`); no unseeded path.
>
> **Reuse, don't reinvent:** `run_arena` computes the behaviour; the UI displays it. The Town's
> live-view and inspector are the machinery. This does not touch the frozen organism.
>
> Flag to the design session: (a) what relationship content is currently defined vs. needs defining;
> (b) which new environments to define and their present `Thing`s. Both are grounded content decisions,
> reviewed like substrate changes. Sync per phase; confirm on `origin/main`.
