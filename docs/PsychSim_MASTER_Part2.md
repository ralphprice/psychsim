# PsychSim — Master Design & Build Document, Part 2 (Supplements & Addenda)

*Additive supplement to `PsychSim_MASTER.md`. The master is in implementation; this document does
**not** modify it. Where a supplement below touches something already built, **reconcile, do not
overwrite**. New guidance produced from here on lands in this Part 2 so the implemented master stays
stable.*

---

## S1. The substrate seed data — disposition, the wiring prerequisite, and reconciliation with the design

This section resolves "what do we do with the JSON data files," and it changes one assumption in the
master's build order.

### S1.1 What the files are, and which is canonical

`docs/neuralnetworks/` holds seven versions of the **substrate itself**: `psychsim_substrate_seed.json`
(v1) through `…_v7.json`. **v7 is canonical; archive v1–v6** (keep for provenance/audit).

v7 is not a bare connectome — it is a rich, self-documenting substrate specification:
**73 circuits** (each with `homeostatic_setpoint`, `time_constant_tau_ms`, `activation_bounds`,
`developmental_online_age`, `plasticity_coeff_schedule_ref`, `transmitters`, `confidence`, `sources`),
**159 connections** (with `default_weight`, `weight_bounds`, `gating_neuromodulator`,
`eligibility_trace_tau_ms`, `is_innate_reinforcer_link`, `developmental_online_age`), a
**15-entry `innate_wiring_catalogue`**, **`physical_endowment`** (7), **`plasticity_rules`** (8),
**`input_channels`** (8), a **`gaps_register`** (10, honest self-documentation), and an
**`honesty_wall` / `scaffold_note`** in `meta`.

### S1.2 Critical: the seed is not wired into the live code (a prerequisite the master leaves implicit)

`core/neuraldesigner/store.py` says in its own docstring that it is *"an AUTHORING sandbox … **NOT
wired into the live substrate (that is the separate substrate-overhaul work)**,"* and it loads
`data/neural/library.json` — a **different file in a different format**, not the v7 seed. Grepping the
codebase for the seed by name returns nothing: **no live code loads v7.** The running system still
uses the legacy `TraitSeed`/`Brain`/`drives` affect engine — the very thing the design supersedes.

**Consequence for build order.** The valence engine (`interocept.py`, `learning.py`, `selection.py`)
is specified to run *on* the substrate. Until v7 is loaded and driving activation, the engine has
nothing to run against. So **the substrate-overhaul is a prerequisite** and should be an explicit
early step — call it **Phase 0.5, before Phase 1**:

> **Phase 0.5 — Make the substrate live.** Bridge the v7 seed into a runtime so it loads and drives
> circuit activation. `core/neuraldesigner/` already contains candidate machinery (`runtime.py`,
> `bridge.py`, `library.py`); the task is to load v7's schema (or adapt it into the runtime's model)
> and expose the 73-circuit / 159-connection graph as the live substrate the engine reads. Acceptance:
> the substrate instantiates from v7, activation propagates across it, and a characterisation test
> shows circuits responding to input — *before* any valence code is layered on.

This does not conflict with the master; it inserts a foundation the master's Phase 1 assumes.

### S1.3 The seed and the valence design align — READ FROM the seed, don't re-declare

The v7 schema already contains the fields the valence appendices assumed we would build. The build
must **populate the engine from the seed**, not hardcode a parallel copy — one source of truth, or the
two will drift:

| Valence design element (master) | Already in v7 seed | Guidance |
|---|---|---|
| State-vector set-points (App. A) | `circuits[].homeostatic_setpoint` | read from seed |
| Innate-perturbation set (App. B) | `innate_wiring_catalogue` (`stimulus`/`target`/`innate_effect`/`mechanism_type`) | read from seed |
| **The App. B.1 value-vs-prior distinction** | seed's `mechanism_type`: `appetitive`/`aversive` vs `arousal_orienting` vs **`learning_rate_modifier`** | **already encoded — respect it** |
| Neuromodulator gates (App. C) | `connections[].gating_neuromodulator` | read from seed |
| Eligibility traces (App. C) | `connections[].eligibility_trace_tau_ms` | read from seed |
| Plasticity schedules (App. C) | `plasticity_rules` + `plasticity_coeff_schedule_ref` | read from seed |
| Physical endowment (§5) | `physical_endowment` | read from seed |
| Developmental onset (§6) | `circuits[].developmental_online_age`, `connections[]` | read from seed |
| Time constants (App. F dynamics) | `circuits[].time_constant_tau_ms` | read from seed |

The striking point: the seed's `innate_wiring_catalogue` already distinguishes **value perturbations**
(sweet/umami/salt → appetitive; bitter/sour/nociception/CO2 → aversive; thermal, affective touch)
from **attentional priors** (`arousal_orienting`: looming, startle, face, biological motion, voice)
from **prepared-learning** (`learning_rate_modifier`: ancestral-threat categories) — i.e. exactly the
Appendix B.1 discipline, built into the data. **Integration principle: the seed is the single source
of truth for substrate structure and parameters; the valence-engine code reads it and supplies the
dynamics.**

