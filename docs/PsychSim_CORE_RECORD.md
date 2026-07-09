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

## OBS-3 — the v8 substrate is fear/avoidance-dominant (aggression a live-but-weak candidate) — CLOSED in v9

> **Update (Part 8 v9 pass): the connectome gap named below is CLOSED.** v9 adds the VMHvl
> hypothalamic-attack area and a provocation-specific drive of it; provocation now produces
> reactive aggression instead of only deepening its suppression. See "OBS-3 closure — the v9
> provocation→attack pathway" further down. The v8 account below is kept as the diagnosis that
> made the fix legitimate.

*Recorded 2026-07 as a bounded core property with a mechanistic account (same posture as OBS-2), found
while building substrate social behaviour (Part 6 substrate-social phase).*

The substrate's multi-affordance social selection (`substrate/social.py`) produces
approach / nurture / avoid / seek_comfort / restrain emergently and situation-appropriately. Aggression
(`aggress`) is a **live candidate** in the same basal-ganglia race -- grounded in real attack effectors
(CeA->PAG/HYPdm), it competes and carries a nonzero phasic drive under threat -- **but it does not win**,
even under strong threat: the threat response resolves to avoidance. The specific mechanistic fact is
that the **attack effectors PAG and HYPdm are net-inhibited in the v8 connectome** (they stay ~0 even
under direct drive), so the winning threat act is fear/avoidance, not attack.

**This is left as-is, not tuned.** Forcing aggression to win (dis-inhibiting PAG/HYPdm by hand) would be
tuning the connectome to produce a desired behaviour -- the exact honesty violation the build has
avoided (cf. the coded DECEIVE act dropped at 8b.4). The behaviour returns if and when the substrate
*earns* it via a grounded connectome change, not by propping it up.

**Whether this is a property or a defect is genuinely uncertain, and left unresolved by design.**
- *Property:* avoidance/freezing are the default threat responses ethologically; reactive aggression is
  the exception that needs specific provocation (thwarting, cornering, pain-with-no-escape), not the
  baseline. A fear-dominant developing organism may be correct.
- *Defect:* reactive aggression clinically exists; if the sensory channels provide no thwarting /
  frustrative-non-reward pathway to the hypothalamic attack area, that is a real connectome gap.

The consumers key on `is_cohesive`/`is_aggressive` over the emergent behaviour, both of which work for
the substrate, so this does not block the Panksepp retirement (invariant 6 is met: the substrate
reproduces the social behaviour the town sim consumes). It is logged as a v9 candidate below.

## Known v9 seed candidates (parked -- a deliberate, cited batch pass, if ever)

No v9 is needed now; these are the accumulated candidates for one future, reviewed seed pass. (Neither
DA/satiety nor continuous maturation needed a seed edit -- both were engine-side.)
- **Social innate-wiring entries (S1.4):** ~~the seed's `innate_wiring_catalogue` lacks explicit social
  perturbations (separation / loss-of-contact -> distress; caregiver proximity -> security).~~ **RESOLVED
  in v9** (Part 8 S16.7): added SR-SEPARATION / SR-PROXIMITY / SR-REJECTION catalogue entries documenting
  the social primary perturbations the functional layer already wires (documentary; no dynamics change).
- **Thwarting / frustrative-non-reward -> hypothalamic-attack pathway (OBS-3):** ~~does the v8 connectome
  lack a documented provocation->attack route ... that would let reactive aggression win under
  provocation?~~ **RESOLVED in v9** (Part 8 v9 pass): the answer was YES (a genuine connectome defect),
  and v9 adds the VMHvl attack area + provocation drive that closes it. See the closure record below.

## Part 6 step 3e — the substrate-social phase (Panksepp retirement), stage 4: the two reductions

The substrate reproduced the social behaviour parity-first (stages 1--3, invariant 6); stage 4 removed
two legacy structures now that the substrate carries the live path. Both are reductions, not new
behaviour: the observable town sim is unchanged.

