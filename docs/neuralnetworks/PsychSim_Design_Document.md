# PsychSim — Architecture and Design Document

*A simulation platform for modelling how a mind develops.*

---

## 0. Status, purpose, and the governing discipline

PsychSim is a computational platform for studying how a human personality develops
over a life course — built as the simulation substrate for research into the
functioning, non-offending psychopath and its early-childhood manifestation
(the *proto-psychopath*), though the platform itself is general.

**Everything in this document is a crude scaffold.** Not one construct here is a
claim about how minds actually work. Each is a deliberately simple placeholder,
put in place so that the *structure* of the simulation can be built and tested,
and so that — once the real neuroscience and psychology have been researched in
depth — each placeholder can be replaced, one at a time, by the observed and
theorised models the research literature provides. The document is written to make
that replaceability explicit: every crude construct is named as such, and Section 9
is a consolidated catalogue of exactly what must be replaced and with what kind of
evidence.

Three principles govern the whole design, and they are non-negotiable:

1. **No encoded psychological effect.** The simulation must contain no hand-written
   rule of the form "a hostile setting raises threat," "warmth builds
   self-control," at invented rates. Feeling and behaviour must *emerge* from an
   evolving internal substrate — the wiring decides outcomes; the designer does
   not. Where the platform once contained such directional verdicts, they have been
   torn out (see Section 8, history).

2. **The substrate is a neutral stage.** Scenario input describes what a situation,
   a person, a thing, or an activity *presents* — its triggers, in a neutral
   vocabulary — never what it does to the person. What it does emerges from the
   individual's wiring, so two individuals can respond oppositely to the identical
   input.

3. **At this crude stage the model should produce chaos, not order.** Because the
   substrate is an incomplete mock-up, running it should *not* yield tidy, realistic
   social behaviour. Orderly outcomes that neatly track the environment would be
   evidence that the model had been forced or hand-tuned, and would need to be
   removed. Undifferentiated or chaotic output at this stage is correct.

---

## 1. The shape of the whole system

PsychSim has one **internal model** (a mind) that interacts with an **external
world** through **interface matrices**:

```
                       ┌─────────────────────────────────────────┐
                       │              THE INTERNAL MODEL           │
                       │   (per person — an evolving substrate)    │
                       │                                           │
                       │   primary neural systems  ──►  behaviour  │
                       │   strengthen with use     ◄──  personality│
                       │   gated by developmental windows          │
                       │   + always-on executive layer (co-active)  │
                       └───────────────┬───────────────────────────┘
                                       │ acts through
        ┌──────────────────────────────┼──────────────────────────────┐
        ▼                              ▼                              ▼
┌─────────────────┐          ┌─────────────────┐          ┌─────────────────┐
│  RELATIONSHIP   │          │   ENVIRONMENT   │          │     GROUP       │
│     MATRIX      │          │     MATRIX      │          │    MATRIX       │
│  (beings)       │          │   (things)      │          │  (groups)       │
│  Park-style     │          │  attraction /   │          │  standing &     │
│  ties           │          │  aversion       │          │  belonging      │
│  ── BUILT ──    │          │  ── BUILT ──    │          │   ── BUILT ──   │
└─────────────────┘          └─────────────────┘          └─────────────────┘
                                       ▲
                                       │ fed by
                       ┌───────────────┴───────────────┐
                       │   THE LIVING WORLD            │
                       │   places, households, a clock │
                       │   that ages the population,    │
                       │   the significant activities   │
                       │   of a life (the diet)         │
                       └───────────────────────────────┘
```

All three interface matrices are now built (relationship, environment, group); the
**group matrix (Section 7) is now built** as the third interface matrix. Around
the mind sits a living world that presents it with situations, people, things, and
activities as it ages, and a set of analysis harnesses that read out what emerges.

**Code layout.** The platform is split into a reusable `core/` and research-specific
`extensions/`:

- `core/affective_engine/` — the internal model (the substrate, development,
  the activity vocabulary, the descriptive read-out).
- `core/sim_world/` — the world and the interface matrices (relationships,
  environment, groups, places, households, time, the day loop, dialogue).
- `core/bifurcation/`, `core/sim_experiment/` — analysis harnesses.
- `core/sim_viz/`, `core/speech/`, `core/neuraldesigner/` — visualisation,
  speech acts, and a lower-level network-design sandbox.
