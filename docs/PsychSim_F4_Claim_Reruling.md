# F4 — claim-level ruling. **The mechanism survives; the LABEL-reordering claim does not. Report F4 on the
# profile, not the argmax.**

**This is the S18 law biting the study layer's most important result, and it is a claim-level retraction, not
a test fix — so it is mine. I read the exact test structure before ruling, because the distinction between what
survived and what died determines F4's honest claim. The distinction is clean, and it points at a resolution
that is more than "suspend the test." Here it is.**

---

## 1. What survived vs what died — verified against the test file

**`test_dev_social.py` has a LAYERED set of assertions, and they did not all break. Precisely:**

**STILL PASSING (F4's mechanism, entirely intact):**
- `test_directed_relationships_accumulate` — relationships form, directed.
- `test_relationships_accumulate_and_differentiate` — warm/wary **differentiate** emergently (affects not
  uniform).
- `test_history_shapes_behaviour` — the act distribution differs by relational history.
- the substrate-divergence assertion — `assertNotEqual(sa.engine.weight, sb.engine.weight)` — **the substrate
  still diverges by history.**
- the recognition-not-valuation keystone, familiarity-gating, the warm/wary-arm routing — all green.

**BROKEN (one test, the strongest downstream claim):**
- `test_classified_outcome_diverges_by_relational_history` — asserts
  `assertNotEqual(base.classification, rel.classification)`, i.e. **that the divergence propagates all the way
  to a different classification LABEL.**

> **So F4's MECHANISM is fully intact — relational history demonstrably shapes the developing substrate, moves
> affiliation +0.0088 in the predicted direction, and produces differentiated emergent relationships. What
> died is only the strongest DOWNSTREAM claim: that the substrate divergence is large enough to REORDER the
> discretized classification label. It is not, on the corrected substrate — the label margin is now 0.0021
> (knife-edge between social_cognition and executive), and a +0.0088 affiliation shift cannot reorder domains
> from there.**

## 2. This is the S18 law, third time this session — and it names the real issue

**The classified-outcome divergence (~50% of seeds, executive → reward_approach) was measured on the
over-driven, ungated cortex. The grounded gate family deflates it to zero** — the same shape as the divergence
sentinel (0.0585 → 0.0401) and the learning tests (+0.0008 → −0.0013). **Every grounded fix this pass deflated
an effect the missing inhibition was inflating.** F4's headline label-reordering was propped up the same way.

> **But there is a second finding underneath, and it is the important one: the classification LABEL is a bare
> argmax over a razor-thin margin (0.0021), and this is the SECOND time that argmax has caused trouble.** The
> first was the psychopathic→reward_approach flip (P2a era), where a 0.05 margin made a grounded shift look
> like a fragile hard flip. **Now the same argmax makes a real, correctly-directed effect (affiliation +0.0088)
> INVISIBLE, because it doesn't reorder the top of a knife-edge profile.** The argmax was flagged then as a
> lossy discretization of a graded profile; F4 is the case that proves the cost. **F4's effect is real and
> visible in the PROFILE (the graded domain shifts) and invisible only in the argmax LABEL.**

## 3. RULING

### (a) Suspend the label-divergence test as expectedFailure, with the finding and resolution condition.
`test_classified_outcome_diverges_by_relational_history` → expectedFailure, recorded: *the classified-LABEL
divergence at ~50% of seeds was inflated by the cortical over-drive (S56); on the grounded substrate the label
margin is knife-edge (0.0021) and the real affiliation effect (+0.0088) no longer reorders the label. The
mechanism survives (substrate diverges, relationships differentiate, affiliation moves in the predicted
direction). Resolution condition: the label-divergence may re-emerge if a later grounded effect is larger, OR
if the classification read-out is changed to report the graded profile/margin rather than a bare argmax label
(see (c)).* **Do NOT delete it — it holds a real claim that is currently false on the corrected substrate and
may become true again.**

### (b) Restate F4's claim honestly and precisely.
**F4's demonstrated result is now:** *relational history, accumulated through emergent mutual exchanges over a
moral-environment childhood, demonstrably shapes the developing substrate — the weights diverge, relationships
differentiate warm/wary emergently, and affiliation moves in the predicted direction (+0.0088, warm childhood →
more affiliation) — traceable to the relationship history alone (the moral-environment stream is byte-
identical). It does NOT currently reorder the discretized classification label, whose margin is knife-edge.*
**The substrate-level and profile-level divergence is the demonstrated result; the label-level divergence is
not.** This is a weaker claim than F4 originally made, and it is the honest one. **The developmental-integration
mechanism is real and confirmed; the claim that it flips the classified outcome is retracted.**

### (c) ★ The real fix is the read-out, and it connects to a standing finding.
**The argmax classification has now caused trouble twice. The honest resolution is not only to suspend F4's
label test — it is to report F4's result on the PROFILE, where the effect is real and visible, rather than on
the bare label, where a knife-edge margin hides it.** F4's affiliation +0.0088 IS the result; the graded
domain profile shows relational history shaping the developing mind exactly as claimed. **Register: the
classification read-out should expose the graded profile and margin (the `runner_up`/`margin` fields discussed
in the P2a-era ruling), and F4 — and the study's developmental claims generally — should be measured on the
profile shift, not the argmax label.** This is the second demonstration that the bare argmax is the wrong
instrument for a graded substrate; F4 makes the case decisively. **This is not fitting to a wanted result — it
is measuring the real, grounded effect on the graded quantity that carries it, rather than on a discretization
that discards it.**

### What NOT to do (both would be fitting to a wanted result):
- **Do NOT weaken S56 to restore the label divergence.** S56 is grounded; the deflation is the honest
  correction. ✓ (your recommendation)
- **Do NOT re-base the test to a seed that still flips.** Cherry-picking a seed where the knife-edge happens to
  fall the wanted way is the definition of fitting to the result. ✓ (your recommendation)

---

## 4. Handoff

1. **Suspend `test_classified_outcome_diverges_by_relational_history`** as expectedFailure with the finding
   (§3a). The mechanism tests stay green (they still pass — F4's mechanism is intact).
2. **Restate F4's claim** in the register (§3b): relational history shapes the developing substrate and moves
   the profile in the predicted direction; it does not currently reorder the discretized label.
3. **Register the read-out finding** (§3c): the bare-argmax classification has now hidden a real effect (F4)
   and exaggerated a fragile one (the psychopathic flip); the study's developmental claims should be measured
   on the graded profile/margin, not the argmax label. **This is a measurement-indicated study-layer
   improvement, drawn when the study's read-out is next addressed.**
4. **Then continue S56 to its close:** CeA at 1.000 is the sole remaining saturating node; the ceiling
   limitation and the coupling both converge on **Lump #13** (CeA CEl/CEm un-lumping) as the final step — now
   with all four cortical gates grounded and the output columns' upstream DRN suppression lifted.

> **F4's mechanism is intact and confirmed — relational history shapes the developing substrate, emergently, in
> the predicted direction. What S56 deflated is only the claim that this reorders the knife-edge classification
> LABEL — the S18 law, third time this session, and the second time the bare argmax has proven the wrong
> instrument. The honest resolution: suspend the label test (it may re-emerge), restate F4's claim on the
> substrate and profile where the effect is real, and register that the study should measure the graded profile
> rather than the argmax label. Do not weaken S56; do not cherry-pick a seed. The developmental-integration
> result stands — on the graded quantity that actually carries it. Then Lump #13 closes S56.**
