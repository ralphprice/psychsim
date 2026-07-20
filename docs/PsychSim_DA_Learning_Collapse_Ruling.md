# The un-suspend refutation + the 80× DA-learning collapse — RULING. **The margin rule worked. The collapse is
# a real substrate defect and it is now the priority.**

**The margin check did exactly what the standing rule is for, and the outcome is the honest one. Then it
exposed something bigger than the test: DA-gated learning has collapsed ~80×, and I verified the reinforcer
pathway is intact — so this is a plasticity-mechanism defect, not a severed connection, and it is more
important than either suspended test. Rulings and the diagnosis scope.**

---

## 1. The un-suspend refutation — the margin rule worked exactly as designed

**The measurement:** the cue-value test reported "unexpected success" at age 4 solely because `+0.0036 > 0` —
but the paired gain is SMALLER than its own unpaired control (0.7×) and sign-unstable across development
(negative at ages 15 and 25). **An effect smaller than its control and sign-unstable is not a demonstrated
learning result.**

> **This is the standing measure-before-characterising rule working precisely. My reasoning was that the test
> reads DYNAMICS (within-agent `anticipatory_value`, not the observer double-gain), which made it a genuine
> CANDIDATE to survive — and that reasoning was sound. But I did not act on the reasoning; the ruling was to
> confirm the margin FIRST. The margin check is what separated candidate from survivor, in the honest
> direction. The dynamics-vs-construct distinction still holds — dynamics findings are the ones that CAN
> survive — but "can survive" is not "does survive," and this particular test is a candidate that the
> measurement refuted.** Both learning tests stay suspended; nothing un-suspended. **The rule caught what my
> reasoning alone would have gotten wrong — which is exactly why the rule exists.**

## 2. ★ The 80× DA-learning collapse — verified as a real substrate defect, and it is the priority

**The finding: `test_learning_requires_the_reinforcer_da_gating` expects a paired gain of ~0.3 (its own
comment); measured +0.0036. DA-gated learning has collapsed ~80×.** I verified where it is NOT:

- **The reinforcer pathway is structurally INTACT.** `IN-GUST:sweet → VTA` is `innate_reinforcer` at moderate-
  strong; VTA's DA efferents reach NAc-core (D1, moderate-strong), NAc-shell, OFC, dlPFC, vmPFC (all D1). **The
  reward circuit exists and the DA teaching signal has its pathways. This is NOT a severed connection.**

> **So the 80× collapse is NOT a connectome defect — the reinforcer can reach VTA and DA can reach its targets.
> That points at the build session's second hypothesis: the eligibility trace is not surviving the settle. This
> is a PLASTICITY-MECHANISM question, not a wiring one — the cue-reward temporal association is not being
> captured by the DA-gated plasticity rule, or the trace is being erased before the reinforcer arrives, or the
> settle dynamics have changed such that the pairing no longer produces the correlation the rule reads.**