- `extensions/sophropathy/` — the research study built on the platform (the
  life-stepper that ages a population, the study world, the stage conditions).
- `extensions/justice/` — a secondary study (criminogenic labelling).

---

## 2. THE INTERNAL MODEL — how a personality is built (the core of the platform)

This is the heart of PsychSim and the part that matters most. It models a mind as
an evolving substrate of primary neural systems that strengthen through use across
the stages of development, and from which behaviour, attitudes, desires — the
whole personality — emerge.

### 2.1 The substrate: primary neural systems as the "networks"

The base of the mind is a set of **primary emotional/motivational systems**, taken
as the crude stand-in for the neural networks a real brain runs on. The current
model uses the seven primary systems of Panksepp's affective neuroscience — chosen
because they are evidence-based, evolutionarily conserved, subcortically rooted,
and already mapped to individual differences in personality:

| System   | Class       | Fires to (its own triggers)              | Behaviour when dominant |
|----------|-------------|------------------------------------------|-------------------------|
| SEEKING  | appetitive  | reward cue, novelty, comfort             | approach                |
| CARE     | appetitive  | a vulnerable other, affiliation          | nurture                 |
| PLAY     | appetitive  | a play signal, safety, affiliation       | play                    |
| LUST     | appetitive  | a mate cue                               | court                   |
| FEAR     | aversive    | threat, pain, novelty                    | avoid                   |
| RAGE     | aversive    | restraint, thwarting, pain               | aggress                 |
| PANIC    | aversive    | separation, loss                         | seek comfort            |

*(Code: `core/affective_engine/drives.py` — `System`, `TRIGGER_AFFINITY`, `BEHAVIOUR`.)*

**This seven-system set is itself a crude placeholder.** It is a defensible
starting point, but the real internal model will require researching and designing
the actual neural triggers, loops, and networks — a long process — of which this is
only a first mock-up.

### 2.2 What an individual is made of: reactivity and strength

Each person's brain holds one `Drive` per system, carrying two quantities:

- **Reactivity** — how readily that system fires. This is *temperament*: the stable
  individual difference a person is born with. A "fearless" child has low FEAR
  reactivity; a warm child high CARE reactivity. Reactivity is drawn per person and
  is where dispositional difference lives.

- **Strength** — how developed and relied-upon that system has become. Strength is
  *not* fixed: it grows with use (Section 2.4). It is the mechanism by which
  experience builds a personality.

*(Code: `drives.py` — `Drive(reactivity, strength)`, `Brain`, `Brain.from_temperament`.)*

### 2.3 How behaviour arises — a lookup, never a verdict

A situation, a person, a thing, or an activity **presents a stimulus**: a bundle of
triggers in the neutral vocabulary (threat, reward cue, novelty, a vulnerable
other, separation, a play signal, affiliation, restraint, and so on). One moment of
behaviour runs as follows:

1. Every system computes its **activation** to that stimulus = its reactivity ×
   (a function of its strength) × how well the stimulus matches its own triggers.
2. Systems **interact** (Section 2.5).
3. The system with the highest activation is **dominant**, and it drives the
   behaviour through a fixed lookup (SEEKING→approach, FEAR→avoid, RAGE→aggress,
   and so on).

The designer writes down only *what a situation presents* and *what each system
fires to* — both descriptions of mechanism. Nobody writes down that a given
situation yields a given outcome. Because reactivities and strengths differ, the
same stimulus produces different dominant systems in different people. A person
"uses different networks in different situations," exactly as intended.

*(Code: `drives.py` — `Brain.respond(stimulus) -> Response(dominant, behaviour, activations)`.)*

### 2.4 How personality is built — use-dependent strengthening

After each moment, the system that drove the behaviour is **strengthened** — it was
relied upon, and reliance sets patterns. This is the crude stand-in for long-term
potentiation ("cells that fire together wire together"): a system that keeps winning
grows stronger and therefore wins more readily in future. Unused systems drift down
gently. Over a life this is what turns experience into a stable personality: the
profile of strengthened systems *is* the person's settled dispositions.

Crucially, this strengthening rule is **general, not outcome-directed.** It says
only "the system used strengthens." It does *not* say which system a given
upbringing should strengthen — that emerges from which systems a life's experiences
happen to engage, given the person's temperament and the developmental timing.

