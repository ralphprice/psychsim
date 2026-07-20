# Scope — the developmental-social integration pass
### Routing partner-specific relational learning through the ontogenetic timecourse. Option A confirmed.

**I verified the two load-bearing claims against the code. Both hold, and together they make the scope narrow
and the recommendation correct — for a principled reason, not convenience. This is the pass that makes the CU
study's central developmental claim mechanistically possible; today it is not.**

---

## 1. The gap, stated precisely (verified)

**The classified developmental outcome — the sophropathic/CU trajectory the study reports — is currently a
pure function of environmental scalars and the random seed.** `run_life`/`run_condition` (the seven-stage CU
study) are `develop(environment)` chained with a classifier; a search of the entire study path for the
dyadic-interaction machinery (`converse`/`adjudicate`/`partner_rel`/the relationship representation) returns
nothing. **Partner-specific relational history cannot accumulate across a simulated childhood, and therefore
cannot influence the developmental trajectory or the classified outcome.** That is the gap.

The pieces to close it all exist but are not composed: the loop that produces a *classified life* is
environment-only and never sees a second agent; the loop that lives a *dyadic childhood* (the arena) reaches a
developed substrate but records a descriptive dead-end and produces no classified outcome; the loop that closes
the *relationship feedback* (the P1 read + P2a write in `converse`/`adjudicate`) is invoked only in a demo and
tests. **The pass composes them.**

## 2. Why option A (build on the arena) is correct — the principled reason

**The single genuinely hard problem in this pass is computational feasibility, and the arena has already
solved it.** Verified envelope: a full dyadic interaction (`converse`) costs ~2× a substrate settle
(~32 ms adult, ~100 ms developing child); naive all-pairs-per-co-present-hour across a childhood is 3–4 orders
of magnitude over the test-suite budget — **infeasible**. The arena is already the *compressed* form:
`E = childhood_years × episodes_per_year` episodes (~54 for an 18-year childhood at 3/year), **one sampled
partner per agent per episode**, co-presence set by the existing `shared_frac`/confinement structure — not
per-hour all-pairs. **The arena is co-presence-over-a-compressed-childhood, per-dyad, already tractable, and
its perception already routes through the perceiver's own circuits** (`felt_response` at `arena.py:360` — the
percept enters via `IN-CONSPEC` and the response emerges from the perceiver's substrate, exactly the emergence
discipline).

**Its only defect is the one the pass fixes:** at `arena.py:363–365` it accrues a descriptive `_Tie` — a flat
`_TIE_STEP` increment, `.affect` written and **read nowhere**. It records that a relationship changed but does
nothing with it. **So the pass is not "integrate development with relationships from scratch." It is: replace
one dead-end bookkeeping step with the real relationship-representation write, feed it back into the percept,
and give the run a classified outcome.** That is a small, well-bounded change on a loop that already does the
hard part correctly.

> **Options B (thread the daily clock) and C (author a new loop) both hit the envelope wall or the
> new-machinery/emergence hazards, as the diagnosis found. A is the minimal existing-machinery path, and it is
> minimal *because* the arena already embodies the compression the envelope requires. Confirmed: build on the
> arena.**

## 3. Scope — the three changes (and nothing else)

1. **Replace the descriptive tie accrual with the relationship-representation write.** At the arena's social-
   episode step, retire the flat `_TIE_STEP` `_Tie` update and write `gm.rel` via the P2a mechanism — the
   emergent-signed, drive-intensity-scaled update to (familiarity, affect, trust). The relationship
   representation is now written by the *emergent act's own read-outs*, not a fixed step.
2. **Feed the relationship representation back into perception.** Add the P1 familiarity-gated colouring — the
   same computation already built and confirmed (`affect → social_valence`, `(1 − trust) → threat`, gated by
   familiarity) — as an **additional term on the `felt_response` percept**, which is the arena's own superior
   channel. **Do not route it through `Person.perceive`'s Appraisal** — the arena explicitly documents that
   path collapses warm approach to a silent null; `felt_response` is the correct percept surface here.
3. **Give the run a classified developmental outcome.** Either attach the classifier to the arena trace, or run
   the arena as the dyadic childhood *inside* `run_life`, so the accumulated relational history produces a
   classified trajectory that can be compared against the environment-only baseline.

**Everything else the diagnosis raised is out of scope for this pass and stays registered.**

## 4. The forks — rulings

