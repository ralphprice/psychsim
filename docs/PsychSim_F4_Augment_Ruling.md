# F4 — the augment ruling. **(A) confirmed. The moral-environment confound is the whole point, and (A) is the
# only form that protects the claim.**

**The build session caught a real confound, and it reframes F4 correctly: this is not "run the Arena inside
`run_life`" — it is "add relational content to the study's existing moral-environment childhood without
changing anything else." I verified `develop()`'s structure; (A) is clean. Here is the ruling.**

---

## 1. Why (B) is disqualified — it breaks the claim, not just the harness

**The CU study manipulates the moral environment (warmth/structure/recognition) through
`develop()`/`_colour_by_env`. That axis IS the study's independent variable.** Option (B) — threading the moral
environment into the Arena and running the whole childhood there — would develop the subject through the
Arena's `micro_env` (Things/activities/encounters) instead of the moral-environment colouring, or would require
rebuilding the moral-environment model inside the Arena's different env architecture.

> **Either way, baseline and treatment would then differ in their ENTIRE developmental content — different
> situations, different environmental colouring — not only in the presence of relationships. That confounds the
> comparison the pass claim depends on: "does relational history divert the classified outcome?" becomes
> unanswerable, because the two arms differ in everything, not one thing.** (B) is disqualified on the claim,
> before cost even enters. The build session's diagnosis is exactly right.

## 2. Why (A) is clean — verified against `develop()`'s structure

**I read `develop()`. It is a per-episode loop:** for each episode `i`, it computes an age fraction, colours a
situation by the environment (`_colour_by_env(situation(kind, rng), env)`), and lives that one moment
(`live_moment(agent, appr, age)`). **Each episode is independent, and the moral-environment colouring is
applied per-episode.**

> **This means a relational episode (the F1–F3 `_social_episode`) can be interleaved between moral-environment
> episodes, at the same computed age, WITHOUT disturbing the colouring of any surrounding episode.** The
> moral-environment episodes develop the substrate exactly as they do today; the relational episodes add
> co-present dyadic content on the same agent (both develop `agent.engine` via BCM plasticity — the build
> session confirmed no substrate conflict). **The subject develops under the same moral environment in both
> arms; the treatment arm simply also lives relational episodes. The two arms differ in relationships and
> nothing else — which is precisely the claim's requirement.**

**RULING: (A). Interleave the F1–F3 relational episodes into `develop()`'s moral-environment childhood on the
same agent. `run_life` continues to develop the subject via `develop()` (moral-env-coloured, solo); at a
defined cadence it also runs a relational episode with a roster. Baseline = `develop()` only; treatment =
`develop()` + interleaved relational episodes.** Minimal, preserves the study's environmental axis, reuses
F1–F3 unchanged.

---

## 3. The remaining forks — rulings

### Fork 1 — the roster (where the co-present others come from) → **a developed-alongside cohort, capped small.**
The subject's relational episodes need co-present others, and **those others must themselves develop** — because
a genuine relationship is with an agent that has its own emergent state, and a relationship formed with a
static prop would be a degenerate relationship (the `_Tie`-was-dead-end problem in another form). **Ruling: a
small cohort of developed-alongside agents** (the subject plus K others, each developed through the same
`develop()` loop, co-present in the relational episodes). **NOT a fixed background roster** (static others =
degenerate relationships) and **NOT the full `group_matrix`** (uncapped cost). **Cap K small** (the envelope
demands it; K on the order of a handful — enough for differentiated relationships, few enough to stay within
budget). This is the honest form: the subject forms relationships with real developing agents, and whether
those relationships are warm or wary emerges from the interactions, not from a fixed roster property.

> *Register the consequence: the cohort's own development is real development, so a "childhood" now develops
> K+1 agents. That is the dominant cost term and it is why K must be capped — but it is also more faithful (a
> child grows up among other children who are themselves growing). The subject is the one classified; the
> cohort exists to be genuine relational partners.*

### Fork 2 — interleave cadence → **relational episodes ADD to solo episodes; they never replace them.**
**Critical for the claim:** the moral-environment development must be IDENTICAL in both arms. If relational
episodes replaced solo ones, the treatment arm would have fewer moral-environment episodes than the baseline —
a second confound. **Ruling: the treatment arm runs the full baseline `develop()` schedule UNCHANGED, and adds
relational episodes at a defined cadence (a `shared_frac` analog).** The baseline arm runs the same `develop()`
schedule with no relational episodes. **The moral-environment developmental content is then byte-identical
across arms; the only difference is the added relational episodes.** The cadence itself is a structural
parameter (how much of childhood is co-present), set plausibly and mechanically — not tuned to produce a
divergence.

