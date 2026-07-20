# The four insertion forks — rulings. **Fork 2 needs correction; the others are confirmed.**

**All four are well-diagnosed. Three are correct as proposed. Fork 2 has a subtle emergence hazard I caught
only by reading the arena's percept vocabulary, and it must be corrected before build — the proposed
translation would blur presentation and valuation. Here is each.**

---

## Fork 1 — extract a shared relationship-update function → **CONFIRMED. Proceed.**

`accrue_relationship(rel, behaviour, win_drive)` in `gamemaster.py`, called by both `adjudicate` and the arena.
This is exactly right and it directly serves the scope's requirement that the developing-childhood write be the
*same* mechanism as the confirmed single-exchange write, not a second implementation. It refactors already-
shipped, already-tested P2a code, behaviour-preserving. **Extract it; both call sites use it. `win_drive` =
`fr.strength` (= `max(drives)`) is the correct scalar.** No concern.

---

## Fork 2 — the percept-colouring translation → **CORRECTION REQUIRED. This is the emergence seam.**

**The proposed mapping writes the perceiver's stored relationship valuation directly onto the percept's
affordance channels:**
```
rel.affect > 0  →  percept["affiliation"] += affect · gain · familiarity
rel.affect < 0  →  percept["threat"]      += −affect · gain · familiarity
(1 − trust)     →  percept["threat"]      += (1−trust) · gain · familiarity
```
**I read the arena's percept construction, and this violates the arena's own keystone.** The percept vocabulary
is explicitly **presentation, not valuation** — the docstring at `_perceive` is emphatic: *"the perturbation
the other's act presents to this agent — a perception in the trigger vocabulary, NOT a valuation."* An act
*presents* `affiliation`/`threat` channels; **the response — the valuation — emerges from the perceiver's own
circuits** when those channels route through `IN-CONSPEC` into the perceiver's reward/defensive systems. The
physical-endowment and kin-signature percepts are built the same disciplined way, and their docstrings state
the keystone twice: *"routes these triggers via the IN-CONSPEC edges into the perceiver's OWN circuits… the
response emerges from the perceiver's circuits, never a coded trait→outcome weight."*

> **The problem: the proposed mapping adds the perceiver's OWN stored affect/trust — a valuation the perceiver
> already holds — directly onto the affordance channels as though it were a fresh perception. That writes a
> valuation into a presentation surface.** It is subtly but genuinely a coded history→response shortcut: "you
> have positive stored affect toward this other, therefore inject affiliation into the percept" is a
> relationship-value→affordance coefficient, which is exactly the kind of coded trait→outcome weight the arena
> is built to avoid. The perceiver's circuits should VALUE the history, not have the history pre-valued and
> injected.

**The honest translation — history enters the way every other conspecific cue enters: as an `IN-CONSPEC`
familiarity cue the perceiver's own circuits then value.** `IN-CONSPEC` already carries `kin_signature`,
`attractive_face`, `formidability_cue` — self-referent/other-borne cues that the perceiver's circuits appraise.
**A relationship history is another such cue: a familiarity/affiliative-history signal borne by this specific
other, routed through `IN-CONSPEC`, valued by the perceiver's own reward/defensive circuits — not written onto
`affiliation`/`threat` as a finished valuation.**

**RULING on Fork 2:**
- **The familiarity-gated relationship history enters as a conspecific cue on `IN-CONSPEC`**, in the same manner
  as the kin-signature and physical-endowment percepts — a per-other signal (magnitude gated by familiarity,
  signed by stored affect, modulated by trust) that the perceiver's substrate then appraises through its own
  circuits. **It does not write directly onto `affiliation`/`threat`.**
- **If `IN-CONSPEC` lacks a band for "relational history/familiarity with this specific other,"** that is the
  one honest addition this pass may need — a conspecific-familiarity band, grounded as the perceptual channel
  by which a known other is recognized as known (the familiarity/recognition signal is real perceptual
  neuroscience — a familiar conspecific is perceived differently from a stranger). **This would be a channel
  addition (an input band), not a coded coefficient — and it is the correct place for the history to enter.**
  Verify whether such a band exists; if not, adding it is in-scope and is the *honest* form of "feed the
  relationship back into perception."
- **The P1 colouring math is preserved in ROLE** — familiarity gates, affect signs, trust modulates — but it
  shapes the *cue presented on `IN-CONSPEC`*, and the perceiver's circuits produce the response. **The math is
  reused; the injection point moves from the affordance channels to the conspecific-cue channel.**

> **This is the same distinction the arena already draws for kin and physical cues, applied to relational
> history. The proposed mapping was one step short of it — it reused the P1 colouring but attached it to the
> valuation surface instead of the presentation surface. Attaching it to `IN-CONSPEC` keeps the emergence wall
> intact: the perceiver VALUES its history through its own circuits, rather than the history being pre-valued
> and injected.** This is the fork where a plausible mapping quietly codes the outcome, and it is exactly what
> the honesty discipline exists to catch.

