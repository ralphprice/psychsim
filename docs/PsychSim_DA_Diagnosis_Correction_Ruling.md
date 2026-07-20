# DA-learning — RULING. **Correction accepted: it's mostly a ruled mechanism + a stale comment. One front stays
# open, and the floor is grounded in DIRECTION but not in VALUE.**

**The diagnosis corrects my framing, and the correction is the point. I called an 80× collapse a substrate
defect; the bisection shows most of it is a deliberate, ruled mechanism plus a stale expectation that was never
recalibrated. The build session corrected the reviewer — the two-role split working in the reverse direction,
which is exactly what it is for. Rulings on the real remainder and the design question, which is mine.**

---

## 1. The correction is accepted in full — most of it is not a defect

**The bisection is clean and the counterfactual is decisive:**
- **`0.3206 → 0.0381` (8.4×) is S10.1 experience-decreasing plasticity** — a deliberate, ruled mechanism (the
  nth relevant experience carries ~1/n weight, a running average, so the developed state rigidifies without a
  separate stabiliser). **Neutralising S10.1 and nothing else (`EXP_PLASTICITY_FLOOR 0.001 → 1.0`) restores
  the delta to EXACTLY +0.320588 — the identical pre-S10.1 value.** And the analytic prediction matches:
  `sum(1/n, n=1..60) = 4.68` vs `60` flat = 12.8×, observed 8.4× (less because the co-activity threshold means
  not every trial counts). **This is not a broken mechanism — it is the mechanism working as designed.**
- **The real error was a STALE EXPECTATION:** the `~0.3` comment predates S10.1 and was never recalibrated when
  the plasticity regime changed underneath it. **A 60-trial protocol calibrated to flat plasticity does not
  mean the same thing under running-average plasticity.**

> **I over-framed this. "80× collapse → substrate defect → highest priority" was the wrong characterisation, and
> the build session's bisection corrected it — most of the drop is S10.1 (ruled, grounded, working) plus a
> comment that went stale when the regime changed. This is the reviewer being wrong and the build session
> catching it with clean data, which is the two-role split operating as designed. The standing rule (measure
> before characterising) applies to me too: I characterised an 80× number as a defect before the mechanism was
> traced. Corrected.** *(This is the second time this arc I've over-attributed a magnitude to a defect that
> measurement then explained — worth noting the pattern in myself, not just flagging it in the build.)*

## 2. The second front IS real and stays open (not patched)

**S10.1 explains `0.3206 → 0.0381`. The further `0.0381 → 0.0036` (~10.5×) across later work is unexplained,
and the discriminating control is strong:**

> **The unpaired cue-alone drift is essentially unchanged across all 157 commits (`+0.005034 → +0.005439`). So
> whatever erodes the paired gain is SPECIFIC to the DA-gated associative pathway — not general plasticity.**
> A general plasticity decay would move the unpaired control too; it doesn't. **This is a real, localised
> erosion of the associative learning pathway, and it stays an open diagnosis.**

