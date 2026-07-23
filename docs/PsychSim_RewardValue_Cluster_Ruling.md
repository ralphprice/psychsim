# Reward/value cluster — RULED. **And a redirect: the prototype blocker is missing from the queue.**

---

## 1. ★ REDIRECT — the graded profile is not on the todo list, and it is item #1

**The declared next step was: wire the graded profile through the study output** (`LifeResult` keeps the
profile; `classify` returns label + margin + runner_up). **It does not appear in the queue.** The queue instead
proceeds to the integrity sweeps — which the prototype plan explicitly listed as *after*, not blocking.

**This matters because the sweeps are cleanup and the graded profile is the prototype blocker.** The bare argmax
has now destroyed one finding (Buckholtz), hidden another (F4's +0.0088), exaggerated a third, and broken a
fourth test. **Until the study reports the graded profile with its margin, every result the prototype produces
is untrustworthy — including the ones the sweeps would be tidying around.** It needs no design ruling; it is
mechanical.

**RULING: the graded-profile wiring goes ahead of the sweeps.** Do it, then sweep.

## 2. The reward/value cluster is ONE question, not three

**All three "coupled" items are downstream of the adult-plasticity floor, and the literature gives it a
grounded ratio.**

**The grounded relation:** in simultaneous juvenile-vs-adult comparisons across multiple assays, adult plasticity
shows **≤50% of the magnitude of the juvenile critical period**, with a higher induction threshold (4d juvenile
vs 7d+ adult). **Adult plasticity is on the order of HALF the developmental peak — not a thousandth.**

> **★ The current floor is `EXP_PLASTICITY_FLOOR = 0.001`. If the model's adult:developmental learning-rate
> ratio is anywhere near that, the floor is two to three orders of magnitude more restrictive than the
> literature's ratio — and that single fact would explain ALL THREE of the cluster's observations at once:**
> - adult punishment learning ~0.002 (deficit ~0.998),
> - `anticipatory_value` cue-alone ~0,
> - the adult DA-gated paired gain +0.0036.
>
> **Three separate near-zero absolute adult-learning results, one candidate cause.**

**This is a coherent story, so it gets a discriminating measurement rather than a ruling:**

**MEASURE: the model's adult:developmental learning-rate ratio.** Run the same paired-learning protocol at the
developmental peak and in the adult, and take the ratio.
- **If the ratio is far below the grounded band (order ~0.5):** the floor is the cause, grounding it to the
  literature's ratio is the fix, and **all three observations should move together** — which is itself the
  confirmation.
- **If the ratio is already in band:** the floor is not the cause, and the three observations need separate
  explanations. That is also a result.

**Then ground the floor to the measured ratio** — set it so the adult:developmental ratio lands in the grounded
band, not so any test goes green. Ground the relation, derive the value; same discipline as the E-I gains.

## 3. `punishment_sensitivity` reference scale — do NOT invent one

**Two reasons:**
1. **"Sensitivity" is a differential property**, not an absolute magnitude — how much behaviour changes per unit
   punishment. **The paired-vs-yoked differential is the construct-valid measure, it is dimensionless, and it
   needs no reference scale.** You already wired the raw differential; that is correct. Report the 2×
   discrimination as the construct.
2. **The saturation near deficit=1 is probably a SYMPTOM of the floor**, not a scaling problem. Inventing a
   `[0,1]` reference to make a saturated absolute readable would be scaffolding around a grounding defect.

**RULING: keep the raw differential, invent no reference scale, and re-measure punishment learning AFTER the
floor is grounded.** If it de-saturates, the scale question dissolves. If it does not, revisit then — with a
grounded reference or none.

## 4. The R8 cue-alone hypothesis — same answer

**Re-measure it after the floor grounding.** The share grows with pairing (+0.06–0.11, memory present in the
ratios) but cue-alone evokes ~0 — consistent with a proportionally-correct weight whose *absolute* magnitude is
too small to drive the target. **That is what a 500×-too-restrictive floor would produce.** If the floor
grounding restores cue-evoked anticipatory value, the hypothesis is answered. If it does not, then there is a
genuine functional gap — a memory preserved in ratios that cannot be expressed — and that gets its own
diagnosis.

---

## 5. Order

1. **Graded-profile wiring** (prototype blocker, mechanical, no ruling needed) — including re-stating the
   affected claims on the graded output.
2. **Measure the adult:developmental learning ratio**, ground the floor to it, and re-measure the three
   observations together.
3. **The integrity sweeps** (both shapes) + the `gaps_register` structural pass.
4. **Batch the gate** — observer Tier-1 (`dc0070f`) + the floor grounding + sweep fixes, one cycle.
5. **Then the structural-zero experiments and the first end-to-end prototype run.**

> **The three cluster items are one question: the adult-plasticity floor is a scaffold at 0.001, the literature
> puts adult plasticity at roughly half the developmental magnitude rather than a thousandth, and that single
> discrepancy would explain the near-zero punishment learning, the cue-alone null, and the small DA gain
> simultaneously. Measure the ratio, ground the floor to it, and watch whether all three move together — that
> is the confirmation. Invent no reference scale for a saturation that is probably the floor's symptom. And put
> the graded-profile wiring first: it is the prototype blocker, it needs no ruling, and it is not on the queue.**
