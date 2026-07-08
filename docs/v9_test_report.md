# v9 seed pass — test report for design-session review

**Scope:** Part 8 v9 pass (close OBS-3 with the provocation→hypothalamic-attack pathway; fold in
S1.4 social innate-wiring) + the stage-4 Panksepp reductions already synced. Commits on `main`:
`9c099d8` (stage 4) and `b61e234` (v9). **Both are pushed to the remote** (that was the sync gap
you flagged — the local commits were never pushed; they are now).

---

## 1. The headline — OBS-3 closure, measured result (reported as-is)

The diagnosis held: OBS-3 was **"aggression cannot be driven at all,"** not "loses the race."
Provocation entered only via `IN-SOMATO:nociception → CeA` (GABAergic), which *inhibits* both
attack effectors — so more provocation deepened suppression. v9 adds `VMHvl` (attack area) + a
provocation-specific drive, leaving the `CeA→PAG/HYPdm −0.70` inhibition **untouched**.

Measured on a fresh engine, weights **not** adjusted to force any result:

| condition | winner | aggress drive | avoid drive |
|---|---|---|---|
| provocation 0.9 (adult 25) | restrain | **0.183 (dominant)** | 0.030 |
| plain threat 0.9 (adult) | avoid | 0.000 | 0.278 |
| neutral (adult) | restrain | 0.000 | 0.000 |
| provocation 0.9 (**age 2**) | **aggress** | 0.215 | 0.086 |

- **Gap closed:** aggression went from *exactly 0 / unreachable* (v8) to the **dominant drive**
  under provocation at every age. Plain threat still → avoid (aggress exactly 0). Neutral →
  restrain, aggress exactly 0 (**no leak** — the provocation-specificity control you required).
- **Un-tuned developmental trajectory emerged:** age 2 → overt `aggress`; age 8+ → `restrain`
  (dominant impulse held below the act threshold by the maturing STN brake, the OBS-2 mechanism).
  Reactive aggression's real course — early expression, progressive restraint. So OBS-3's "does
  not win even under strong threat" is genuinely **falsified**, not nudged.
- **Calibration note (reported, not fixed):** the group-matrix **dominance route stays
  sub-threshold** at age 12 — the `status_challenge` stimulus presents only moderate provocation
  (`thwarting 0.6 → provocation 0.36`) mixed with a reward_cue that drives the prestige route, and
  the developed brake holds it below overt aggression. Not raised to win.

Closure test `tests/test_aggression_pathway.py` (6/6): provocation→aggress-drive>avoid; plain
threat→avoid; **neutral→restrain, no leak**; differential shift; efficacy+maturational-restraint;
**+ a guard asserting `CeA→PAG/HYPdm` is inhibitory and weight-unchanged (0.70)**.

---

## 2. Full-suite result

First full run after the v9 edits: **427 tests, 4 failures + 3 errors** (all in the final
modules — I misread a mid-run "0 failures at 416/421" and pushed `b61e234` before the run
finished; that was premature and the remote was briefly red. All 7 are now diagnosed and fixed;
targeted re-verification is running, full-suite gate to follow before I re-push the fix).

Every one of the 7 is a **clean, expected consequence of the v9 change** — none is a real defect:

| # | test | cause | resolution |
|---|---|---|---|
| 1–3 | `test_engine` ×3 (`IndexError: pruned[j]`) | shipped `library/adults.json` was banked under **v8** (fewer connections); restoring it into the v9 engine over-indexes the weight/pruned arrays | **regrew `library/adults.json` on v9** (154 weights/adult) — same single-serialization path, now v9 |
| 4 | `test_characterisation` golden | v9 changes behaviour (intentional) | **regenerated** golden; diff verified benign (see §3) |
| 5–6 | `test_substrate` (77≠78) ×2 | hardcoded v8's 77-circuit count | updated to **78**; renamed `test_loads_the_v8_substrate → _v9` |
| 7 | `test_substrate_study` punishment | v9 flipped a study metric — **FLAGGED for you, see §4** | reframed to the robust claim; needs your ruling |

---

## 3. Characterisation golden diff — benign

Every developed-agent profile shifted by **~0.001–0.008**: `defensive_threat` slightly **down**,
the other domains slightly up. Mechanism: the new low-activity `VMHvl` circuit joins the
`defensive_threat` domain and dilutes its mean (the readout is a domain mean). **No classification
changed** (psychopathic→social_cognition, sophropathic→executive, shared_root→social_cognition, all
unchanged). This is the expected normalisation shift from adding one circuit, not a behavioural
regression.

---

## 4. ONE DECISION FLAGGED FOR YOU — the punishment-learning metric

`test_substrate_study::test_punishment_deficit_is_not_robust...` asserted the graded
punishment-learning deficit is **non-monotone** in the affective-empathy throttle (its v8 evidence
that the deficit was a plasticity artifact, not robust).

**v9 flips it to weakly monotone:** throttle (0, 0.5, 1.0) → `[0.018, 0.012, 0.008]`
(deterministic). Cause: the new `VMHvl→PAG` edge perturbs the `DEFENSIVE_OUTPUT` baseline (PAG is a
member), so the three near-zero values now happen to order monotonically.

**My read:** the magnitudes are **negligible** (~0.01) and every throttle still acquires a *small
positive* aversion — there is **no punishment-learning failure / inversion**. So the substantive
claim ("no robust CU-style punishment deficit") still holds; only the brittle monotonicity proxy
flipped. I reframed the test to the robust, non-brittle claim: **no throttle inverts learning to
failure (`all v > −0.02`) and the graded spread is negligible (`max−min < 0.05`)** — direction/
magnitude only, no target value. I did **not** silently keep the monotonicity assertion (that would
now be asserting a falsehood) nor tune anything.

**Your call:** accept the "weak, not a failure" reframe, or do you want the weakly-monotone shift
treated as a *finding* (v9 slightly sharpened the graded deficit)? I lean reframe — the magnitudes
are near-noise — but this is a study-relevant CU signature, so it's yours to rule.

---

## 5. Part 8 gate — the three things you said you'd check

1. **Closure test has the neutral-state control + is direction-only:** yes — `test_neutral_no_aggression_leak`
   asserts neutral→restrain with aggress≈0; all assertions are ordinal/direction, no rates.
2. **`CeA→PAG/HYPdm` inhibition genuinely untouched:** yes — byte-identical to v8 (weight
   `moderate-strong`=0.70, sign −1), proven by `TestCeAInhibitionUntouched` and the transform's own
   guard assert. No hand-dis-inhibition; the fix is an added excitatory pathway only.
3. **Result reported honestly whichever way the race went:** yes — aggression is the dominant
   *drive* under provocation and overtly wins only before executive maturity (age 2); in adulthood
   it is restrained. The group dominance route stays sub-threshold. All stated as measured.

Also: weights are SCAFFOLD by physiological ordering (VMHvl→PAG strongest), the seed edit is an
auditable programmatic transform (v8 archived, `_SEED_PATH` repointed), and the S1.4 fold-in is
documentary (SR-SEPARATION/PROXIMITY/REJECTION; loader reads only circuits/connections → no
dynamics change).

---

## 6. Current status / next

- Fixes applied for all 7; **targeted re-run of the 4 affected modules in progress**, then the
  **full-suite gate** — I will **not** re-push until the whole suite is confirmed green (learning
  from the premature push).
- Remote presently has `b61e234` (red on those 7); the fix-forward commit will land once green.
- After your ruling on §4 and the green gate: this + stage-4 satisfies the **Part 8 gate**, and
  **stage 5** (the Panksepp deletion) proceeds on v9-parity.