**Reduction A — the Panksepp learned-monitor Executive was retired.** The old `affective_engine/executive.py`
(the `Executive` class, `consult`/`checks`, `monitor_executive`, `install_monitors_from_memory`,
`moral_orientation_readout`, `_system_from_label`) plus its `exec_store` + HTTP/UI editing surface are
**deleted**. It was a *separate* control layer bolted beside the Panksepp brain: a learned inhibitory
monitor whose thresholds were installed from episodic memory, and a vmPFC-style moral read-out over the
7 Systems. The substrate's own **STN brake** (`substrate/behaviour.py`, the go/no-go selection race that
matures with age) is now the **sole** executive, and the moral read-out lives substrate-side
(`observer.profile_from_substrate`). `moral_orientation_readout`'s only remaining caller was the dormant
Executive, so it went out with it -- no separate handling. No live importer of the dropped machinery
remains (substrate `executive_hold` / `developed_executive_control` are the STN brake, unrelated).

> **Deferred capability (v9/study candidate): experience-conditioned inhibitory monitoring.** The STN
> brake is a **maturational** control (it strengthens with age in the selection race), not a monitor
> **conditioned on specific learned associations**. The retired Executive could `install_monitors_from_memory`
> -- restraint keyed to particular remembered cues. The substrate has no equivalent "learn to inhibit
> *this* cue from *this* episode" hook yet. If a future study needs experience-specific restraint beyond
> the age-graded brake, that is a real capability to add on the substrate (a plasticity-grounded
> inhibitory route), not to resurrect as a bolt-on arbiter. Parked alongside OBS-3 (aggression) and the
> social innate-wiring entries as an accumulated, cited candidate -- not needed now.

**Reduction B — `CharacterLibrary` is now a thin layer over the `AgentBank` (single serialization path).**
The library's `LibraryEntry` used to store a Panksepp `Brain.to_dict()` and rebuild it with
`Brain.from_dict()`; the engine placed grown adults by swapping `person.mind.brain`. Now `grow()` banks the
grown agent's developed substrate through the bank's own serializer (`snapshot(DevelopedAgent(engine=...))`,
stored as `LibraryEntry.state`), `make_agent()` restores it (`restore`, restored-never-edited), and the
engine places it with `AffectiveAgent.adopt_engine(...)` (swap the developed engine + refresh the resting
baseline). **Invariant held: every write of developed state goes through the bank's `snapshot`/`restore` --
no parallel substrate serializer survives.** The shipped `library/adults.json` was regrown in the new
`state` format. The `add_person` reseed (`brain = brain_from_seed(...)`) is gone: the substrate is seeded
deterministically from the temperament's gains in `AffectiveAgent.__post_init__` (`seed_substrate`), so an
authored subject is reproducible from its seed alone -- the reseed only ever pinned the now-inert Panksepp
brain's RNG.

**Still interim-legacy (removed in stage 5, the deletion hold):** `AffectiveAgent.__post_init__` still
constructs a `self.brain = brain_from_seed(...)` (the inert Panksepp brain), and two `test_observer` cases
still read `brain.to_dict()` as a not-mutated measurement. These are the last `.brain` references; they go
with `Brain`/`System`/`Drive` in stage 5. The Part 8 v9 ruling (aggression circuit before or after the cut)
was decided **before**: v9 lands first (below), so stage 5 retires Panksepp against a v9-parity substrate.

## OBS-3 closure — the v9 provocation→attack pathway (Part 8 v9 pass)

The design session ruled **aggression-first (v9-before-cut)**: earn the aggression the substrate lacked
via a grounded connectome change, then retire Panksepp against a substrate whose aggression is properly
represented. The edit is a new `psychsim_substrate_seed_v9.json` (v8 archived; `_SEED_PATH` repointed).

**The diagnosis (why it was legitimate, not a thumb on the scale).** OBS-3 was not "aggression loses the
race" — it was **"aggression cannot be driven at all."** Provocation entered the substrate ONLY folded
into `IN-SOMATO:nociception` (`social.py`), which drives the **GABAergic** `CeA` — the dominant projection
into both attack effectors (`CeA→PAG −0.70`, `CeA→HYPdm −0.70`). So more provocation only DEEPENED attack
suppression; the wiring guaranteed the opposite of aggression. A genuine connectome defect.

