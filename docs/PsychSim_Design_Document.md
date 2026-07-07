# PsychSim — Architecture and Design Document

*A simulation platform for modelling how a mind develops.*

*Updated to reflect the system as it stands. This document is the **design and
philosophy** reference. Two companions carry different loads and should be read
alongside it: `PsychSim_Handover.md` is the single source of truth for the
**codebase** (exact repository map, how to run it, live server and UI); `ARCHITECTURE.md`
states the **organising principle** and the core/extension boundary in brief.
`PsychSim_Park_Review.md` records the lineage of the day-to-day town layer. The
`docs/neuralnetworks/` material — a proposed category-free substrate overhaul — is
under active discussion and is **deliberately not folded into this document**; where
that work will land is noted, but its design is not adopted here.*

---

## 0. Status, purpose, and the governing discipline

PsychSim is a computational platform for studying how a human personality develops
over a life course — built as the simulation substrate for research into the
functioning, non-offending psychopath (the *sophropath*) and its early-childhood
manifestation (the *proto-psychopath*), though the platform itself is general. In the
thesis this is **Study 4**, the life-course society-model simulation; PsychSim is its
implementation.

**Everything in this document is a crude scaffold.** Not one construct here is a
claim about how minds actually work. Each is a deliberately simple placeholder, put in
place so that the *structure* of the simulation can be built and tested, and so that —
once the real neuroscience and psychology have been researched in depth — each
placeholder can be replaced, one at a time, by the observed and theorised models the
literature provides. The document is written to make that replaceability explicit:
every crude construct is named as such, and Section 11 is a consolidated catalogue of
exactly what must be replaced and with what kind of evidence.

Three principles govern the whole design, and they are non-negotiable:

1. **No encoded psychological effect.** The simulation must contain no hand-written
   rule of the form "a hostile setting raises threat," "warmth builds self-control," at
   invented rates. Feeling and behaviour must *emerge* from an evolving internal
   substrate — the wiring decides outcomes; the designer does not. Where the platform
   once contained such directional verdicts, they have been torn out (Section 11,
   history).

2. **The substrate is a neutral stage.** Scenario input describes what a situation, a
   person, a thing, or an activity *presents* — its triggers, in a neutral vocabulary —
   never what it does to the person. What it does emerges from the individual's wiring,
   so two individuals can respond oppositely to the identical input.

3. **At this crude stage the model should produce chaos, not order.** Because the
   substrate is an incomplete mock-up, running it should *not* yield tidy, realistic
   social behaviour. Orderly outcomes that neatly track the environment would be
   evidence that the model had been forced or hand-tuned, and would need to be removed.
   Undifferentiated or chaotic output at this stage is correct.

A fourth commitment, architectural rather than scientific, has become central since
this document was first written and is stated in full in Section 1: **the core is a
general platform; anything specific to a particular piece of research is an extension
bolted onto it.**

**A foundational correction, now adopted (read this first).** The original internal
model built the mind *out of* Panksepp's seven affective systems (§2.1). That has been
judged an error and is being retired. Panksepp's systems are *categorised descriptions
of observed neural activity* — labels for the end-result — not the generative primitives
a mind runs on. Building the substrate out of them models the wrong layer: it bakes the
output categories into the mechanism (the very thing Principle 1 forbids), and it limits
change to level-shifts on seven dials when the thing that actually changes across a life
is *which pathways fire, how often, in what combination, and the synaptic and structural
change that follows*. The successor is a **category-free neural substrate**: comprehensive
neural pathways, circuits, and networks, driven by sensory, proprioceptive and
interoceptive input, sculpted across development by use-dependent plasticity and
structural growth, from which emotion is an **emergent read-out** — never a cause fed back
in. Genetic and physical endowment (temperament, and physical traits such as
attractiveness, congenital health, and dexterity — the set is still being decided) enter
as the newborn's *initial conditions*, and a frontal executive layer (working memory and
inhibitory control) regulates the older systems. This direction is documented in the new
§§2.11–2.14, the resolution of the §2.10 inconsistency, and the `docs/neuralnetworks/`
design record, which this document now treats as the **adopted forward direction** rather
than a proposal under discussion. The honest scope of that ambition — what is achievable
and what is not — is stated in §2.14 and Section 14.

---

## 1. The shape of the whole system

PsychSim has grown from a mind-plus-matrices model into a layered **platform**. The
organising principle, enforced throughout the tree, is:

> **The core is a general life-course simulation platform on which many models can be
> tested. Anything specific to a particular piece of research is an extension bolted
> onto it, or lives in swappable data configuration.**

Two consequences follow, and both are enforced in the imports:

- **The core never depends on an extension.** Dependencies point *inward*: the core
  knows nothing about sophropathy; the sophropathy study is built on the core.
- **Research content lives in extensions or in editable data** — the specific circuits,
  the classifier taxonomy, the family model, the staged design, the town profile. The
  core supplies *mechanisms*; an extension or a data file supplies *content*.

At the centre of the core sits one **internal model** (a mind) that engages an external
**living world** through three **interface matrices**, is given a **voice** by a
language layer, is **rendered** by a visualiser, and is **experimented on** by analysis
harnesses. Research studies bolt on top:

```
   ┌──────────────────────────── extensions/ (research bolt-ins) ───────────────────────────┐
   │  sophropathy: family/parent model · seven-stage programme · life-stepper · town-life ·  │
   │               the LIVE engine   │   justice: criminogenic labelling (optional)          │
   └───────────────────────────────────────────┬─────────────────────────────────────────────┘
                                                │ depends on
   ┌────────────────────────────────────────────▼────────────────────────────────────────────┐
   │                                   core/  (universal platform)                             │
   │                                                                                           │
   │   ┌───────────────────────── THE INTERNAL MODEL (per person) ─────────────────────────┐   │
   │   │  primary neural systems ─► behaviour / personality  (strengthen with use,          │   │
   │   │  gated by developmental windows)   +  an always-on executive layer (co-active)      │   │
   │   └───────────────────────────────────────┬───────────────────────────────────────────┘   │
   │                                            │ acts through                                  │
   │        ┌───────────────────────┬───────────┴───────────┬───────────────────────┐           │
   │   RELATIONSHIP MATRIX      ENVIRONMENT MATRIX       GROUP MATRIX                            │
   │   (beings: standing ties)  (things: attraction /    (groups: standing & belonging)         │
   │                             aversion)                                                      │
   │                                            ▲ fed by                                        │
   │   ┌────────────────────────────────────────┴───────────────────────────────────────────┐  │
   │   │  THE LIVING WORLD — places & interiors, local norms, households (real demography),   │  │
   │   │  a multi-speed clock that ages the population, the day loop, ambient exposure, the   │  │
   │   │  activity diet, a spawned town + day-to-day town-life (A* pathfinding, role days)    │  │
   │   └─────────────────────────────────────────────────────────────────────────────────────┘  │
   │                                                                                           │
   │   speech (AI-as-voice)  ·  visualiser (plan-view & isometric)  ·  neural designer         │
   │   (the swap seam)  ·  bifurcation/edge explorer  ·  experiment framework                   │
   └───────────────────────────────────────────────────────────────────────────────────────────┘
        configured by  ▸  data/  (towns, roles, things, groups, social, neural, executive)
        driven live by  ▸  a step-loop engine + stdlib streaming server + a React control panel
```

**Code layout.** The platform is a reusable `core/` and research-specific `extensions/`,
with an editable `data/` configuration layer, a `ui/` control panel, and top-level
runners. (This map follows `PsychSim_Handover.md`, which is authoritative for the
codebase.)