*(Code: `drives.py` — `imprint(brain, response, age_years)`; rate `USE_LR`, decay `DISUSE_DECAY`.)*

### 2.5 Inter-system dynamics

The systems are not independent; they interact, per the affective-neuroscience
evidence. Two interactions are currently modelled, both crude first-pass:

- **Thwarted SEEKING feeds RAGE.** When SEEKING is engaged but the situation
  presents restraint or thwarting, RAGE activation is boosted — the mechanism by
  which frustrated pursuit turns to anger.
- **FEAR recruits SEEKING.** Strong FEAR raises SEEKING somewhat — the organism
  seeking safety.

This is a deliberately thin sketch of a very rich real phenomenon; the true web of
inter-system control is a major target for research and redesign.

*(Code: `drives.py` — inter-system block in `Brain.respond`.)*

### 2.6 Developmental stages — when experience leaves its deepest marks

Experience does not leave equal marks at every age. Plasticity is high in early
childhood, dips in middle childhood, rises again in adolescence (late prefrontal
maturation), and is low in adulthood — grounded in the critical/sensitive-period
literature. A **developmental-window** function gates the strengthening: the same
experience strengthens a system far more when the window is open than when it has
closed, and once a window closes the adaptations become comparatively fixed.

The current model is a **crude four-phase** shape:

| Phase             | Approx. age | Window (plasticity) |
|-------------------|-------------|---------------------|
| Early childhood   | 0–5         | very open (~0.9→0.7)|
| Middle childhood  | 5–11        | narrowing (~0.6→0.4)|
| Adolescence       | 11–18       | resurgence (~0.55→0.4)|
| Adulthood         | 18+         | low, settling (~0.35→0.1)|

*(Code: `drives.py` — `window_plasticity(age_years)`.)*

**This is explicitly a placeholder for the richer 5-to-7-stage developmental model
to be built.** The intended replacement is a proper staged model of child
development in which distinct systems have distinct sensitive windows (attachment
and fear-learning very early; social and self-regulatory systems maturing later),
each stage with its own openness profile and its own characteristic experiences. It
is a strong hypothesis of this research that the proto-psychopathic trajectory is
laid down most decisively during particular early windows — but that is getting
ahead of the modelling, and the staged model must be grounded in the developmental
literature before any such claim is examined.

### 2.7 What emerges — the personality, and the read-out

Run this substrate across a life and a personality falls out of it: a settled
profile of which systems are strong and which are weak, which come to dominate in
which kinds of situation. That profile is what constitutes, in the model's crude
terms, the person's **default behaviours, attitudes, opinions, beliefs, and desires
(wants and needs)** — the appetitive systems (SEEKING, CARE, PLAY, LUST) expressing
what draws a person and what they pursue; the aversive systems (FEAR, RAGE, PANIC)
expressing what they avoid and what provokes them.

The model reads this out **descriptively only.** A read-out reports which primary
system dominates and the full profile of strengths — and attaches *no* label. In
particular it does **not** compute a "psychopathic" or "sophropathic" verdict:
whether any such label applies to an emergent profile is a separate, later
interpretive question, kept deliberately outside the mechanism. (The platform once
contained a hand-coded classifier that mapped internal quantities to those labels;
it has been removed, because it was exactly the encoded verdict the discipline
forbids.)

*(Code: `drives.py` — `dominant_profile`, `MindReadout`, `read_mind`; neutral projection `profile_axis` for analysis.)*

### 2.8 Carrying temperament in, reproducibly

A person's temperament can be seeded, so that experiments are reproducible (the same
seed yields the same starting reactivities) while a population still varies
individual to individual. Disposition seeds (e.g. a "fearless" temperament) map onto
the systems' reactivities — a low-fear seed becomes low FEAR reactivity, and so on —
carrying *temperament only*, never an outcome.

*(Code: `drives.py` — `brain_from_seed`, `_SEED_TO_SYSTEM`; `agent.py` — `AffectiveAgent.temperament_seed`.)*

### 2.9 The executive layer — an always-on co-active layer

