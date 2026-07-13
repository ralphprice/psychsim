# HSO — Claude Code handover: M1 + M2 (the audit-first diagnosis)

**Sealed design authority: `docs/PsychSim_Homeostatic_SelfOrganization_SPEC.md`.** Build against it.
This handover covers **only M1 and M2** — the audit-first hard gate (sealed ruling #1). M3/M4/M5 are
NOT scoped yet; their design is determined by what M1/M2 find. **Do not build any rebuild mechanism.
This phase is DIAGNOSIS: measure what's real, report, stop.**

Roadmap context: v14 Phases 2–5 are on hold behind HSO. The VTA reward-completion pass is downstream of
HSO. This is the next work. The organism on origin/main is v14 Phase 1.1 (83 circuits / 180 connections).

---

## 0. What this phase IS and IS NOT

- **IS:** measure whether the substrate's existing homeostatic machinery is real or hollow. Produce two
  committed ledgers (the setpoint/timescale/weight grounding audit, and the weight-plasticity crux
  test). Report findings. Change NO values, build NO mechanism.
- **IS NOT:** fixing anything, grounding setpoints, strengthening homeostasis, re-deriving results.
  Those are M3+, scoped *after* M1/M2 report. If you find yourself wanting to fix a fitted setpoint or
  strengthen R4-HOMEO — STOP; that's M3, and M3 isn't scoped until this lands.

**The principle being tested (spec §0):** a value may be fixed only if it is a property of the SUBSTRATE
(setpoints, time constants, signs, structure — grounded), not the STATE (weights — plastic,
self-organizing). The audit asks, per value: is this an honestly-grounded substrate property, or a
frozen/fitted value masquerading as one?

---

## 1. M1 — the fixed-values audit (setpoints, time constants, weight-bases)

Classify every fixed value into: **measured / class-grounded / scaffold-honest / FITTED.** The FITTED
ones are the fudges. Produce a committed per-value ledger. **Run this against the seed as data — do not
change the seed.**

### 1.1 Setpoints (all 83 `homeostatic_setpoint`)
**Known starting fact (already observed):** all 83 setpoints are currently the identical value **0.1**
— a single uniform placeholder, not 83 grounded per-population target rates. So the audit's finding is
partly visible already: the setpoints are **uniform-scaffold**. The audit's job is to make this precise
and honest:
- Confirm the uniform-0.1 state and record it as a **disclosed scaffold** (a uniform setpoint is a
  defensible *starting assumption*, but it is NOT grounded per-population biology).
- For each population, research whether the literature gives a **measured target firing rate** or a
  **class property** (tonic-pacemaker vs. phasic vs. interneuron rates differ — e.g. DA pacemaker tonic
  rate is a class property even where the absolute is scaffold). Record what grounding is *available*
  per population — but **do NOT change the values** (that's M3). The deliverable is the *audit*: which
  setpoints could be grounded, which are class-grounded, which remain honest-scaffold.
- **This directly explains F1** (the VTA pacemaker failure): VTA needed a *different* setpoint than the
  uniform 0.1, and the uniform scheme couldn't represent it. The audit confirms real populations have
  *different* target rates; the uniform 0.1 is the simplification. Record F1 as evidence.
- **No quota (sealed ruling #2):** the honest target is every setpoint classified into measured /
  class-grounded / scaffold-honest — **none fitted**. How many are fully groundable is whatever the
  literature supports.

### 1.2 Time constants (`time_constant_tau_ms`, `eligibility_trace_tau_ms`)
**Known starting fact:** `time_constant_tau_ms` is near-uniform (78×200ms, 4×100ms, 1×300ms) — again a
placeholder, not the measured mechanism-differentiated hierarchy. Audit against the measured hierarchy
(spec §4): ionotropic (~1.7–50ms) ≪ metabotropic (150ms–2.5s) ≪ neuromodulatory (10s–min) ≪ plasticity.
Classify each: does its tau reflect its mechanism (ionotropic/metabotropic/neuromodulatory), or is it
the uniform 200ms placeholder? Record which are mechanism-grounded vs. placeholder. **Do not change
them** (M3). **This is the root of F2:** the plasticity gate conflated tonic (neuromodulatory, slow) and
phasic DA because the timescale hierarchy is placeholder-uniform, not mechanism-differentiated.

### 1.3 Weight-bases (all 208 `default_weight_basis`)
**Known starting fact (already observed):** the weight-basis distribution is **anatomy: 114,
assumption: 74, innate_reinforcer: 19, literature: 1.** So **74 of 208 edges (36%) self-declare their
basis as `"assumption"`** — these are the self-admitted guesses, the prime fudge candidates. And weights
are symbolic bands (`low`/`moderate`/`moderate-strong`/`strong`), NOT precision-fitted decimals — which
is *more* honest than false precision (no `0.447` threaded into a window), but the `assumption`-basis
ones are still ungrounded.
- Produce the per-edge basis ledger: edge → weight-band → basis-class (anatomy/assumption/
  innate_reinforcer/literature).
- Flag all 74 `assumption`-basis edges as the **ungrounded-weight set**. (Under HSO these become plastic
  and self-organize — so "ungrounded weight" is *less* alarming than it sounds, because the weight won't
  be *set* at all after M3; but the audit must surface them so M3/M4 know which weights were never
  grounded.)
- **Do NOT change any weight.** M3 makes weights plastic; this phase only *counts* their current bases.

### 1.4 M1 deliverable
A committed ledger (e.g. `docs/hso/M1_fixed_values_audit.md` or a structured data file):
per-setpoint, per-timescale, per-weight → its grounding class. Headline counts: setpoints
(measured/class/scaffold/fitted), timescales (mechanism-grounded/placeholder), weights
(anatomy/assumption/innate/literature). Plus the F1 and F2 root-cause confirmations. **Report; do not
remediate.**

---

## 2. M2 — the weight-plasticity crux test (does the substrate ACTUALLY self-organize?)

This is the decisive test. The spec's central suspicion: the machinery *exists on paper*
(`homeostatic_setpoint`, R4-HOMEO — `homeo_factor(mean_activity, setpoint) = 1.0 - rate*(mean_activity -
setpoint)` at `plasticity.py:105`, applied every `HOMEO_EVERY` steps at `engine.py:196`) but may be
**present-but-hollow** — too weak, or dominated by the seed default weights, so weights are *nominally*
plastic but *effectively static*. The VTA weight threading into a narrow window is the signature of an
effectively-static weight (a genuinely homeostatic weight can't be threaded — the system would move it).

### 2.1 The test (spec §2.3)
For a representative set of weights across classes (and ideally all 208):
1. Develop an agent to a stable state (the normal developmental run).
2. **Perturb a weight** away from where development left it.
3. Continue development.
4. **Measure: does R4-HOMEO pull the circuit's activity — and the weight — back toward the
   setpoint-consistent value, or does the weight stay perturbed?**
   - **Self-corrects** → weights are genuinely plastic (homeostasis is real).
   - **Stays perturbed** → weights are **effectively static** (homeostasis too weak / seed default
     dominates) — the machinery is hollow.

### 2.2 The complementary test (does the seed default dominate?)
Spawn two agents with **different default weights** on the same edge; develop both identically. If they
converge to the *same* developed weight → the seed default is just a starting point (good, plastic). If
they stay at *different* developed weights determined by their seed defaults → the seed default
**dominates** and development isn't organizing the weight (hollow).

### 2.3 What M2 decides (and why it gates everything)
- If **most weights self-organize** → HSO is a **targeted repair** (strengthen where hollow), M3 is
  small.
- If **most weights are effectively static** → HSO is a **genuine rebuild** (the homeostatic rule needs
  real replacement), M3 is large.
- **M2 also decides the spawn-default scheme (sealed ruling #3):** if weights self-organize regardless
  of start → fully-uniform spawn works; if the start-point matters → class-uniform. This is an M2
  *output*, not a pre-commitment.

### 2.4 M2 deliverable
A committed report (`docs/hso/M2_weight_plasticity_crux.md`): the list of **effectively-static weights**
(perturbation doesn't self-correct) vs. **genuinely-plastic weights**; the seed-default-dominance
result; and the verdict — **targeted-repair or full-rebuild**, with the spawn-default recommendation
(uniform/class-uniform) that the evidence supports. **Report; do not build M3.**

---

## 3. Honesty + process (unchanged from the whole project)

- **Full suite is the gate, not inline checks.** (Twice this session, inline checks missed what the full
  suite caught.) Any change (even audit tooling that touches the engine) → full suite green before
  clearing. But note: **M1/M2 should change NO substrate values**, so the suite should stay green
  throughout by construction — if it goes red, you've changed something you shouldn't have.
- **This is a DUAL audit.** The reviewer runs M1/M2 *independently against the remote* and reconciles —
  an audit for fitting cannot be certified by the entity that may have fitted. Push your ledgers; the
  reviewer re-derives them.
- **Change nothing, fix nothing, build nothing.** Diagnosis only. The temptation to fix a fitted
  setpoint or strengthen R4-HOMEO the moment you find it is the exact "build before you know" error the
  audit-first gate exists to prevent. Surface it in the ledger; leave it for M3.
- **Commit the ledgers to `docs/hso/`; push; stop for reviewer verification before any M3 scoping.**

---

## 4. Hand-off note (for the implementation session)

> **HSO M1 + M2 — the audit-first diagnosis.** Design authority:
> `docs/PsychSim_Homeostatic_SelfOrganization_SPEC.md` (sealed). This is DIAGNOSIS ONLY — measure what's
> real, produce two committed ledgers, change/fix/build NOTHING. M3+ is scoped only after this reports.
>
> **M1 — fixed-values audit.** Classify every setpoint (all 83, currently uniform 0.1 — a placeholder,
> not grounded per-population rates), every timescale (currently near-uniform 200ms — a placeholder, not
> the measured ionotropic≪metabotropic≪neuromodulatory hierarchy), and every weight-basis (208 edges:
> 114 anatomy, **74 assumption** = the ungrounded set, 19 innate_reinforcer, 1 literature) into
> measured/class-grounded/scaffold-honest/**FITTED**. Confirm F1 (VTA needed a non-uniform setpoint) and
> F2 (the timescale hierarchy is placeholder, conflating tonic/phasic DA) as root-cause evidence. NO
> quota; NO value changes. Ledger → `docs/hso/M1_fixed_values_audit.md`.
>
> **M2 — the weight-plasticity crux (the decisive test).** For weights across classes: perturb a
> developed weight → does R4-HOMEO (`homeo_factor`, plasticity.py:105) pull it back (genuinely plastic)
> or does it stay perturbed (effectively static / hollow)? And: do two agents with different seed
> defaults on an edge converge (default is a start) or stay split (default dominates)? **Verdict:
> targeted-repair or full-rebuild** — this gates M3's size. Also outputs the spawn-default recommendation
> (uniform vs. class-uniform, sealed ruling #3). Ledger → `docs/hso/M2_weight_plasticity_crux.md`.
>
> **Honesty/process:** full suite is the gate (but M1/M2 change nothing, so it stays green by
> construction — red = you changed something you shouldn't); dual audit (reviewer re-derives
> independently against the remote); change/fix/build NOTHING (the urge to fix on discovery is the error
> the gate prevents). Commit ledgers to `docs/hso/`, push, STOP for reviewer verification before M3 is
> scoped.
