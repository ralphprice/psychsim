# Dev-social pass (F1–F4) — CONFIRMED. And what opens next.

**I verified the F4 claim at the seam that matters, not the report. It holds, the honesty guarantee is real,
and the whole dev-social pass is sound. This is the milestone where the study's central developmental claim
becomes mechanistically demonstrated. Confirmation, then the ruling on what comes next.**

---

## 1. F4 confirmed — verified at the honesty seam

The claim rests entirely on one guarantee: **the two arms differ ONLY in relational content — the moral-
environment development must be byte-identical across `relational=False` and `relational=True`.** I verified
the mechanism that enforces it:

- **`_RelationalChildhood` makes the subject's `develop()` the clock.** Relational episodes fire from the
  `on_episode` hook AFTER each moral moment, and **`on_episode` never receives `develop()`'s rng** (verified in
  the signature). The cohort and relational rngs are **structurally-disjoint tuple seeds**, so no relational or
  cohort draw can collide with or perturb the subject's moral-environment situation stream.
- **Relational episodes ADD, never replace** — the subject's full moral-environment schedule runs unchanged in
  both arms.
- **Consequence, verified:** the subject's moral-environment appraisal stream is byte-identical across arms;
  the only thing that diverges is the substrate STATE that later moments read — **which is exactly the
  phenomenon the claim asserts.**

> **★ And the build session verified the RIGHT invariant, which is the subtle and correct move: it tested that
> the moral-environment STREAM is identical, NOT that the weights are equal. The weights MUST diverge — that
> is the result. A weight-equality check would have been the wrong test, and worse, it would have tempted an
> unfaithful "fix" to force weights back into agreement. Verifying the input stream's identity while letting
> the substrate state diverge is precisely how you confirm this class of claim honestly.** This is the
> discipline operating correctly at the most important seam in the pass.

**The claim is demonstrated:** on identical seed and identical moral environment, a `relational=True` childhood
diverges in its classified outcome from the `relational=False` baseline — warmly-related childhoods develop
more affiliation/reward-oriented adults via the grounded `familiar_warm → PVN-OT` bonding pathway, the warm/
wary relationships differentiate emergently from the mutual exchanges (never assigned), and divergence scales
with co-presence. **576 tests, the one authorized defensive-floor failure and two deferred-item expected
failures, zero regressions. F1–F4 complete.**

## 2. The methodological finding worth recording: the mutual-exchange requirement

The build caught that a **one-sided relational episode is degenerate** — if the subject only perceives its own
act echoed back, only familiarity accrues and the outcome barely moves. **The mutual exchange (both parties
perceive the other's ACTUAL prior act) is what lets warm/wary differentiate and the outcome diverge.**

> **This is a genuine finding about what a relationship IS in the model, and it should be recorded: a
> relationship requires two parties each perceiving and responding to the other's real behaviour — an echo of
> one's own act is not a relationship. This is the same truth the emergence discipline enforces elsewhere
> (the response must emerge from the other's real state), now confirmed at the dyadic level. It also
> retroactively validates the "developed-alongside cohort, not static props" ruling: the cohort members must
> act for real, or the relationship is degenerate.**

---

## 3. What this resolves and what it does NOT

**Resolves:** the P2b-vacuous note. Development is no longer relationally vacuous — relational history now
accumulates over a moral-environment childhood and diverts the classified outcome. **The developmental-
integration gap is closed.**

**Does NOT yet resolve — and this gates P3:** the **three-store reconciliation** (`gm.rel` / `Society.Tie` /
the RPE `RelationshipMatrix`). This is registered as the architecture decision that must be settled BEFORE
population-scale life-histories, and it still must be. **P3 does not open until it is.**

---

## 4. RULING — what opens next: the harsh-mirror demonstration NOW, then the three-store decision

**Two things are on the table: the harsh-cohort/harsh-environment demonstration, and P3. The ruling is: run
the harsh mirror first (it is a measurement, not a build), then take the three-store reconciliation as the
architecture decision that gates P3. Do NOT open P3 directly.**

### First — the harsh-mirror demonstration (a measurement, no new build)
**The warm result is shown: warm childhood → reward/affiliation-oriented adult via `familiar_warm → PVN-OT`.
The mirror is owed, and it matters for the study's credibility:**

> **A mechanism that produced ONLY the prosocial developmental direction would be suspect — it would suggest
> the machinery is biased toward the benign outcome. The wary → defensive divergence (harsh cohort / harsh
> moral environment → a more defensively-oriented adult via `familiar_wary → CeA`) is the mirror, and
> demonstrating BOTH directions from the SAME machinery is what shows the mechanism is even-handed and that the
> divergence is genuinely driven by relational content, not by a prosocial bias baked in.** The warm result
> alone is half a demonstration; both together are the finding.

**This is a MEASUREMENT using the machinery F1–F4 just built — no new mechanism, no new circuit.** Run
`run_life(relational=True)` with a harsh cohort (relationships that turn wary through hostile exchanges) and/or
a harsh moral environment, and show the classified outcome diverges toward the defensive/`CeA` direction, the
mirror of the warm/`PVN-OT` result. **Same honesty control: the two arms differ only in relational content;
the wary relationships must EMERGE from hostile mutual exchanges, never be assigned.** Its claim: the mechanism
produces both developmental directions from the same substrate, selected by the emergent valence of the
accumulated relationships. **Low cost, high value, closes the demonstration symmetrically. Open this now.**

### Then — the three-store reconciliation (the architecture decision that gates P3)
Once both developmental directions are demonstrated, **the next architectural move is the three-store
reconciliation, and it must precede P3.** The decision (registered, now due): `gm.rel` (the familiarity/affect/
trust representation the loop reads and writes), `Society.Tie` (the society-level standing/reciprocity/strain
construct), and `RelationshipMatrix` (the reward-prediction-error partner-value learner, currently self-
referential) are three representations of dyadic relationship state. **P3 (population-scale life-histories)
cannot proceed while three stores disagree about what a relationship is — at population scale the fragmentation
becomes N×N×three.** The decision: which is canonical, and whether the RPE learner (the most principled — it
learns partner value by reward-prediction-error, which is what a relationship's value IS) subsumes the others.
**This is a design-session architecture decision; scope it deliberately when the harsh mirror is done.**

---

## 5. Handoff

**Open the harsh-mirror demonstration now: a measurement with the F1–F4 machinery, showing wary → defensive
divergence (the `familiar_wary → CeA` mirror of the warm `familiar_wary → PVN-OT`... — the warm→PVN-OT result),
under the same only-relational-content-differs control, wary relationships emerging from hostile mutual
exchanges. No new build; it closes the demonstration symmetrically and shows the mechanism is even-handed.**

**Then take the three-store reconciliation as the architecture decision that gates P3 — scoped deliberately,
design-session-first, because it is the prerequisite for population scale.**

> **The dev-social pass is complete and confirmed: relational history, accumulated through emergent mutual
> exchanges over a moral-environment childhood, diverts the study's classified outcome — verified at the
> honesty seam, with the right invariant checked. The warm direction is shown; the harsh mirror completes it;
> then the store reconciliation opens the road to population scale. The mechanism the study's central
> developmental claim needs is live.**