**RULING: this stays a diagnosis, not a patch.** Leading suspects (the build session's, and I concur):
- **R8 competitive normalisation redistributing weight as the connectome grew 77 → 100 circuits** — as new
  edges were added (S56, Lump-13), R8 renormalises incoming weight sums, which could be redistributing weight
  away from the potentiated cue-reward synapse specifically. **This is checkable: does the cue-reward synapse's
  post-pairing weight survive the R8 normalisation, or is it renormalised down as the target gains afferents?**
- **Cumulative E-I damping of the DA teaching signal** — the E-I work (S56) increased inhibitory tone; if that
  damps VTA's drive or the DA signal reaching the associative synapse, the teaching signal weakens.
- **Diagnose before ruling:** trace whether the paired erosion tracks the connectome growth (R8) or the E-I
  changes (damping), by measuring the paired gain at the specific commits where circuits were added vs where
  E-I tone changed. **Do not patch until the mechanism is identified — the same discipline that just corrected
  my over-framing.**

## 3. ★ The design question — is adult learning meant to be that rigid? Grounded in DIRECTION, not in VALUE.

**This is the real substance, and it is mine. I researched the developmental-plasticity literature:**

**The DIRECTION is grounded — adult plasticity IS genuinely reduced, and S10.1 is correct to rigidify:**
> "The magnitude of synaptic and structural modification induced by experience DIFFERENTIATES developmental
> plasticity from the adult form of plasticity after the closure of the early postnatal critical period in most
> brain regions" (Hensch 2004; Katz & Shatz 1996). Critical periods are "favorable but circumscribed moments"
> after which learning "becomes more difficult." **So experience-decreasing plasticity that rigidifies the
> developed state is CORRECTLY grounded in the biology — the developed brain is less plastic than the
> developing one, and S10.1 implements exactly that. The mechanism stands.**

**And the nonzero floor is grounded in principle:**
> "Synaptic plasticity of the brain remains possible throughout life, and into adulthood." **Adult plasticity
> is reduced but NONZERO — so a nonzero floor (lifelong residual plasticity) is correct. An adult that could
> not learn at all would be wrong; a floor of exactly zero would be wrong. The floor being nonzero is
> grounded.**

**BUT the specific VALUE (0.001) is a scaffold the literature does not pin:**
> The literature establishes the RELATION (adult plasticity is reduced-but-nonzero relative to the
> developmental peak) but does not give a number for "how reduced." **`EXP_PLASTICITY_FLOOR = 0.001` is
> explicitly labelled `SCAFFOLD`, and correctly so — the direction is grounded, the value is not.** At 0.001, a
> fully-developed agent has effectively no remaining plasticity on well-used connections, which may be too
> rigid (the literature says reduced, not abolished).

**RULING:**
- **The S10.1 mechanism STANDS** — grounded in the biology (adult rigidification is real; the magnitude of
  experience-induced modification distinguishes developmental from adult plasticity).
- **The nonzero floor is correct in principle** — adult plasticity is reduced-but-nonzero; a lifelong residual
  floor is grounded.
- **The 0.001 VALUE is a scaffold to be grounded when the reward/value learning system is next characterised.**
  The floor should be set so the ADULT learning rate matches the biological reduced-but-nonzero level relative
  to the developmental peak — i.e. grounded to the ratio of adult:developmental plasticity the literature
  supports (reduced by a large but finite factor), **NOT set to make a test green.** This is the same "ground
  the relation, and the value follows from it" discipline used for the E-I gains and the pacemaker rates: the
  relation (adult << developmental, but > 0) is grounded; the value is derived from that relation when the
  learning system is characterised, not chosen. **Register: the adult-plasticity floor is a scaffold; ground it
  to the adult:developmental plasticity ratio when the reward/value learning system is characterised.**
- **Recalibrate the stale `~0.3` comment** to the S10.1-regime expectation (the running-average protocol's
  actual predicted magnitude), so the guard's stated expectation matches the mechanism. **Keep the bound loose
  until the second front is diagnosed AND the floor is grounded** — then set it to the grounded magnitude. ✓
  (the build session's instinct to leave it loose is right).

## 4. Sequencing — the DA collapse moves BACK down (it's mostly ruled), the second front joins the queue

**Since most of the "collapse" is ruled mechanism + stale comment, it is NOT the foundational emergency I
ruled it as. Corrected placement:**
1. **F4 margin fix — done.**
2. **age_window fix** — the hard-constraint violation; re-measure developmental claims after. **(This is the
   genuine highest-priority real fix — unchanged.)**
3. **Finish/verify the selector build** + the freezing-column-driver diagnosis.
4. **Diagnose the second front** (the DA associative-pathway-specific `0.0381 → 0.0036` erosion — R8 vs E-I
   damping; the unpaired control isolates it as associative-specific). Diagnosis, then ruling.
5. **Re-derive the six read-out sets** over live anatomy, remove the double-gain.
6. **Ground the adult-plasticity floor** (to the adult:developmental ratio) when the reward/value learning
   system is characterised; recalibrate the stale comment now.
7. **OFC→DA grounding; the test-integrity sweep; fresh full gate.**

> **The correction is accepted: I over-framed an 80× number as a substrate defect when the bisection shows it
> is mostly S10.1 (a ruled, biologically-grounded rigidification mechanism working as designed) plus a stale
> expectation comment. The build session corrected the reviewer with clean data — the split working in reverse.
> The second front is real and stays an open diagnosis (the associative-pathway-specific erosion, isolated by
> the unchanged unpaired control — R8 redistribution or E-I damping, to be traced not patched). And the design
> question is grounded in direction but not value: adult plasticity IS reduced-but-nonzero (Hensch/Katz-Shatz;
> "plasticity remains possible throughout life"), so S10.1's rigidification and a nonzero floor are both correct
> — but the 0.001 floor is a scaffold to be grounded to the adult:developmental plasticity ratio when the
> learning system is characterised, not tuned to a test. The mechanism stands; the value is owed. Recalibrate
> the stale comment, keep the tests suspended and the bound loose, diagnose the second front, and ground the
> floor when the reward system is next addressed.**
