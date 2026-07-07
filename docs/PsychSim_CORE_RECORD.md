# PsychSim — Core Record

*A living record of **core-validation observations**: what the finished core organism does under
probing. Distinct from the sealed MASTER/Part docs (design, not editable here) and from
**study findings** (the psychopathy study is deferred work run **on** this core; its findings will
belong to the study, not here). Per Part 7 S14.4: core-validation observations belong in the core
record; psychopathy findings belong to the study when it is run.*

---

## The core / module boundary (Part 7 S14.1)

- **The core** is the universal organism and its machinery: the substrate; the **four matrices**
  (social, environmental, group, **self-reflection**); the **1/n developmental plasticity**; behaviour
  selection; and the general instruments (the **bank**, the **Arena**). None of this is about
  psychopathy — it would all exist if psychopathy had never been mentioned.
- **The circuit-breaker module** is *only* the throttle panel that attenuates specified circuits on a
  given character. That is the **entire** footprint of the study-specific plugin. Switch it off and you
  have a complete, ordinary simulated human. **The module is done** (the breakers were built; that was
  it).

Consequence (S14.2): everything built after the circuit breakers — self-reflection, the Arena,
banking, the 1/n schedule — was **core completion and validation**, not psychopathy work. The throttle
was used as a **probe/stressor to exercise the core**; the earlier "psychopathy divergence" framing was
a labelling error. The psychopathy **study** (slider sweeps, scan controller, CU/field-data matching)
has **not been run**.

---

## OBS-1 — Gate-A: the complete core under a circuit-attenuation probe (Part 7 S14.3)

*Recorded 2026-07 as a **core-validation observation**, not a study finding.*

> On the complete core organism (age/experience-decreasing 1/n plasticity; all four matrices, with
> self-reflection routed as a **non-feedback read-out**), under a graded attenuation of the
> affective-empathy circuitry: **development converges** (the developed state settles, it does not
> oscillate), and the developed outcome is **well-posed and stable across two independent channels**
> (behavioural executive control and developed self-regard) and across development duration. The
> behaviour is stable and mechanistically traceable throughout. The hypothesised
> differential-susceptibility interaction between fearlessness and childhood environment **does not
> robustly emerge**; what *does* robustly emerge is the reads-but-doesn't-feel dissociation
> (structural/activation-level) and a strong main effect of childhood environment on developed
> self-regard.

**Measured values** (v8 substrate; development 350–600 ticks; throttle 0.0 intact / 0.7 attenuated):

| channel | interaction (throttled_swing − intact_swing) | across durations | reading |
|---|---|---|---|
| executive control (behavioural) | −0.009 | −0.007 / −0.010 / −0.011 | well-posed, ≈0 |
| developed self-regard | −0.030 | −0.032 / −0.029 / −0.026 | well-posed, negative |
| composite (scaffold 0.25 weight) | +0.010 | — | sign is a weight artifact; not headlined |

self-regard cells: intact **+0.29 / −0.20**, attenuated **+0.35 / −0.11** (warm / harsh). Regime-B
un-throttled development settles: warm exec +0.300 → +0.285 → +0.260 over 200 → 400 → 800 ticks.

### Note A — a mechanistically-legible wrong-way result (candidate finding, not buried; S14.3)

The attenuated (fearless) agent is somewhat **buffered** against a harsh childhood — *less*
environment-driven self-criticism — because the same attenuation that blunts threat-based responses
also blunts the threat-colouring of self-appraisal (the self-regard read-out draws on the threat
circuits that the throttle hypofunctions). It runs **opposite** to differential susceptibility, and it
is **traceable**, which makes it a checkable claim about the world. Flagged for the deferred study.

### Note B — the width of the null is bounded (S14.3)

Self-reflection was tested as a **non-feedback read-out** (it observed the developed state without
altering it — executive trajectory byte-identical with/without it). So the earned statement is
"self-reflection *as a non-feedback read-out* does not carry the effect," **not** "self-reflection
cannot." Whether self-reflection *as a feedback loop* would behave differently is a distinct, untested
question — deliberately not opened, recorded here as a boundary.

