# The final audit — RULING. **The substrate holds; the instruments that read it do not. Fix the instruments,
# re-measure, report what survives.**

**This is the most consequential review the project has received, and the build session verifying every
critical claim — including catching the stale-bank false alarm before relaying it — is the discipline working
at the moment it matters most. Before the item rulings, the correct reading of this audit, because it is easy
to read as catastrophic and that would be wrong.**

---

## 1. What this audit actually means — the best possible failure mode

**An independent reviewer, auditing for construct validity, found ONE pattern across Tier 1: the substrate is
more disciplined than the instruments that read it.** Findings 1–5 are the same failure — a measurement layer
that multiplies the manipulation into its own result, or reads upstream of a dead effector. **This is
structurally the best news the project could receive from a hostile audit, for a specific reason:**

> **The substrate — the hard part, grounded edge by edge over the entire project, defended by the honesty wall
> through every pass — HOLDS. The reviewer confirms it: "the live substrate path holds the line… real multi-
> candidate accumulator races over emergent drive… no situation→act rule anywhere," the arena is "the
> strongest file audited," scan_match and phenomena are "exemplary." What failed is the READ-OUT / OBSERVER /
> STUDY layer — the instruments that measure the substrate. And instruments are cheap to fix relative to the
> substrate they read.** A hostile audit that found the substrate fabricated would be fatal; a hostile audit
> that finds the substrate sound and the instruments naive is a to-do list, not a refutation.

**This is the two-role split and the substrate-first discipline vindicated: we spent the project making the
substrate honest, and an independent check confirms the substrate is honest — the debt is in the layer we had
NOT yet subjected to the same grounding discipline. The honest response is to apply that discipline to the
instruments now.**

## 2. The decisive verification — the emergent substrate findings are NOT invalidated

**The most important question: are the four emergent findings (Gross, Tremblay, Buckholtz, adolescent reward-
seeking) measured through the broken observer, or on substrate dynamics? I traced it:**

- **The temperament throttle DOES enter substrate dynamics** — `engine.py:196` and `:223` show `_gain`
  multiplies the actual drive propagation through the network, and `:240` gates the plasticity ceiling. **So
  the throttle genuinely shapes how the substrate develops and behaves. It is a REAL manipulation of the
  substrate, not merely an observer artifact.** (This is legitimate — a temperament that weakens a domain's
  output is a real developmental difference.)
- **BUT the observer then multiplies by the gain a SECOND time** — `observer.py:135`: `activity(c) * _gain(c)`.
  **The manipulation is applied once in the substrate (legitimate) and then RE-APPLIED in the read-out (the
  tautology). That double-application is the specific defect in finding 1.** The construct score collapses by
  the gain factor because the gain is counted twice — once in the dynamics it legitimately shaped, once again
  in the measurement.

> **This distinction is everything. Findings measured on substrate DYNAMICS (e.g. the aggression-pathway tests
> read `e.activity(...)` directly — the Tremblay trajectory, the provocation-specificity, the emergent drive
> races) are NOT double-gained and are NOT invalidated by finding 1. Findings measured through the OBSERVER's
> construct scores (CU, empathy, boldness, the classified outcomes) ARE compromised — by the double-gain AND by
> the dead-read-out-set problem (findings 4–5). So the audit does not erase the emergent substrate results; it
> erases the trust in the observer-derived CONSTRUCT scores and the classified outcomes, which is a different
> and more contained claim.** The emergent findings must be RE-VERIFIED on the corrected instruments, and the
> ones measured on dynamics will very likely survive; the ones that only ever existed as observer construct
> scores may not. That re-verification is the work.

## 3. RULINGS — the items needing the design session