### S1.4 Small reconciliation deltas (precise)

- **Selection-loop nuclei (App. F) are mostly present already** — v7 has **DStr** and **Caud-assoc**
  (dorsal striatum), **STN**, **VP** (ventral pallidum), **SNc**, and thalamic relays (MDthal, etc.).
  The only arguable additions are the canonical motor-loop *output* nuclei — **GPe, GPi/SNr, and a
  dedicated motor thalamus (VA/VL)**. Given the functional-illustrative scope, the existing
  VP/DStr/STN/MDthal loop may already suffice for action selection; **add the pallidal-output +
  motor-thalamus nuclei only if fuller motor-selection fidelity is wanted.** This *softens* the
  Appendix F "add selection nuclei" flag — reconcile against what is there first.
- **Social innate-wiring entries are lighter than the design requires.** The catalogue strongly covers
  taste/pain/thermal/touch/looming/startle/orienting, but the **social perturbations** emphasised in
  App. B.2.B and the social-valence research — **separation / loss of contact → separation distress**,
  and **caregiver proximity → security** — are not explicit catalogue entries (though the
  `PAG-PANIC` and affiliation circuits exist). **Add these as `innate_wiring_catalogue` entries**
  (existing schema + `mechanism_type`), so the social primaries live in the data, not only the code.
- **Reconcile citations.** Check the seed's embedded `sources` against the VERIFIED workbook (e.g. the
  `Vidal-Gonzalez 2004` → 2006 slip).
- **Numbers stay scaffold.** The seed's own `gaps_register` and `scaffold_note` already say this;
  honour it — calibrate per master Part IV.

### S1.5 Net disposition — what to do with the JSON files

1. **v7 = canonical** substrate; archive v1–v6.
2. **Substrate-overhaul first (Phase 0.5):** bridge v7 into a runtime so it loads and drives activation
   — the prerequisite the codebase itself flags.
3. **Wire the valence engine to read from v7** (set-points, innate-wiring, gates, eligibility,
   endowment, developmental ages, time constants) — one source of truth.
4. **Apply the small deltas:** add the social innate-wiring entries; add pallidal-output/motor-thalamus
   nuclei only if needed; reconcile the seed's citations against the verified workbook.
5. **Keep all numbers scaffold**; calibrate per master Part IV.

### S1.6 One reassurance

This is good news, not a problem: the independently-built v7 substrate and the session's valence/
motivation design are highly consistent — the same architecture reached from the data side and the
mechanism side, including the honesty-wall distinctions. The main work is *integration* (wire it in,
read from it) plus a few small additions — not redesign.

---

## S2. Substrate-dynamics spec (the "make v7 live" sub-phase)

Recon confirmed that "make v7 live" is not wiring — it is **building the substrate engine**: a loader
plus a dynamical engine running 73 circuits / 159 connections under the 8 meaning-blind plasticity
rules. That is the overhaul the whole project points at, and the master doc never specified its
dynamics (it treated the substrate as a prerequisite). This section specifies the load-bearing
decisions so it can be built correctly; the seed already fixes most of them.

### S2.1 Sequencing decision: Option A, with this section as the "C" dynamics spec