**The edit (minimal, cited, weights SCAFFOLD by physiological ordering — not tuned to a target):**
- **New circuit `VMHvl`** — ventrolateral ventromedial hypothalamus, the hypothalamic attack area
  (Lin et al. 2011; Falkner & Lin 2014; Hashikawa 2017), distinct from the reproductive VMHdm the seed's
  `VMH` collapses. Glutamatergic (+1), online 0.0, `hypothalamic_low_flat` plasticity.
- **3 edges:** `IN-INTERO:provocation→VMHvl` (strong), `VMHvl→PAG` (strong; VMHvl→dPAG attack output,
  Wang 2015), `VMHvl→HYPdm` (moderate-strong; recruits the medial hypothalamic attack area, Panksepp RAGE).
- **Provocation split** (`appraisal_to_substrate_input`): the `provocation` term now routes 0.2 to
  nociception (still carries threat → avoid) + 0.6 to the new `IN-INTERO:provocation` channel (→ VMHvl).
  Genuine competition, not a scripted flip. `thwarting`/`restraint` triggers likewise reach both.
- **`aggress` affordance re-grounded** `(CeA,PAG,HYPdm)→(VMHvl,PAG,HYPdm)` — a correctness fix: CeA's
  activation was inflating the "aggress drive" while CeA was *suppressing* the real effectors.
- **NOT touched:** the `CeA→PAG/HYPdm` inhibition (byte-identical to v8; guarded by a test). No
  hand-dis-inhibition — fear stays the baseline threat response.

**Measured result (reported as-is; the phasic race decided, weights not adjusted to force it):**
- **The gap is closed.** Provocation makes `aggress` the **dominant drive** at every age (adult: aggress
  0.18 vs avoid 0.03) — it went from unreachable (exactly 0 in v8) to leading. Plain threat still → `avoid`
  (aggress exactly 0); neutral → `restrain` (aggress exactly 0, **no leak** — the required provocation-
  specificity control).
- **An un-tuned developmental trajectory emerged.** At **age 2**, strong provocation → **overt `aggress`**
  (crosses the act threshold); by **age 8+** the same provocation → **`restrain`** — aggression is the
  dominant impulse but held below the threshold by the *maturing STN brake* (the OBS-2 maturation
  mechanism). This is reactive aggression's real course (early expression → progressive restraint), and it
  fell out of the v9 pathway meeting existing maturation — nothing was tuned to produce it. So OBS-3's
  "aggression does not win even under strong threat" is genuinely **falsified** (it wins under strong
  provocation before executive control matures), not merely nudged.