**RULING: this is a real substrate-level defect and it is now HIGHER priority than the suspended tests — because
it is foundational.** If DA-gated learning has collapsed 80×, the substrate's REINFORCEMENT LEARNING is broken —
and the entire reward/value system, cue-value acquisition, and every learning-dependent developmental result
depend on it. **This is not two suspended tests; it is the mechanism those tests (and much else) rest on.** The
vacuous guard the build session found (`test_learning_requires_the_reinforcer_da_gating` passes by asserting the
unpaired change is `< 0.05`, trivially true when every change is ~0.005 — "a control that cannot fail because
the effect it controls for no longer exists") is the symptom; the collapsed mechanism is the disease.

## 3. The diagnosis scope (its own pass, diagnosis-first — I cannot complete it from the seed)

**This needs the plasticity dynamics traced, which the build session must do. The diagnosis:**

1. **Does the reinforcer actually elevate VTA/DA during pairing?** Measure VTA activity (and the DA output to
   NAc-core) under the reinforcer cue. If VTA doesn't rise, the innate-reinforcer drive isn't reaching it
   (despite the edge existing) — a settle/gain question. If it does rise, DA is being produced and the defect
   is downstream (the trace).
2. **Does the eligibility trace survive the settle window?** Is the cue-reward temporal association being
   captured by the DA-gated plasticity rule, or is the trace decaying/normalising away before the reinforcer
   arrives? **Check whether a recent change broke it** — the E-I homeostasis work, R8 competitive
   normalisation (which erodes weights toward a sum — could be erasing the potentiated cue-reward synapse), or
   a settle-timing change from the S56/Lump-13 builds.
3. **Is this a regression, and from where?** Did DA-gated learning produce ~0.3 at some prior commit? **If so,
   bisect what changed** — the collapse is large enough (80×) that it likely traces to a specific mechanism
   change, not gradual drift. The S56 plasticity-layer work (the clamp reversal, the homeostasis rulings) and
   the Lump-13 connectome surgery are the leading suspects for having perturbed the plasticity dynamics.

**Do NOT tighten the loose bound** — the build session correctly left it loose and loudly annotated;
re-scaling to the observed +0.005 magnitude would manufacture a green over a missing mechanism. **The bound
stays loose until the mechanism is restored, then it is set to the restored magnitude.** ✓

**The `OFC→VTA`/`OFC→NAc-core` ungrounded edges remain a suspect but are not sufficient** — the build session
is right that an 80× shortfall is too large for a `low`-band assumption edge alone (Stage 3's OFC gate reduced
DA only ~6%). **The OFC→DA grounding is still owed (it re-enables the dissociation test), but it is not the
cause of the 80× collapse.** Keep them separate: the collapse is its own diagnosis.

## 4. The vacuous-guard pattern — the systematic sweep is worth doing, scheduled after the ruled queue

**Three vacuous guards found in one day, all the same shape:** `OFC-GABA`'s gate check (derives the gate list
from the flag it validates), the throttleable `len > 20` bound, and this DA-learning control (bounds an effect
that has vanished). **The pattern: a test that reads the property it is meant to validate, or bounds an effect
that has since disappeared — a green certifying nothing.**

> **RULING: the systematic sweep is worth doing, and it is the test-suite analog of the audit's central
> finding. The audit found the OBSERVER instruments measure the manipulation into their own result; the
> vacuous-guard pattern is the TEST instruments certifying conditions that are trivially or circularly true.
> Both are "the instrument doesn't actually measure what it claims." The audit ruling ordered grounding the
> observer instruments; this sweep is the same discipline for the test guards.** Schedule it once the ruled
> queue clears — a pass over the test suite for guards that (a) derive their assertion from the property they
> check, or (b) bound an effect whose magnitude has changed such that the bound is now trivially satisfied.
> **Register it as the test-integrity sweep, the guard-side counterpart to the read-out re-derivation.**

---

## 5. Sequencing — the DA collapse moves up

**The DA-gated-learning collapse is foundational (reinforcement learning underlies the whole reward/value
system), so it moves ahead of the read-out re-derivation** — a read-out fix over a substrate whose learning is
broken would measure a broken substrate cleanly. Revised order:

1. **F4 margin fix — done.**
2. **age_window fix** — the hard-constraint violation; re-measure developmental claims after.
3. **★ Diagnose the 80× DA-learning collapse** (§3) — foundational; likely a plasticity-mechanism regression
   from the S56/Lump-13 work. Diagnosis-first, then ruling. **This is the new priority.**
4. **Finish/verify the selector build** + the freezing-column-driver diagnosis.
5. **Re-derive the six read-out sets** over live anatomy, remove the double-gain (after the effector is revived
   AND learning is restored).
6. **OFC→DA grounding** (re-enables the dissociation test — separate from the collapse).
7. **The test-integrity sweep** (§4) — the vacuous-guard counterpart to the read-out re-derivation.
8. **Fresh full gate on current main.**

> **The margin rule worked: my dynamics-reading made the cue-value test a candidate, and the measurement
> separated candidate from survivor honestly — it stays suspended, both learning tests unchanged. But it
> exposed the real finding: DA-gated learning has collapsed 80×, and I verified the reinforcer pathway is
> intact, so this is a plasticity-mechanism defect — the eligibility trace not surviving the settle, likely a
> regression from the S56/Lump-13 plasticity work. That is foundational — reinforcement learning underlies the
> whole reward system — so it moves ahead of the read-out re-derivation. Diagnose it first: does the reinforcer
> elevate VTA, does the trace survive the settle, and what commit broke it. Do not tighten the bound over a
> missing mechanism. And the three vacuous guards in one day are worth a systematic sweep — the test-side
> counterpart to the audit's instrument finding. The substrate's WIRING holds; a plasticity mechanism running
> on it has regressed, and that is the next thing to make honest.**