Build the substrate as **its own reviewed sub-phase (8a)**, standalone and tested, → commit → design
review → **then 8b** (wire interocept/learning/selection onto it, retire the legacy net engine,
complete honesty #2, reconcile params<-seed). Not one 5-item push (Option B): the single largest,
foundational change must not land without an intermediate review of the foundation. This section is
the dynamics spec the implementer asked for; the seed supplies the rest.

**Acceptance is split — an important reframe.** The substrate *alone* produces **circuit activity**,
not psychological phenomena (those need the valence engine + matrices + development on top). So:
- **8a (substrate) acceptance = MECHANISTIC + review** (S2.6), not the emergent psychological phenomena.
- **8b (integrated) acceptance = emergent-phenomena validation** (App. D / Part IV).

This de-risks A: the substrate can be validated on its own terms first.

### S2.2 Circuit dynamics — a leaky-integrator rate model (per the seed schema)

The seed's circuit schema already specifies this ("hard bounds for the leaky integrator", "integrator
time constant"). Each **live** circuit is a rate unit whose activation relaxes toward its net input:

```
tau_i * d a_i/dt = -(a_i - baseline_i) + input_i          # leaky integrator
input_i = sum_j ( w_ji * a_j )   over live incoming connections j   # (+ external drive for input channels)
a_i clamped to activation_bounds_i
```

Discrete Euler step with a fixed dt (SCAFFOLD, in params). `tau` from `time_constant_tau_ms`
(SCAFFOLD). Circuits are **only rate units** — nothing in the update references what a circuit
"is"; "fear"/"threat" appear nowhere. This is the honesty wall at the dynamics level.

### S2.3 The two-switch live set (development)

Structure exists in full; **activation is a gated subset** (seed principle). A circuit/connection is
in the **live set** iff `developmental_online_age <= current_age` AND `calibration_active_default ==
true`. Development = circuits switching on by age (reward/threat early, prefrontal late), reproducing
the maturation gradient the valence design assumes — for free, from the data.

### S2.4 Plasticity composition — the 8 rules, as the seed intends

The seed's rules compose into one per-connection, per-step weight update. Compose in this order
(all terms **local and meaning-blind**):

1. **R3-BCM** (workhorse) is the correlation term: `dw ~ a_pre * a_post * (a_post - theta)`, `theta`
   tracking the circuit's own recent mean `a_post`. Subsumes R1-HEBB and gives potentiation/
   depression/competition/self-stabilisation in one rule. (R2-RATE is the modelling choice that we do
   this at rate level, not STDP — flagged scaffold.)
2. **R5-NMOD gate** (the DANGER POINT): multiply the eligibility trace by a `modulator_scalar` that is
   the **live OUTPUT of the gating neuromodulator circuit** named on the connection
   (`gating_neuromodulator`: DA<-VTA/SNc, ACh<-BF-ACh, NA<-LC, 5HT<-raphe). It must **never** be a
   value set from an outcome judgment. This is where outcomes are most easily smuggled back in —
   enforce that the modulator is wired from a circuit's activity.
3. **R6-DEVGATE**: scale the whole update by `eta(age, circuit)` (high early, adolescent bump, low
   adult). Age enters **only here, as a rate, never as a target**.
4. **R4-HOMEO**: slow multiplicative scaling of a circuit's incoming weights toward its
   **firing-rate `homeostatic_setpoint`** (S2.5). Must act fast enough not to be outrun by BCM growth
   (the "temporal paradox" — a timescale constraint, in params, SCAFFOLD).
5. **R8-BOUNDS**: clamp to `weight_bounds` and normalise incoming weights (competition = a
   consequence, not a tuned outcome).
6. **R7-STRUCT** (slow clock): prune weights held ~0 too long; add connections between co-active
   **anatomically adjacent** circuits within connectome limits.

### S2.5 Set-point mapping — TWO different set-points (correcting the reconciliation note)

My earlier params<-seed note conflated two things. They must stay separate:

- **Per-circuit `homeostatic_setpoint`** (in the seed; e.g. all interoception circuits = 0.1) is
  **firing-rate homeostasis** — the target mean *activity* of a nucleus, consumed by **R4-HOMEO**. It
  lives in the substrate engine and stays there.
- **Interoceptive state-vector set-points** (interocept.py) are the regulated **body-variable**
  targets (energy, thermal, arousal, social contact). These are a **functional layer**, and their
  magnitudes stay **SCAFFOLD in params** — the seed does not carry them either.

**The mapping decision:** the interoceptive state **variables** should be **defined as read-outs over
designated seed interoception circuits / input channels** — e.g. arousal/stress <- PVN / RVLM /
SympOut / AdrenalCortex (HPA + sympathetic); pain <- PBN / lamina-I via IN-SOMATO; energy/hydration/
thermal <- visceral afferents via IN-INTERO/NTS; social contact <- the affiliation circuits (PVN-OT
etc.). That **grounds the state vector's structure in the substrate**. The set-point **magnitudes**
remain scaffold. So `interocept` does **not** read its set-points from `homeostatic_setpoint`; it
reads its *variables' activity* from designated circuits, and keeps scaffold set-point numbers.

### S2.6 Standalone substrate (8a) acceptance — mechanistic and testable

- The 73/159 substrate **instantiates from v7**; the live set gates correctly by age (S2.3).
- **Activation propagates and settles**: inject input -> activity flows along live connections ->
  relaxes to baseline when input stops (the leaky integrator behaves; bounds respected).
- **Plasticity is meaning-blind and stable**: co-active connections strengthen (BCM); `theta` tracks
  the circuit's own activity; homeostatic scaling prevents runaway/silence; weights stay bounded; and
  a source-level check confirms **no rule references a circuit's identity/meaning or any outcome**.
- **Developmental gating** works: circuits come online by age; `eta(age)` modulates plasticity.
- **R5 discipline holds**: every plasticity modulator is a neuromodulator **circuit output**, not a
  set scalar.
- `gaps_register` items (unknown newborn weights, incomplete connectome, unmapped fMRI correlates)
  are carried as **flagged scaffold/assumptions** — not invented to fill; the register stays as the
  audit trail.

Then: commit -> design review -> 8b.

### S2.7 8b integration note — unify the plasticity, don't duplicate it

Critical for 8b: **learning.py's three-factor plasticity (App. C.4) *is* R5-NMOD**, and the RPE
dopamine signal *is* the DA modulator from VTA/SNc. So the valence learning engine and the substrate
plasticity are **the same mechanism** — at 8b they must **unify** into the substrate's neuromodulated
plasticity (one implementation, gated by real neuromodulator-circuit outputs), not run as a second,
parallel learner. Likewise selection.py runs **over the live circuit substrate**, and interocept's
state vector reads the interoception circuits (S2.5). This unification, plus the legacy-engine
retirement and honesty #2, is 8b — and its acceptance is the emergent phenomena.