```
psychsim/
  core/
    affective_engine/   drives.py (the substrate), executive.py, activities.py,
                        development.py, memory.py, agent.py, core.py, *_store.py
    sim_world/          relations.py, environment_matrix.py, group_matrix.py,
                        world.py, person.py, gamemaster.py, interior.py, norms.py,
                        daily.py, population.py, timeline.py, builder.py
    sim_viz/            floorplan.py (PLAN VIEW), compositor.py, mapmodel.py,
                        procedural.py, settlement.py (DemographyProfile), binding.py
    neuraldesigner/     data-driven circuit/pathway/network authoring (the swap seam)
    sim_experiment/     experiment framework (+ readout.py)
    bifurcation/        edge explorer (+ graded mode)
    speech/             the language layer (acts.py, render.py, faithfulness.py)
    modular/            registry.py — Module + discover_modules (the plug-in system)
    config/             townprofile.py, loader.py, matrixstore.py (data-file config)
  extensions/
    sophropathy/        module.py, society/world.py, stages.py, timeline_driver.py,
                        townlife.py, engine.py (the LIVE step-loop engine), report.py, library.py
    justice/            criminogenic labelling (system.py, experiment.py)
  data/                 EDITABLE config: towntypes/ modules/ roles/ things/ groups/
                        social/ neural/ executive/
  library/              adults.json — shipped grown-adult background (deterministic)
  ui/                   Vite + React + TypeScript control panel (built -> ui/dist)
  sims/                 saved simulations (<slug>.psychsim + <slug>.json)
  psychsim_server.py    the live streaming server (serves ui/dist if built)
  project.py            spawn_universe / ProjectSpec — the start point for a study
  run_pipeline.py  run_tests.py  run_townlife_demo.py  pyproject.toml
```

The simulation core is **Python standard library only** (no third-party dependencies);
only building the UI needs Node.

---

## 2. The internal model — how a personality is built

This is the heart of PsychSim and the part that matters most. It models a mind as an
evolving substrate that is shaped through use across the stages of development, and from
which behaviour, attitudes, and desires — the whole personality — emerge.

**Two models are described here.** §§2.1–2.10 describe the model **as currently
implemented in code** — a substrate built from Panksepp's seven primary systems, with an
always-on executive above it. That model is honest and runnable, and much of the platform
(development, the matrices, the read-out) runs on it today. But its foundation has been
judged an error (see Section 0), and §§2.11–2.14 describe the **adopted successor**: a
category-free neural substrate. Where the two conflict, the successor is the direction of
travel; the seven-system sections are retained because they document what the code does
now and what the migration starts from.

### 2.1 The substrate: primary neural systems as the "networks" *(current code; superseded)*

In the **current code**, the base of the mind is a set of **primary
emotional/motivational systems** — a stand-in for the neural networks a real brain runs
on, using the seven primary systems of Panksepp's affective neuroscience. They were
chosen because they are evidence-based, evolutionarily conserved, and mapped to
individual differences; the design has since concluded this was the *wrong layer to build
on* (Section 0), so what follows describes the implementation as it stands, with the
successor in §§2.11–2.14:

| System   | Class      | Fires to (its own triggers)   | Behaviour when dominant |
|----------|------------|-------------------------------|-------------------------|
| SEEKING  | appetitive | reward cue, novelty, comfort  | approach                |
| CARE     | appetitive | a vulnerable other, affiliation | nurture               |
| PLAY     | appetitive | a play signal, safety, affiliation | play               |
| LUST     | appetitive | a mate cue                    | court                   |
| FEAR     | aversive   | threat, pain, novelty         | avoid                   |
| RAGE     | aversive   | restraint, thwarting, pain    | aggress                 |
| PANIC    | aversive   | separation, loss              | seek comfort            |

*(Code: `core/affective_engine/drives.py` — `System`, `TRIGGER_AFFINITY`, `BEHAVIOUR`,
`Brain`, `Brain.respond`.)*

This seven-system set is a placeholder for the brain's real machinery, named as such in
Section 11 and now the explicit target of the substrate overhaul **that has been adopted**
(§§2.11–2.14). The reason it is being replaced rather than merely tuned is architectural:
the seven systems are the *output categories*, and building the mechanism out of them
smuggles the answer into the substrate, which Principle 1 forbids.

### 2.2 What a "situation" is, and how a system fires

A situation is presented to the substrate as a neutral **stimulus** — a bundle of
triggers, describing only what the situation *involves*, never what it should do to the
person. Each system's `TRIGGER_AFFINITY` decides how strongly it responds; the
system with the greatest activation is dominant, and its `BEHAVIOUR` is what the person
does. Two people with different wiring, given the identical stimulus, can act
oppositely — which is Principle 2 made mechanical. The bridge from the appraisal
vocabulary the world speaks to the substrate's stimulus form is `appraisal_to_stimulus`.

### 2.3 Reading the mind, without judging it

The substrate is read **descriptively only**. `read_mind` reports which primary system
dominates and the full profile of strengths (`dominant_profile`, `MindReadout`), and
attaches *no label*: it does not compute a "psychopathic" or "sophropathic" verdict.
For analysis a **neutral projection** of the profile onto a chosen contrast is available
(`profile_axis` — appetitive/affiliative strength minus aversive/defensive strength),
used to read the substrate as one continuous number for sweeps and edge-finding. It is a
measurement choice, not a claim about what the mind "is."

*(The platform once contained a hand-coded classifier that mapped internal quantities to
"psychopathic/sophropathic" labels; it has been removed, because it was exactly the
encoded verdict the discipline forbids. See Section 11, history.)*

### 2.4 Use-dependent strengthening (the crude LTP)

A system that keeps winning grows stronger and therefore wins more readily in future;
unused systems drift down gently. This is the crude stand-in for long-term potentiation
("cells that fire together wire together"): over a life it is what turns experience into
a stable personality — the profile of strengthened systems *is* the person's settled
dispositions. Crucially the rule is **general, not outcome-directed**: it says only "the
system used strengthens," never which system a given upbringing should strengthen — that
emerges from which systems a life's experiences happen to engage, given temperament and
timing.

*(Code: `drives.py` — `imprint(brain, response, age_years)`; rates `USE_LR`,
`DISUSE_DECAY`.)*

### 2.5 Inter-system dynamics

The systems interact, per the affective-neuroscience evidence. Two interactions are
currently modelled, both a crude first pass: **thwarted SEEKING feeds RAGE** (frustrated
pursuit turning to anger), and **FEAR recruits SEEKING somewhat** (the organism seeking
safety). This is a deliberately thin sketch of a very rich real phenomenon and is a
major target for redesign.

*(Code: `drives.py` — inter-system block in `Brain.respond`.)*

### 2.6 Developmental stages — when experience leaves its deepest marks

Experience does not leave equal marks at every age. Plasticity is high in early
childhood, dips in middle childhood, rises again in adolescence (late prefrontal
maturation), and is low in adulthood — grounded in the critical/sensitive-period
literature. A **developmental-window** function gates strengthening: the same experience
strengthens a system far more when the window is open than when it has closed.

| Phase             | Approx. age | Window (plasticity)  |
|-------------------|-------------|----------------------|
| Early childhood   | 0–5         | very open (~0.9→0.7) |
| Middle childhood  | 5–11        | narrowing (~0.6→0.4) |
| Adolescence       | 11–18       | resurgence (~0.55→0.4)|
| Adulthood         | 18+         | low, settling (~0.35→0.1)|

*(Code: `drives.py` — `window_plasticity(age_years)`.)*

This four-phase shape is **explicitly a placeholder** for the richer 5-to-7-stage
developmental model to be built, in which distinct systems have distinct sensitive
windows (attachment and fear-learning very early; social and self-regulatory systems
maturing later). It is a strong hypothesis of this research that the proto-psychopathic
trajectory is laid down most decisively during particular early windows — but the staged
model must be grounded in the developmental literature before any such claim is examined.