### Fork 3 — baseline-vs-treatment control → **`relational: bool` on `run_life`, default `False`.**
Default off = today's environment-only life (the baseline, unchanged). `True` = the interleaved-relational
life (the treatment). **The pass test compares the two classifications on identical seed and identical moral
environment** — so any divergence in the classified outcome is attributable to the relational content alone.
This is the direct test of the claim and it mirrors the `ArenaSpec.relational` fork already built for F1–F3.

### Fork 4 — performance → **one sampled partner per relational episode; cohort capped; the Arena's sampling
### discipline throughout.**
The CU study builds N subjects × classify; adding K-cohort relational episodes must not go all-pairs. **Reuse
the Arena's confirmed discipline: one sampled partner per episode, cohort capped small, relational bookkeeping
decoupled from the settle (the O(1) `accrue_relationship` write is free; only the co-present `felt_response`
episodes cost settles).** Measure the envelope on the chosen cadence × cohort size before scaling to the full
study N. If the envelope is tight, the cadence and K are the levers — mechanical structural parameters, reduced
for tractability, never compressing developmental time.

---

## 4. The F4 claim (the exit test — the one that matters for the thesis)

**F4 closes when the CU study's classified developmental outcome diverges as a function of the subject's
accumulated relational history — with the moral-environment development held IDENTICAL across the baseline and
treatment arms, so the divergence is attributable to relational content alone, and traceable to the
relationship representation, with no scripted co-presence and no parallel plasticity channel.**

Concretely: run a subject through `run_life` twice — `relational=False` (baseline) and `relational=True`
(treatment) — on identical seed and identical moral environment. **The moral-environment development is
verifiably identical (same episodes, same colouring); the treatment arm additionally accumulated relationships
through structurally-sampled co-presence with a developing cohort. Does the classified outcome diverge, and
does the divergence trace to the relationship representation?** When it does, **the study's central
developmental claim — that relational history shapes the trajectory — is mechanistically demonstrated on the
study's own classified output, for the first time.**

## 5. The honesty line for this build (the confound IS the adversary)

- **The two arms must differ ONLY in relational content.** This is the whole discipline of F4. **Verify it: the
  moral-environment development (situations, colouring, schedule, ages) must be byte-identical across
  `relational=False` and `relational=True`** — same `develop()` calls, same seed, same environment. If anything
  else differs between the arms, the claim is confounded. **Relational episodes ADD; they change nothing about
  the solo developmental content.**
- **Never script who-meets-whom.** Co-presence and partner sampling come from the cohort structure and the
  cadence, not a hand-picked partner. A hand-selected relationship to manufacture a divergence is the emergence
  wall.
- **No parallel plasticity channel.** The relationship representation changes the subject's trajectory ONLY by
  re-entering perception in the relational episodes (the F2 `IN-CONSPEC` cue → the subject's own circuits →
  emergent behaviour → BCM plasticity). It is never added to `develop()` as a term.
- **Cohort development is real, not a shortcut.** The cohort agents develop through the same honest `develop()`
  loop; they are genuine relational partners, not props with assigned relationship values.

---

## 6. Handoff

**F4 is ruled: (A) interleave relational episodes into the moral-environment `develop()` childhood; a small
developed-alongside cohort as the roster; relational episodes ADD to (never replace) solo episodes so
moral-environment development is identical across arms; a `relational: bool` on `run_life` defaulting off;
one-partner-per-episode sampling with a capped cohort for the envelope.**

**The build session's next move is the specific diagnosis of the chosen path: exactly where in `run_life`'s
stage loop the relational episodes interleave, how the cohort is constructed and developed alongside, the
cadence parameter, and the measured envelope on a single `run_life` before scaling to the study's N. Report
that, then build F4, test the classified-outcome claim against the environment-only baseline (verifying the
moral-environment development is byte-identical across arms), and hold.**

> **F4 connects the confirmed relational mechanism (F1–F3) to the study's classified outcome, under the strict
> control that the two arms differ only in relational content. It is the pass where the study's central
> developmental claim becomes mechanistically demonstrable — and the moral-environment confound the diagnosis
> caught is exactly what (A) is designed to prevent. Build it under that control; the confound is the thing to
> protect against.**