### ★ URGENT — the F4 unexpected success (rule before anyone reads the gate as confirmation)
**The F4 label test is passing again, and per the audit NOT because the effect grew — the margin collapsed to
0.000158 (noise).** A naive green read would re-instate the claim I explicitly retracted, on a coin flip.
- **RULING: keep F4 retracted. Keep the `expectedFailure`, but CORRECT the test so an unexpected success
  cannot read as confirmation.** The test must assert the divergence is REAL (the margin is adequate — above
  the `_BLEND_MARGIN` 0.05) before treating a label difference as a result. **A label divergence at margin
  0.00016 is the argmax landing on noise — it must FAIL the "is this a real divergence" check, not pass as a
  success.** Wire `MindReadout.margin` (the documented-but-unused remedy) into the test: F4's claim is
  confirmed only if the classified outcome diverges AND the margin is adequate. Until then, F4 stays retracted
  and the test asserts the retraction (small effect, inadequate margin). **This also resolves the audit's
  finding 7 in miniature — the margin fields exist and are read by nothing; F4's test is where they must first
  be wired.**

### HIGHEST-PRIORITY REAL FIX — the age_window life-course bug
**`lifecourse.py:147` calls `develop()` without `age_window`, so every stage runs (0.0, 1.0) over span 18.0 —
the adulthood stage is lived at ages 0–18, and every maturation curve and plasticity schedule resets to
infancy at each stage boundary.** This is a direct violation of the never-compress-developmental-time hard
constraint, in the module that implements the life course.
- **RULING: fix this FIRST, before the read-out work.** Pass `age_window` per stage in `lifecourse.py` so each
  stage occupies its correct slice of the lifespan (childhood-home → early years, adulthood → adult years),
  and developmental mechanisms advance monotonically rather than resetting. **Every developmental result —
  including the F1–F4 dev-social results and any life-course-ordered claim (the harsh-then-warm-turn preset) —
  is measured through this bug, so nothing developmental can be trusted until it is fixed.** It is small, it is
  a hard-constraint violation, and it is upstream of everything else. **The build session's sequencing
  recommendation (age_window first) is correct — do that.**
- **Register: every developmental claim to date must be RE-MEASURED after the age_window fix** — the ordering
  bug may have inflated, deflated, or scrambled them (the S18 law suggests inflation is the likely direction,
  but this is measured-not-assumed). This includes re-checking whether the F1–F4 divergence survives correct
  developmental timing.

### The six read-out sets — re-derive, remove the double-gain, but DIAGNOSE THE DEAD EFFECTOR FIRST
**The read-out sets were renamed past a dead effector (the CeA split changed `CeA→CEl` as a pure string rename;
no set was pointed at the live output populations; `_OBS_AGGRESS` is anti-correlated with the attack signal
because it reads `CEl` (which suppresses attack) and `dPAG`≡0 while `VMHvl` — the actual attack locus — is in
no set).**
- **RULING: this is downstream of the Lump #13 selector work still in flight.** The read-out sets read a
  defensive output layer that is currently dead (vlPAG/dPAG/CEm-active pinned at 0) — which is EXACTLY what the
  merged Stage-BC selector build is meant to revive. **Do not re-derive the read-out sets over a dead effector
  — that would relocate the problem, as the build session correctly noted.** Sequence: **finish the Lump #13
  selector build (revive the defensive output), THEN re-derive the six read-out sets against the live post-
  split anatomy (CEm output populations for defensive output, VMHvl for attack), AND remove the double-gain
  (`observer.py:135` should read `activity(c)` — the dynamics already carry the throttle; do not re-apply it).**
  The read-out fix and the selector build are coupled: the selector gives the read-outs something live to read.

### CU/empathy identity, punishment_sensitivity, restraint, instrumental_aggression
- **CU ≡ 1 − empathy: report ONE, not both.** They are the same variable; any figure showing both reports one
  twice. **RULING: the observer returns one (empathy, or CU) and derives the other only if explicitly needed as
  its complement, clearly labelled as such — never as an independent construct.**
- **`punishment_sensitivity = 0.3 + 0.7·fear` is a hardcoded trait→outcome mapping — the banned pattern, as the
  headline learning result.** **RULING: replace it with the real `study.punishment_learning` yoked-control
  probe** (which the reviewer confirms is "a genuinely well-designed confound-canceller… just pointed at a dead
  read-out set"). The probe exists and is sound; wire it in (after the effector is revived, so it reads a live
  set). **The hardcoded formula is the same class of defect as the OFC→DA-inflated learning tests — a learning
  claim resting on something that isn't the substrate's actual learning. Retract the formula-derived result;
  re-measure on the probe.**
