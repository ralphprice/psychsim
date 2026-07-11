# PsychSim — Outstanding Work Register (scope freeze)

**Purpose: stop functional drift.** This is the complete list of what is done, what remains, and what
is explicitly deferred. **Nothing outside this list gets built without a deliberate decision to expand
it.** If a new idea appears, it goes to "Parking lot" (§4) — it does not get built into the current
work. The intention is fixed; we finish it, we don't grow it.

Current head: `b328978` (v13 -- DRN 5-HT node + cortical inhibitory interneurons, 2.1b) on `origin/main`. Seed head: `v13`.

---

## 1. DONE — built, reviewed, on origin/main (do not reopen)

- **Core organism** — substrate, four matrices (social/environmental/group/self-reflection), 1/n
  plasticity, behaviour selection. Complete and validated.
- **Legacy fully retired** — Panksepp engine gone; substrate is the sole engine (stage 5).
- **Honesty #2** — coded outcome categories removed as causal primitives (8b.4).
- **Emergent-phenomena battery** — 5/5 emerge (adolescent risk, DA/satiety, negativity bias,
  ambivalent bond, punishment-for-one=reward-for-another). Two mechanism gaps closed, no seed edit.
- **Instrument suite:** developed-agent bank · parallel-instance harness · Arena · scan controller
  (search-for-effect + search-for-match) — all built, honesty-gated structurally.
- **Seed lineage:** v9 (aggression circuit, OBS-3 closed) · v10 (physical endowment + biological sex,
  IN-CONSPEC) · v11 (4 Allen afferents, honest signs) · **v12 (2.1a sign-convention upgrade — per-edge
  receptor-derived signs; 3 flips MeA→VMHvl/VP→LHb/BNST→VMHvl; v11's MeA→VMHvl "brake" retired; CLEARED,
  the heaviest review since the Panksepp cut)**. Each byte-additive or sign-only, reviewed.
- **UI console** — Phases 0–8 + accessibility. Tab shell, read-only Neural view over the live seed,
  clock/day-night, monitored-agent badges, face-only markers, pause fixed.

## 2. QUEUED — the finish line (build these, in this order, then STOP)

The intention is: **complete the CU study apparatus on complete regulatory anatomy, then run the
study.** Three items remain. Nothing else.

### 2.1 — the serotonin pass, split into two ordered passes (organism; DESIGN SPEC FIRST → review → build)

The 5-HT raphe spec (`PsychSim_v12_5HT_Raphe_DESIGN_SPEC.md`, on origin/main) discovered a prerequisite
that was not visible until it was written: **5-HT cannot be added honestly under the current
sign convention.** Serotonin's sign is receptor-determined and *opposite across targets* (5-HT1A
inhibitory on the attack area; 5-HT2 excitatory on the PFC controllers), so a nucleus-level `+1`-everywhere
dorsal raphe would assert the *inverse* of the biology on the aggression-regulation pathway. Ruled: fix
the convention first (design-session ruling, option **(C)**). So §2.1 is two ordered passes — this is a
reordering forced by a discovered prerequisite, **not** a new feature.

**2.1a — sign-convention upgrade — ✅ DONE, CLEARED (v12, `e33fb08`; the heaviest review since the
Panksepp cut).** `_sign()` is now per-edge, `f(source transmitter, cited dominant target receptor)`, sign
derived from a fixed `params.RECEPTOR_SIGN` pharmacology table (never written directly). 20 edges cited a
receptor → exactly **3 flips**: MeA→VMHvl −/+ (glutamatergic aggression projection, MODERATE — mixed-nucleus
ambiguity flagged), VP→LHb −/+ (glutamatergic, HIGH — closes the fidelity gap), BNST→VMHvl +/− (GABAergic).
v11's MeA→VMHvl "brake" **retired** as an artifact; one authorised scaffold-weight recalibration
(MeA→VMHvl 0.5→0.1, magnitude only, so it primes-not-drives — provocation-specificity re-proven). Ambiguities
documented not fudged (α2A-PFC kept + on fallback; SNc→DStr D1/D2 near-arbitrary; undetermined edges on
fallback). Full re-verification green (v9 closure, E5 floor, DA, phenomena 5/5, golden 0-classification-flips,
library regrown). **Caveat carried forward:** the MeA→VMHvl flip rests on a MODERATE-confidence receptor
determination (MeA is genuinely mixed); v12's "conspecific cue primes attack, provocation-gated" is a
candidate, not a settled fact — revisit if MeApd-vs-MeA projection-specificity sharpens.