### 2.7 What emerges — the personality

Run this substrate across a life and a personality falls out of it: a settled profile of
which systems are strong and which are weak, which come to dominate in which kinds of
situation. That profile *is*, in the model's crude terms, the person's default
behaviours, attitudes, opinions, beliefs, and desires — the appetitive systems expressing
what draws a person and what they pursue, the aversive systems what they avoid and what
provokes them.

### 2.8 Carrying temperament in, reproducibly

A person's temperament can be **seeded**, so experiments are reproducible (the same seed
yields the same starting reactivities) while a population still varies individual to
individual. Disposition seeds — for example a "fearless" temperament — map onto the
systems' reactivities (a low-fear seed becomes low FEAR reactivity, and so on), carrying
*temperament only*, never an outcome.

*(Code: `drives.py` — `brain_from_seed`, `_SEED_TO_SYSTEM`; `agent.py` —
`AffectiveAgent.temperament_seed`.)*

### 2.9 The executive layer — an always-on co-active layer

Above the primary systems sits the **executive-function layer**: the frontal-cortex
system that, in a real brain, can override instinctive drives and is the seat of
inhibitory control, deliberation, conscience, and purpose. It is grounded in two bodies
of work: executive function (Diamond — inhibitory control, working memory, cognitive
flexibility; the prefrontal cortex inhibiting the limbic system; slow maturation peaking
in the mid-20s), and the affective conscience (Blair's amygdala–vmPFC model — a
care-based moral system, fed by the aversive distress of victims, dysfunctional in
psychopathy so that "intelligence becomes uncoupled from conscience").

**The executive pathways are always on.** Unlike a system called upon only when needed,
they run continuously and are **consulted on every brain event**. They do not *act* on
every event: they fire only on the specific patterns they have **learned to monitor**,
and when a monitored pattern matches they apply a **direct effect** — the clearest being
inhibition, damping a prepotent drive so a different system can take over (the override).
The magnitude of that effect is **gated by maturation**, so a child's immature executive
intervenes weakly and an adult's strongly — tying the override to the developmental
model (prefrontal maturity in the mid-20s, the reason adolescents are impulsive). The
effect is exercised *through* the substrate's own dynamics — it changes which system
wins; it is not a verdict bolted on top.

**What is built, and what is deferred.** The *mechanism* is built: the always-on
consultation, the learned-pattern registry, the direct inhibitory/amplifying effect, the
maturation gating, and the record of consultations and firings. What is **deliberately
deferred** is the *content* — exactly which patterns the executive learns to monitor and
how strongly each modulates. In a real brain these are learned from experience and are
precisely what the research must establish; they must not be hand-invented, any more than
the directional rules of the primary systems may be. So the registry is **empty by
default**: in a run, the executive is consulted on every event (thousands of
consultations across a childhood) but does not yet act, because nothing has been learned
to monitor.

**How memory installs what the executive monitors.** The first learning route is built.
The executive learns, *from episodic memory*, which prepotent drives to monitor. Every
social event records its outcome — the drive that was run and the emergent valence of
what followed (whether it bettered or worsened the person's social position, a signal,
not a per-drive rule). On *deliberative* steps an installer (`install_monitors_from_memory`)
reads that memory: where a drive's responses have, on balance, led to bad outcomes over
enough instances, it installs an inhibitory monitor for that drive. This is reversal /
reinforcement learning of response inhibition — the orbitofrontal/ventromedial function
whose *failure* characterises psychopathy. It hand-picks nothing: which drive is
regulated emerges from the person's own history. **Honest state:** in the current crude
world the social environment mostly *rewards* (even aggression is net-rewarded via
dominance-based status), so little is remembered as net-costly and the executive learns
to inhibit little live; the mechanism is proven, and what is actually learned awaits an
environment that also *punishes* (future work).

Alongside this, the layer carries four monitored read-outs that make it the model's
**self-awareness**: **inhibitory capacity** and **deliberation** (which mature toward the
mid-20s ceiling and gate the strength of any executive act), **moral orientation** (a
*read-out of the substrate's* care-based conscience — the CARE system's development,
pulled down by a strong RAGE disposition; a psychopathic-leaning wiring reads low,
exactly as the amygdala–vmPFC model expects, but nothing forces it), and **purpose**
(formed goals / philosophy, which accrue only through deliberative experience). This is
where the research question can be *watched without being decided*: strong deliberation
and formed purpose alongside a low affective moral orientation is the "conscience
uncoupled from deliberation" pattern — and is also, on the research hypothesis, the route
by which a person with a weak affective conscience might build a *cognitive* conscience
and purpose (the possible sophropathic path). The layer lets us observe whether that is
happening; it does not stipulate that it does.

*(Code: `core/affective_engine/executive.py` — `Executive` (`monitors`, `consult`,
`learn_to_monitor`), `MonitoredPattern`, `monitor_executive`, `maturation_ceiling`,
`moral_orientation_readout`; attached to the `Brain` and consulted inside `Brain.respond`
on every event. Declarative monitor specs can be authored via
`exec_store.py` / `data/executive/monitors.json`, but the registry ships empty by design.)*

### 2.10 A known architectural inconsistency: two affect pathways coexist

This is flagged plainly, in the spirit of the document's honesty. The *direction* is now
decided (Section 0): both implementations below are superseded by the category-free
substrate of §§2.11–2.14. What remains is the migration, and this section records the
starting state it migrates from.

The codebase currently carries **two** affect implementations:

- **The seven-system substrate (current default, above).** `drives.py`'s seven-system `Brain` with
  `imprint`, `window_plasticity`, and the executive. **Development, the three interface
  matrices, the activity diet, and the descriptive read-out all run on this** (via
  `development.py`'s `live_stimulus` / `live_moment`, which call `agent.brain.respond`,
  and `classify`, which calls `read_mind`). This is what Section 2 describes.

- **A legacy circuit-and-network engine.** `core.py` defines eight leaky-integrator
  circuits (THREAT, ANXIETY, SEEKING, FRUSTRATION, CARE, SOCIAL_LOSS, and two regulatory
  circuits CONTROL and INSTRUMENTAL_CONTROL), a catalogue of **named behavioural
  networks** (affiliative_warmth, strategic_prosociality, cool_instrumental_boldness,
  reactive_aggression, callous_exploitation, fearful_withdrawal), and trait seeds
  (`shared_root`, `shared_root_calculating`, `sophropathic`, `psychopathic`,
  `psychopathic_successful`); `agent.py`'s `AffectiveAgent.settle` runs the five-step
  appraise→activate→score→arbitrate cycle with **hysteretic arbitration** and returns a
  dominant *network*. This is the model the **thesis Study 4 (Part B)** and `ARCHITECTURE.md`
  describe as "the affect mechanism," and the one from which the (now-removed)
  callous-exploitation classifier was read.

Both are still present, and each `AffectiveAgent` builds *both* (its `__post_init__`
constructs the `drives.Brain` and the circuit/network machinery). The two are used by
different callers: the world/Game-Master behaviour path and the speech layer's
act-selection (`act_from_network`, Section 6) still key off the **named behavioural
network** an agent settles on, while development, classification, and the matrices run on
the **substrate**. Section 5 of the earlier draft asserted behaviour runs "on
`brain.respond`, not any legacy activation model," which is the *intended* end state but
is not yet true across the world and speech layers.