Above the primary systems sits the **executive-function layer**: the frontal-cortex
system that, in a real brain, can override instinctive drives and is the seat of
inhibitory control, deliberation, conscience, and purpose. It is grounded in two
bodies of work: executive function (Diamond — inhibitory control, working memory,
cognitive flexibility; the prefrontal cortex inhibiting the limbic system; slow
maturation peaking in the mid-20s), and the affective conscience (Blair's amygdala-
vmPFC model — a care-based moral system, fed by the aversive distress of victims,
that guides a person away from harming others, and that is dysfunctional in
psychopathy so that "intelligence becomes uncoupled from conscience").

**The executive pathways are ALWAYS ON.** Unlike a system that is called upon when
needed, the prefrontal control pathways run continuously, monitoring and conducting
the other networks — so the executive is **consulted on every brain event**. It does
not, however, *act* on every event: it fires only on the specific patterns it has
**learned to monitor** (from memory and experience), and when a monitored pattern
matches an event it applies a **direct effect** — the clearest being inhibition,
the prefrontal cortex damping a prepotent drive so that a different system can take
over (the override). The magnitude of that effect is **gated by the executive's
maturation**, so a child's immature executive intervenes weakly and an adult's
strongly — tying the override directly to the developmental model (prefrontal
maturity in the mid-20s, the reason adolescents are impulsive).

This is the architecture: on every `respond`, after the primary systems produce their
activations, the executive is consulted; for each learned monitored pattern that
matches, it inhibits (or amplifies) the target system's activation, gated by its
inhibitory capacity, and the dominant system is then chosen from the modulated
activations. The effect is exercised *through* the substrate's own dynamics — it
changes which system wins, it is not a verdict bolted on top.

**What is built, and what is deferred.** The *mechanism* is built: the always-on
consultation, the learned-pattern registry, the direct inhibitory/amplifying effect,
the maturation gating, and the record of consultations and firings. What is
**deliberately deferred** is the *content* — exactly which patterns the executive
learns to monitor, and how strong each modulation is. In a real brain these are
learned from experience and are precisely what the research must establish; they must
not be hand-invented, any more than the directional effect rules of the primary
systems may be. So the registry is **empty by default**: in a run, the executive is
consulted on every event (the loop genuinely runs — thousands of consultations across
a childhood) but does not yet act, because nothing has been learned to monitor. When
research establishes what the prefrontal pathways monitor and how they modulate, those
patterns are installed through the learning hook and the layer begins to gate
behaviour.

**How memory installs what the executive monitors.** The first such learning route is
built. The executive learns, *from episodic memory*, which prepotent drives to monitor.
Every social event records its outcome to memory — the drive that was run and the valence
of what followed (whether it bettered or worsened the person's social position, an
emergent signal, not a per-drive rule). On *deliberative* steps (learning, reflection) an
installer (`install_monitors_from_memory`) reads that memory: where a drive's responses
have, on balance, led to bad outcomes over enough instances, it installs an inhibitory
monitor for that drive, so the always-on executive thereafter damps it. This is reversal /
reinforcement learning of response inhibition — the orbitofrontal/ventromedial function
whose *failure* characterises psychopathy (the prepotent drive is never brought under
control because its costs are not learned from). It hand-picks nothing: which drive is
regulated emerges from the person's own history. Honest state: in the current crude world
the social environment mostly *rewards* (even aggression is net-rewarded via dominance-
based status), so little is remembered as net-costly and the executive learns to inhibit
little live; the mechanism is proven, and what is actually learned awaits an environment
that also *punishes* (future work).

Alongside this, the layer still carries the four monitored read-outs that make it the
model's **self-awareness**: **inhibitory capacity** and **deliberation** (which mature
toward the mid-20s age ceiling and gate the strength of any executive act),
**moral orientation** (a *read-out of the substrate's* care-based conscience — the
CARE system's development and reactivity, pulled down by a strong RAGE disposition; a
psychopathic-leaning wiring reads low, exactly as the amygdala-vmPFC model expects,
but nothing forces it), and **purpose** (formed goals / philosophy, which accrue only
when the person engages in deliberative experience).