- **`restraint`'s age effect is an observer multiplier (raw substrate flat 0.231→0.283; the 5.6× is the
  scaffold curve); `instrumental_aggression` hardcoded to 0.0.** **RULING: these are the same disease as the
  read-out sets — authored effects in the instrument. Fold into the read-out re-derivation: the maturation of
  restraint should come from the substrate's developmental dynamics (now that age_window is fixed), not an
  observer curve; instrumental_aggression being structurally 0 must be either grounded from the substrate or
  declared absent (not silently bounding the meanness dimension).**

### OFC-GABA structural_element + the vacuous guard (finding 11)
- **RULING: this the build session can fix without further ruling** — add `structural_element: true` to
  OFC-GABA (it IS a gate, and without the flag a low-SEEKING seed throttles it and disinhibits OFC — the
  directional perversity we registered as closed, now reopened by the missing flag), AND fix the guard
  (`test_substrate.py:151`) to assert the gate class BY CONSTRUCTION (all cortical E-I interneurons are
  structural) rather than deriving the gate list from the flag it is supposed to check. **A guard that reads
  the property it validates is vacuous — assert the invariant independently.**

## 4. What the build session fixes without a ruling (accepted)
The stale comments and node names, the missing Stage-3 REGEN note, the citation/provenance corrections, the
missing selector tests, the OFC-GABA flag, and the gaps_register integrity (the type anomaly at [75], the
stale CeA/PAG names, the contradictions, the unregistered memory layer). **All accepted — these are record-
integrity and truth-in-documentation fixes.** ★ **But add one: the register needs the SAME discipline as the
substrate.** 155 flat prose strings with no ids, no status, and internal contradictions is itself a validity
risk (the register is the project's memory, and it is now unreliable). **Register a pass to give the
gaps_register structure (ids, status, supersede markers) — it is the record-integrity analog of the instrument-
grounding this whole audit calls for.**

## 5. Sequencing — the ruling

1. **The F4 test correction** (URGENT — before the gate reads as confirmation): keep retracted, wire the margin
   check so noise-margin divergence cannot pass as success.
2. **The age_window life-course fix** (highest-priority real fix): pass age_window per stage; it is a hard-
   constraint violation upstream of every developmental result. Re-measure developmental claims after.
3. **Finish the Lump #13 selector build** (already in flight): revive the defensive output layer, so the read-
   out sets have something live to read.
4. **Re-derive the six read-out sets** against the live post-split anatomy AND remove the observer double-gain;
   fold in restraint (from dynamics) and instrumental_aggression (grounded or declared absent).
5. **Replace punishment_sensitivity** with the yoked-control probe; **report CU or empathy, not both.**
6. **OFC-GABA flag + guard-by-construction; gaps_register structural pass.**
7. **RE-VERIFY the four emergent findings** on the corrected instruments — report which survive. (The dynamics-
   measured ones likely do; the observer-construct-only ones may not.)

> **The audit's one-line finding is correct and it is good news: the substrate is more disciplined than the
> instruments that read it. We grounded the substrate over the whole project and it holds under a hostile
> independent check — the debt is in the read-out/observer/study layer, which never received the same
> discipline. The emergent findings measured on substrate DYNAMICS are not invalidated by the observer's
> double-gain; they must be re-verified on corrected instruments, and will likely survive. The response is not
> alarm — it is to apply the substrate's grounding discipline to the instruments: fix the F4 noise-margin now,
> fix the age_window hard-constraint violation first, revive the effector via the selector build already in
> flight, then re-derive the read-outs over live anatomy without the double-gain, replace the hardcoded
> learning formula with the real probe, and re-measure. The substrate held. Now make the instruments worthy of
> it.**