**2.1b — DRN (5-HT) node + missing cortical inhibitory interneurons — ✅ DONE, on origin/main (v13, `b328978`); awaiting design-session full review.** The DRN 5-HT node (receptor-signed efferents — opposite signs across targets; DRN->VTA inhibitory; the PFC->raphe loop self-limiting through a DRN-GABA GAD2+ interneuron; low-5-HT -> more provoked aggression emerges as a scan_match target). Plus the missing local inhibitory interneurons the pass surfaced: vmPFC-GABA + dlPFC-GABA (the two DEMONSTRATED self-saturating PFC circuits), all silence-tested. dmPFC declined (downstream-resolved) -> scheduled below. Purely additive (0 cut); coherence: fixing vmPFC saturation also restored a healthy DRN tonic AND a proper adolescent-risk inverted-U, no tuning. Full suite 518 green.

**Two SCHEDULED future passes this pass created (deliberate additions, not drift -- the substrate growing to completeness in the right order):**
- **Systematic cortical-E/I pass** -- the other cortical pyramidal circuits (dmPFC, OFC, dACC, and the rest) also lack their local PV/SST interneurons; their current afferent balance masks it. Their real interneurons enter here, grounded + reviewed, as a batch. Any afferent change to a masked cortical circuit must re-check for saturation.
- **Adolescent-risk maturation** -- whether the PFC-interneuron developmental trajectory (delaying the interneuron relative to its pyramidal circuit -> an adolescent window of immature prefrontal control) needs wiring. The adult substrate already produces the adolescent-risk inverted-U on its own, so this is a refinement to test, informed by the shape-test result -- a deliberate pass, not a gap.
- **Proactive inhibitory-interneuron audit** (design-session note) -- two passes (DRN, PFC) each surfaced a saturating circuit missing its inhibitory partner; the substrate has excitatory long-range projections well-represented and local inhibitory interneurons under-represented. Worth a deliberate systematic audit *after the study* rather than discovering them one saturation at a time.
- **Why required, not optional:** the substrate lacks its principal aggression/impulsivity *regulating*
  neuromodulator. Measuring aggression regulation without 5-HT is measuring a regulated system with the
  regulator absent — cherry-picking-by-omission (the v11 error, one level up).
- **Scope:** dorsal raphe (5-HT) node + serotonergic projections (aggression circuitry, amygdala, PFC,
  striatum) + the top-down regulation loop (vmPFC/OFC/LHb→DRN) + `NEUROMOD_SOURCE["5HT"]=["DRN"]`.
  Median raphe (MRN) DEFERRED (§4). Existence/direction only; weights SCAFFOLD; receptor-signed via 2.1a;
  the 5-HT dampening of impulsive aggression must EMERGE from the signed loop, never coded, and is a
  `scan_match` target.
- **Standard:** real verified citations, byte-additive (v11→v12 for 2.1a re-sign, →v13 for the node, or
  one combined v12 — a build-sequencing detail for the 2.1a/2.1b specs), one review each.
- **Discipline note:** 2.1b is the *only* new-anatomy organism change queued. After it, the organism is
  frozen for the study.

### 2.2 — CU-study control surface (instrument; spec exists: `PsychSim_CU_Study_Spec.md`)
- Can be built **in parallel with 2.1** — it's plumbing on the scan controller and does not depend on
  the raphe node existing.
- **Three pieces:** (a) the backtester = the scan controller applied to a CU objective (measured
  signature or held-out clinical profile, target age ~18, family/environment context); (b) validated-
  CU-seed save/load (neutral name `CU-Profile-A`, transparent/editable config, provenance-carrying,
  `candidate_hypothesis`/`corroboration:false`); (c) spawn integration (validated seeds in the dropdown
  — a NEW seeding path, NOT a replacement for the already-removed `fearless` presets; see §3).
- **Honesty (already specced):** objective is measured-or-held-out, never a drawn CU target; family
  variables are perturbation patterns, never coded effects; a config earns the CU name only by
  validation.
- **5-HT / sign-upgrade dependency:** a CU seed validated *before* BOTH the sign-convention upgrade (2.1a)
  AND the DRN node (2.1b) land must carry `validated_on: pre-5HT-substrate (pre-sign-upgrade);
  aggression-regulation conclusions provisional` in its provenance — the sign upgrade changes the
  aggression circuit's dynamics too, so both are prerequisites for non-provisional aggression findings.
- **FIRST STEP before build:** commit `PsychSim_CU_Study_Spec.md` to origin/main (it is currently
  local-only — a sync gap) and answer the four open questions in its §9.

### 2.3 — UI redundant-artifact removal (the cleanup you asked for; §3 below is the concrete list)
- Small, bounded, no new features. Remove what the redesign superseded and the deprecated study
  interface. Do this as its own commit so it's legible.
- **IN PROGRESS:** the deprecated temperament presets + `respawn` `fearless_frac` server path are
  DONE (395e813, its own commit). Remaining §3 items (dead `neuraldesigner` route, stale
  Panksepp-as-current docstrings, orphaned components) still to audit.

## 3. UI redundant artifacts to remove (concrete, bounded — no new UI)