This layer is where the research question can be *watched without being decided*.
Strong deliberation and formed purpose alongside a low affective moral orientation is
the "conscience uncoupled from deliberation" pattern (Blair's cognitive cunning) — and
is also, on the research hypothesis, the route by which a person with a weak affective
conscience might build a *cognitive* conscience and purpose (the possible sophropathic
path). The layer lets us observe whether that is happening; it does not stipulate that
it does.

*(Code: `core/affective_engine/executive.py` — `Executive` (with `monitors`,
`consult`, `learn_to_monitor`), `MonitoredPattern`, `monitor_executive`,
`maturation_ceiling`, `moral_orientation_readout`. The executive is attached to the
`Brain` and consulted inside `Brain.respond` on every event; in the life-stepper it is
both co-active and state-monitored, with an empty learned registry so the loop runs
without yet acting.)*

---

## 3. The interface with the world — the matrices

The internal model does not float free; it engages a world through interface
matrices. Each matrix is a per-person ledger that accumulates a history and shapes
future engagement — and each runs on the *same* substrate, so the feelings recorded
in a matrix are the emergent output of the person's own systems, never typed in.

### 3.1 The relationship matrix (beings) — BUILT

A person's relationships with other beings are held as a Park-style ledger of
**standing ties**. Each `Tie` carries three running quantities — **standing** (how
warm/upheld the relationship is), **reciprocity** (how balanced), and **strain**
(current tension) — and knows the **role** the pairing plays (parent–child,
teacher–pupil, employer–employee, colleagues, teammates, captain–player, community
member), which sets the power differential and what each party is expected to give.

An **interaction** runs both parties' responses through the substrate: the tie
presents each a stimulus coloured by its standing, strain, and power; each person's
systems fire; and the tie updates according to whether the emergent behaviour was
*cohesive* (an appetitive, affiliative engagement) or *aggressive* (RAGE). The
book-keeping rates by which strain and standing move are crude ledger parameters
(like all the model's numbers, tunable), but *which* way a tie moves is driven by
emergent behaviour, not decreed. At this crude stage, ties frequently run to
rupture as strain feeds back on itself — the expected chaos, not a manufactured
cohesion.

*(Code: `core/sim_world/relations.py` — `Tie`, `Society`, `Exchange`, `interact`, `RolePair`, `STANDARD_TIES`.)*

### 3.2 The environment matrix (things) — BUILT

Exactly parallel to relationships with beings, a person accumulates relationships
with **things**: objects, pets, plants, places (a wood, a stream, a park), and
sensory things (music, food). Each `Thing` **presents a stimulus** (what it
involves — a busy road presents threat, a stream gentle novelty); an **encounter**
runs that stimulus through the person's substrate; and the dominant system *is* the
felt sensation — an appetitive response accrues **attraction**, an aversive one
**aversion**, scaled by how strongly the system fired. Encounters also strengthen
the system used, so what a person keeps being drawn to shapes them. Reading the
ledger gives the person's **inventory of attractions and aversions** — the things
they seek out and the things that repel them.

Nothing about what a thing evokes is typed in: a fearful child and a bold child
build opposite inventories from identical things, because their wiring decides.

**Inherited defaults (epigenetic leans).** Some things carry a small inherited lean
present at birth — a prepared wariness of certain hazards. These are a *revisable
head-start*, not a fixed verdict: encounters run through the substrate and evolve
them, so a bold child can lose an inherited wariness through exposure while a
fearful one deepens it. In runs, an inherited predator/snake wariness of −0.25 at
birth spreads across children as their lives diverge.

**The inventory is evidence-based, not folk-intuitive.** The things spawned in the
world, and how often, are chosen by data on what a child really encounters and what
really harms them — salience = impact × frequency. This produced a specific,
important, and grounded feature of the model: a **mismatch between inherited fear
and modern hazard.** Inherited wariness is tuned to *ancestral* threats (heights,
snakes, spiders) that pose little modern risk; the high-impact *modern* hazards
(cars, pools, medicines, electricity) are evolutionarily novel and carry *no*
inherited fear, so a child must learn them entirely through exposure. In runs the
model reproduces the real danger: children come out innately wary of snakes (which
rarely hurt them) and often unwary of, even drawn to, traffic (the leading cause of
child-injury death). No wild predator or stranger-abductor is spawned, because the
evidence shows both are statistically negligible relative to the mundane hazards and
to harm from known people.

*(Code: `core/sim_world/environment_matrix.py` — `Thing`, `Bond`, `EnvironmentMatrix`, `encounter`, `default_things`, `birth_matrix`.)*

---

## 4. The human-interior diet — the significant activities of a life

A life is not made of bare situations; it is made of **activities**, each a
characteristic *bundle* of triggers presented together. The activity vocabulary
gives the substrate that richer diet, so that real structure has something to
emerge from.

Each `Activity` describes the stimulus it presents (in the substrate's own trigger
vocabulary) and the **developmental window** it belongs to — never what it does to
the person. The current set spans the ordinary fabric of a childhood (play, a family
meal, being comforted, exploration, being driven to school, learning, sport, talking
with friends, screen time, achievement), the ordinary *hard* experiences a real life
also contains (being told off, failing at a task, rejection, loss, boredom —
included for realism, not to force any outcome), and age-gated later activities
(independence and group belonging from pre-adolescence; intimacy only from
adolescence). A child lives a mostly-activity diet, age-gated so activities arise
only when appropriate, each run through the substrate; which system an activity
engages, and what it does to the person, emerges.

Sexual activity is represented only as an age-gated bundle of the LUST/affiliation
triggers the model already contains — abstract, never content, and strictly gated
away from children.

**Honest state:** the diet is now rich and age-graded, but at this crude stage the
substrate still funnels most children to a SEEKING-dominated profile (reward and
novelty cues recur across activities, FEAR recruits SEEKING, and use-strengthening
compounds the winner). This is the crude mock-up showing through — the vocabulary is
rich enough, but the *dynamics* are not yet — and it is not to be tuned away. The
richer diet is in place for when the substrate matures.

*(Code: `core/affective_engine/activities.py` — `Activity`, `ACTIVITIES`, `activities_for_age`, `sample_activity`; run via `development.py` — `live_stimulus`.)*

---

## 5. The living world

Around the mind sits the world that presents it with all of the above as it ages.

- **Places and interiors** — homes, schools, workplaces, and their rooms and
  affordances, with parenting climate (warmth, structure) attached to homes, and
  households composed to real demographic proportions.
- **A time clock** that ages a whole population: advancing the clock steps every
  child through developmental moments on the substrate (drawing age-appropriate
  activities, meeting the world's things, and undergoing the home's own situations),
  so that a population grows up and its emergent read-outs can be inspected. This is
  the **life-stepper**, the spine of the research study.
- **A day loop and a dialogue layer**, both now running on the substrate: a person's
  moment-to-moment choices and their spoken acts arise from `brain.respond`, not from
  any legacy activation model.

*(Code: `core/sim_world/world.py`, `population.py`, `timeline.py`, `daily.py`, `gamemaster.py`; the study's life-stepper: `extensions/sophropathy/timeline_driver.py`.)*

---

## 6. The analysis harnesses

The platform can be run experimentally and read out on the emergent drive-profile:

- **Bifurcation / edge exploration** — sweep environmental parameters and read a
  neutral projection of the emergent profile at each cell, to look for transitions
  and separatrices. Runs are reproducible via seeded temperament.
- **Stage conditions** — a set of experimental conditions (perfect, imbalanced,
  control, and so on) each reporting a distribution of emergent dominant systems and
  the mean profile. *(Note: these numbered "stages" are experimental conditions, not
  the developmental stages of Section 2.6.)*

Both harnesses were reconceived to measure the *emergent* quantities rather than the
deleted verdict, and both honestly show that, at this crude stage, the substrate
produces little differentiation — which is the correct thing for them to report.

*(Code: `core/bifurcation/`, `core/sim_experiment/`, `extensions/sophropathy/stages.py`.)*

---

## 7. THE GROUP MATRIX — the third interface matrix (BUILT)

We have modelled a person's relationships with *beings* (the relationship matrix)
and with *things* (the environment matrix). The third interface, now built, is the
person's relationship with **groups** — their standing within the groups they belong
to, how they behave inside them, and what they gain from and contribute to them.
Group membership is one of the most powerful shapers of human behaviour, and the
matrix is grounded in four established frameworks: **social identity theory**
(Tajfel & Turner — categorization, identification, comparison; in-group/out-group;
self-categorization), the **need to belong** (Baumeister & Leary — a fundamental,
individual-varying human motivation), **ostracism / the need-threat model**
(Williams — exclusion threatens belonging, self-esteem, control, and meaning,
driving aggression, withdrawal, or conformity), and the **dual model of status**
(Henrich & Gil-White — status attained by *dominance*, taken through threat and
coercion, or *prestige*, freely conferred for competence). *(These are pointers to
research to be cited properly in the write-up; no specific findings are asserted
here.)*

*(Code: `core/sim_world/group_matrix.py` — `Group`, `Membership`, `GroupMatrix`,
`group_encounter`, `default_groups`; wired into the life-stepper so children
accumulate memberships as they grow.)*

### 7.1 The concept, symmetric with the other two matrices

Just as a person carries a ledger of ties to individuals and a ledger of bonds to
things, they should carry a ledger of **memberships** in groups. A group is not
reducible to the set of dyadic ties within it (which the relationship matrix already
holds): a group has an identity a person can belong to, a status hierarchy a person
occupies a position in, and norms a person conforms to or resists — and belonging as
such (independent of any particular relationship) exerts its own pull. The group
matrix models that group-level layer.

### 7.2 Structure as built (crude first version, grounded, to be refined)

By deliberate parallel with the existing matrices:

- **A `Group`** — a neutral container describing a group a person can belong to
  (a family, a class, a friendship clique, a sports team, a workplace team, a
  community, a subculture). It carries descriptive attributes only — its size, its
  cohesion, its status relative to other groups, the strength of its norms, and
  whether it is an in-group or an out-group from the person's vantage — never a
  verdict about what membership does to the person.

- **A `Membership`** (the parallel of a `Tie` and a `Bond`) — a person's running
  relationship with one group, carrying quantities such as:
  - **standing / status** — the person's position within the group's hierarchy
    (peripheral ↔ central; low ↔ high status);
  - **belonging / identification** — how strongly the person identifies with the
    group and takes its identity as their own;
  - **contribution** and **benefit** — what the person gives to the group and gets
    from it (support, resources, esteem, protection);
  - **conformity / friction** — how far the person's behaviour aligns with the
    group's norms versus chafes against them.
  These are running traces, updated by group encounters — not stipulated.

- **A `GroupMatrix`** — a person's ledger of memberships, from which one can read
  their **social identity**: the groups they belong to, where they stand in each,
  and which memberships are central to who they are.

### 7.3 How it must run — on the substrate, emergent

A **group encounter** (belonging, being included or excluded, gaining or losing
status, being asked to conform, contributing, competing with an out-group) must
present a *stimulus bundle* in the substrate's own vocabulary — affiliation and
safety for acceptance; separation and threat for exclusion or status loss; reward
cue for status gain; thwarting and restraint for coerced conformity — and the
person's own systems must decide the response. Standing, belonging, contribution and
conformity then accrue from the *emergent* behaviour, exactly as tie-strain and
thing-attraction do. Nothing about what a group does to a person may be typed in: a
person high in CARE and one high in SEEKING should come to occupy and value the same
group differently, emergently.

This connects directly to the internal model: repeated group experience strengthens
the systems it engages, so a person's groups shape their personality (a child who
finds belonging through play strengthens PLAY; one who gains status through
aggression strengthens RAGE) — and, in turn, their evolving personality shapes how
they stand in their groups. Group membership is thus both an input to and an output
of the internal model, through the same substrate.

### 7.3a What emerges — dominance and prestige, the relevant result

Because standing accrues from the *emergent* response, the ROUTE to status emerges
from temperament, exactly as the dual model predicts: a strongly dominance-disposed
temperament (RAGE-prone) takes rank by **dominance** — construing a contested,
positional status opportunity as a fight — and resists the group's norms; a prosocial
temperament (CARE/SEEKING-prone) earns rank by **prestige** and conforms more. This is
directly relevant to the research question: coercive status-seeking versus earned
status is close to the psychopathic-versus-sophropathic contrast, and here it is not
typed in — it falls out of the wiring meeting the group. (At this crude stage, as
elsewhere, the substrate's broad reward-reactivity means the prestige route usually
wins for ordinary temperaments and clear dominance is rare; that is the honest crude-
stage behaviour, not a defect.)

### 7.4 Grounding, and refinement still to come

The crude version above is a scaffold. Before it is refined it must be grounded in
the group-psychology literature — the well-developed research areas on social
identity and in-group/out-group processes, group status and hierarchy, norms and
conformity, social comparison, group cohesion, and the relationship layer structure
of personal social networks (the tiered inner-circle / wider-circle / acquaintance
structure of how many relationships a person actively maintains). Those frameworks
will supply the real quantities a membership should carry and the real dynamics by
which they change, replacing the first-pass sketch here. *(No specific findings or
citations are asserted in this document; the named areas are pointers to research,
to be read and cited properly when the group matrix is built.)*

### 7.5 A note on tiering (deferred)

A related refinement, explicitly deferred until after the group matrix and the rest,
is to tier a person's relationships and memberships by how much is actively tracked:
a small inner circle held in rich detail, a wider circle held more thinly, and
beyond that acquaintances held only sparsely — reflecting the real cognitive limits
on how many relationships a person can actively maintain. This is the least
important addition and is noted here only for completeness.

---

## 8. What is crude, and what must replace it (the replaceability map)

This section is the honest catalogue. Everything below is a placeholder awaiting the
real research.

| Construct (current, crude) | What it stands in for | To be replaced by (after research) |
|---|---|---|
| Seven Panksepp systems as the "networks" | the brain's real neural/affective machinery | a researched model of the actual triggers, loops, and networks — a long design effort |
| `TRIGGER_AFFINITY` (which system fires to what) | the tuning of real circuits to real inputs | evidence-based affinities from affective neuroscience |
| Two inter-system rules (SEEKING→RAGE, FEAR→SEEKING) | the rich web of inter-system control | the real inter-systemic dynamics from the literature |
| `window_plasticity` — 4 crude phases | the staging of neural development | a proper **5-to-7-stage developmental model**, with per-system sensitive windows |
| `USE_LR`, `DISUSE_DECAY` (use-strengthening rates) | long-term potentiation and disuse | rates/curves grounded in plasticity research |
| Behaviour lookup (dominant system → one behaviour) | the mapping from drive to action | a richer, context-sensitive action model |
| Relationship-tie book-keeping rates | how relationships strengthen and strain | grounded relationship-dynamics models |
| Environment `ACCRUE` rate; inherited-lean values | how bonds and prepared fears form | conditioning/prepared-learning research |
| Activity bundles and significances | the real texture of lived experience | empirically-characterised activities and exposures |
| The **group matrix** — built, crude (Section 7) | group psychology's effect on the person | deeper models of identity, status, norms, cohesion, and relationship-tiering |
| The **executive layer** — always-on mechanism + a memory-driven learning route built; further learned content deferred (Section 2.9) | prefrontal top-down control of the substrate | researched models of WHICH patterns the pathways monitor and HOW strongly they modulate; an environment that also PUNISHES so inhibition is actually learned |
| Every numeric parameter | — | calibration against human studies |

**A note on history.** Earlier versions of the platform contained hand-written
directional verdicts — a development rule that raised "control" under warmth and
crept "threat" under harshness at invented rates, and a classifier that mapped
internal quantities to "psychopathic/sophropathic" labels. These were exactly the
encoded psychological effect the discipline forbids, and they have been **removed**;
development and classification now run on the emergent substrate and a descriptive
read-out. This document describes the platform after that correction.

---

## 9. Grounding used so far

The crude substrate is not arbitrary; its starting shape draws on established,
verified sources (recorded here as the basis to build from, to be cited properly in
the research write-up):

- **Panksepp's affective neuroscience** — the seven primary emotional systems
  (SEEKING, CARE, PLAY, LUST; FEAR, RAGE, PANIC/GRIEF), subcortically rooted,
  evolutionarily conserved, strengthening through use, interacting (thwarted
  SEEKING → RAGE; FEAR recruiting SEEKING), and mapped to personality
  (Panksepp 1998; Montag & Panksepp).
- **Critical / sensitive periods** — restricted developmental windows of heightened
  plasticity that fix when they close; high early-childhood plasticity and an
  adolescent resurgence with late prefrontal maturation (Knudsen 2004; Hensch).
- **Prepared learning** — inherited readiness to fear ancestral hazards (snakes,
  spiders, heights), with modern hazards carrying no such readiness.
- **Child-injury epidemiology** — road traffic and drowning as the dominant real
  hazards; the statistical rarity of stranger-predation relative to harm from known
  people — used to build the environment inventory on real salience.

---

*End of document. This describes PsychSim as built: an evolving internal substrate
from which personality emerges, interacting with the world through a relationship
matrix and an environment matrix, with a group matrix specified and ready to build —
and every construct a crude scaffold, to be replaced by researched models of the
real neuroscience and psychology.*