*Reproduce:* `core/substrate/divergence.py::divergence_all_channels`; tests in
`tests/test_substrate_divergence.py` (`TestRegimeBStability`, `TestDivergenceWellPosedAndNear_Zero`,
`TestSelfReflectionRoutedIntoOutcome`).

---

## What is validated vs what is still ahead (Part 7 S14.4)

- **Validated:** the core organism is complete and behaves stably, traceably, and well-posedly under a
  circuit-attenuation probe.
- **Ahead (deferred study):** the psychopathy study proper — throttle sweeps, the scan controller,
  field-data matching — run on this finished core.

---

## 8b.4 — honesty migration #2: the outcome-category network engine removed

*Recorded 2026-07. The irreversible honesty cut, scoped per the design ruling (Option 1).*

**What was removed** (the outcome-category *network engine* — the encoded-answer path): `TraitSeed.access`
and every category-named seed weight; the `Network`/`default_catalogue`/`network_score`/`_arbitrate`
scorer in `agent.py`/`core.py`; the `GOVERNED`/`EXPLOITATIVE` groupings; `response_to_network`/
`_BEHAVIOUR_TO_NETWORK`; the category-named readout shims/`Outcome`/`probe`. **No outcome-category name
survives as a causal primitive.** The outcome-category vocabulary now lives in **code** only in
`observer.py` (computed over emergent behaviour, never fed back); the only other appearances are
documentation comments in `core.py` (the canonical record of what was removed).

**How consumers were re-pointed:** everything causal now keys on the emergent action (`Response.behaviour`:
approach/nurture/play/court/avoid/aggress/seek_comfort) and on the feature read-outs `is_cohesive`/
`is_aggressive` — `gamemaster` (adjudication/effects/memory), `daily`, `speech/acts`, `sim_viz`,
`justice`, the sophropathy study layer. Where a distinction the emergent features can't yet express was
lost, it was **dropped honestly, not renamed**: speech no longer *generates* a coded DECEIVE act, and
justice no longer splits callous-vs-reactive severity (both were encoded answers; they can return as
real feature read-outs when the engine produces them).

**Deliberate Phase-0 baseline reframe.** The baseline is now the emergent Panksepp response + feature
read-outs, **not** the legacy category arbitration. `test_characterisation`'s golden was regenerated to
reflect this intended change — the changed numbers are the reframe, **not a regression**.

**Still interim-legacy:** the Panksepp `Brain` (drives.py) remains the live behaviour engine, flagged in
code with a deferred-retirement pointer. It was **not** touched — the substrate has no social-behaviour
parity yet (invariant 6).

Suite: green (396). Held here for the honesty-#2 review.

## Roadmap split (what "retire the legacy engine" became)

The old single item "8b.4 retire legacy" split cleanly into two, per the ruling:

1. **8b.4 = honesty-#2 category removal (this cut).** Done. The outcome-category network engine is gone;
   categories are observer-only.
2. **Panksepp-engine retirement = a later, separately-scoped, parity-gated substrate-social phase.** It
   needs the substrate to produce and observe social behaviour first (multi-affordance selection →
   observable acts + a circuit observer adapter + rewiring `sim_world`). That missing capability is the
   **same** one the Part 6 Arena needs (multi-agent social behaviour), so when reached the two may be a
   single build. Sequenced after the substrate can actually produce/observe social behaviour; never
   before parity (invariant 6).

Remaining order: honesty-#2 review → **8b.5** (params ← seed; finalises the developed-state format the
Part 6 bank waits on) → **8b.6** (emergent-phenomena battery + the two mechanism gaps, both engine-side,
no seed edit) → **Part 6 instrument batch** → the Panksepp-retirement / substrate-social phase.

## 8b.5 — params ← seed reconciliation (developed-state/params representation now final)

*Recorded 2026-07. Lower-stakes; synced at completion for a lighter review.*

The audit found the substrate side already disciplined: `substrate/model.py` reads **every**
per-circuit/connection parameter from the seed (tau, homeostatic_setpoint, baseline, bounds, gating
neuromodulator, eligibility tau, developmental ages, innate wiring), and `substrate/params.py` holds
only code-side dynamics scaffold. No per-circuit seed value is hardcoded anywhere.