**Adopted resolution.** Neither of these becomes canonical. **Both are superseded by the
category-free neural substrate** (§§2.11–2.14). In the migrated architecture there is one
lineage: world behaviour and speech-acts are derived from the successor substrate's
**emergent read-out** (Panksepp-style categories among the things read *out*, never the
primitives the substrate is built *from*), and both `drives.py`'s seven-system `Brain` and
`core.py`/`agent.py`'s network arbitration are retired (or kept only as optional read-out
projections for comparison). Until the migration lands, the seven-system substrate remains
the default the rest of this document describes; the point of these subsections is to fix
where the code is going, so the two legacy lineages are not developed further in parallel.

---

### 2.11 The successor: a category-free neural substrate

The adopted internal model replaces the seven-system base with a **substrate of neural
pathways, circuits, and networks** catalogued at nucleus grain, in which **personality and
behaviour are not programmed but emerge** from neural activity that experience sculpts across
a life. The design premise, in one line:

> Comprehensive neural pathways fire in patterns and combinations; sensory, proprioceptive
> and interoceptive input drives that activity; use-dependent reinforcement and structural
> growth gradually sculpt unique connection strengths; the resulting activity *is* what we
> read out as emotion; and the whole is what we call the person.

Everything in the substrate serves that premise and one discipline, which is Principle 1 in
its sharpest form: **the mechanism must never contain the answer.** Concretely, this is
enforced by an **honesty wall** on the learning rules — a rule may update a connection using
only *local, activity-derived* quantities (pre- and post-synaptic activity, the current
weight, an activity-derived modulator, an age coefficient). "Co-active connections
strengthen" is allowed (mechanism); "threat strengthens avoidance" is forbidden (outcome).
No circuit knows it is "fear"; no state knows it is "threat."

**What is catalogued.** Each circuit carries its nuclei, transmitters, a baseline and
bounded activation, a developmental *online age* (the biological gate at which it comes
into play), and a plasticity schedule; each connection carries a source, a target, a
newborn default weight, a gating neuromodulator, and a plasticity schedule. Value enters
the newborn **only** through a small set of cited **primary-reinforcer** links (e.g.
nociception, looming, startle) — the single unavoidable seed of innate value — with every
other weight either hardwired-backbone anatomy or a near-zero associative site that
experience grows. Adult activity patterns (including anything Panksepp would name) are
**emergent validation targets, not inputs**. The seed data is being assembled system by
system; at the current version it spans the defensive-threat, reward-approach, sensory,
executive, affiliation/social, and interoception–autonomic systems.

**Provenance is coded, not assumed.** Every circuit and connection records a `confidence`
tier and an `evidence_base` (`human`, `human+animal`, or `animal_dominant`), and every
*invented* dynamic — time constants, eligibility/plasticity/homeostatic timescales,
structural-plasticity thresholds — is explicitly marked **SCAFFOLD**, to be replaced by
measured values. This is what keeps the catalogue honest about how much of it is
established fact versus placeholder (see §2.14 and the review that accompanies this
document).

*(Design record and data: `docs/neuralnetworks/PSYCHSIM_MASTER_DOCUMENT*.md` and
`docs/neuralnetworks/psychsim_substrate_seed_v*.json`; the swap seam that receives it is
the neural designer, Section 9.)*

### 2.12 Embodiment and endowment — sensory, proprioceptive, interoceptive input, and genetic/physical traits

The substrate does not float on abstract "situations"; its activity is **driven by the
body**. This is the deeper reason for the category-free design: emotion is taken to arise
from the interaction of **sensory**, **proprioceptive**, and **interoceptive** signals with
the neural circuitry that appraises them — feeling as an embodied, generated state rather
than a dial that is set. The sensory hierarchies are largely value-neutral relays (value
enters only at the cited primary-reinforcer links); the interoceptive–autonomic system
supplies the bodily signal that much of affect is built on. *(Note: the sensory system is
not merely planned — it is already substantially designed in the seed data; proprioception
and a fuller interoceptive loop are the near additions.)*

On top of the neural endowment sits a **genetic and physical endowment**: the newborn's
initial conditions. This includes temperament (carried as the reactivity of the primary
circuits, never as an outcome) and a set of **physical traits** — candidates named so far
are attractiveness, congenital health, and dexterity, with the full set still to be
decided. The discipline for these is exact and load-bearing: **a physical trait changes
what the world does to the agent, never what the agent is.** An attractive or physically
capable child elicits different responses from others and can attempt different things, and
*those experiences* drive the plasticity that shapes the person — the trait is an input to
the agent's history, not a lever on personality. Wiring "attractive → confident" directly
would be precisely the encoded outcome the honesty wall forbids.

### 2.13 The executive suite — regulation, memory, and inhibition as circuitry

The frontal executive is modelled as its own family of circuits (dorsolateral and
ventrolateral prefrontal cortex, dorsal anterior cingulate, frontopolar cortex,
pre-supplementary motor area, frontal eye fields, mediodorsal thalamus, and the
basal-ganglia stopping route, reusing the ventromedial/orbital frontal nodes). Its role is
**regulation**: working-memory maintenance (thalamo-cortical and fronto-parietal loops,
dopamine-gated input gating) and **inhibitory control** (the hyperdirect route braking
basal-ganglia output), exerted top-down over the older affective and sensory systems. Two
properties make it faithful and keep it honest. First, it is the **least innate,
latest-maturing** part of the model — it is seeded with *no* innate value at all, comes
online in stages through childhood, and matures into the mid-twenties (the reason
adolescents are impulsive); its regulatory strength is gated by that maturation, so a
child's executive intervenes weakly and an adult's strongly. Second, **what** it learns to
monitor and inhibit is not hand-written but **learned from experience** — the
orbitofrontal/ventromedial route by which a response that reliably leads to bad outcomes
comes to be suppressed (the reversal/reinforcement learning whose *failure* is a signature
of psychopathy). This preserves the current design's hard-won separation of *mechanism*
(built) from *content* (learned), carried across to the successor substrate. (In the
current code the executive is already present as an always-on monitored layer, §2.9; the
successor gives it an explicit circuit-level home and wires its effect through the substrate
where it really acts.)

### 2.14 Development, and the honest scope of the ambition

**Development is the point of the whole exercise.** The substrate's circuits come online on
biological schedules, their plasticity waxes and wanes with age, and the connection
strengths are sculpted by the particular life the agent leads. Personality, on this account,
is the *sediment of experience through maturing circuitry* — which is exactly what a
life-course study of divergent developmental outcomes needs its engine to capture, and
exactly what a seven-dial model could not.

**But the scope of the claim must be stated plainly, because it is the project's chief
risk.** No validated, runnable, whole-brain circuit model of the human brain exists — this
is one of the largest open problems in neuroscience, and it is not something a doctoral
project (or the field today) can deliver. What the substrate is, and should be described as,
is a **functional, illustrative, mechanistic model at nucleus grain**: most newborn weights
are qualitative assumptions (the literature reports *adult* patterns, not birth strengths);
most dynamics are scaffold placeholders awaiting measured values; much of the evidence is
animal work applied to a human model; and the confidence tiers say so. That honesty is not a
weakness to be hidden — it is the source of the model's credibility, and it is what
distinguishes this from a black box tuned to give the desired answer. The phrase "a working
model of the human brain that evolves exactly like a human" is an aspiration and a direction,
**not** a description of what the code is or will be within this programme; used literally in
the write-up it would be the single biggest threat to examinability. The governing test
remains **behavioural concordance** — does the substrate *behave* in a way concordant with
the constructs? — and complexity should be earned against that test, added system by system
only where it changes behaviour the validation gate can see and where its parameters can be
grounded or are honestly flagged. Breadth for its own sake adds audit burden (every added
knob is another place an outcome could hide) without adding evidential weight.

---

## 3. The interface with the world — the three matrices