- **Canonical relationship store → `gm.rel` this pass.** It is the only store that closes the P1 read + P2a
  write loop. `_Tie` becomes a view (or is retired); `Society.Tie` remains the distinct society-level construct;
  migration to the reward-prediction-error learner (`RelationshipMatrix`) is a later, separate decision. **Do
  not introduce a fifth store.** (Register: with the arena's `_Tie` folded in, the store count is being
  *reduced*, which is the right direction — the four-store tangle is a pre-P3 architecture decision, and this
  pass makes it three by demoting `_Tie` to a view.)
- **Update magnitude → adopt the P2a drive-scaled bands; retire the flat `_TIE_STEP`.** The relational update
  in the developing childhood must be the *same* emergent mechanism as the confirmed single-exchange write —
  not a second, flat-stepped implementation. This unifies the write and removes a divergent constant.
- **Percept channel → keep `felt_response`; reuse the P1 colouring as an added term.** Verified correct: it
  routes through the perceiver's own circuits and does not collapse warmth. The P1 colouring math is reused, not
  re-derived.
- **Partner selection → one sampled partner per episode (the existing arena behaviour).** All-pairs is the
  dominant cost driver and the envelope forbids it. **Co-presence and partner sampling must come entirely from
  the existing placement/`shared_frac`/confinement structure — never a hand-selected partner** (see honesty
  constraints).
- **Computational cost → decouple the free relationship-bookkeeping from the expensive settle; precompute
  per-agent resting activation before the loop** (removes the developing-child cache-thrash). The relationship
  write is O(1) and must not inherit the settle cost.
- **Persistence → thread a persistent relationship store across episodes** (so the representation survives the
  childhood), and **fork the arena harness into a relationship-off mode (the existing deterministic regression
  trace) and a relationship-on mode (the integrated life).** This preserves the arena's regression-diff
  semantics — which is a real testing asset — while adding the new capability alongside it, not in place of it.
- **Replace vs augment → augment.** Co-present episodes route through the dyadic write-and-read; solo/idle
  episodes keep the environment-only developmental path. **The relationship representation never enters
  `develop()` as a plasticity term** — it changes the trajectory only by re-entering perception on the next
  co-present episode.

## 5. The pass claim (the exit test)

**This pass closes when an agent's developmental trajectory and classified outcome diverge as a function of the
specific relationships it accumulated across its simulated childhood — and that divergence traces entirely to
the accumulated relationship representation, with no scripted co-presence and no parallel developmental
plasticity channel.** Concretely: two agents with identical substrates and identical environments, differing
only in the relational histories that emerge from their (structurally, not hand-) sampled co-presence, reach
different classified outcomes — and the difference is attributable to the relationship representation written by
their exchanges and read back into their perception, not to any coded divergence. **When that holds, the CU
study's developmental claim — that relational history shapes the trajectory — is mechanistically supported for
the first time.**

## 6. The honesty constraints (binding on the build)

- **Never script who-meets-whom.** Co-presence and partner sampling come only from the existing
  placement/timetable/`shared_frac`/confinement structure. A hand-picked partner to manufacture a relationship
  is the emergence wall — it would make the divergence an artifact of the selection, not the mechanism.
- **The relationship representation is written by the emergent act's own read-outs** (the P2a mechanism) and
  **read back only as familiarity-gated perceptual colouring** (the P1 mechanism). No new relational rule.
- **No parallel plasticity channel in `develop()`.** The relationship representation changes behaviour *only*
  by re-entering perception. This is the ruling already established, and it is the line this pass must hold at
  the seam.
- **Any familiarity rescaling for compressed contact counts must be a mechanical count-rescale, not a tuned
  value** — the compression is of wall-clock time, never of developmental time, and never a knob set to produce
  an outcome.
- **Threading a persistent store through a life is substrate-adjacent → regrow + full-suite gate.** The pass is
  gated on the full suite (the authorized defensive-floor failure and the two deferred-item expected failures
  remain the only permitted reds) and the relationship-off regression mode must remain byte-identical.

---

## 7. Handoff

**The pass is scoped. Build on the arena, the three changes in §3, the fork rulings in §4, the claim in §5, the
constraints in §6. The build session's first move is the usual discipline: confirm the exact insertion points —
where `_Tie` accrual is replaced by the `gm.rel` write, and where the `felt_response` percept takes the
familiarity-gated colouring term — and report before building.** Then build, test the pass claim, hold.

> **This pass integrates partner-specific relational learning into the ontogenetic timecourse: a developing
> agent now accumulates a relational history through its emergent exchanges, and that history shapes its
> trajectory by re-entering its perception — never by a scripted path and never by a hidden plasticity channel.
> It is the mechanistic precondition for the study's central developmental claim, and it is built by composing
> three mechanisms that already exist and are already confirmed. One pass; then the population scale (P3), for
> which the store-reconciliation decision is the gating prerequisite.**
