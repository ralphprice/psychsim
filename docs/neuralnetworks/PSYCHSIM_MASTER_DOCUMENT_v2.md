# PsychSim — Master Design Document

**Companion to `psychsim_substrate_seed.json`. Status: design settled; assembly beginning.**

This document details the PsychSim brain model as it now stands, and — as agreed — records the conclusions of our design discussions so the reasoning behind the architecture is not lost. It is the reference the build works from.

*Context, held lightly:* the eventual destination is a PhD (application rewrite; a bias-aware review of psychopathy / difficult children / ASPD / behavioural genetics; research design; and the write-up of results). That is the destination, not a lens on the engineering. The current work is PsychSim itself — a **generic** brain simulator — and this document concerns only that.

---

## 1. What PsychSim is trying to be

A faithful, mechanistic simulation of a developing human mind, in which **personality and behaviour are not programmed but emerge** from neural activity that is shaped, across a life, by experience. The design premise, in one line:

> Comprehensive neural pathways fire in patterns and combinations; sensory, proprioceptive and interoceptive input drives that activity; use-dependent reinforcement and structural growth gradually sculpt unique connection strengths; the resulting activity *is* what we read out as emotion; and the whole is what we call the person.

Everything below serves that premise and, above all, one discipline: **the mechanism must never contain the answer.**

---

## 2. The corrected architecture — the central conclusion

Several turns of discussion converged on an architecture that is importantly different from where we started. The corrections matter enough to state plainly, because each fixed a real error.

**2.1 Panksepp's seven systems are a read-out, not a foundation.** The seven affective systems (SEEKING, FEAR, RAGE, LUST, CARE, PANIC/GRIEF, PLAY) are *categorised descriptions of observed neural activity* — labels for the end-result — not the generative primitives of the mind. Building the substrate *out of* seven systems and letting life "move the levels" on them would model the wrong layer: it bakes the output categories into the mechanism, and it limits change to level-shifts on seven dials when the thing that actually changes across a life is *which pathways fired, how often, in what combination, and the resulting synaptic and structural change*. So the substrate is **category-free**. Emotions — including anything Panksepp would name — are **emergent read-outs computed from substrate activity**, used for description and validation, never fed back in as causes. (This is also the theoretically safer stance: it sits neutrally between Panksepp's basic-emotion view and Barrett's constructionist view rather than committing to hardwired emotions.)

**2.2 Directional weights are the newborn's initial conditions, not forbidden "encoded outcomes."** An earlier framing treated co-activation weights as illegitimate. That was wrong, and the correction is central: a **default starting weight that experience then modifies is the developmental mechanism itself.** The weight is a synaptic strength; reinforcement raises it, disuse lowers it; the adult pattern is the *result* of a life of that, not an input to it. So weights belong in the model — as *initial conditions that plasticity acts on*. What is forbidden is not weights, but *frozen adult weights played back as truth*. Same numbers, entirely different role: seed-plus-plasticity, not hard-coded effect.

**2.3 We assemble comprehensively; we do not cherry-pick.** To recreate a brain, the task is maximal assembly from every reputable source, plus honest cataloguing of what is still missing (including, notably, the fMRI/brain-activity literature that hints at emotional and behavioural correlates we have not yet captured). Mainstream frameworks (RDoC, Panksepp, the resting-state networks) are fine as *organising scaffolds for assembly*; the error is only ever letting them *bound* what we collect. (An earlier draft inflated this into a grand "paradigm contamination" narrative imported from psychopathy scholarship — that was rhetorical over-reach; PsychSim is a generic simulator and does not inherit those stakes. The narrow, true residue: the first pass was consensus-first and thin, so the fix is broader assembly with gaps flagged.)

**2.4 The body is in the loop from the start.** Emotion is *felt* through sensory–proprioceptive–interoceptive feedback between body and brain, so the physical body, its sensory apparatus, and the bodily feedback loops are part of the substrate, not an add-on. The same inter-agent loops will later grow the relationship matrix between two sim-people.

**2.5 Structure is built in full; activation is gated and progressive.** We will get chaos whatever we do — a category-free substrate with real update rules but immature wiring *should* be incoherent early; coherence is what should slowly emerge, and if it appears too early and too tidy we have cheated. Rather than manage chaos by narrowing what exists, we build broadly and switch on a controllable subset, graduating and tuning as we widen the live set.

---

## 3. The architecture in layers

### 3.1 Structure — circuits and connections
Every circuit is a node (nuclei/regions, transmitters) with an activation level and hard bounds. Every connection carries what the plasticity rules consume: a **default (newborn) weight** with its basis (literature / assumption / innate-reinforcer), weight bounds, the **gating neuromodulator**, an **age-plasticity-coefficient** reference, an **innate-reinforcer flag**, a **developmental-online age**, and a **calibration-active** flag. The exact field lists are in the seed file's `schemas`. Assembly proceeds by populating circuits and connections against this schema, comprehensively, gaps catalogued.

