# PsychSim — Master Design Document (v8)

**Companion to `psychsim_substrate_seed_v14.json`. Status: the substrate is ASSEMBLED and running; the work is now completing under-built systems, and the studies the platform exists to run.**

*Version history: v1–v7 recorded the design settling and the first six assembly logs. **v8 (2026-07-15)** is the first version written against a *built and running* organism rather than an assembling one. It records: the execution of the Panksepp retirement; the receptor-sign convention (§3.7); the phasic correction to plasticity rule 5; assembly logs for the seven systems added since v7 (aggression, endowment/sex, receptor-signing, DRN + interneurons, kinship, memory, the noradrenergic system); the development pathway (§16); the governing principles as earned (§17); and the substrate's known systemic conditions (§18). **The status claim in every prior version — "design settled; assembly beginning" — was eight versions out of date and is corrected here.***

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
Every circuit is a node (nuclei/regions, transmitters) with an activation level and hard bounds. Every connection carries what the plasticity rules consume: a **default (newborn) weight** with its basis (literature / anatomy / assumption / innate-reinforcer), weight bounds, the **gating neuromodulator**, a **`dominant_receptor`** + **`dominant_receptor_basis`** (§3.7), an **age-plasticity-coefficient** reference, an **innate-reinforcer flag**, a **developmental-online age**, and a **calibration-active** flag. The exact field lists are in the seed file's `schemas`.

**As built (v14): 83 circuits · 214 connections · 9 input channels · 7 domains** — defensive threat 14 · reward & approach 12 · sensory 18 · interoception 14 · executive 10 · affiliation 6 · social cognition 4. The domains are *not* a hard partition — the whole point is that they interact — but they are how the substrate is organised.

**The weight-basis reality, stated plainly because it governs what the model may claim:** `anatomy` 114 · **`assumption` 74** · `innate_reinforcer` 19 · `literature` 1. **Over a third of connections self-declare their weight-basis as an assumption.** Weights remain *symbolic bands* (`low`/`moderate`/`moderate-strong`/`strong`), never fitted decimals — which is more honest than false precision, since no value has been threaded into a window — but the assumption-basis set is ungrounded and is what the **209-edge target-cell audit (§16.5)** exists to resolve.

### 3.2 Inputs — the body in the loop
**Nine** input channels (seed file `input_channels`): vision, audition, olfaction, gustation, somatosensation, proprioception, vestibular sense, interoception, and **`IN-CONSPEC` — the perception of *another individual***, a dedicated social channel separate from generic vision, reflecting that the brain processes persons through dedicated pathways. Exteroceptive channels carry the world (and the innate cues — looming, voice, sweet); proprioception supplies the efference-copy comparison behind agency; **interoception is the channel that makes emotion *felt*** — cardiac, respiratory, gastric, chemo/baro and humoral signals returning via NTS → parabrachial → insula/hypothalamus, closing the body↔brain loops in which affect is constituted.

**The channels are the honesty wall at the boundary:** the world cannot reach in and set a circuit. It can only present a stimulus to a sense, and what that stimulus evokes is up to the substrate — which is why two agents can respond oppositely to identical input.

### 3.3 Physical endowment — starting conditions
A normal-distributed physical draw per agent (seed file `physical_endowment`): attractiveness, size, musculature, agility, congenital health, sensory acuity, and the per-circuit temperament reactivity priors. These are **starting conditions and biases on how the world responds to the agent** — attractiveness, for instance, is a bias on *others'* reactions (and thus a driver of the future relationship matrix), not a worth judgement. They are the legitimate genetic/physical layer — explicitly *not* the "gaming-style ability dials" we rejected.