*(Note: this makes Fork 2 slightly larger than "add a term" — it may add an `IN-CONSPEC` band. That is correct
and in-scope: the scope said "feed the relationship representation back into perception," and the honest way to
do that is through the perceptual channel for known-others, not by editing the affordance percept. If verifying
the band shows one already exists, use it; if not, the band is the right addition.)*

---

## Fork 3 — the relationship-off / relationship-on fork → **CONFIRMED, with the trace ruling.**

The `ArenaSpec` flag (`relational: bool = False`) selecting `_Tie`-accrual (relationship-off, byte-identical
regression trace) vs relationship-representation-accrual (relationship-on) is correct and preserves the
regression asset. **On what the relationship-on trace records:** record the relationship representation's own
variables (affect/trust/familiarity), and **derive `strain` as a view** for continuity of the trace format
(strain ≈ a function of negative affect / low trust), so existing trace consumers still read a `strain` field
but it is now a derived projection of the real representation, not an independent store. **`_Tie` is demoted to
that derived view; it is no longer written independently.** This reduces the store count (four → three) in the
right direction, as the scope noted.

---

## Fork 4 — the classified outcome → **RULING: run the arena as the dyadic childhood INSIDE `run_life`.**

The two options are not equivalent for testing the pass claim, and that decides it:
- **Attaching a classifier to the arena trace** tests a *proxy* — it classifies the arena's own trace, which is
  a regression/trace harness, not the study's developmental outcome. It would show relational divergence in the
  arena's terms but not connect it to the CU study's classified trajectory.
- **Running the arena as the dyadic childhood inside `run_life`** tests the *actual pass claim*: that the CU
  study's classified developmental outcome (the sophropathic/CU trajectory `run_life`/`run_condition` produce)
  **diverges as a function of relational history.** This is the claim as written in the scope, and only this
  option tests it. It routes the co-present portion of the developing life through the dyadic arena machinery
  while solo/idle development keeps the environment-only path (the augment ruling) — so `run_life` becomes:
  environment-only development for solo time, arena-based dyadic development for co-present time, both feeding
  the same maturing substrate, then classified.

**RULING: run the arena as the dyadic-childhood component inside `run_life`.** This is the more consequential
integration and it is the one the pass claim requires — the classified outcome must be the *study's* outcome,
diverging by relational history, or the pass has not demonstrated what it claims. **This makes the pass claim
directly testable against the environment-only baseline `run_life` already produces:** same substrate, same
environment, with vs without the relational-childhood component → does the classified trajectory diverge, and
does the divergence trace to the relationship representation.

*(Scope note: this is the larger of the two Fork-4 options and it touches `run_life`'s structure. It is correct
and in-scope — the scope's §3.3 named it as the alternative and the claim requires it — but it means the build
is: extract the shared write (F1), the `IN-CONSPEC` history cue (F2, corrected), the harness fork (F3), AND the
`run_life` integration (F4). If that is more than one clean pass, the natural split is: first the arena-internal
changes (F1–F3) tested against the arena's own relationship-on/off diff, THEN the `run_life` integration (F4)
tested against the study baseline. Build session's call on whether to split, but the F4 integration is where the
pass claim is actually demonstrated and must not be dropped.)*

---

## Summary of rulings
1. **Shared write function — yes**, `accrue_relationship` serving both sites. Proceed.
2. **Percept colouring — CORRECTED**: the relationship history enters as an `IN-CONSPEC` conspecific-familiarity
   cue valued by the perceiver's own circuits, **not** written onto the `affiliation`/`threat` affordance
   channels. Add the `IN-CONSPEC` familiarity band if one does not exist (the honest form of the feedback).
3. **Relationship-off/on fork — yes**, `ArenaSpec` flag; relationship-on trace records the real variables with
   `strain` as a derived view; `_Tie` demoted to that view.
4. **Classified outcome — run the arena inside `run_life`** (not a classifier on the arena trace), because only
   that tests the pass claim; split from F1–F3 as a second sub-pass if cleaner.

## The emergence line, restated for this build
**Fork 2 is the whole game here.** The relationship history must be VALUED by the perceiver's circuits, never
injected as a finished valuation. It enters perception the way kin-signature and physical cues enter — as a
conspecific cue on `IN-CONSPEC` — and the response emerges. **If the build finds itself writing stored affect
directly onto an affordance channel, stop — that is the coded shortcut, and it is precisely the seam the arena
was built to keep honest.**

**Confirm insertion points once more with Fork 2 corrected (locate/verify the `IN-CONSPEC` familiarity band),
then build F1–F3, test against the arena relationship-on/off diff, then integrate F4 into `run_life` and test
the pass claim against the environment-only baseline. Hold at each gate.**
