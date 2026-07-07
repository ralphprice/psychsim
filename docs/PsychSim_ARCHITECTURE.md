# psychsim — Architecture

**A universal life-course simulation platform, with research-specific extensions
bolted on.**

This document is the design. It states the one organising principle, describes
the core (universal) layers and the extension pattern, draws the dependency
boundary, and records what is done and what remains.

---

## 1. The organising principle

> **The core is a general platform on which many models can be tested. Anything
> specific to a particular piece of research is an extension bolted onto it.**

Two consequences, enforced throughout:

- **The core never depends on an extension.** Dependencies point *inward*: the
  core knows nothing about sophropathy; the sophropathy extension is built on the
  core. (Verified: the edge explorer was decoupled from the extension so the core
  imports only the core.)
- **Research choices live in extensions, or in swappable configuration** — the
  specific circuits, the classifier taxonomy, the family model, the staged
  design. The core supplies the *mechanisms*; an extension supplies the *content*.

```
        ┌──────────────────────── extensions/ ────────────────────────┐
        │   sophropathy: family/parent model + seven-stage programme   │
        └───────────────────────────────┬─────────────────────────────┘
                                         │ depends on
        ┌────────────────────────────────▼────────────────────────────┐
        │                           core/ (universal)                  │
        │  world · affect engine · neural designer · experiment ·      │
        │  visualiser · edge explorer                                  │
        └──────────────────────────────────────────────────────────────┘
```

---

## 2. The core (universal platform)

Six packages, each a mechanism that is independent of any particular study.