The one open item was a **stale pre-S2.5 reconciliation note** in `affective_engine/params.py` that
told a future reader to "read set-points from `seed.homeostatic_setpoint`." The seed data disproves it:
`homeostatic_setpoint` is **uniformly 0.1 across all 77 circuits** — firing-rate homeostasis (R4-HOMEO),
a *different quantity* from the regulated body-variable set-points (energy 0.80, arousal 0.20, …). Per
**S2.5** those interoceptive set-points **stay scaffold** (the seed does not carry them); the state-vector
*structure* is grounded in the substrate via the S2.5 bridge (`interocept.SUBSTRATE_READOUT` /
`state_from_substrate` — each variable reads activity from designated circuits, all present in v8). The
functional `PERTURBATION_GAINS` is likewise scaffold at a finer abstraction than the seed's 15-entry
coarse catalogue (and carries social perturbations the catalogue still lacks, S1.4 — adding them would
be a seed edit / v9, out of scope).

Resolved: the note now records the correct post-S2.5 status, and a guard test
(`tests/test_params_seed_reconciliation.py`) enforces the split — substrate reads from the seed, no seed
data duplicated in params, the two set-points stay separate, the state vector grounds in real circuits —
so the representation **cannot silently drift**. **The developed-state/params representation is now final**
(the gate the Part 6 bank waits on). Suite 402, green.

## OBS-2 — 8b.6: the emergent-phenomena battery + the two mechanism-gap fixes

*Recorded 2026-07 as core-validation observations. Universal-organism phenomena, not psychopathy findings.*

**Both mechanism gaps closed engine-side (no seed edit, no v9), and meaning-blind:**

- **Continuous maturation → executive control capacity (Part 3 S5.4).** Added `plasticity.maturation()` —
  a functional CAPACITY curve (distinct from `eta`, a plasticity rate) — fed into behaviour selection so
  control capacity keeps maturing into the mid-20s (late/PFC schedules) while reward-sensitivity peaks in
  mid-adolescence on a nonzero floor (Steinberg dual-systems). Age enters only as a rate; the schedule
  ASSIGNMENT is seed data. **Result: the adolescent-risk inverted-U EMERGES** — risk index 0.070 (age 3)
  → **0.195 (age 16, peak)** → 0.177 (age 30), above both childhood and adulthood. No coded "risk" rule.
- **DA/satiety state-dependence (Part 7 S15).** Closed the loop: the energy deficit drives the
  `IN-INTERO:nutritive_state` channel → LH → VTA (the seed's own chain). **Result: food-reward DA is
  amplified when hungry (0.525) vs sated (0.398), ~1.32×.** The modulator is LH circuit activity —
  R5-clean, never DA scaled by a computed `r`.

**The battery — five targets, all EMERGE cleanly (none forced):**

| phenomenon | result | how |
|---|---|---|
| adolescent-risk imbalance | **emerges** (inverted-U, peak age 16) | mature reward × still-maturing control |
| DA/satiety state-dependence | **emerges** (hungry > sated, 1.32×) | energy deficit → LH → VTA modulation |
| negativity bias | **emerges** ( \|−0.48\| > \|+0.42\| ) | one asymmetric learning rule (aversive faster) |
| ambivalent bond | **emerges** (attachment 0.70 + threat 0.60, held in inner circle despite value −0.20) | salience-allocated matrix + two pulls |
| punishment-for-one = reward-for-another | **emerges** (same event: +0.245 hungry / −0.105 sated) | valence computed from each agent's own state |

Differential susceptibility remains the **gate-A earned negative** (OBS-1) — not re-litigated.

**Deliberate developmental reframe (recorded, not a regression):** with the dual-systems maturation, the
*youngest* agent is no longer the most impulsive — acting-readiness now peaks in adolescence. The
behaviour test that encoded the pre-Gap-1 "young = most impulsive" assumption was updated to assert the
corrected ordering (an adolescent acts at least as readily as both a younger child and an adult).

**Honest edge flagged:** at very young ages (~4) the agent fully restrains under a reward cue — an
artifact of the coarse live-circuit set that early (many circuits online later), not the phenomenon. The
peak-at-adolescence result is robust across the age curve. Reproduce: `substrate/phenomena.py`,
`tests/test_phenomena_battery.py`. Suite 408, green.