- **Deprecated temperament presets** (`typical` / `fearless` / `fearless (calc.)`) and `respawn`'s
  `fearless_frac` server path — **REMOVED (395e813, 2026-07-11)**, ahead of the CU dropdown, per the
  researcher's direction. Rationale: a temperament preset implies a seeded OUTCOME, which the substrate
  does not do; the population selector falls back to standard roles (a standard agent is seeded, its
  disposition MEASURED, never selected), so there is **no seeding gap** — superseding the earlier
  "keep until 2.2c" note. **Scope removed:** the UI dropdown (`PopulationSection`), the `add_person`
  temperament arg (UI + server), and the server `respawn` `fearless_frac` API path. **UNTOUCHED:** the
  sophropathy MODULE's `fearless_frac` (its study spawn knob, exercised across the suite via
  `live_spec`) — out of this bounded scope. Grep-clean: no `fearless` in `ui/src` or the server spawn
  path; no temperament-preset option in the profile selector.
- **The dead `neuraldesigner` sandbox route**, if still present anywhere — the live Neural view (read-
  only over the seed) replaced it. Confirm it's gone or drop it.
- **Any stale docstrings** still describing the retired Panksepp engine as current (audit
  `group_matrix.py`, `README.md`, `observer.py` prose — provenance comments recording the retirement
  stay; anything implying the engine is *live* goes).
- **Orphaned components** superseded by the tab redesign (confirm `Controls.tsx`, `MatrixEditor.tsx`,
  `NeuralEditor.tsx` are deleted, not just unimported).
- **NOT removed:** provenance docstrings stay (they're history, not staleness); the descriptive
  temperament read-outs (`Inspector`, `DevelopmentCohortTab`, `LibrarySection` — showing a subject's
  *given* temperament) stay (they measure/display, they don't select an outcome). *(The deprecated
  presets themselves WERE removed ahead of the CU dropdown — 395e813 — the standard-roles fallback
  leaves no seeding gap.)*

## 4. DEFERRED / PARKING LOT — real, recorded, NOT built now (require a deliberate decision to promote)

These are legitimate but out of the current scope. They do not get built into the finish-line work.
Promoting any of them is an explicit, separate decision — not a drift.

- **Development peer-perception pathway** — who a developing agent encounters (peer-sampling model).
  Physical perception currently fires Arena-only; extending it to development needs the sampling model
  specced and reviewed (it could encode who-meets-whom). Deferred.
- **Connection-level throttling** (S4.1) — the throttle module manipulates nodes; edge-level was
  deferred. `manipulation_scope: "nodes only"` travels on scan results until/unless built.
- **PH-AGILITY / PH-SENSORY as bearer capacities** — ruled out of the social channel; may enter later
  as bearer-capacity parameters (a different mechanism). Deferred.
- **VP→LHb sign fidelity** — ✅ **CLOSED** (resolved by the 2.1a convention upgrade, v12: the glutamatergic
  LHb-projecting population is signed excitatory from its receptor, −/+, not by override). No longer open.
- **Bank version-guard (bank-hardening)** — `_restore_engine`'s length-guard catches a *connection-count*
  mismatch but NOT a *sign-only* version change (a v11-grown bank restored into v12 loads without a stale
  flag even though the sign convention changed under it). For now a **cache regrow** under each new seed
  version covers it (done for v12). Add a **version-stamp** to the snapshot + a version check on restore
  when convenient, so a future sign/param-only version mismatch is caught by a version check, not a length
  check. Deferred (small, non-blocking).
- **Median raphe (MRN) node** — the second serotonergic source, more implicated in anxiety/hippocampal
  tone than aggression. A separate, smaller addition than the DRN (2.1b). Deferred; promote only if the
  study needs it.
- **Other neuromodulatory systems we may have missed** — the register is not closed; as we learn of
  systems that affect the circuitry we add them (grounded, cited, whole-system, not the subset that
  suits a hypothesis). None currently identified beyond 5-HT (2.1) and MRN (above). Deferred by
  definition until identified.
- **Real held-out field-data patterns** — for search-for-match / the CU study's clinical-profile
  objective. Researcher-supplied, properly sourced, `not_used_in_calibration`. Not synthetic. Pending.

## 5. The rule that keeps this from drifting

1. **The finish line is §2 (three items) → then run the study.** That is the whole remaining
   intention.
2. **New ideas go to §4 (parking lot), not into §2.** Promotion is a deliberate, separate decision.
3. **Organism changes are frozen after 2.1b** (the DRN node; 2.1a the sign upgrade precedes it). No
   further seed versions before the study without an explicit re-opening.
4. **Every change is byte-additive, cited, reviewed, and confirmed on origin/main** — the discipline
   that held eleven seed versions.
5. **When §2 is done and the study is run, the build is complete.** Resist "one more system" unless it
   is genuinely identified as missing (§4) and promoted deliberately.
