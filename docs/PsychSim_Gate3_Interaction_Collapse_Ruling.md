# Gate 3 — RULING. **The descent is cleared. And the new failure is bigger than it reads: the sentinel itself
# has collapsed.**

**The gate cleared the descent — three aggression/freezing failures gone in the full suite, all four expected
failures the intended ones. The golden was correctly held. But the new failure needs a correction to the
build session's reading, because the test's OWN docstring contains the history that discriminates it, and it
points the other way.**

---

## 1. The descent is cleared, and the golden was correctly held

**`test_plain_threat_still_avoids`, `test_defensive_threat_produces_freezing`, and
`test_generic_threat_drives_avoidance_not_aggression` all pass in the FULL SUITE** — the `PL→vlPAG` driver and
the CRF+ competing pair cleared them in integration, not just in isolation. **All four expected failures are the
intended ones. The Lump #13 close is confirmed at the suite level.**

**The golden: correctly NOT regenerated.** It is stale for three compounding reasons (domain-mean dilution, the
`age_window` fix, the Lump #13 anatomy) and it is owed a DELIBERATE regeneration with the note — **after the
read-out work, not swept along with a substrate change. That is exactly what the Stage-3 regen failed to do,
and not repeating it is right.** ✓

## 2. ★ The interaction failure — the build session's hypothesis needs correcting, and the finding is bigger

**The hypothesis offered was "a near-zero quantity is flipping sign around zero." The test's own docstring
contains the discriminating history, and it says otherwise:**

> **At S56 Stage 1 the interaction term was 0.0401 and STABLE across durations** — `350/500/600 =
> 0.0363/0.0401/0.0417, spread 0.0054`. And the full S18 arc is recorded there:
> **`0.0755 → 0.0534 → 0.0335 → 0.0585 → 0.0401`.**

**So the term was NOT noise-scale before this pass. It was ~0.04, stable, with a five-point history. It is now
0.0013 / −0.0012 / −0.0025 — a collapse of roughly 30×, during this pass.**

> **★ The sign instability is the CONSEQUENCE of the collapse, not an independent defect. Once a quantity is at
> noise scale, its sign is arbitrary — so the test fails on sign because the EFFECT IS GONE, not because
> something destabilised. The build session's read of the current state is right (a near-zero quantity flipping
> around zero); what it missed is that the quantity only became near-zero in this pass. The finding is not
> "an unstable test" — it is "the divergence interaction has collapsed to nothing."**

**The leading hypothesis for the cause — and it is specific and testable: the `age_window` fix.** The
divergence interaction measures whether the environment differentially engages the executive across
development. **The replay bug ran ages 0→18 FOUR TIMES, resetting every maturation curve to infancy at each
stage boundary — which would massively inflate a developmental effect. Correcting the timing would deflate
it.** Lump #13's anatomy is the secondary candidate.

## 3. ★ The thesis-level significance — the S18 law has claimed its own sentinel

**If the divergence interaction was substantially an artifact of the developmental-replay bug, then the S18 law
has now deflated the very quantity that tracked it five times.** The earned-negative sentinel — the measurement
that confirmed "artifacts inflate, grounded completions shrink" at every stage of this project — **has itself
been ground to zero by grounding.**

> **That is the strongest possible confirmation of the law, and it needs stating carefully rather than
> triumphantly: the divergence effect appears to have been, in substantial part, an artifact of substrate and
> timing incompleteness — and full grounding has erased it. The sentinel did its job all the way to its own
> disappearance.** For the thesis this is a genuinely strong methodological result: an effect the model
> repeatedly measured, tracked across six grounding passes, and which shrank monotonically under every
> correction, until correct developmental timing removed it entirely. **A model that ground its own headline
> divergence effect to zero rather than defending it is demonstrating exactly the conservative error direction
> S18 claims.**

## 4. RULING

1. **Diagnose by attribution — measure the interaction term at the specific commits.** Before/after the
   `age_window` fix, and before/after Lump #13. **This is cheap (minutes) and it is the discriminating
   measurement:** it distinguishes "correct developmental timing deflated a timing-inflated effect" (the S18
   hypothesis) from "Lump #13's anatomy destabilised something." **Do this first — it is quick and potentially
   thesis-significant.**
2. **Do NOT touch the test until diagnosed. And when diagnosed, it likely needs RESTATING, not fixing.** A
   sign-stability assertion on a quantity that has legitimately gone to zero is asserting the wrong thing —
   **the same shape as the coordinate-pinning test just correctly rewritten.** The honest form asserts what is
   now true: **the interaction magnitude is at-or-below noise (the effect is absent), rather than that a
   vanished effect has a stable sign.** If the diagnosis confirms the collapse is the grounding working, the
   test becomes an assertion that the effect is absent — with the S18 arc recorded as its finding.
3. **The audit's separate finding about this test still stands and compounds it:** it varies `ticks` while
   holding `years` fixed, so it tests **integration resolution, not duration** — its docstring claims something
   it does not measure. **Address both together when the test is restated:** fix what it varies (or rename what
   it claims), AND restate what it asserts.

## 5. Order

**The interaction diagnosis first** — it is cheap, it is the discriminating measurement, and it may be
thesis-significant (§3). **Then the harsh mirror** — the thing the whole descent was for, now unblocked, and
the biggest remaining item. **Then the queue:** the DA second front, the read-out re-derivation + double-gain
removal, the adult-plasticity floor, the record/test-integrity sweeps, and the deliberate golden regeneration
after the read-out work.

*(The performance work can ride alongside whenever convenient — it is orthogonal and gate time is a real
constraint at 7h45m.)*

---

> **The gate cleared the descent — the Lump #13 close confirmed at suite level, the golden correctly held for a
> deliberate regeneration. The new failure is bigger than it reads: the test's own docstring shows the
> interaction term was 0.0401 and stable at S56 Stage 1, so it has COLLAPSED ~30× in this pass, and the sign
> instability is the symptom of an effect that is gone rather than one that destabilised. The leading
> hypothesis is the age_window fix — correct developmental timing deflating an effect the four-times-replay bug
> was inflating — which would mean the S18 law has now claimed its own sentinel, the strongest confirmation the
> law could receive. Measure the attribution first (cheap, discriminating, potentially thesis-significant),
> restate the test to assert what is now true rather than pinning a vanished effect's sign, address the audit's
> ticks-vs-years finding at the same time, and then open the harsh mirror. The model ground its own headline
> divergence to zero rather than defending it — that is the discipline producing its most consequential
> negative result yet.**