- **Calibration note — the group dominance route sits just below threshold (resolved by measurement,
  Part 8 #2, Option A):** the group-matrix **dominance route stays sub-threshold** under the
  `status_challenge` stimulus's moderate provocation. This was checked directly to rule out that the
  moderate level had been *chosen* to keep the route sub-threshold (a goalpost-move). It had not:
  measured, the group/coarse-trigger path routes `thwarting → 0.6 provocation : 0.3 nociception`, while
  the direct-appraisal path routes `0.6 : 0.2`; that extra nociception drives avoidance and holds the
  aggression drive at **~0.184 against the ~0.215 that crosses** — a **knife-edge just below threshold**.
  So the sub-threshold result is a **consequence of the (independently-defensible) stimulus ratio, not a
  tuned level**. The attack mechanism is **robustly demonstrated where it should be** — the closure test,
  strong *direct* provocation at age 2 → overt aggression. **No assertion is forced across the knife-edge**
  (an assertion that passes only at one tuned point is staging, not evidence — the same anti-brittleness
  discipline as the punishment-metric reframe). *Minor open calibration item (decoupled from any outcome):*
  the `0.6:0.3` vs `0.6:0.2` provocation:nociception inconsistency between the coarse-trigger and appraisal
  paths could be revisited as its own deliberate decision — justified by what goal-blockage's threat
  fraction *should* be and measured against everything it affects — **never** bundled into "so the route
  crosses." Changing a parameter to flip a result across a threshold is the pattern the build refuses.

Guardrails proven: `tests/test_aggression_pathway.py` asserts direction-only (provocation → aggress-drive
> avoid; plain threat → avoid; neutral → restrain, no leak; the differential shift; behavioural efficacy +
maturational restraint) plus a guard that `CeA→PAG/HYPdm` is inhibitory and unchanged.

**S1.4 social innate-wiring fold-in (batched here, Part 8 S16.7):** added `SR-SEPARATION`, `SR-PROXIMITY`,
`SR-REJECTION` to the `innate_wiring_catalogue` — documentary entries for social primary perturbations the
functional layer already wires (`IN-INTERO:contact_loss→PAG-PANIC`; `IN-SOMATO:affective_touch→NAc-shell`).
The loader reads only circuits/connections, so these change no dynamics; they close the S1.4 documentation
gap without confounding the aggression closure test.

## Substrate-social phase COMPLETE — the substrate is the sole engine (Part 6 step 3e, stage 5/5)

The Panksepp drive-engine is retired (`drives.py` deleted in full; `.brain` gone; the `is_cohesive`/
`is_aggressive` feature read-outs relocated to `substrate.social.is_cohesive_act/is_aggressive_act` and
consumed by `gamemaster`/`relations`; honest test reframes). **Verified against origin/main by the design
session.** The core organism is complete and it is the only engine: coded outcome-categories gone,
substrate the single source of structure, development converges, the phenomena battery passes, and the
OBS-3 aggression gap was closed by a grounded connectome fix (the v9 VMHvl pathway), not a thumb on the
scale. Every irreversible step (8b.4 category cut, the Executive retirement, this drive-engine cut) was
mapped, parity-gated, reviewed, and reversible-in-spirit until it wasn't.

> **Watching the sim — read this first.** An idle town skews **appetitive**: `approach`/`restrain`
> dominate, and the aversive/aggressive repertoire (`avoid`/`seek_comfort`/`aggress`) is largely absent
> from the idle stream. This is **correct, not a missing repertoire.** The town's default social contexts
> are mostly cooperative, and aggression is **provocation-gated by design** (the OBS-3 closure: reactive
> aggression is provocation-specific with a maturing STN brake). A cooperative town should not be full of
> fights; the full repertoire appears under the appropriate perturbations (threat→avoid, separation→
> seek_comfort, strong provocation in an immature agent→aggress), as the tests confirm. Anyone watching
> the live sim should be told this up front, or they will mistake correct behaviour for a defect.

*Deferred doc hygiene (with the UI-sync pass):* `sim_world/group_matrix.py:38` and `sim_world/README.md:45`
still describe the retired engine in prose ("own primary systems fire, the dominant one drives behaviour";
"dominant behavioural network") — stale architecture descriptions to update so they are not read as current.

## OBS-4 — the Arena earned its keep on day one (a methodological note, Part 6 S12)

*Recorded 2026-07 while building the Arena (Part 6 Step 4).* The Arena's **first act** was to expose a
**silent null in the inter-agent social channel that no single-agent test could have surfaced** — the kind
of finding a development-and-regression harness exists to catch.

The first dyadic loop routed each agent's perception of the other's act through the *speech intents*
(`speech.acts`: behaviour → intent → `appraisal_from_act`). But `approach` maps to the `ASSERT` intent,
whose appraisal dimensions (`goal_relevance`/`controllability`) `appraisal_to_substrate_input` **does not
read** — so a warm approach delivered **nothing** to the perceiver's substrate. Two agents talked through a
channel that dropped the most common social act, and the dyad died into mutual `restrain`. That was **not** a
substrate property or an honesty failure — it was plumbing that silently nulled the message. Had it shipped,
the Arena would have recorded "agents don't engage" as an emergent finding; it would have been an artifact.

Caught by **probing, not assuming** (measure before asserting). The fix: a **direct act→perturbation
perception mapping in the trigger vocabulary Things use** (`_ARENA_PERCEPTION`), fed via `felt_response` —
what a perceived act physically presents, never a valuation; `is_cohesive_act`/`is_aggressive_act` kept for
tie accrual only. Two channels, each at the fidelity its job needs.

*Why this belongs in the record:* when the study later asks "how much do we trust the Arena's dynamics?",
part of the answer is "it found, on day one, the one plumbing fault that would have invalidated them." The
Regime-B guard (two intact agents remain viable/settled/non-escalating in a closed loop — Part 5 S9.3 tested
in the multi-agent regime for the first time) closes the S12.6 closed-loop-instability concern with a test,
not a hope.