### `core/sim_world` — world & agents
Places (home, school, workplace, public), objects with affordances, institutions
with a climate and incentive regime, situated people, a two-rate clock, and the
Game-Master that turns behaviour into world change. Each `Person` *is* an
embodied affective agent: it owns an `AffectiveAgent` mind, ages on the clock,
perceives the local world as an appraisal, and — through the Game-Master's
`converse` — holds dialogic encounters with co-present others (see the language
layer below): it speaks the act its settled network makes, and answers the act
it hears. *Universal:* any social simulation of people moving between settings
and interacting through communication. A place now has an **interior** of areas, **affordance-objects** whose actions carry preconditions (a role present, being observed or unobserved, a door's lock state) and impose an appraisal on the actor, and a **rule-based day loop** (`daily.py`) that moves agents through waking, washing, eating, school, work and leisure. Areas connect through neutral access rules (open, role-restricted or closed -- respect for boundaries, not locks), and each place carries a norm profile so the same conduct is assessed by where it happens. This enriches the *world*, not the *mind*: no autonomous LLM planning is introduced. The core ships no venues, routines or behaviour categories: what a home or school is, and what conduct each place expects, are supplied by a study as an extension (the reference sophropathy world in extensions/sophropathy/world.py). This keeps the instrument neutral -- it presumes nothing about what any behaviour means. A society is also a web of standing relationships, and a working one *notices* when a tie is upheld or strained: `relations.py` gives the core the ordinary relationships any society has -- parent-child, teacher-pupil, boss-employee, colleagues, teammates, a community group -- each a directed tie with a power differential and a relational state that registers strain and repair, with reciprocity and restraint as the functioning default. This is normal social cohesion, so it is core; the disposition that strains the fabric, and its developmental meaning, is the study's extension.

The loop is closed: `extensions/sophropathy/lived.py` raises a child by LIVING a childhood in an actual home and school -- meeting the situations those places afford and the caregiving of the parent-child tie -- and feeds each lived situation to the SAME validated `develop_step` (extracted from `develop`), with the plasticity-gating environment derived from the home lived in. The classifier then reads the adult outcome. So a fearless child yields a sophropathic outcome in a warm-firm home and a psychopathic one in a harsh home, while a typical child resists psychopathy in the same harsh home (differential susceptibility). The outcome is PRODUCED by the life lived, not stipulated -- which makes this a test-bed: every later refinement to homes, schools, ties or norms is observable as a change in what comes out. No new developmental mechanism is introduced; the world supplies the experience and the existing rule consumes it.

### `core/affective_engine` — the affect mechanism
Neural-style circuits → behavioural networks → hysteretic arbitration →
development, plus episodic memory. *Universal mechanism.* It ships **configured**
with a default circuit/network/seed set (the set this research uses), which is
the one piece of research content still inside the core — swappable via the
neural designer (below). The development rule supports **graded (sigmoid)**
affordances as well as hard cutoffs (`develop(..., graded=True)`).

### `core/neuraldesigner` — data-driven affect authoring
Define circuits, input features, external triggers, internal **pathways**
(cascades and loops), and networks as *data*; store them as a JSON library;
run them; visualise them; export networks into the engine. *This is the seam*
that turns "the specific circuits" from hard-coded core into swappable content —
the route to running other affect models on the same platform.

### `core/sim_experiment` — experiment framework
Raise one agent through a staged life course; cross trait × environment factors;
replicate across seeds and aggregate. *Universal:* any trait × environment study.

### `core/sim_viz` — visualiser
The map data model, an isometric compositor, and a **tileset slot**
(`PlaceholderTileset` now, `PngTileset` for real art produced to the graphics
spec), bound to `sim_world`. *Universal:* renders any world.

Three tilesets share one interface: `PlaceholderTileset` (bare shapes), `ProceduralTileset` (the tiles drawn in code as vector SVG — a whole town with no art assets, style-consistent by construction), and `PngTileset` (the raster slot for produced art). Swapping them is a one-line change.

### `core/bifurcation` — edge explorer
Parameter sweeps, 2-D phase maps, separatrix extraction, and a bisection
edge-finder. *Universal:* find the outcome boundaries of any configuration or
model, in binary or graded mode. It presupposes no result.

### `core/speech` — the language layer (two channels)
The AI-as-voice architecture, kept strictly to one side of the engine.
- **`acts.py`** — the **causal** channel. Agents exchange typed, parameterised
  `SpeechAct`s (AFFILIATE, PROPOSE, THREATEN, DECEIVE, …), and each receiver
  appraises the *act*, never any wording of it, so everything causal stays
  inside the seeded engine. Deception is a property of the act (an `intent`
  hidden behind a `surface`); detection is a seeded roll against the receiver's
  vigilance, not a linguistic judgement. Articulacy is carried as a rendering
  knob, capability as an engine parameter — the two never mix.
- **`render.py`** — the **observer** channel. `TemplateRenderer` is to voice
  what `PlaceholderTileset` is to graphics: a deterministic, dependency-free
  stand-in that voices acts as dialogue for humans. `LLMRenderer` is the
  documented drop-in slot for a fine-tuned small model (LoRA-adapted,
  conditioned on act × register × articulacy). Swapping renderers changes
  nothing causal, because nothing reads rendered text back.
- **`faithfulness.py`** — the acceptance gate. From a rendered line alone, an
  independent probe must recover the act, register band, and articulacy band
  (targets: .90 / .80 / .80). This inverts Park et al. (2023): the model is the
  voice, never the cognition. *Universal:* any agent simulation that wants
  legible dialogue without letting an LLM's cultural priors leak into mechanism.

The layer is not a bolt-on: it is wired into `sim_world` through
`GameMaster.converse`, so agents in a running world actually talk. The speaker
emits the act its settled network makes (with register from its life-stage and a
rendering-only articulacy knob); the hearer's vigilance — grounded in its threat
gain and its trust in the speaker — sets the seeded detection probability; the
hearer then appraises the *perceived* act and settles its own reply. A believed
exploit is therefore remembered as warmth and a detected one as betrayal, with
the words never touching the causal path.

---

## 3. The extension pattern (research bolt-ins)

An extension lives under `extensions/<name>/`, imports the core, and adds the
content of one research programme. The reference extension:

### `extensions/sophropathy`
- **`society.py`** — the child dispositions the study contrasts (typical vs
  fearless / proto-psychopath–sophropathic), dispositional parents, and the
  **parent → caregiving-environment** mechanism (warmth from a parent's CARE,
  structure from their CONTROL).
- **`stages.py`** — the seven-stage programme (perfect condition → imbalance →
  control → manipulation → faithful modelling → parent effect → full interaction).

### `extensions/justice`
The criminogenic-justice module (optional; mechanism, not magnitude).
- **`system.py`** — labelling theory (Becker 1963; Lemert 1967) as a runnable,
  sweepable mechanism: detection of visible antisocial acts → a contact ladder
  (warned → charged → convicted) → a **labelled environment** in which the child
  grows (warmth, structure and recognition degraded by stigma and exclusion).
  Development runs in *segments* so a childhood can be re-based between segments
  without restarting at age zero; with `justice=None` the runner reduces exactly
  to plain segmented development, giving a clean ON/OFF comparison.
- **`experiment.py`** — grows the *same* cohort twice (identical trait seeds,
  situation streams and randomness), once OFF and once ON, so any shift in the
  outcome distribution is attributable to the labelling mechanism alone.

The result has genuine dynamic range and does not fabricate: near the outcome
separatrix, aggressive early labelling manufactures the psychopathic phenotype
in up to 100 % of children (dose-responsive in detection rate, label severity
and timing), while a child clear of the boundary is unmoved even under
aggressive labelling. Because contact accumulates only *after* a child offends,
the mechanism also predicts its own timing signature: criminogenic effects
should be strongest for *early* system contact. All of this is a hypothesis
about the mechanism — never evidence about people.

New research = a new extension (e.g. `extensions/<othermodel>`), reusing the core
unchanged.

---

## 4. The classifier

Psychopathy is scored by the **callous-unemotional core** — exploiting, or being
unmoved by, a *vulnerable other* — not by reactive aggression (conduct/
dysregulation) nor by pursuing a victimless reward. This definition is now
consistent across every layer (the fix was back-ported into the core engine), and
it is what makes the control condition meaningful: a normal, empathic child in a
harsh home reaches an *intermediate* outcome, while the fearless child reaches the
*psychopathic* one. Note this classifier taxonomy is itself research content; a
different study would supply its own.

---

## 5. Honest scope

- **Functional, not biophysical.** The engine is inspired by circuit-level
  affective neuroscience; it is not a simulation of neurons. Its warrant is
  behavioural.
- **Illustrative, not fitted.** All parameters are illustrative; every number the
  platform prints is computed by the mechanism from those parameters, not an
  empirical estimate and not invented. Calibration to the human studies (Study 2,
  Study 5) is a named, pending step; where those studies would set values, the
  code carries clearly-marked `PLACEHOLDER`s.
- **A simulation generates hypotheses; it is not evidence about people.** An edge
  the explorer locates is a prediction to be tested and a claim about the model
  until the model is calibrated.

---

## 6. Status and roadmap

**Done**
- All seven core layers built and tested; the sophropathy and justice extensions
  built and tested.
- **Language layer** (`core/speech`) built *and integrated into the world*:
  speech-acts drive appraisal, the template renderer passes the faithfulness gate
  (~.92 / .91 / .88), deception detection is seeded and vigilance-graded, the LLM
  renderer slot is stubbed, and `GameMaster.converse` makes agents in a running
  world actually talk (speaker emits its settled network's act; hearer appraises
  the perceived act and replies).
- **Criminogenic-justice extension** (`extensions/justice`) built: labelling as a
  sweepable mechanism with a clean ON/OFF comparison; demonstrated dynamic range
  (0 % → 100 % near the separatrix) without fabricating effects off it.
- **Architecture consolidated:** one bare-import convention across the whole tree
  (the new packages were brought into line), and the package manifest in
  `pyproject.toml` now installs every package including `speech` and `justice`, so
  `pip install -e .` yields the complete platform.
- One repository, no duplicated copies; **89 tests pass**; end-to-end pipeline runs.
- Classifier back-ported into the core so all layers agree.
- Graded (sigmoid) affordances added to the development rule and wired into the
  explorer, so bifurcation surfaces can be smooth rather than knife-edge at 0.5.

**Next (clearly scoped)**
- **Fully data-drive the core circuits** via the neural designer, so the default
  affect model becomes just one loadable library and the core carries no research
  content at all.
- **Animation exporter** in `sim_viz`: a frame sequence following a sim across a
  life course.
- **Wire the extension to the visualiser**: render a whole society (stages 1–2)
  as a city, tinted by family type.
- **Calibrate** the illustrative parameters to Study 2 / Study 5 (replaces the
  Stage 5 placeholders).
- **Graded-model edge study**: re-run the explorer in graded mode at fine
  resolution to map the smooth separatrix — the elaborate edge-condition search.
- **Fit the rendering model**: LoRA-adapt a small open-weights model into the
  `LLMRenderer` slot from synthetic paired data, and clear `faithfulness.evaluate`
  before it is trusted for observer transcripts.
- **Justice × disposition sweep**: run the ON/OFF comparison across the fearless
  vs typical dispositions and detection/severity/timing grids, to map where the
  mechanism bites — and test its early-contact timing signature.

---

## 7. Layout

```
psychsim/
  core/                         # universal platform (no research content, bar the default affect config)
    sim_world/        world & agents
    affective_engine/ the affect mechanism (+ graded development, back-ported classifier)
    neuraldesigner/   data-driven affect authoring (the swap seam)
    sim_experiment/   experiment framework
    sim_viz/          visualiser (+ tileset slot)
    bifurcation/      edge explorer (+ graded mode)
    speech/           language layer (acts + renderer + faithfulness gate)
  extensions/
    sophropathy/      the research bolt-in (society + seven stages)
    justice/          criminogenic labelling module (optional)
  tests/              89 tests across core + extensions
  docs/ARCHITECTURE.md
  run_tests.py        the whole suite
  run_pipeline.py     end-to-end demonstration
  pyproject.toml
```


## Spawning a populated settlement

The visualiser can generate a whole town from a spec (`sim_viz.generate_settlement`): a street grid, plots, buildings, greenery and traffic laid into a CityMap the compositor renders, sized from a target population via a demography profile of ratios (`spec_for_population`). `sim_world.populate` then binds a society into it -- households in the homes, pupils in the school, workers in the workplaces, and the standard relational ties among them -- so a generated place becomes a society whose lives can be run at community scale. Deliberately rough; a starting point to be revised.


## Project startup -- spawning a universe

`project.py` is the reset / start point for any new piece of research. A project is a name, a target community size, a demography profile, and a choice of extensions (a registry that acts as the dropdown). Spawning it sizes a settlement from REAL ratios -- household size 2.41, working-age 62.9%, ~1.2 cars per household, ~280-pupil primary schools (ONS Census 2021 and DfT National Travel Survey 2021, England) -- generates and renders it, populates it with a society, and applies whatever the selected extensions contribute (for sophropathy, seeding a minority of children with the fearless proto-psychopath disposition). The core spawns a balanced society working as it should; each extension declares in the registry how it perturbs that baseline, so a different study is a different selection and the core is untouched. Demography ratios are anchored to national figures now and can be pinned to a specific ONS area later. Deliberately rough; a runnable starting point.


## The top-down glass-roof view

`sim_viz/floorplan.py` renders the settlement from directly above with every building drawn as its floor plan -- as though single-storey under a glass roof -- so you look straight down into furnished rooms. Each building is drawn from the SAME `Venue`/`Area`/`AffordanceObject` data the simulation runs on: a home shows its kitchen, lounge, bathroom and bedrooms with a table, sofa, sink and beds, and sims are placed in the room they are using. The picture is the model, not a separate drawing. It is one view -- pure SVG with a viewBox, so panning and zooming for detail is trivial (an interactive wheel-zoom/drag-pan HTML viewer is generated alongside). This replaces the exterior isometric 'building block' render for looking at what a sim's day looks like inside, closing the gap between the interior model and the picture.


## Realistic households and floor plans

Household composition follows ONS 2021/2022 proportions (of families with dependent children: 1 child 44%, 2 children 41%, 3+ 15%; ~22% lone-parent; ~30% of homes have dependent children), so a spawned settlement has childless homes alongside one-, two-, three- and four-child families. Because larger families are far more likely to be overcrowded (ONS: 25.7% of 3+ child households vs 8.6%), siblings share bedrooms more often as the family grows, and each home is built with the matching number of child bedrooms. Floor plans are laid out realistically: rooms flank a central corridor and open onto it through doorways (gaps in the walls), with an entrance from outside and rooms sized by type -- not blocks pushed together.


## Socio-economics, comfort and home size

Room-sharing and home size are governed by socio-economic status, not family size alone, anchored to the English Housing Survey. Only ~3% of households are overcrowded and most children have their own room, but sharing is concentrated in lower-SES tenures (owner-occupier ~2-3% overcrowded vs social-rented ~22% with children), while wealthier homes are often UNDER-occupied (55% of owner-occupiers) and carry a spare room. Each household is given a tenure (England ~64% owner / 19% private rent / 16% social), from which its bedroom-sharing, spare rooms, and a `comfort` score (space per person) follow. The home is built to match -- shared bedrooms where poorer/larger, a study/box room where wealthier -- so comfort and ease of living, themselves developmental inputs, are visible in the floor plan and available to the study as a household attribute.


## Outdoor space: streets, gardens and settlement type

Homes connect to the outside: a front door onto the street and, where the household has one, a back door to a private GARDEN drawn as outdoor space behind the house. Garden access and size are governed by settlement type AND socio-economics, anchored to ONS: ~12% of GB households have no garden (21% in London, near-universal in rural areas), and owner-occupiers -- mostly houses -- are far more likely to have one than social renters, who more often live in flats. Three named settlement profiles set the area character: rural (near-universal, large gardens), suburban (the ~15%-no-garden baseline) and inner-city (garden-poor, compensated by more public parks). The garden affords outdoor play -- a developmental input like comfort -- and appears in the glass-roof view, so a leafy owner-occupier house with a study and a large garden and a shared-room social-rented flat with none sit side by side, as they do in a real settlement. This completes the environmental refinement for now.


## Controlling the passing of time

`sim_world/timeline.py` is one clock with many speeds. At the fine end it runs in real time -- you watch sim-people interact tick by tick; at the coarse end it fast-forwards, advancing by day, week, month or year and surfacing the events that happened over that span at that granularity (the same event stream shown at the chosen resolution -- individual interactions close up, rolled-up summaries when racing ahead). The `TimeController` drives a study-supplied `world_step(clock, minutes)` callback that advances the simulation and returns events; the core provides the clock, the scales (`TimeScale`), the bucketing into periods, and optional real-time pacing for a live view. The sophropathy driver (`make_stepper`) runs relational exchanges over a spawned universe and emits events on state transitions -- a tie strains, ruptures or repairs -- with a cohesion snapshot and a yearly milestone, so a run is legible whether watched in real time or fast-forwarded over years.


## The clock, the day loop and development, connected

`make_life_stepper` closes the loop between the three layers: advancing the clock ages the whole population through their lived days to classified outcomes. Each child carries a developmental state -- their mind, the plasticity-gating environment derived from their own home's parenting climate and the parent-child tie, and a situation pool drawn from their home and school. As simulated years pass, each child lives developmental episodes (fed to the validated `develop_step`), ages through the life stages, and at the end of childhood is classified. A child already part-grown at the start has lived those early years -- the missed episodes are run at initialisation -- so outcomes emerge across the timeline as children grow up, not all at once. The society's relational dynamics tick alongside. Because home climate varies across the population (warmth and structure drawn per household), the outcome tracks the child's home -- warmer homes yield more sophropathic outcomes -- which is the evidence the environment transmits correctly through development. The outcomes are produced by the mechanism as it runs: a test-bed for reasoning about the model, NOT evidence about people. Real findings come only from the study's data.


## The mundane is formative: ambient exposure

Development is driven by two forces, not one. The first is the rare, sharp EPISODE -- an opportunity, a provocation, a moment with a vulnerable other -- handled by `develop_step`. The second, added here, is continuous AMBIENT EXPOSURE (`expose`): the developmental effect of simply BEING in an environment for hours on end. Each environment now has an ambient character -- warmth, restoration (calm/greenery/safety) and threat (hostility/danger) -- and a child accumulates its pull in proportion to the time spent there. A warm, restorative setting gently builds conscience-control and lets threat-sensitivity settle; a hostile one erodes control and sensitises threat.

Crucially, the mundane hours are so many that their cumulative weight rivals or exceeds the rare episodes -- the principle of proportionality of exposure. The life of a child is modelled as a daily round across environments, each for its share of the waking day: the home (its parenting climate, warm or abusive), the JOURNEY TO SCHOOL (a delightful park route or a hostile neighbourhood, by settlement type), the school, and the neighbourhood. Because this repeats every day for years, the ordinary walk to school can be formative on its own: two otherwise-identical children in identical homes, differing only in whether their daily walk is through a park or a hostile street, diverge -- the hostile route leaving a markedly more threat-sensitised child. This corrects an earlier bias in which only dramatic moments shaped development; the long, mundane stretches that fill most of a life now carry the weight they should. The exposure rates are illustrative and a calibration target, like all the model's parameters.


## The environment matrix: a person's relationship with things

Parallel to the Park relationship matrix (a ledger of standing ties to people), each person carries an EnvironmentMatrix -- a ledger of Bonds to the inanimate and living things of their world: objects, pets, plants, places (a wood, a stream), and sensory things (music, food). A Thing PRESENTS a stimulus in the substrate's own trigger vocabulary; an `encounter` runs it through the person's brain, and whichever primary system dominates IS the felt sensation -- an appetitive response (SEEKING/CARE/PLAY/LUST) accrues ATTRACTION, an aversive one (FEAR/RAGE/PANIC) accrues AVERSION, scaled by how strongly the system fired. The encounter also imprints, so what a person keeps being drawn to strengthens the systems behind it. Reading attractions() and aversions() off the ledger gives the inventory of what a person seeks out and what repels them. Nothing about what a thing evokes is typed in: two temperaments build opposite inventories from identical things, because their wiring decides.

Some things carry a small INHERITED (epigenetic) lean at birth -- a prepared wariness of predators, a mild pull toward food -- grounded in prepared-learning findings. These are a REVISABLE head-start, not a fixed verdict: encounters run through the substrate and evolve them, so a bold child can lose an inherited wariness through exposure while a fearful one deepens it. The matrix is wired into the life-stepper: as a child lives, they meet the ordinary things of a small default world (pet, food, wood, stream, music, a predator), and their inventory builds and evolves across the childhood alongside their development. The default set is deliberately small but non-sterile; enriching it is part of the ongoing stimulus-vocabulary work.


## The environment inventory: real salience, not folk intuition

The things spawned in the world are chosen by EVIDENCE on what a child really encounters and what really harms them, weighted by salience = impact x frequency, each thing carrying a `frequency` so the living world presents it as often as it occurs.

Real hazards are mundane. Road traffic is the leading cause of child-injury death worldwide; drowning is the leading cause ages 1-4 and second ages 5-14; falls, burns and poisoning follow. Stranger-predators are statistically negligible (stranger-abduction-homicide odds ~1 in 750,000; most harm to children is by known people), so no wild predator or stranger is spawned -- the earlier 'predator' default was exactly the folk bias the research corrects.

The model encodes a grounded MISMATCH between inherited fear and modern hazard. Prepared-learning tunes inherited wariness to ANCESTRAL threats (heights, snakes, spiders); the high-impact MODERN hazards (cars, pools, medicines, electricity) are evolutionarily novel and carry NO inherited fear -- so modern hazards present a strong threat cue but inherited_aversion = 0, and a child develops wariness only if exposure fires their FEAR system, while ancestral hazards start wary from birth. In runs this reproduces the real danger: children come out innately wary of snakes (rare harm) and often UNWARY of, even drawn to, traffic (the leading killer). This is the environment matrix reading the world correctly -- inherited defaults evolving through exposure, on a substrate that decides the feeling, with nothing typed in.


## Stage 4: the human-interior diet (significant activities)

The developmental diet is no longer a thin cycle of bare situations. A life is made of ACTIVITIES -- play, a family meal, being driven to school, learning, sport, talking with friends, screen time, and, from adolescence, intimacy -- each a characteristic BUNDLE of triggers rather than a single one. `activities.py` supplies this vocabulary; each Activity DESCRIBES the stimulus it presents (in the substrate's own trigger vocabulary) and the developmental WINDOW it belongs to, never what it does to the person. A child lives a mostly-activity diet, age-gated so activities arise only when appropriate, run through `live_stimulus` on the substrate: the bundle fires the primary systems, the dominant one drives behaviour, and the systems used strengthen. Two children at the same match feel it differently because their wiring decides.

The set includes the ordinary HARD experiences of a real life too -- being told off, failing at a task, rejection, loss -- because a life contains them (realism), not to force any outcome. Sexual activity is represented only as an age-gated bundle of the LUST/affiliation triggers Panksepp's model already contains -- abstract, never content, and strictly gated away from children.

Honest state: the diet is now rich and age-graded, but at this crude stage the substrate still funnels most children to a SEEKING-dominated profile -- reward and novelty cues recur across activities, FEAR recruits SEEKING, and use-strengthening compounds the winner. That is the crude mock-up showing through, not a defect to be tuned away: the richer diet is in place for when the real neural triggers, loops and networks mature.