### 3.2 Inputs — the body in the loop
Eight input channels (seed file `input_channels`): vision, audition, olfaction, gustation, somatosensation, proprioception, vestibular sense, and interoception. Exteroceptive channels carry the world (and the innate cues — looming, voice, sweet); proprioception supplies the efference-copy comparison behind agency; **interoception is the channel that makes emotion *felt*** — cardiac, respiratory, gastric, chemo/baro and humoral signals returning via NTS → parabrachial → insula/hypothalamus, closing the body↔brain loops in which affect is constituted.

### 3.3 Physical endowment — starting conditions
A normal-distributed physical draw per agent (seed file `physical_endowment`): attractiveness, size, musculature, agility, congenital health, sensory acuity, and the per-circuit temperament reactivity priors. These are **starting conditions and biases on how the world responds to the agent** — attractiveness, for instance, is a bias on *others'* reactions (and thus a driver of the future relationship matrix), not a worth judgement. They are the legitimate genetic/physical layer — explicitly *not* the "gaming-style ability dials" we rejected.

### 3.4 The plasticity engine — the eight rules
This is what makes the model *develop*. All rules are **local and meaning-blind**: they see pre- and post-synaptic activity, the current weight, an activity-derived neuromodulatory scalar, and an age coefficient — never that a circuit "is fear" or a state "is threat." (Full entries, forms, and citations in the seed file's `plasticity_rules`.)

1. **Hebbian coincidence** (Hebb 1949) — co-active connections strengthen; unstable alone, so never stands alone.
2. **Rate-level, not spike-timing** — a flagged modelling choice: our circuits carry activation levels, so STDP's timing rule can't apply literally; we use its rate-level BCM equivalent.
3. **BCM sliding threshold** (Bienenstock, Cooper & Munro 1982) — the workhorse: potentiation above a threshold, depression below, with the threshold computed from the circuit's *own* recent activity. One rule gives potentiation, depression, competition, and self-stabilisation.
4. **Homeostatic scaling** (Turrigiano 1998, 2008) — slow multiplicative renormalisation toward a set-point; must out-run Hebbian growth (the "temporal paradox") — a timescale constraint, not an outcome one.
5. **Three-factor neuromodulatory gating** (Reynolds & Wickens 2002; Frémaux & Gerstner 2016) — a dopamine/ACh/NA-like scalar multiplies a decaying eligibility trace so a coincidence consolidates only if a modulator arrives while eligible. **This is the danger point:** the modulator must be the *output of a circuit whose activation is set by its wiring*, never a value we set because we judge an outcome good or bad. This is where outcomes are most easily smuggled back in.
6. **Developmental gating** (Knudsen 2004; Hensch 2005) — everything scaled by η(age, circuit): high early, dips, adolescent resurgence, low in adulthood. Age enters *only here*, as a rate, never as a target; it abstracts the parvalbumin/perineuronal-net critical-period machinery.
7. **Structural plasticity** (Holtmaat & Svoboda 2009; Petanjek 2011) — weights held near zero are pruned; sustained co-activation between adjacent unconnected circuits can add a connection within connectome limits. This is the "growth from stimulation," and the overproduction-then-pruning arc.
8. **Bounds and competition** (Oja 1982) — finite weight bounds and normalisation make learning necessarily competitive: strengthening some costs others.

### 3.5 Activation gating — two distinct switches
"Not active" means two different things, and they must not be conflated:
- **`developmental_online(age)`** — *biology*. A circuit comes online on its maturational schedule (brainstem/limbic before PFC). This is the natural gate encoded in the developmental parameters.
- **`calibration_active`** — *your tuning dial*. A circuit that exists and is mature can still be masked to zero this run so you can bring subsets online progressively and tune them. Masking is the activation gate set to zero — not deletion, not a hidden weight edit — and it is fully reversible.

Keeping these separate means we never mistake "not mature yet" for "switched off for calibration." Manually masking a circuit the schedule says should be online is logged as a calibration choice, not confused with biology.

### 3.6 Read-out and validation
Emotions and any Pankseppian label are computed *from* substrate activity for description only. **Validation** is where the consensus literature earns its keep: we check whether typically-developed agents *drift toward* the documented adult co-activation patterns, and whether atypical developmental histories produce atypical structure. The documented patterns are the thing we test against — never the thing we assert.

---

## 4. The innate-wiring core — where honesty is won or lost

For *differential* development to occur, the newborn needs some initial sense of which stimuli matter, or the modulator in rule 5 never fires differentially and nothing is reinforced one way over another. In real brains this is hardwired as a small set of **primary reinforcers**. We cannot avoid seeding these — but the discipline is absolute: we seed them as **cited, birth-present anatomy**, never as rules. This is the single place innate structure is unavoidable, and the place the whole edifice stays honest or quietly becomes a lookup table. We went **broad** on this set (with evidence), across three categories (full catalogue in the seed file):

**Primary reinforcers (innate stimulus→valence connections, present at birth).** Sweet→appetitive+calming, bitter/sour→aversive (all present in anencephalic newborns, cross-species, cross-cultural), nociception→aversion+arousal, thermal comfort/discomfort, affective (C-tactile) contact→calming, and interoceptive homeostatic drives (hunger/satiety/thirst/air-hunger). Note the honest exception: **salt is *not* reliably present at birth** (it emerges ~4–6 months), so the "tastes are innate" generalisation is qualified in the data.

**Prepared perceptual biases (innate detectors that bias what is attended).** Looming→a subcortical defensive circuit (superior colliculus→pulvinar→amygdala); sudden intense sound→the acoustic startle arc; face-like/top-heavy configurations→subcortical orienting. Each carries its real caveat: for faces in particular, the innate component may be a *non-specific* bias for top-heavy, high-contrast, low-spatial-frequency input rather than a face-specific template, with cortical face-specialisation emerging from experience.

**Prepared learning biases — and the exemplar of the whole discipline.** Ancestral-threat categories (snakes, spiders, angry faces, heights) are learned about *faster* and extinguished *slower*. The critical point, and the worked example that guards the wall: **human infants are not born afraid of snakes or spiders.** They show rapid *detection*, not fear. So this is **not** an innate fear weight — it is a **modifier on the plasticity learning-rate/extinction for those stimulus categories.** Writing "snake → fear (innate)" would be both a smuggled outcome *and* empirically false. Writing "aversive associations to this category consolidate faster" is a mechanism. That is the line, in one case.

**The wall, stated once more:** a rule may update a weight using local, activity-derived quantities only. *"Co-active connections strengthen"* is mechanism, and allowed. *"Threat strengthens avoidance"* is outcome, and forbidden. The primary-reinforcer links are the one unavoidable seed of innate value, admitted as anatomy with citations.

---

## 5. Development and individual differences

Identical starting circuitry diverges into distinct persons through the interaction of three things: the **genetic/physical draw** (per-circuit reactivity priors + the physical endowment, which biases both what input arrives and how the world responds), the **experience stream** integrated through the local plasticity rules within each circuit's developmental window, and **stochastic developmental noise** amplified by activity-dependent competition. No two histories yield the same adult weight structure. This is why the model captures individual variation by changing *parameters on the wiring and the history through it*, not by changing the wiring's rules — and why "chaos now, coherence later" is the correct expectation rather than a bug.

---

## 6. The forward plan — from one brain to a social world

Two pieces are explicitly held for when the single-agent substrate is sound:

- **Two sims face to face.** The same sensory→interoceptive feedback loops that constitute an agent's affect become, between two agents, the substrate for a **relationship matrix**: persistent, emergent dyadic states we can name — trust, affection, and longer-run stances like love/hate — accruing from the history of each agent's circuit responses to the other. As with everything else, these are *emergent read-outs of accumulated interaction*, not allocated values.
- **Richer bodily and sensory feedback.** Deepening the interoceptive/proprioceptive channels and their coupling, so the felt-body basis of emotion is fuller.

Both inherit the same wall: the loops are mechanism; trust and love are read-outs of where the mechanism has been driven.

---

## 7. The seed dataset, and how assembly proceeds from it

`psychsim_substrate_seed.json` is the foundation the broad assembly builds on. It contains:
- `meta` — the principles, the honesty wall, and the scaffold note.
- `schemas` — the exact fields every **circuit** and **connection** must carry (plus the catalogue/input/endowment schemas). *This is the contract the assembly populates.*
- `plasticity_rules` — the eight rules as structured data the engine can reference.
- `innate_wiring_catalogue` — the cited primary reinforcers, prepared perceptual biases, and the prepared learning bias.
- `input_channels`, `physical_endowment` — the body and the starting draw.
- `gaps_register` — the honest list of what is missing (default birth weights, exhaustive projections, fMRI correlates, quantitative innate strengths, receptor/glial detail, genotype→parameter maps, and more).

**How to extend (the broad assembly).** For each circuit we can find anywhere in the brain, add a circuit record; for each documented projection, add a connection record with a default weight (sourced, or flagged assumption) and its metadata. Keep it in this one growing file. The rule for what may be entered: **structure, connectivity, transmitters, developmental timing, and stimulus entry points are collected freely; directional co-activation values are entered only as *default starting weights* (initial conditions), never as fixed outcomes; and any innate value enters only through the catalogue's cited primary-reinforcer links.**

**The earlier 97-circuit artefact** (`neural_circuit_model.json`) is not discarded: its circuit inventory, projections, transmitters, and developmental parameters are reusable *structure*, and its adult co-activation weights are reusable as **validation targets** (what a typically-developed agent should drift toward) — but **not** as the substrate's live weights. It was assembled consensus-first and is thinner than the experimental literature warrants, so the redone assembly supersedes it as the structural source while keeping it as a validation reference.

---

## 8. What this is not, and the honest frontier

- It is **not** a mind built from emotion categories; emotions are outputs.
- It is **not** a playback of documented adult patterns; those are validation targets. (A separate "circuit engine" that *does* play the documented patterns back exists as a knowledge inspector, and is deliberately walled off from this substrate — its hand-authored curves must never migrate in.)
- It is **not** quantitatively grounded yet: default birth weights, coupling timescales, and innate strengths are largely qualitative or scaffold, to be replaced by measured values.
- The biggest honest gaps are logged in the seed file and will grow as assembly reveals more: chief among them, real newborn weights, an exhaustive projection map, and the fMRI/activity evidence linking states to circuit dynamics.

The model is a **living scaffold with a hard honesty wall**: assemble everything, seed the newborn with cited anatomy only, let local rules and a lived history do the shaping, and read emotion and personality out of what emerges — checking, but never asserting, against what the literature documents.


---

## 9. Assembly log — first populated system (threat / defensive)

Assembly of the broad structure has begun, written into the data doc (`psychsim_substrate_seed_v2.json`) against the schema defined in §3.1 and §7 — not into prose. The **threat/defensive system** is populated first, deliberately: it is the best-evidenced affective system and it exercises every part of the schema at once — innate-reinforcer entry points, neuromodulatory gating, associative-plasticity sites, a defensive-output backbone, and a genuine early-vs-late developmental split. If the schema carries this, the rest widens from the same pattern.

**Grain.** Nucleus level — the amygdala subnuclei are kept separate (lateral `LA`, basal `BA`, central `CeA`, intercalated `ITC`) rather than lumped as "amygdala," because the learning site (LA), the output hub (CeA), and the inhibitory extinction gate (ITC) develop and behave differently, and the model needs them distinct. **Thirteen circuits, twenty-six connections.**

**What this first system proves about the schema** — three checks on the discipline:

1. **Value enters only through cited anatomy.** Of the twenty-six connections, exactly three routes carry innate value — nociception → LA/CeA (catalogue entry `PR-NOCICEPTION`), the looming channel superior-colliculus → pulvinar → CeA/PAG (`PB-LOOMING`), and the startle link `StN` → CeA (`PB-STARTLE`). Each is a birth-present connection from the innate-wiring catalogue, flagged `is_innate_reinforcer_link: true`. Nothing else asserts meaning: the CeA → PAG / hypothalamus defensive **backbone** is present but is plain output anatomy (moderate-strong, *not* "threat is bad"), and every sensory → amygdala **associative** site starts near zero and is grown only by experience through the plasticity rules.

2. **Newborn weights stay honest.** They are qualitative (`low` / `low-moderate` / `moderate` / `moderate-strong`), because the literature gives *adult* co-activation patterns, not birth strengths. Only the innate links are confidently non-zero at birth; everything else is flagged `assumption` in `default_weight_basis` and `source`.

3. **The schema carried it with one small addition.** Populating threat required only one new field — an optional `function` one-liner on each circuit record — added to the schema and to every record. All prior fields and every original key (catalogue, plasticity rules, inputs, endowment, gaps) are preserved unchanged.

**An emergent developmental signature — noted, not authored.** At birth this system can *detect and express* threat (the innate cues plus the CeA → PAG / hypothalamus backbone) but essentially cannot *regulate* it: vmPFC-driven extinction and ventral-hippocampal context are developmentally offline (`developmental_online_age` ≈ 14 y and ≈ 3 y respectively). Because the associative sites in LA are most plastic early and gated by noradrenaline (arousal), early aversive experience should write strongly and resist extinction until regulation matures. That "sticky early fear, late control" pattern is a **consequence of the timing entered**, not a rule anyone typed — exactly the kind of thing the substrate is meant to produce, and the first small sign that it can.

**Honest gaps for this system** (added to the register): default weights are reasoned assumptions everywhere except the three cited innate links; the plasticity η(age) schedule references (`amygdala_high_early`, `pfc_low_early_high_late`, …) are qualitative labels, not yet quantified curves; and the superior-colliculus → pulvinar → amygdala route and the intercalated-cell microcircuitry are simplified. All flagged in the data, none faked.

**Next.** Reward/approach — the dopaminergic mirror of this system; the two pair as the approach/avoid core — then sensory input, then the executive suite (working memory, inhibitory control, the frontal apparatus).