### 3.4 The plasticity engine — the eight rules
This is what makes the model *develop*. All rules are **local and meaning-blind**: they see pre- and post-synaptic activity, the current weight, an activity-derived neuromodulatory scalar, and an age coefficient — never that a circuit "is fear" or a state "is threat." (Full entries, forms, and citations in the seed file's `plasticity_rules`.)

1. **Hebbian coincidence** (Hebb 1949) — co-active connections strengthen; unstable alone, so never stands alone.
2. **Rate-level, not spike-timing** — a flagged modelling choice: our circuits carry activation levels, so STDP's timing rule can't apply literally; we use its rate-level BCM equivalent.
3. **BCM sliding threshold** (Bienenstock, Cooper & Munro 1982) — the workhorse: potentiation above a threshold, depression below, with the threshold computed from the circuit's *own* recent activity. One rule gives potentiation, depression, competition, and self-stabilisation.
4. **Homeostatic scaling** (Turrigiano 1998, 2008) — slow multiplicative renormalisation toward a set-point (`homeo_factor = 1 − rate·(mean_activity − setpoint)`, `HOMEO_RATE = 0.002`, applied every 20 steps); must out-run Hebbian growth (the "temporal paradox") — a timescale constraint, not an outcome one. **Two conditions on this rule are now known and are NOT yet resolved (§18):** *(a)* the set-point is an **ungrounded uniform 0.1 on 82 of 83 circuits** (LC alone is grounded), so any circuit whose true target rate exceeds it is persistently over-suppressed in proportion to its own activity — and we do not know which; *(b)* **`plasticity_schedule=None` does not exempt an edge from this rule** — only bounds-pinning does. "Non-plastic" currently requires two mechanisms to mean what it says.
5. **Three-factor neuromodulatory gating** (Reynolds & Wickens 2002; Frémaux & Gerstner 2016) — a dopamine/ACh/NA-like scalar multiplies a decaying eligibility trace so a coincidence consolidates only if a modulator arrives while eligible. **This is the danger point:** the modulator must be the *output of a circuit whose activation is set by its wiring*, never a value we set because we judge an outcome good or bad. This is where outcomes are most easily smuggled back in.
   **v8 correction — the gate is PHASIC, and the earlier form was wrong.** The gate now reads a *deviation*, not a *level*: `max(0, mean(source activation) − mean(source mean_activity))`. The prior absolute-level form meant a neuromodulator with any resting tone taught **continuously, at baseline, in the absence of any event** — over-consolidating everything and, worse, making a *tonic tone difference* look like a *learning difference*. This is not a refinement of rule 5 but its intended reading: the biology is that phasic bursts teach and tonic level sets gain, and the two are different signals. The correction **resolved the deferred tonic/phasic ambiguity in the dopamine gate at the same time**, since both ran through this one line. *(A residual inconsistency is registered: `reward_signal()` is still an absolute accessor while described as "the RPE" — §18.)*
6. **Developmental gating** (Knudsen 2004; Hensch 2005) — everything scaled by η(age, circuit): high early, dips, adolescent resurgence, low in adulthood. Age enters *only here*, as a rate, never as a target; it abstracts the parvalbumin/perineuronal-net critical-period machinery.
7. **Structural plasticity** (Holtmaat & Svoboda 2009; Petanjek 2011) — weights held near zero are pruned; sustained co-activation between adjacent unconnected circuits can add a connection within connectome limits. This is the "growth from stimulation," and the overproduction-then-pruning arc.
8. **Bounds and competition** (Oja 1982) — finite weight bounds and normalisation make learning necessarily competitive: strengthening some costs others. The normalisation holds total incoming drive at `target = max(1.0, len(weights) × 0.5)` — a **SCAFFOLD conserved-resource constant**. Its `0.5` is load-bearing beyond this rule: it is the **equilibrium the uniform-start diagnostic adopted as the substrate's operating point** (§16.6), chosen because it is the mechanism's own fixed point — *not* because it made anything pass.

### 3.5 Activation gating — two distinct switches
"Not active" means two different things, and they must not be conflated:
- **`developmental_online(age)`** — *biology*. A circuit comes online on its maturational schedule (brainstem/limbic before PFC). This is the natural gate encoded in the developmental parameters.
- **`calibration_active`** — *your tuning dial*. A circuit that exists and is mature can still be masked to zero this run so you can bring subsets online progressively and tune them. Masking is the activation gate set to zero — not deletion, not a hidden weight edit — and it is fully reversible.

Keeping these separate means we never mistake "not mature yet" for "switched off for calibration." Manually masking a circuit the schedule says should be online is logged as a calibration choice, not confused with biology.

### 3.6 Read-out and validation
Emotions and any Pankseppian label are computed *from* substrate activity for description only. **Validation** is where the consensus literature earns its keep: we check whether typically-developed agents *drift toward* the documented adult co-activation patterns, and whether atypical developmental histories produce atypical structure. The documented patterns are the thing we test against — never the thing we assert.

### 3.7 The receptor-sign convention — signs are derived, never written *(NEW in v8; landed v12a)*

**The single most important honesty mechanism added since v7, and it belongs in the architecture, not the assembly logs.**

Whether a connection excites or inhibits is **not a field anyone sets**. Each connection declares a `dominant_receptor` and a cited `dominant_receptor_basis`; the **sign is derived** from the receptor's coupling via the `RECEPTOR_SIGN` table (Gq/Gs → excitatory; Gi/Go, ionotropic-Cl⁻ → inhibitory). The consequence is structural rather than procedural:

> **A dishonest sign requires citing a false receptor. That is a checkable lie against the literature — not a quiet tweak.**

Three things this convention forced, each of which had to be gotten right rather than forced:

**(a) The target cell decides the net effect.** A projection's sign follows from *which cell type it lands on*, not from the source's transmitter. Oxytocin **excites CeA-lateral GABAergic interneurons**, which then inhibit CeA output — so the net effect on CeA output is inhibitory *via an excitatory synapse onto an inhibitory cell* (Knobloch et al. 2012). Signing `PVN-OT → CeA` as `+` would have asserted the opposite of the biology. The honest resolutions are to **split the target** (add the grounded interneuron) or to **defer the sign with a recorded reason** — never to force a sign that asserts a false effect. The same care produced the `vlPFC → ITC` re-target (vlPFC is glutamatergic and cannot directly inhibit LA; it routes through the GABAergic intercalated cells — Milad & Quirk 2002) and the DRN and α2A-in-PFC resolutions.

**(b) Same transmitter, opposite behavioural valence — emergent, from the target.** Vasopressin at **V1a** drives *pair-maintenance* in septum/reward regions and *territorial aggression* in BNST/threat regions. **Both are `+` from the receptor.** The valence is not in the sign and was never written: it emerges from which target the excitation reaches. This is the convention's deepest payoff — it makes a whole class of behavioural dualities fall out of anatomy.

**(c) A GABAergic source needs the real mechanism, not a sign flip.** CeA is GABAergic, so a plain excitatory `CeA → LC` edge would come out *inhibitory* — threat *lowering* noradrenaline, backwards. The honest fix is not to override the sign but to cite the mechanism the biology actually names: the **CeA-CRF → LC** projection acting on **CRF-R1**, which is Gs-coupled and therefore excitatory (Van Bockstaele). The rule that keeps this honest: **when a sign comes out wrong, the question is which real receptor mediates it — never which sign we need.**

*Receptors added since v7: OTR, V1a (Gq → +1), CRF-R1 (Gs → +1).*

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

## 6. From one brain to a social world — DELIVERED, and what replaced the plan

**Both pieces v7 held for later have been built**, and the wall held through both:

- **Two sims face to face — DONE.** The **Arena** puts saved agents in a compact social world; the **four matrices** (social, environmental, group, self-reflection) supply the experience stream. A matrix never tells an agent how to feel — it presents a *situation* as a pattern of sensory stimulation, and the agent's own substrate produces the response, which then updates the bond, the standing, the self, and so becomes the next situation. **A relationship is not a stored feeling; it is a history of encounters, each lived through the substrate.** Dyadic states remain read-outs of accumulated interaction, never allocated values.
- **Richer bodily feedback — DONE** (§14, the interoception/autonomic assembly).

**The forward plan is now the study roadmap, and it has a hard shape.** The researcher's CU §9 answers defined the study's requirements so rigorously that the study moved from the *first* task to the *last*: **v14 → v15 → the daily life-course & multi-environment capability → the psychometric observer → the 209-edge target-cell audit → the CU study → the interventions.** A CU study measuring only brain read-outs would measure a pale shadow of the construct, which is behavioural and cross-context; building it properly means building the world the child lives in first. **§16 records the full pathway, including the six-level descent the current work sits inside.**

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

## 8. What this is not, and the honest frontier *(rewritten for v8)*

- It is **not** a mind built from emotion categories; emotions are outputs.
- It is **not** a playback of documented adult patterns; those are validation targets. (The separate "circuit engine" that *does* play documented patterns back remains a knowledge inspector, walled off — its hand-authored curves must never migrate in.)
- It is **not a theory. It is a representation.** This distinction became load-bearing in v8's work and deserves stating: the substrate is a *stand-in for a brain*, and its findings are **measured off it, never built into it.** Coding a known result — even a true one — destroys the substrate's ability to test it and converts the model from an instrument into an assertion. The tell is always the same: **does this value come from the physics, or from the result we expect?**
- It is **not quantitatively grounded**, and v8 can now say exactly where the line falls:
  - **Grounded:** structure (which circuits, which connections); **signs** (derived from cited receptors, §3.7); **target cells** where the literature establishes them.
  - **Scaffold, disclosed:** weights (symbolic bands; **74 of 208 assumption-basis**); **baselines and homeostatic setpoints** (82 of 83 circuits at an ungrounded uniform 0.05/0.1 — LC is the sole grounded exception); **timescales** (near-uniform 200 ms, not the measured ionotropic ≪ metabotropic ≪ neuromodulatory hierarchy).

**The standing caveat, which governs every claim made from this substrate:**

> **Until the 209-edge target-cell audit (§16.5) is complete, "nothing in the substrate was coded for convenience" is NOT established.** It is the thing the audit will make true — or reveal the exceptions to. Every result produced before it, *including the emergent adolescent inverted-U*, is **provisional in that specific sense**: it emerged from a mostly-grounded substrate, not an audited one. The inverted-U is probably still real (it fell out of interneuron anatomy, which *is* grounded) — but "probably" is the honest word until the audit confirms the edges it depends on. **The audit is what upgrades every prior result to the standard the thesis needs.**

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


---

## 10. Assembly log — second system (reward / approach)

Reward/approach is populated next — the dopaminergic mirror of threat; the two pair as the **approach/avoid core** of motivation. Written into the data doc (`psychsim_substrate_seed_v3.json`) at the same nucleus grain. **Twelve circuits, twenty-four connections.**

**Value enters only through cited anatomy — again.** Six appetitive routes, each a catalogue entry: sweet → NAc-shell *and* → VTA (`PR-SWEET`, the dual "liking" + "wanting" entry), umami → NAc-shell (`PR-UMAMI`), affective touch → NAc-shell (`PR-CONTACT`), warmth → NAc-shell (`PR-THERMAL`), and nutritive/energy state → lateral hypothalamus (`PR-HOMEOSTATIC`). The mesolimbic backbone (VTA → NAc → VP) is plain anatomy; the cue → value associative sites (sensory → OFC, amygdala → NAc) start weak and are grown only by experience.

**The dopamine gate mirrors the noradrenaline gate.** Where LC-noradrenaline gates threat plasticity, **VTA-dopamine gates approach plasticity** (rule R5): the reward-prediction-error signal is what consolidates which coincidences survive. This falls straight out of the same three-factor rule — no new machinery, just a different modulator that is itself a circuit output.

**The negative arm is structural, not authored.** The lateral-habenula → RMTg → VTA route suppresses dopamine on worse-than-expected outcomes, so **disappointment / reward-omission is produced by the wiring**, exactly as reward is — there is no "disappointment rule."

**Shared substrate, not silos.** Reward reuses threat-system circuits: the basal amygdala (`BA`) and ventral hippocampus (`HPCv`) supply appetitive cue-value and contextual-reward inputs to the accumbens, and mesocortical dopamine reaches the same `vmPFC` node that drives extinction in the threat system. The amygdala, hippocampus and vmPFC are genuinely **bivalent** — the model reflects that rather than duplicating them, which is the first sign the two systems compose rather than sit side by side.

**An emergent developmental signature — noted, not authored.** The dopamine system carries a heightened adolescent plasticity schedule (peak striatal dopamine, then pruning) while OFC/vmPFC valuation and control mature late. So the substrate should show **strong reward learning with weak top-down valuation in adolescence** — heightened reward- and sensation-seeking — as a consequence of the timing entered: the reward-side counterpart of threat's "sticky early fear, late control." And because approach and avoid now coexist, **approach/avoid conflict** becomes possible as an emergent balance between the two systems' outputs, rather than anything scripted.

**Honest gaps for this system** (register): as with threat, newborn weights are qualitative assumptions except the six cited innate links; the dopaminergic developmental schedule (`da_system_high_adolescent_peak`) and the others remain qualitative labels, not quantified curves; and the hedonic-hotspot micro-organisation of NAc-shell / ventral pallidum and the habenular input circuitry are simplified.

**Next.** Sensory input — the channels that feed both systems (vision, audition, somatosensation, and the rest) — then the executive suite (working memory, inhibitory control, the frontal apparatus).


---

## 11. Assembly log — third system (sensory input)

Sensory input is populated next — the channels that feed *both* the threat and reward systems (and everything to come). Written into the data doc (`psychsim_substrate_seed_v4.json`) at the same grain. **Eighteen circuits, thirty-two connections**, across six modalities: visual (retina → LGN → V1 → ventral/dorsal streams), auditory (cochlea → brainstem → MGN → A1/belt), somatosensory (ascending relay → VPL → S1 → S2/parietal), olfactory (bulb → piriform, bypassing thalamus), gustatory (NTS → gustatory cortex), and vestibular. The superior-colliculus/pulvinar and startle nodes from the threat system are reused, not duplicated.

**This system is mostly value-neutral — and that is the point.** Sensory circuits are processing hierarchies that carry *no* innate value; populating them cleanly shows the schema handles pure relays as happily as it handles motivated systems. Value enters only at the cited links, and this pass places the ones that belong to perception:

- **The remaining prepared perceptual biases.** Face-like/top-heavy input and biological motion drive subcortical orienting (superior colliculus/pulvinar) — `PB-FACE`, `PB-BIOMOTION` — with the honest caveat carried in the data that the face bias may be a *non-specific* top-heavy/high-contrast bias, and that cortical face specialisation (the fusiform area in the ventral stream) is **experience-built, not innate**. Voice/infant-directed-speech preference (`PB-VOICE`) is flagged as **partly prenatal-learned** (mother's voice learned in utero), not purely innate. The sensory limb of the acoustic startle arc (cochlea → StN) completes `PB-STARTLE`.
- **The aversive taste reinforcers.** Bitter and sour → the central amygdala (`PR-BITTER`, `PR-SOUR`), completing the taste set — sweet and umami went to reward, bitter and sour go to aversion, exactly as the catalogue specifies.

**Discriminative pain stays separate from affective pain.** The nociceptive route into the sensory system — nociception → VPL → S1 — carries *where and how much*, and is flagged as **sensory, not value**. The aversive *value* of pain lives in the threat system (nociception → amygdala). Keeping the discriminative and affective streams apart is the honesty discipline applied to a sensory case: the sensory system knows a pinprick's location without the model having decided it is bad.

**The placeholders are resolved.** The generic `sensory_thalamus` / `sensory_cortex` sources used when threat and reward were built are now given concrete modality-specific pathways (e.g. ventral-stream → amygdala for a detailed visual cue, ventral-stream → OFC for cue-value, auditory belt → amygdala). The earlier generic connections are left untouched, not rewritten — the concrete routes simply sit alongside them.

**A developmental note — structural, not authored.** The sensory hierarchies carry experience-expectant critical periods (vision/ocular-dominance to roughly 7–8 years; native-phoneme tuning in the first year), so they are shaped by early input, and deprivation in the window yields lasting deficits — a direct expression of the plasticity rules under the developmental schedule. And because the innate subcortical detectors (looming, face-like, biological motion, voice) are present at birth and bias *what the developing cortex is exposed to*, cortical specialisation such as the fusiform face area should **emerge from the innate orienting bias plus experience** rather than being wired in. That is the intended shape — cited innate structure seeding experience-driven specialisation — not a tuned result.

**Honest gaps for this system** (register): newborn weights are qualitative assumptions except the cited innate links; the many new plasticity schedules (`visual_cp_early`, `auditory_phoneme_first_year`, …) are qualitative labels, not quantified curves; sub-modality detail (retinal cell types, cochlear tonotopy, S1 submodalities) is compressed to the area level; and multisensory integration and the thalamic reticular gating are not yet represented.

**Next.** The executive suite — working memory, inhibitory control, and the frontal apparatus — which is where top-down regulation of both threat and reward will finally have a home.


---

## 12. Assembly log — fourth system (executive suite)

The executive suite is populated next — working memory, inhibitory control, and the frontal apparatus — and it is the **capstone**, because its job is to *regulate* the affective and sensory systems already built, and because it is the last thing to mature. Written into the data doc (`psychsim_substrate_seed_v5.json`) at the same grain. **Ten circuits, twenty-four connections** (dlPFC, vlPFC, dACC, frontopolar cortex, pre-SMA, frontal eye fields, mediodorsal thalamus, subthalamic nucleus, associative caudate, basal-forebrain cholinergic system), reusing the existing frontal nodes (vmPFC, dmPFC, OFC) rather than duplicating them.

**Zero new innate value — and that is the honest, expected result.** For the first time, a whole system is added with **no innate-reinforcer links at all**. That is correct: the executive apparatus is the least innate, most experience-dependent, latest-maturing part of the brain (frontopolar cortex comes online around twelve and matures into the twenties and beyond). Nothing here is seeded with value; everything here is built by experience and, above all, exists to *control* what the older systems do.

**What the executive suite is, mechanistically, is regulation.** Its connections fall into four groups:

- **Working memory** — a thalamo-cortical maintenance loop (dlPFC ↔ mediodorsal thalamus), a fronto-parietal loop that *reuses the sensory parietal node* (dlPFC ↔ S2/posterior-parietal), and dopamine-gated input gating through the associative caudate (dlPFC → caudate, deciding update-versus-maintain).
- **Inhibition / stopping** — the hyperdirect route (vlPFC and pre-SMA → subthalamic nucleus) braking basal-ganglia output.
- **Top-down regulation of affect** — the integrative core: dlPFC → vmPFC and vlPFC → amygdala *down-regulate threat* (reappraisal, on top of the extinction route already present); dlPFC → accumbens and OFC → dlPFC *control approach and impulse*.
- **Top-down attention** — frontal eye fields → superior colliculus and dorsal visual stream.

**The same modulators now tune cortex across systems.** Mesocortical dopamine (D1 inverted-U), locus-coeruleus noradrenaline (α2A; stress-level release impairs the PFC), and basal-forebrain acetylcholine (attentional gain) all reach dlPFC — and the cholinergic system also tunes sensory cortex. So the very modulators that gate affective and sensory learning also gate executive learning: one gating mechanism, applied everywhere, exactly as rule R5 intends.

**The capstone developmental signature — the thing this system finally makes coherent.** The affective and sensory systems are online and highly plastic *early*; the executive suite is online-but-weak early and matures *last*. So top-down regulation of threat (reappraisal, extinction) and of reward (impulse control, stopping) is **structurally weak in childhood and adolescence and strengthens into adulthood** — not because anything was tuned to make it so, but because that is the maturational asymmetry entered into the developmental schedule. This is what retrospectively explains the earlier notes: "sticky early fear, late control" and "adolescent reward-seeking" are the same phenomenon seen from the threat and reward sides — an early, plastic, expressive affective brain running ahead of a late-arriving regulator. Whether self-regulation actually *emerges* in the running model, and how chaotically it does so early on, is for the simulation to show; it is not authored here.

**Integration, not a fourth silo.** With this system the four now compose: the executive suite borrows the sensory parietal node for working memory, takes value from OFC and context from the ventral hippocampus, regulates the amygdala and accumbens directly, and is tuned by the same VTA/LC/basal-forebrain modulators that gate affective and sensory plasticity. The bivalent nodes (amygdala, hippocampus, vmPFC) already stitched threat to reward; the executive suite now stitches control across all of it.

**Honest gaps for this system** (register): newborn weights are qualitative assumptions throughout (the executive suite has essentially no confidently non-zero birth weights — it is nearly all built by experience); GPi/SNr basal-ganglia output nuclei are not yet built, so the subthalamic "stop" is routed to the available ventral-pallidal proxy; and the frontal white-matter tracts (which carry these routes) are represented only implicitly as connections.

**Next.** Several systems remain and can come in any order: affiliation/social (the CARE / separation-distress / play substrates — needed before two agents can build a relationship), interoception and the autonomic loops (the felt-body side of emotion), episodic memory (hippocampal, beyond the contextual role it already plays), and motor output (which would let the basal-ganglia and cerebellar loops close). To be chosen.


---

## 13. Assembly log — fifth system (affiliation / social)

Affiliation/social is populated next — the bonding, care, separation-distress and social-recognition substrates — because it is the prerequisite for the two-agent relationship matrix on the horizon, and it completes the affective core beside threat and reward. Written into the data doc (`psychsim_substrate_seed_v6.json`). **Six nuclei, nineteen connections** (hypothalamic oxytocin/vasopressin neurons, medial preoptic CARE hub, medial amygdala, septum, a separation-distress PAG column, and ventromedial hypothalamus), working mostly through new connections onto existing nodes rather than as a new box.

**The strongest honesty caveat of any system so far — carried in the data, not buried.** The oxytocin/affiliation literature is robust in animals (vole pair-bonding) but **weak and inconsistent in humans** — intranasal-oxytocin effects largely fail to replicate. So every affiliation circuit and connection is tagged `confidence: Em` and `evidence_base: animal_dominant`, with the caveat written into each `source` string. Any conclusion that leans on this system should be treated with the most caution of anything built so far; where the anatomy is human-known the *social-bonding function* attributed to it is largely animal-derived, and the data says so.

**Affiliation is distributed and modulatory, not a silo.** It adds only six nuclei but many connections, because it works *through* the existing substrate: oxytocin broadcasts to the accumbens (making social contact rewarding), to the central amygdala (damping threat — affiliation buffers stress), and to the septum, BNST and preoptic area; the CARE hub drives the VTA (parental approach); separation-distress runs through a distinct periaqueductal column; and social recognition reuses the olfactory (piriform → medial amygdala, e.g. mother-odour learning) and visual (ventral-stream → medial amygdala) inputs already built.

**Oxytocin becomes a fifth gating modulator.** Alongside dopamine (reward), noradrenaline (threat/arousal), and acetylcholine (attention), **oxytocin now gates plasticity for *social* stimuli** under the same three-factor rule (R5) — and, exactly as with the others, it is the output of a circuit (the oxytocin neurons), never a value we set. So "social learning" needs no special mechanism; it is the general rule with a social modulator.

**One innate seed only — and it is the distress side, framed honestly.** The single innate link added is *contact-loss → separation-distress*: the infant cry/protest is unlearned and cross-species (Panksepp), so it is admitted as innate **wiring** (loss of caregiver contact drives the distress output), *not* as a "separation is bad" rule. The positive side — that contact is rewarding — was already placed as `PR-CONTACT` → accumbens in the reward system. Everything else in affiliation (bonding, care, sexual behaviour) is hormone-gated and experience-built, not birth-value, which is why the CARE and LUST connections carry no innate flag and are gated by parturition or pubertal steroids.

**Why this is the substrate the relationship matrix will grow from.** Bonding (oxytocin → accumbens), care (preoptic → VTA), separation-distress (the PANIC column), and social recognition (medial amygdala) are the *per-agent* machinery. When two agents are eventually placed together, the history of each agent's responses to the other — soothing on contact, distress on separation, reward on reunion — will accrue into named dyadic states (trust, affection, and longer-run love/hate). As with every read-out in this model, those states will be **emergent from accumulated interaction, never allocated**.

**Honest gaps for this system** (register): as noted, the whole system is animal-dominant/`Em`; PLAY (Panksepp) is only gestured at (periaqueductal/thalamic with opioid/endocannabinoid modulation) and a dedicated circuit is deferred as the catalogue flags it mostly-animal/hypothesised in humans; human social-chemosignalling is treated via main olfaction because the vomeronasal organ is vestigial; and the specific human oxytocin-receptor distribution that would set these weights is not established.

**Next.** Interoception and the autonomic loops (the felt-body side of emotion — arguably the next most useful, since it closes the body↔brain feedback that makes emotion *felt* and that the relationship matrix will also draw on), episodic memory, or motor output. To be chosen.


---

## 14. Assembly log — sixth system (interoception & the autonomic loops)

Interoception and the autonomic loops are populated next — the **felt-body substrate**, and the system that closes the body↔brain feedback the whole model turns on. Written into the data doc (`psychsim_substrate_seed_v7.json`). **Fourteen circuits, thirty-four connections.**

**The system is a closed loop, in two limbs.** The **ascending (afferent) limb** carries bodily state to the brain: visceral and vagal afferents (and the lamina-I spinothalamic pain/thermal/visceral limb) → nucleus tractus solitarius → parabrachial nucleus → interoceptive thalamus (VMpo) → **posterior insula** (primary interoceptive cortex) → **mid** → **anterior insula**. Following Craig, that posterior-to-anterior sequence is an "increasingly homeostatically efficient" re-representation whose anterior pole is the meta-representation of the body — the "material me," the seat of subjective feeling and emotional awareness. The **descending (efferent) limb** carries control back to the body: the central autonomic network (amygdala, hypothalamus, mPFC, cingulate) converges on the **hypothalamic PVN** and brainstem, driving **RVLM → intermediolateral column → sympathetic ganglia/adrenal medulla** (fight-flight) and **nucleus ambiguus / dorsal motor nucleus of vagus** (the parasympathetic, cardiac and visceral, brake). The loop closes because efferent output changes organ state, which re-enters through the afferent limb — and because the anterior insula itself projects back onto the brainstem autonomic nuclei (the corticofugal von-Economo loop).

**This is where emotion is felt.** The connection that matters conceptually is anterior insula → dorsal cingulate / amygdala / OFC: Craig's limbic-*sensory* insula feeding the limbic-*motor* cingulate, i.e. the point at which bodily state becomes felt affect. This is the loop the project has been oriented around from the start, and it is the per-agent machinery the future two-agent relationship matrix will draw on — trust, affection and their opposites will accrue from dyadic interoceptive and autonomic responses to another person, not from allocated values.

**The slow arm: HPA, closing with feedback.** The neuroendocrine loop — PVN CRH → pituitary ACTH → adrenal cortisol — is included because it is a genuine body↔brain feedback loop, and it closes: cortisol feeds back via glucocorticoid receptors in the hippocampus (and PFC and PVN itself) to dampen its own drive. That negative feedback is represented structurally, not as a rule.

**One innate alarm — an interior threat cue.** The single innate link added is CO₂/acidosis → amygdala: the amygdala directly chemosenses a fall in brain pH (via ASIC1a) and triggers unconditioned fear/panic and sympathetic fight-flight (Ziemann et al., 2009; Klein's false-suffocation-alarm; the human ACCN2/panic association). This is a documented, unlearned **interior** threat — the interoceptive counterpart of exterior cues such as looming — and it references the catalogue's air-hunger term under `PR-HOMEOSTATIC`. The positive homeostatic values (satiety, warmth) were placed earlier via `PR-HOMEOSTATIC` and `PR-THERMAL`, so interoception adds value at exactly one honest point.

**Honesty posture.** The ascending afferent anatomy, the insular hierarchy, and the autonomic efferent anatomy are all `E` (human + animal, textbook-stable). The **descending predictive/allostatic framing** — that the anterior insula *issues interoceptive predictions* corrected by ascending prediction errors (Barrett & Simmons; Seth) — is theoretically influential but carries limited direct causal human evidence, and is tagged `Em`. **Polyvagal theory is not used**: its core physiological premises are widely regarded as refuted, and the model uses the standard two-branch autonomic organisation with Benarroch's central autonomic network.

**Honest gaps for this system** (register): medullary/retrotrapezoid respiratory chemoreceptors (the reflexive breathing response to CO₂, distinct from the amygdala fear response), the enteric nervous system, the baroreflex interneurons (CVLM), and organ-level state are compressed or deferred; and glucocorticoid effects on the amygdala are complex rather than simply inhibitory and are left qualitative.

**Next.** Episodic memory (hippocampal, beyond the contextual role it already plays) or motor output (which would close the basal-ganglia and cerebellar loops); then the two-agent relationship matrix, for which the felt-body loops built here are the prerequisite.

---

## 15. Assembly log — the systems added since v7 (seeds v9 → v14)

v7 closed with six systems assembled. What follows is the record of the seventh system and of the six *mechanisms* added after assembly proper ended — the point at which the work stopped being "populate the catalogue" and became "make the machine honest."

### 15.1 Seventh system — social cognition; and aggression (seed v9)
The social-cognition domain (4 circuits — rSMG-TPJ, dmPFC, pSTS, PCun-PCC) completes the seven-domain structure. **Aggression** was added as the v9 keystone and is worth recording because of what its acceptance test proved. `VMHvl` — the hypothalamic attack area — was wired **as the anatomy dictates**: provocation reaches it, a prefrontal brake and the executive can hold it below threshold, and the outcome is *measured*:
- under genuine provocation, aggression crosses threshold and emerges;
- under a plain non-social threat, the agent avoids rather than attacks;
- **with no provocation at all, the agent restrains.**

**That last check is the load-bearing one — the "neutral floor."** If aggression leaked out of a neutral situation, it would mean aggression had been coded as a standing tendency rather than earned by the situation. The floor holding is how the substrate proves it did not smuggle the answer in. **This is the pattern every later keystone copies.** Note also what the v9 wiring made structurally true, because it constrained a later decision: **`CeA → PAG` and `CeA → HYPdm` are inhibitory**, so damping CeA *disinhibits* attack (§15.7c).

### 15.2 Physical endowment and sex (seed v10) — the bearer-property pattern
The endowment layer landed with a pattern that became a template: **a trait is a *stimulus the bearer presents*, not a force acting on the perceiver.** `physical_stimulus` presents a bearer-pure cue on `IN-CONSPEC`; the response emerges from the *perceiver's own* circuits via `felt_response`. Attractiveness is not a worth-value — it is a cue that other agents' substrates respond to, and thus a driver of their behaviour toward the bearer. **Every later social property (the kinship signature, the distress display) is built on this pattern**, and it is why they are honest.

### 15.3 The receptor-sign convention (seed v12a) — see §3.7
Recorded in the architecture rather than here, because it is not a system: it changed how *every* connection in the substrate declares itself.

### 15.4 DRN and the cortical inhibitory interneurons (seed v13)
The serotonergic node and the cortical interneuron populations. Their significance is that they were the first case where **the honest representation required splitting a node** rather than signing an edge — the same requirement that later produced `CeA-GABA` and the `vlPFC → ITC` re-target. **The emergent adolescent inverted-U falls out of this interneuron anatomy** — which is why it is the platform's credibility highlight, and also why the §8 caveat matters: it emerged from grounded structure, but the audit has not yet certified every edge it rides on.

### 15.5 Kinship and attachment (seed v14) — Phases 1, 1.1, 2 of 5

**The keystone, and the acceptance gate on every phase:**
> **Relatedness is an upstream spawn-time FACT that sets *cue similarity* — nothing more. Every bond — its strength, its fractiousness, its dissolution — EMERGES from the perceiver's own recognition and reward circuits. A bond is measured, never set.**
No line may map relatedness → bond or any family variable → an outcome. **Grep-clean is a per-phase gate.**

**Phase 1 + 1.1 — the OT/VP bonding pathway.** Ten existing `PVN-OT`/`MPOA` projections were given receptor-honest signs (OTR/V1a → Gq → `+`, each cited). The core is `PVN-OT → NAc-shell` via **OTR** — oxytocin drives social reward (Dölen et al. 2013). **The sign makes a conspecific's cues *rewardable*, not bonded: a bond still requires repeated interaction.** That is the Phase-1 form of "earned, not coded." The **vasopressin duality** (§3.7b) and the **CeA target-cell subtlety** (§3.7a) both landed here.

**Phase 2 — the signature is a VECTOR, and this was a keystone ruling, not a preference.** Each agent carries a multi-locus signature (the MHC/scent analogue); relatedness sets the *shared-locus fraction*; the perceiver computes component-wise overlap **against its own self-signature** (self-referent matching, routed `MeA → aIns`/`dmPFC`). **Nepotism emerged.**

*Why the scalar alternative was inadmissible — the sharpest statement of the wall in the whole project:* to produce a scalar similarity, something must compute `relatedness → a number` and hand that number to the perceiver. **That computation is the forbidden step.** The perceiver would be responding to a similarity *calculated for it from relatedness*, not one it perceived — the mechanism containing the answer, with one layer of indirection. The vector keeps relatedness genuinely upstream: it sets which *loci* two agents share (a bearer fact, §15.2), and the perceiver's own circuits derive the similarity. **The scalar smuggles; the vector doesn't.** Post-spawn, relatedness appears in **no** computation.

And the mechanism's elegance is the biology's: **no agent needs to know "this is my offspring."** A parent perceives a cue that partially matches *itself*, and affiliation emerges. The same self-referent match yields incest-aversion for free — "too much like me" is the Westermarck signal.

**Phases 3–5 — OPEN** (§16.2). **The three emergence tests — REQUIRED, and they need Phases 2+3 both present**, because Phase 2 establishes the cue-similarity channel and Phase 3 the co-rearing channel; only with both can the tests separate them: ① co-rearing UNRELATED agents → a bond forms; ② relatedness WITHOUT co-rearing → NO bond; ③ incest-aversion emerges from co-rearing regardless of relatedness. **If a bond ever appears from relatedness alone, the keystone is violated — stop.**

### 15.6 Memory — Phase 1
Unified to **one sub-symbolic substrate**; the symbolic MemoryStream overlay retired. Deliberately unlike Park's generative-agents architecture, which stores retrievable symbolic events with recency/importance/relevance weighting. Here a memory is not an item to be retrieved — it is a change in the substrate.

**The PFC↔memory presentation loop is mechanism-live but CLOSURE-BLOCKED.** `vlPFC → LA` was re-targeted to **`vlPFC → ITC`** (§3.7a). Closure requires a **learned control-disposition** to present — which did not exist, and which forced the descent into the learning pathways.

**★ The layer's actual purpose is NOT BUILT** (§16.3): beliefs, attitudes and opinions held with variable strength and accessibility, controlling behaviour through the executive and forming the personality — **where rules, law-obedience, morality, ethics and the higher emotions evolve**, with heterogeneous origins (innate, experiential, *reasoned*, and brainstem-survival-linked). This is the crux of the sophropathy/CU work and it remains ahead.

### 15.7 The noradrenergic system — the LC arc
Entered because vicarious aversive learning needs an NA teaching signal, and **`LC` had ZERO afferents: a neuromodulator hub wired to distribute but never driven. Structurally dead — exactly the `PVN-OT` pattern before it.** Each step below is a real grounded mechanism; none was forced.

**(a) `CeA → LC` via CRF-R1** — the GABAergic-source problem and its honest fix (§3.7c).
**(b) The teaching signal is PHASIC** — rule 5's correction (§3.4). Making it phasic exposed the systemic finding that **LC *and* BF-ACh were both unafferented**; scope was ruled to complete LC (on the critical path) and **register BF-ACh** (26 edges, off it) — the PVN-OT precedent: complete the hub the work needs, register the rest.
**(c) `CeA → LC` is a PHASIC/adapting drive.** A CeA↔LC latch appeared. The reviewer's proposed fix — strong α2 plus CeA self-inhibition — was **falsified by the build session with clean data**: CeA self-inhibition is tonic, and because `CeA → PAG`/`HYPdm` are **inhibitory** (§15.1), damping CeA *disinhibits attack* and **breaks the v9 aggression keystone**. The reviewer's error, named: *proposing a tonic brake to fix a latch caused by a tonic drive.* The real fix — grounded in the fact that **CRF release is phasic and adapts, it does not clamp** — dissolves the latch **at its source, regardless of α2**, leaves baseline and acute CeA untouched, and preserves the keystone.
**(d) The α2 autoreceptor (`LC → LC`)** is **non-plastic** — an autoreceptor is a *structural element*, not a learned association; making it plastic was a category error — and **bounds-pinned**, at its grounded value, **verified not load-bearing**.
**(e) `LC` is an autonomous pacemaker**, baseline **0.15**, grounded in electrophysiology (Aston-Jones & Cohen 2005), **not** selected from the window where tests pass — *a non-resolving grounded value is a finding, not a tune.*
**(f) The setpoint is PAIRED to the baseline.** Reviewing against the remote caught baseline 0.15 against setpoint 0.1 — an **unsatisfiable homeostatic pressure**. The erosion was **event-driven, not rest-driven**: α2 pulls LC to setpoint at rest, but LC firing on aversive events lifts `mean_activity` and erodes `CeA → LC` by −7.4% per 60k steps. **The implication is the thing worth recording: the more threat an agent experienced, the more its threat-learning eroded — which would have silently biased the core warm-vs-harsh comparison the whole thesis rests on.**

**★ The headline: the CU punishment "signature" was a DOUBLY-CONFOUNDED ARTIFACT.** It first appeared as a large graded deficit — read through a *tonic-NA-confounded teaching signal* **and** a *tonic-NA-confounded measurement*: the read-out summed CeA/PAG/BA, and **LC projects directly into CeA and BA**, so it could never be tone-invariant *by construction*. It was only ever valid while LC was dead. On the cleaned mechanism, with a **yoked-unpaired control read-out validated tone-invariant to ±0.0000** (the reviewer's own CS+/CS− proposal was tried first and **failed**, showing +0.136 with nothing learned): **every throttle learns; there is no CU-style failure-to-learn; "weak, not a failure" HOLDS. The robust CU signature is the reads-but-doesn't-feel dissociation — not the punishment deficit.** *It was caught precisely because it looked like the finding we most wanted.*

### 15.8 Vicarious learning — routing
Substantially **emergent** once NA was live. `_add_consequence_percept` presents **the bearer's own evoked distress** (its defensive population above its own running baseline — bearer-pure and phasic, §15.2) through the existing `vulnerable_other` trigger → `IN-VIS:biological_motion` → `SC-Pv` → `CeA` → `LC` → phasic NA → the NA-gated control edges.

**`vicarious < direct` EMERGED UNCODED** (NA 0.127 vs 0.208). The reduction was **not** a gain term and **not** a chosen cue intensity — either would be the finding coded in, one step removed. It came from the **structural difference the biology names**: direct pain engages CeA **and** VPL/S1/S2; observed distress engages the affective route only — the vicarious-pain dissociation. The magnitude then fell out of the transduction chain: the bearer's display (0.472) is sub-maximal relative to the noxious stimulus (0.9) that caused it. **Nothing chose that number.**

**A construct-validity discovery landed here and it is the most important methodological finding in v8's work.** `AFFECTIVE_EMPATHY = (LA, BA, CeA, MeA, aIns)` **contains CeA — which is LC's sole afferent.** So "low affective empathy impairs vicarious learning" is **true by construction**: throttling the set throttles the mechanism's own input node. **This is a different failure from result-aiming.** "No result is a target" protects against *aiming at* an answer; it does **not** protect against an experiment that **cannot answer**. The set also contains the aggression source and the threat hub, and it is the CU study's **primary instrument** — so a full throttle-set audit is now a required gate (§16, §18).

### 15.9 Emotional expression — THE GAP (nothing built)
`_DISTRESS_DISPLAY = ("CeA","PAG","BA")` — **affective circuits, not effectors. The felt state is read and called the shown state.** Therefore **an agent cannot show what it does not feel, nor hide what it does** — which forbids voluntary suppression, learned display rules, expressivity variation, developmental change, **and displays-without-feeling: the manipulation/mimicry half of psychopathy. The model structurally forbids a phenomenon the thesis is about.**

The literature says expression is **not a read-out in the brain either**: two anatomically separate descending systems converge on the same effectors — **involuntary/emotional** (limbic → extrapyramidal) and **voluntary/volitional** (motor cortex → pyramidal) — **doubly dissociable in patients**. **PAG is the expression hub**, controlled by **two descending pathways: an *emotional* system exerting *excitatory* control, and a *volitional* system from lateral premotor cortex that *suppresses*.** **Pathological laughing/crying is what happens when the suppressor is lost — which is precisely the agent we have built.** Display rules are **learned** (modelling, correction, reinforcement) and **audience-dependent**; the developmental trajectory runs from the newborn who cries uncontrollably to the school-age child who *can control its expression to others*, driven by protracted PFC maturation **and** experience, with amygdala–mPFC connectivity **flipping from positive to negative** across childhood.

**The payoff, and the reason this is on the critical path:** the psychopathy expression profile *is* a dual-pathway dissociation — involuntary blunted (shallow affect, reduced mimicry, reduced contagious yawning), volitional intact and used strategically (increased deceptive expression). **Build the two pathways faithfully and the signature should EMERGE. We would not code "psychopaths fake emotion."**

**Present and unused:** `PAG` · **`PAG-PANIC` — in-seed as *"the infant-cry/protest output"*** · `SympOut` · `IML` · `preSMA` (*"motor inhibition interface"*) · the dlPFC/vlPFC/dACC regulation network · the social matrix for audience · the learning pathways by which display rules are acquired.

---

## 16. The development pathway

*(Live detail: `PsychSim_Return_Path_Register.md` — the authority on where we are.)*

**16.1 The spine.** The CU §9 answers defined the study's requirements so rigorously that the study moved from first task to last: **v14 → v15 → daily life-course & multi-environment → psychometric observer → the 209-edge audit → the CU study → the interventions.**

**16.2 The family module.** v14 Phases 1/1.1/2 done; **3–5 open**; the three emergence tests pending Phase 3. **The family needs no special machinery.** The research finding is that shared family environment explains remarkably little personality variance and that family power is **structural — proximity, duration, interaction density** — with non-shared experience driving divergence. The researcher's framing: *a family is a hothouse of development — and the **Arena already is one**.*

**16.3 Dominance hierarchy — PAUSED.** Diagnostic: **17 of 18 hierarchy circuits already present**; the hothouse and the agonistic interactions already exist; **the only genuinely-missing piece is rank as a learned quantity.** The PFC override pathway exists but is thin (`dmPFC → LA` still unsigned/fallback) and has no rank signal to regulate. **Two questions unanswered:** (Q1) rank as **emergent circuit-tuning from agonistic history** rather than a bookkept `status: 0.7` tally? (Q2) override in the same pass, or rank first? **Paused because rank is a *belief* — an instance of §15.6's layer, which must exist first.**

**16.4 The descent.** v14 Phase 3 → the family-psychology dive → dominance hierarchy → **the representational layer** → learning pathways → **the LC arc** → vicarious → **expression (current)**. Each level was entered because a diagnostic found the level below load-bearing. **The cascade returns to v14 Phase 3, which is where it started.**

**16.5 The 209-edge target-cell audit — a MANDATORY pre-study gate.** **Dual**: build session and reviewer audit independently against the remote and reconcile — *an audit for fitting cannot be certified by the entity that may have fitted.* Per edge: is the **target cell** cited? does the sign follow? Classification: **GROUNDED / WRONG-TARGET / MISSING-ELEMENT / UNGROUNDED-BUT-UNRESOLVED.** That last is the honest release valve — **an edge marked "target-cell unresolved in the literature" is a documented limitation; only a *hidden* guess is a fudge. The audit converts hidden guesses into either grounded edges or disclosed uncertainties.** Output = a permanent per-edge grounding record, **which IS the first rigorous pass of the anatomical reference document** — you cannot write a referenced account of every circuit and edge without establishing each edge's grounding, so they are the same work. *Expect corrections. If it returns "all 209 perfectly grounded," the audit was not strict enough.*

**16.6 Side branches — not the spine.** **HSO (Homeostatic Self-Organization)** — a full cross-homeostatic architecture, proposed for a problem **§4 and the three weight categories had already solved**; audited (machinery present-but-hollow), M3 spec'd, then **rethought and shelved**. Replaced by **uniform-start (0.5 = the rule-8 normalisation equilibrium) + the existing plasticity**, with the learning-discrimination caveat resolved by a **grounded innate reward-pathway strength** — *not* by moving the operating point to where tests pass. **The distinction is the whole discipline: a value with an external justification whose effect on learning is a downstream consequence is honest; a value whose only justification is "it makes the test pass" is a fudge.** **Episodic memory / plug-and-play** — feasibility and inertness *proven*; **deferred as a future parallel version** for cross-system comparison; unsolved part: the population→rate lossy readout. **Deliverables** (System Overview, Technical Spec, Deck, Arena UI, scan controller) — done, off-spine.
**The test that separates a branch from the spine: can the level above be built without it? HSO — yes. The LC arc — no.**

---

## 17. The governing principles, as earned

*§2 and §4 state the design's premises. These twelve were **learned** — each from a case where the project nearly got it wrong. They were recorded nowhere authoritative before v8.*

1. **Instability = a MISSING PATHWAY, not a wrong weight.** Research the missing element, add it cited. Never rebalance, never cut. Positive-feedback saturation almost always means a missing inhibitory element.
2. **When a value is load-bearing for a functional result, the arbitrariness is in a mechanism the value compensates for. Trace the mechanism; do not tune the value.** *(The α2 latch: the strong-α2 requirement was the tell that the drive was unphysiologically tonic.)*
3. **No result is a target — BOTH ways.** Don't aim at a wanted result; **and don't ACCEPT a wanted-looking result that a mechanism artifact might have produced.** Cleaning a mechanism can only strengthen a real finding or dissolve a false one — either way the answer becomes trustworthy.
4. **Construct validity is a SEPARATE check.** Principle 3 protects against *aiming at* an answer; it does **not** protect against an experiment that **cannot answer**. Before any throttle or lesion claim: **verify the manipulation set does not contain the mechanism's own nodes.**
5. **The model is a REPRESENTATION, not a theory. Findings are MEASURED, never built in.** *The tell: does the value come from the physics, or from the result we expect?*
6. **No grounded values into a partial assembly.** The system is *expected* to be unstable until all real components are present; then go to the research. **Ground a value only where it is groundable in isolation** — LC's pacemaker rate: yes (intrinsic, citable). CeA's operating point: no (afferent-driven — a property of an unfinished system).
7. **Diagnose against the actual code FIRST, surface, then build.** It has caught a wrong premise every time.
8. **Integrate, don't bolt on. Register co-revealed gaps; don't bundle them.** Complete the hub the current work needs; register the rest against the phase that owns it.
9. **The design document is the authority — return to it.** §4's three weight categories had already answered HSO. **This only works if the document is true, which is why v8 exists.**
10. **Paired values describe one quantity and must be set together.** Baseline and homeostatic setpoint are a circuit's intrinsic target rate; setting one alone made the homeostat fight the pacemaker. A grounded deviation must be **listed, cited, and paired** — enforced by test, verified by injection.
11. **A committed test that pins current state is not a design guard — and re-expressing one must preserve what it actually protected**, not merely what it literally asserted.
12. **The two-role split is itself an honesty mechanism, and the reviewer is not always right.** The build session has falsified reviewer rulings with clean data repeatedly — the A+B latch fix (broke the aggression keystone), the CS+/CS− read-out (failed tone-invariance), the erosion mechanism (event- not rest-driven). **Each time the corrected version was more faithful *and* more minimal.** The split works because neither role can certify itself.

---

## 18. Known systemic conditions of the substrate

Not bugs — **properties of a substrate assembled iteratively**, each discovered by exercising it. Recorded so they are not re-discovered.

1. **Unafferented hubs.** A neuromodulator hub can be wired to *distribute* while never being *driven* — inert, and invisible until something exercises it. **Found and fixed: `PVN-OT`, `LC`. Outstanding: `BF-ACh` (26 edges — the cholinergic attention/social-cognition system, entirely dead), `SNc` (masked by VTA).**
2. **A read-out validated while a hub was dead may not be robust to its revival.** The punishment read-out is the pinned instance — it could never have been tone-invariant once LC lived. **This will recur as BF-ACh and SNc are completed. Re-audit then.**
3. **The ungrounded uniform setpoint is a systematic bias.** Any circuit whose true target rate exceeds 0.1 is persistently over-suppressed in proportion to its own activity — and we don't know which. **`CeA` is a severe instance: it rests at 0.550 against a setpoint of 0.1 (~9× LC's erosion pressure), with 17 afferents, none bounds-pinned, including innate `nociception → CeA`.** Unlike LC's — whose pacemaker floor made the pressure *unsatisfiable* and therefore visible — **CeA's is self-limiting and therefore invisible**: it settles by dragging threat responsiveness toward a placeholder over developmental time. It **cannot be grounded in isolation** (principle 6) and is re-homed to the future self-regulation mechanism.
4. **R4 has no plasticity guard** (§3.4).
5. **Per-edge phasic character is load-bearing in four places** — the teaching signal, `CeA → LC`, the distress display, and the cross-agent contagion loop. One property; several consequences. **The contagion loop is damped *only* by the display's phasic adaptation — so it must be re-checked if that changes.**
6. **A chronically distressed agent becomes invisible.** At `CeA` = 1.000 the display reads **0.000** by tick 800 — total signal loss through adaptation. **Chronic-adversity conditions are off-limits for study claims until §15.9 lands.**
7. **The faithful self-regulation mechanism is the audit home for provisional values** — homeostatic plasticity + maturing inhibition + critical-period gating + (late) executive maturation. Literature-checked: Hebbian/BCM is *intrinsically* destabilising and is maintained by homeostatic plasticity; its forms differ juvenile vs mature; PV-interneuron maturation lags; executive maturation is a *later* contributor. **Stability must EMERGE. It must never be an optimizer.**

**Unexplained observations, disclosed:** the throttle sweep is **robustly non-monotone** (`[0.117, 0.016, 0.093]`, 12/12 seeds) and **unexplained** — it graduates to investigation the moment the throttle carries inferential load. `teen ≤ adult` acting-readiness is robust; **`teen ≤ child` is not** (flips with reward intensity at 1–2 step margins), with an LC → dlPFC age-graded mechanism as a structurally-real candidate.