The internal model does not float free; it engages a world through interface matrices.
Each matrix is a per-person ledger that accumulates a history and shapes future
engagement — and each runs on the *same* substrate, so the feelings recorded in a matrix
are the emergent output of the person's own systems, never typed in. All three are
**built**.

### 3.1 The relationship matrix (beings)

A person's relationships with other beings are held as a Park-style ledger of **standing
ties**. Each `Tie` carries three running quantities — **standing** (how warm/upheld the
relationship is), **reciprocity** (how balanced), and **strain** (current tension) — and
knows the **role** the pairing plays (parent–child, teacher–pupil, employer–employee,
colleagues, teammates, captain–player, community member), which sets the power
differential and what each party is expected to give.

An **interaction** runs both parties' responses through the substrate: the tie presents
each a stimulus coloured by its standing, strain, and power; each person's systems fire;
and the tie updates according to whether the emergent behaviour was *cohesive* (an
appetitive, affiliative engagement) or *aggressive* (RAGE). A cohesive society repairs
low strain over time; `Society.cohesion()` reads the share of ties upheld. The
book-keeping rates by which strain and standing move are crude ledger parameters (like
all the model's numbers, tunable), but *which* way a tie moves is driven by emergent
behaviour, not decreed. At this crude stage ties frequently run to rupture as strain
feeds back on itself — the expected chaos, not manufactured cohesion. The core registers
*that* a relationship worked or was strained and attaches no judgement of character;
*why* a tie strains, and what its strain-patterns mean developmentally, is the
perturbation a study introduces.

*(Code: `core/sim_world/relations.py` — `Tie`, `Society`, `Exchange`, `interact`,
`RolePair`, `STANDARD_TIES`; the emergent read on the substrate via
`drives.respond_to_appraisal`, `is_cohesive`, `is_aggressive`.)*

### 3.2 The environment matrix (things)

Exactly parallel to relationships with beings, a person accumulates relationships with
**things**: objects, pets, plants, places (a wood, a stream, a park), and sensory things
(music, food). Each `Thing` **presents a stimulus** (a busy road presents threat, a
stream gentle novelty); an **encounter** runs that stimulus through the substrate; and
the dominant system *is* the felt sensation — an appetitive response accrues
**attraction**, an aversive one **aversion**, scaled by how strongly the system fired.
Encounters also strengthen the system used, so what a person keeps being drawn to shapes
them. Reading the ledger gives the person's **inventory of attractions and aversions**.
Nothing about what a thing evokes is typed in: a fearful child and a bold child build
opposite inventories from identical things.

**Inherited defaults (epigenetic leans).** Some things carry a small inherited lean
present at birth — a prepared wariness of certain hazards — a *revisable head-start*, not
a fixed verdict: encounters run through the substrate and evolve them, so a bold child
can lose an inherited wariness through exposure while a fearful one deepens it. **The
inventory is evidence-based, not folk-intuitive:** what a child really encounters and
what really harms them (traffic, water) drives which things are spawned and how often —
salience = impact × frequency — rather than folk predators, capturing the
inherited-fear-versus-modern-hazard mismatch.

*(Code: `core/sim_world/environment_matrix.py` — `Thing`, `Bond`, `EnvironmentMatrix`,
`encounter`; data-driven inventory in `data/things/*.json`, `default_things()`.)*

### 3.3 The group matrix (groups)

The third interface — the last of the three to be built — is the person's relationship
with **groups**: their standing within the groups they belong to, how they behave inside
them, and what they gain from and contribute to them. A group is not reducible to the set
of dyadic ties within it: it has an identity a person can belong to, a status hierarchy a
person occupies a position in, and norms a person conforms to or resists — and belonging
as such exerts its own pull. A `Group` is a neutral container (a family, a class, a
clique, a team, a workplace, a community, a subculture); a `Membership` carries standing,
belonging, contribution, and conformity, and a **dominance-versus-prestige** status route
that *emerges* from temperament (status taken by threat and coercion versus freely
conferred for competence). The matrix is grounded in four established frameworks: social
identity theory (Tajfel & Turner), the need to belong (Baumeister & Leary), ostracism /
the need-threat model (Williams), and the dual model of status (Henrich & Gil-White) —
pointers to be cited properly in the write-up, not findings asserted here.

*(Code: `core/sim_world/group_matrix.py` — `Group`, `Membership`, `GroupMatrix`,
`group_encounter`, `default_groups`; wired into the life-stepper so children accumulate
memberships as they grow.)*

---

## 4. The human-interior diet (activities)

A child lives a mostly-activity diet, age-gated so activities arise only when
appropriate, each run through the substrate; which system an activity engages, and what
it does to the person, emerges. The diet is rich and age-graded — play, learning, sport,
friends, being driven to school, and adverse experiences (failure, rejection, loss).
Sexual activity is represented only as an age-gated bundle of the LUST/affiliation
triggers the model already contains — abstract, never content, and strictly gated away
from children (14+).

**Honest state:** the vocabulary is rich, but at this crude stage the substrate still
funnels most children to a SEEKING-dominated profile (reward and novelty cues recur, FEAR
recruits SEEKING, use-strengthening compounds the winner). This is the crude mock-up
showing through — the vocabulary is rich enough, the *dynamics* are not yet — and it is
not to be tuned away. The richer diet is in place for when the substrate matures.

*(Code: `core/affective_engine/activities.py` — `Activity`, `ACTIVITIES`,
`activities_for_age`, `sample_activity`; run via `development.py` — `live_stimulus`.)*

---

## 5. The living world

Around the mind sits the world that presents it with all of the above as it ages. This
layer has grown far beyond the earlier draft and is now substantial in its own right.
Everything in it enriches the *world*, not the *mind*: no autonomous language-model
planning is introduced, and the core ships **no venues, routines, or behaviour
categories of its own** — a study supplies those as an extension, keeping the instrument
neutral.

### 5.1 Places, institutions, and the Game-Master

The world is a graph of **places** (a home with rooms; a school with classroom,
playground and staff room; workplaces; public space), populated by **objects** with
affordances, and structured by **institutions** (a family, a school, an employer, a peer
group) that carry a **climate** (warmth, structure) and an **incentive regime** (reward
for cooperation, sanction for defection). Movement is local: you can only go somewhere
adjacent, and the world exposes to each agent only what it could perceive from where it
is. A **Game-Master** turns the mode a person settles on into world change —
relationships shift, reputation moves, and the institution's response feeds the same
validated development rule — and it is **rule-based and inspectable, not a model call**,
so the world is legible and reproducible.

*(Code: `core/sim_world/world.py` — `World`, `Place`, `WorldObject`, `Institution`,
`Clock`, `LifeStage`, `stage_for_age`; `person.py` — `Person`, `Body`; `gamemaster.py` —
`GameMaster`, `institution_to_environment`; `builder.py` — `build_world`, with
`WARM_FIRM_PRESET` and `HARSH_INCONSISTENT_PRESET`.)*

### 5.2 Interiors and neutral norms

A place has an **interior** of **areas** and **affordance-objects** whose actions carry
preconditions (a role present, being observed or unobserved, a door's lock state) and
impose an appraisal on the actor. Areas connect through neutral **access** rules (open,
role-restricted, or closed — respect for boundaries, not locks). Each place carries a
**norm profile**, so the same conduct is assessed by *where* it happens — but the core
ships no categories of its own: what a home or school is, and what conduct each place
expects, come from a study.

*(Code: `core/sim_world/interior.py` — `Area`, `AffordanceObject`, `Affordance`, `Door`,
`Access`, `Venue`; `norms.py` — `Norm`, `NormProfile`, `category_of`, `assess`,
`observer_reaction`, `departure_magnitude`.)*

### 5.3 Households and real demography

The population is composed to real demographic proportions rather than by intuition. Each
household is given a **tenure** (England ~64% owner / 19% private rent / 16% social),
from which bedroom-sharing, spare rooms, and a **comfort** score (space per person)
follow, and the home is built to match — shared bedrooms where poorer or larger, a study
or box room where wealthier — so comfort, itself a developmental input, is visible in the
floor plan. Homes connect to the outside (a front door onto the street; a **garden** where
the household has one), with garden access and size anchored to ONS (~12% of GB
households have no garden, 21% in London), across three settlement profiles (rural,
suburban, inner-city). The garden affords outdoor play — another developmental input.

*(Code: `core/sim_world/population.py` — `Household`, `Population`, `HouseholdProfile`,
`populate`; demography in `core/sim_viz/settlement.py` — `DemographyProfile`.)*

### 5.4 Time: one clock, many speeds

`timeline.py` is one clock with many speeds. At the fine end it runs in real time — you
watch sim-people interact tick by tick; at the coarse end it fast-forwards by day, week,
month or year, surfacing the events of that span at that granularity (the same event
stream shown at the chosen resolution). A `TimeController` drives a study-supplied
`world_step(clock, minutes)` callback that advances the simulation and returns events; the
core provides the clock, the scales, the bucketing into periods, and optional real-time
pacing for a live view. Two clocks run conceptually: a fine **interaction clock** (social
episodes) and a coarse **developmental clock** (aging and life-stage transitions).

*(Code: `core/sim_world/timeline.py` — `TimeScale`, `Instant`, `Event`, `Period`,
`SimClock`, `TimeController`, `SCALE_NAMES`.)*

### 5.5 The day loop and ambient exposure

A **rule-based day loop** moves agents through waking, washing, eating, school, work and
leisure — machinery only, with the content supplied by a study. Development is then driven
by **two** forces, not one. The first is the rare, sharp **episode** — an opportunity, a
provocation, a moment with a vulnerable other. The second is continuous **ambient
exposure**: the developmental effect of simply *being* in an environment for hours. Each
environment carries an ambient character (warmth, restoration, threat), and a child
accumulates its pull in proportion to time spent there — a warm, restorative setting
gently building conscience-control while a hostile one erodes it and sensitises threat.
Because the mundane hours are so many, their cumulative weight rivals or exceeds the rare
episodes (the proportionality of exposure): two otherwise-identical children in identical
homes, differing only in whether the daily walk to school is through a park or a hostile
street, diverge. This corrects an earlier bias in which only dramatic moments shaped
development.

*(Code: `core/sim_world/daily.py` — `Block`, `Routine`, `Inhabitant`, `run_day`,
`run_days`; the ambient route `expose` alongside `develop_step` in the development rule.)*

### 5.6 The life-stepper — growing a population up over years

`make_life_stepper` closes the loop between the layers: advancing the clock ages the whole
population through their lived days to emergent outcomes. Each child carries a
developmental state — its mind, the plasticity-gating environment derived from its own
home's parenting climate and the parent–child tie, and a situation pool drawn from its
home and school. As simulated years pass, each child lives developmental episodes (fed to
the validated `develop_step`), ages through the life stages, and is read out at the end of
childhood; a child already part-grown at the start has its missed early years run at
initialisation. Because home climate varies across the population, the outcome tracks the
child's home — warmer homes yield more sophropathic-leaning read-outs — which is the
evidence the environment transmits correctly through development. **The outcomes are
produced by the mechanism as it runs: a test-bed for reasoning about the model, not
evidence about people.**

*(Code: `extensions/sophropathy/timeline_driver.py` — `make_life_stepper`,
`make_stepper`.)*

### 5.7 Spawning a town, and a whole study

The visualiser can generate a whole **town** from a spec — a street grid, plots,
buildings, greenery and traffic laid into a `CityMap` the compositor renders, sized from a
target population via a demography profile of ratios. `populate` then binds a society into
it — households in the homes, pupils in the school, workers in the workplaces, and the
standard relational ties among them. `project.py` is the reset/start point for any new
study: a project is a name, a target community size, a demography profile, and a choice of
extensions. Spawning it sizes a settlement from **real ratios** (household size 2.41,
working-age 62.9%, ~1.2 cars per household, ~280-pupil primary schools — ONS Census 2021
and DfT National Travel Survey 2021, England), generates and renders it, populates it, and
applies whatever the selected extensions contribute (for sophropathy, seeding a minority
of children with the fearless proto-psychopath disposition). The core spawns a balanced
society; each extension declares how it perturbs that baseline, so a different study is a
different selection and the core is untouched. Deliberately rough; a runnable starting
point.

*(Code: `core/sim_viz/` — `generate_settlement`, `spec_for_population`;
`core/sim_world/population.py` — `populate`; `project.py` — `ProjectSpec`,
`spawn_universe`.)*

### 5.8 Day-to-day town-life (modelled on Park)

On top of the spawned town sits a **day-to-day life** layer that makes the world watchable
as life: people are somewhere for a reason and move between places over a day, meeting
because they are co-located. It provides a spatial address layer (walkable tiles, building
entrances, rooms), **A\* pathfinding**, **role-based daily schedules** (child /
adult, weekday / weekend, from role + age with individual jitter — *no* language model),
and a batch day-cycle stepper. This is modelled on Park et al.'s generative-agents
"Smallville," with one deliberate difference that is the whole point: Park's cognition —
schedules, choices, dialogue, and the *effects* of actions — is LLM-driven, exactly the
hand-authored-effect pattern PsychSim rejects. PsychSim takes Park's spatial/loop skeleton
(*is → decide → move*) and replaces its cognition with the emergent substrate: schedules
from role and age, interactions when co-located run through the matrices, effects emerge.
The day cycle just gives people a reason to be somewhere and someone to meet; interactions
and development keep running on the substrate throughout.

*(Code: `extensions/sophropathy/townlife.py` — `astar`, `scheduled_block`,
`simulate_townlife`, `render_townlife_html`. See `PsychSim_Park_Review.md` for the full
lineage.)*

---

## 6. The language layer (AI as voice, not mind)

Agents are given a voice by a **two-channel** language layer, kept strictly to one side of
the engine. This is the deliberate inversion of Park et al. (2023), in which the language
model *is* the cognition: here the model, when one is fitted at all, only renders, and
nothing it produces is ever read back into the engine. The layer is **core** — a universal
capability, not specific to the sophropathy research.

**The causal channel (`acts.py`).** Agents never exchange free text; they exchange typed,
parameterised **speech-acts** — `AFFILIATE`, `COMFORT`, `REQUEST`, `PROPOSE`, `ASSERT`,
`REFUSE`, `THREATEN`, `TAUNT`, `DECEIVE`, `WITHDRAW` — and each receiver appraises the
*act*, never any wording of it, so everything causal stays inside the seeded, inspectable
engine. **Deception is a property of the act**, not the words: a `SpeechAct` carries an
`intent` (what it really is) behind a `surface` (what it presents itself as); a receiver
appraises the surface unless it detects the intent, and detection is a **seeded roll
against the receiver's vigilance** — an engine matter, not a linguistic one. **Articulacy
is a rendering knob; capability is an engine parameter** — how well an agent pursues its
goals lives in the engine, how fluently its acts are voiced lives here, and the two never
mix.

**The observer channel (`render.py`).** `TemplateRenderer` is to voice what the
placeholder tileset is to graphics: a deterministic, dependency-free stand-in that voices
acts as dialogue for humans. `LLMRenderer` is the documented drop-in slot for a fine-tuned
small model (LoRA-adapted, conditioned on act × register × articulacy — the Study 4 Part E
plan). Swapping renderers changes nothing causal, because nothing reads rendered text back.

**The acceptance gate (`faithfulness.py`).** A renderer may be trusted for observer
transcripts only if, from a rendered line alone, an independent probe can recover the act,
the register band, and the articulacy band (targets .90 / .80 / .80). The template
renderer currently clears the gate at roughly **.92 / .91 / .88**. Intent is deliberately
*not* recoverable — a deception must sound like its surface.

**Wired into the world.** The layer is not a bolt-on: `GameMaster.converse` makes agents in
a running world actually talk. The speaker emits the act its settled behavioural network
makes (register from its life stage, articulacy a rendering-only knob); the hearer's
vigilance — grounded in its threat gain and its trust in the speaker — sets the seeded
detection probability; the hearer then appraises the *perceived* act and settles its reply.
A believed exploit is remembered as warmth, a detected one as betrayal. The words never
touch the causal path. *(Note: act selection currently reads the agent's named behavioural
network via `act_from_network` — see the pathway inconsistency in Section 2.10; under the
recommended resolution, acts would derive from the emergent substrate read-out instead.)*

*(Code: `core/speech/` — `acts.py` (`SpeechAct`, `SpeechChannel`, `ACT_TYPES`, `REGISTERS`,
`act_from_network`, `perceive_act`, `appraisal_from_act`), `render.py` (`TemplateRenderer`,
`LLMRenderer`, `articulacy_band`), `faithfulness.py` (`evaluate`, `passes`, `probe_line`).)*

---

## 7. The visualiser

A visualiser renders any world the platform builds — universal, not study-specific. It
provides a map data model and an **isometric compositor**, and a **tileset slot** with
three interchangeable implementations behind one interface: `PlaceholderTileset` (bare
shapes), `ProceduralTileset` (tiles drawn in code as vector SVG — a whole town with no art
assets, style-consistent by construction), and `PngTileset` (the raster slot for produced
art). Swapping them is a one-line change. Separately, and this is the **designed look**,
`floorplan.py` renders the top-down **"glass-roof" plan view**: houses as floor plans, with
rooms, doorways, gardens and furniture, drawn server-side so the picture *is* the model.

*(Code: `core/sim_viz/` — `mapmodel.py`, `compositor.py`, `procedural.py`, `binding.py`,
`floorplan.py` — `render_settlement_plan`; `settlement.py` — `DemographyProfile`,
`generate_settlement`, `spec_for_population`.)*

---

## 8. The analysis harnesses

The platform can be run experimentally and read out on the emergent drive-profile.

**Bifurcation / edge exploration.** Sweep environmental (and dispositional) parameters and
read a neutral projection of the emergent profile at each cell, to look for transitions and
separatrices; it supports 2-D phase maps, separatrix extraction, and a **bisection
edge-finder**. It presupposes no result — it varies the parameters and reports whatever the
mechanism does — and it runs in **graded (sigmoid)** as well as binary mode, so outcome
boundaries can be smooth rather than knife-edge. A `Config` is a complete set of parameters
for a single simulated life (disposition, caregiving environment, and optionally a mid-life
change of environment so timing can be explored); the explorer reports both the discrete
read-out and the continuous measures underlying it, because the bifurcation is really a
transition in the continuous measures. Runs are reproducible via seeded temperament.

**Experiment framework.** Raise one agent through a staged life course, cross trait ×
environment factors, replicate across seeds, and aggregate — universal to any trait ×
environment study.

**Stage conditions.** A set of experimental conditions (perfect, imbalanced, control, and
so on) each reporting a distribution of emergent dominant systems and the mean profile.
*(These numbered "stages" are experimental conditions, not the developmental stages of
Section 2.6.)* Both harnesses were reconceived to measure the *emergent* quantities rather
than the deleted verdict, and both honestly show that, at this crude stage, the substrate
produces little differentiation — the correct thing for them to report.

*(Code: `core/bifurcation/` — `Config`, `run_config`, `RunResult`; `core/sim_experiment/`
(+ `readout.py`); `extensions/sophropathy/stages.py`.)*

---

## 9. The neural designer and data-driven configuration (the swap seam)

The direction of travel for the whole architecture is to move research *content* out of the
core and into swappable data, so the core carries only *mechanism*. Three pieces implement
this seam.

**The neural designer.** A sandbox for authoring the affect model *as data*: define
circuits, input features, external triggers, internal **pathways** (cascades and loops),
and **networks** (weighted aggregates of pathways); store them as a JSON library; run them;
visualise them as an SVG wiring diagram; validate them (with loop-detection). This is the
route by which "the specific circuits" become swappable content rather than hard-coded
core — the seam through which alternative affect models, and now the **adopted category-free
substrate**, drop in. Its authoring vocabulary (circuits, pathways, networks) is the same
one the substrate seed is written in, so the seed (`docs/neuralnetworks/psychsim_substrate_seed_v*.json`)
is the concrete payload this seam is meant to receive. **Honest state:** it is an **authoring
sandbox only — not yet wired into the live substrate**. Wiring the substrate seed into a
running engine — replacing the seven-system `drives.Brain` per §§2.11–2.14 — is the explicit
next build and is exactly the migration the §2.10 resolution calls for.

**Editable data configuration.** The world and mind are increasingly defined by editable
files under `data/` — `towntypes/`, `modules/`, `roles/`, `things/`, `groups/`, `social/`,
`neural/`, `executive/` — with a config loader and a generic **matrix CRUD** over the three
matrices' *definition* items (Things, Groups, RolePairs), while the emergent traces (Bonds,
Memberships, Ties) stay read-only. A researcher edits the world and the mind as data; edits
apply on the next spawn.

**The plug-in registry.** `modular/registry.py` provides `Module` and `discover_modules` —
the plug-in system that lets a study register itself as a selectable extension (the
"dropdown"), which `project.py` uses when spawning a universe. Both the sophropathy study
and the justice study are modules; a new study is a new module reusing the core unchanged.

*(Code: `core/neuraldesigner/` (`store.py`, `data/neural/library.json`); `core/config/`
(`townprofile.py`, `loader.py`, `matrixstore.py`); `core/modular/registry.py`;
`core/affective_engine/exec_store.py` with `data/executive/monitors.json`.)*

---

## 10. The live platform — engine, server, UI (the current frontier)

The newest layer turns the batch simulation into something you can watch and steer.

**A live step-loop engine.** `SimEngine` refactors the batch stepper into a genuine
continuous loop: `step()` advances one tick; `snapshot()` returns live JSON state
(positions, drives, clock); `town()` returns geometry; `person_detail(cid)` returns full
inspectable state; live controls add/respawn people and set the tick rate. It also renders
the plan-view "glass-roof" SVG server-side (the picture *is* the model) and **saves/loads a
whole running world** — evolved minds, memories, positions and clock — to
`sims/<slug>.psychsim` with a JSON metadata sidecar. *(Development itself runs over real
life spans via the life-stepper, not the compressed live clock; the live loop is for
day-to-day life and inspection.)*

**A streaming server.** `psychsim_server.py` is a **standard-library** HTTP server that
runs the engine step loop on a background thread while "playing," with CORS. Endpoints
cover town and plan geometry, live state, per-person detail, saves, health, and a command
channel (play / pause / speed / add / respawn / save / load), plus the in-app editor
endpoints (`/matrix`, `/neural`, `/executive`). If a built UI exists at `ui/dist` it also
serves that single-page app, so one command serves both the app and the live sim.

**A control panel.** `ui/` is a Vite + React + TypeScript app: a fast grid view *and* the
designed plan-view floor plans with live people overlaid, camera-follow, smooth motion, and
click-to-inspect (subjects solid, background people faded). It hosts three **authoring
editors** — a **matrix editor** (Things / Groups / RolePairs), a **neural editor** (the
neural-designer sandbox, with an SVG wiring diagram and integrity checks), and an
**executive-function editor** (declarative monitor specs). The old single-file CDN
`psychsim_ui.html` is retained only as the retired proof-of-concept.

**Discipline reminder:** the neural editor and executive editor are **authoring surfaces,
not shortcuts around the discipline**. The executive registry ships empty by design
(Section 2.9); authored monitors and networks must be *researched* patterns, and the
neural-designer output is not yet wired into the live substrate. Never hand-install the
directional effects the discipline forbids.

*(Code: `extensions/sophropathy/engine.py` — `SimEngine`; `psychsim_server.py`; `ui/`;
saves in `sims/`.)*

---

## 11. What is crude, and what must replace it (the replaceability map)

This section is the honest catalogue. Everything below is a placeholder awaiting the real
research.

| Construct (current, crude) | What it stands in for | To be replaced by (after research) |
|---|---|---|
| Seven Panksepp systems as the "networks" | the brain's real neural/affective machinery | **the adopted category-free neural substrate** (§§2.11–2.14): catalogued pathways/circuits/networks with emergent-emotion read-out, wired in via the neural designer (Section 9) |
| Substrate seed: qualitative newborn weights + SCAFFOLD dynamics | real birth-strength connectivity and measured time-constants/plasticity curves | measured values from the literature; until then each is confidence-coded and marked scaffold, not asserted |
| Genetic/physical endowment (attractiveness, health, dexterity — TBD) | how bodily and genetic initial conditions shape a life | a decided, grounded trait set entering only as inputs to the agent's experience, never as trait dials |
| Sensory / proprioceptive / interoceptive embodiment | the bodily basis of emotion generation | fuller sensory hierarchies, proprioception, and an interoceptive–autonomic loop, grounded and staged |
| `TRIGGER_AFFINITY` (which system fires to what) | the tuning of real circuits to real inputs | evidence-based affinities from affective neuroscience |
| Two inter-system rules (SEEKING→RAGE, FEAR→SEEKING) | the rich web of inter-system control | the real inter-systemic dynamics from the literature |
| `window_plasticity` — 4 crude phases | the staging of neural development | a proper 5-to-7-stage developmental model, with per-system sensitive windows |
| `USE_LR`, `DISUSE_DECAY` (use-strengthening rates) | long-term potentiation and disuse | rates/curves grounded in plasticity research |
| Behaviour lookup (dominant system → one behaviour) | the mapping from drive to action | a richer, context-sensitive action model |
| The legacy circuit/network engine + named networks (Section 2.10) | a superseded affect model still driving world behaviour and speech-acts | retired in favour of the category-free substrate (§2.10 resolution); world behaviour and speech-acts derive from the successor's emergent read-out |
| Executive layer — mechanism + memory-learning route built; monitored content deferred | prefrontal top-down control of the substrate | researched patterns the pathways monitor and how strongly they modulate; an environment that also *punishes* so inhibition is actually learned |
| Relationship-tie / environment / group book-keeping rates | how relationships, bonds and memberships strengthen and strain | grounded social- and relationship-dynamics models |
| Inherited-lean values; environment `ACCRUE` rate | how prepared fears and bonds form | conditioning / prepared-learning research |
| Activity bundles, ambient character, and significances | the real texture of lived experience | empirically-characterised activities and exposures |
| Role daily schedules; town-life on-arrival interactions | a real day's shape and the encounters it affords | grounded time-use data; richer co-located interaction |
| Demography ratios (anchored to ONS England 2021) | a real population's composition | pinned to a specific ONS area, or another country, when a study needs it |
| Template renderer (voice) | fluent, faithful natural dialogue | a LoRA-adapted small open-weights model in the `LLMRenderer` slot, cleared through `faithfulness` |
| Every numeric parameter | — | calibration against the human studies (Study 2, Study 5), replacing the marked placeholders |

**A note on history.** Earlier versions contained hand-written directional verdicts — a
development rule that raised "control" under warmth and crept "threat" under harshness at
invented rates, and a classifier that mapped internal quantities to
"psychopathic/sophropathic" labels. These were exactly the encoded psychological effect the
discipline forbids, and they have been **removed**; development and classification now run
on the emergent substrate and a descriptive read-out. Some obsolete tests that asserted the
old verdicts are intentionally skipped and honestly marked. This document describes the
platform after that correction.

---

## 12. Running the platform, and verification status

The fastest confirmation that everything works is the test suite; the end-to-end pipeline
is the fullest single demonstration; and the server plus UI is the live, watchable surface.

```bash
python run_tests.py        # the whole suite (core platform + extensions)
python run_pipeline.py     # spawn a small world, age a population, print a summary
python psychsim_server.py  # the live server; serves ui/dist if the UI has been built
```

Driving a study from Python starts at `project.py`:

```python
from project import ProjectSpec, spawn_universe
from sim_world import TimeController, TimeScale
from sophropathy import make_life_stepper

uni  = spawn_universe(ProjectSpec(name="demo", target_population=100,
                                  profile="england_2021", extensions=["sophropathy"],
                                  fearless_frac=0.4, seed=3), place_residents=False)
step = make_life_stepper(uni, seed=1)
TimeController(step).run(TimeScale.YEAR, steps=22)   # age the population over ~22 years
```

**Verification status.** The Python engine, every server endpoint (including the plan view,
saves, save/load, and static UI serving), the full test suite (a few hundred tests pass;
the skips are the intentional obsolete verdict tests), the UI type-check and production
build, and a headless render of every UI component have been exercised. The remaining
unverified item is the in-browser look and feel (overlay alignment, easing, camera-follow),
which needs a human at a browser. The build decision recorded in the thesis (adopt, adapt,
or build from scratch — Gate C) is the wider framing for how far this platform is taken.

---

## 13. How this document relates to the others

- **`PsychSim_Handover.md`** — the single source of truth for the codebase: the exact
  repository map, how to run everything, the live server and UI, and the current
  test/verification state. When code and this design document disagree, the Handover and
  the code win.
- **`ARCHITECTURE.md`** — the organising principle and the core/extension boundary in
  brief, with the core packages and the done/next roadmap.
- **`PsychSim_Park_Review.md`** — the review of Park et al.'s generative-agents simulation
  and the lineage of the town-life layer (what was adopted, and the cognition that was
  deliberately not).
- **`docs/neuralnetworks/`** — the design record and seed data for the **category-free
  neural substrate** (Panksepp as read-out rather than foundation): the master document
  (versioned) and the substrate seed (`psychsim_substrate_seed_v*.json`). This is now the
  **adopted forward direction**, documented in §§2.11–2.14 and resolved in §2.10; it is the
  successor the current seven-system code migrates to. The one caveat travelling with it is
  data provenance — the seed's own citations are sound on the sample checked, but any
  separately generated reference list (e.g. a `*_TO_VERIFY` spreadsheet) must be verified
  against primary records before use, per the companion review and the thesis's own
  Appendix 2.B.

---

## 14. What this is, and what it is not

PsychSim is a **research instrument**: a tool for testing the internal coherence of the
society model and for generating hypotheses. However rich it becomes, it is **not evidence
about human beings**. A pattern the platform produces — an outcome that tracks a home, an
edge the explorer locates — is a prediction to be tested and a claim about the model until
the model is calibrated to the human studies and validated against behaviour. Every output
carries that bound. The move to a category-free neural substrate deepens the mechanism but
does not change this: even fully assembled, it is a **functional, illustrative** model, not
a biophysically faithful reconstruction of a human brain, and it should be described as such.
Its richness buys *fidelity of process* (personality as emergent developmental sediment),
not *fidelity of biology*. The discipline that makes the instrument worth trusting is the one
stated at the top and honoured throughout: the mechanism must never contain the answer.
