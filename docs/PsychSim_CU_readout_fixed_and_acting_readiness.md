# CU read-out fixed (tone-invariant, validated) + the CU answer + acting-readiness diagnosed — finding (HOLDING commit)

Per the ruling: fixed the punishment read-out **on measurement principle**, **validated tone-invariance** (the
mandatory gate), then **read the CU answer off it**. Also diagnosed acting-readiness (a/b/c). The CU read-out is
done and I could land it; acting-readiness needs your "surface → decide" call, so I'm **holding the whole commit**.

## 1. Corrected punishment read-out — a YOKED unpaired control (tone-invariance VALIDATED)
The old `punishment_learning` (defensive-output **after** − **before**) is confounded by construction: LC → CeA,
BA (2 of the 3 DEFENSIVE_OUTPUT circuits), so tonic NA is inside the signal, and the before/after timepoints
drift. Two candidate fixes; I validated each against the mandatory check (**≈0 when nothing is learned, at every
NA tone**):

- **CS+ vs CS− differential** (visual CS+ vs olfactory CS−): **FAILED validation** — the two modalities have
  *different NA gains*, so the contrast grows with tone (+0.000 / +0.136 / +0.179 at LC 0.05/0.15/0.25 with
  nothing learned). Rejected — a real disqualification, not tuned away.
- **Yoked unpaired control** (conditioned = CS paired with punishment; yoked = **same** CS exposures + **same**
  punishments, temporally **unpaired**; read `defensive-to-CS(conditioned) − defensive-to-CS(yoked)`):
  **PASSED exactly** — **+0.0000 at LC 0.05, 0.15, 0.25** when nothing associative is learned. Tonic tone *and*
  non-associative sensitization both cancel (same tone, same # punishments; only the *pairing* differs). This is
  the standard associative-conditioning control, and it's tone-invariant by validation, not assertion.

## 2. The CU answer, read off the validated read-out (at grounded LC 0.15)
Associative punishment learning **[throttle 0.0, 0.5, 1.0] = [0.117, 0.016, 0.093]**:
- **Every throttle still learns (all POSITIVE)** — no CU-style failure-to-learn, no inversion. **The robust
  "weak, not a failure" claim HOLDS** — now on a tone-robust read-out, so it's *trustworthy*, not confounded.
- The graded pattern is **non-monotone** (0.5 lowest), not a clean graded deficit — echoing the original v8
  non-monotonicity. So the punishment *deficit* is **not** the robust CU signature.
- **Verdict (whatever it says, either direction):** on the clean mechanism + tone-robust read-out, throttling
  affective empathy does **not** produce a punishment-learning failure. The robust CU signature remains the
  **reads-but-doesn't-feel dissociation** (`test_throttle_blunts_affect_while_sparing_cognition`, still green),
  exactly as the existing tests already claim — but now that conclusion survives a validated read-out.
- **On the original tonic-NA "CU scare":** it was measured with this same confounded read-out, so it was
  plausibly *doubly* confounded (teaching signal + measurement). The corrected read-out shows the punishment
  deficit was never the robust signal — consistent with retiring that scare as an artifact.

**Proposed test update** (the honest, tone-robust assertions): keep "every throttle acquires POSITIVE aversion
(no failure-to-learn)" — now a *strong* pass, not marginal; **drop the brittle `spread < 0.06` / monotonicity
operationalisation** (it was reading the confounded compression) and document that the graded deficit is
non-robust/non-monotone and not the CU signature.

## 3. Acting-readiness — diagnosed (b + c): real NA mechanism on a too-thin margin
`teen.steps ≤ child.steps` flipped (teen 35→39, child 37→38). Diagnosed:
- **(b) real mechanism:** `steps` = BG accumulation to a threshold raised by `executive_hold`. Tonic NA →
  **LC→dlPFC → executive_hold ↑** (teen dlPFC 0.83→0.93, hold 0.184→0.203), age-graded by dlPFC maturation
  (bigger on teen than young child). `go_drive` ~unchanged. A genuine NA→control effect, not a read-out artifact.
- **(c) too-thin margin:** the ordering is **not robust** — across reward intensity (LC 0.15): rew 0.6 → teen≤child
  ✓, 0.7 → ✗, 0.8 → ✗, 0.9 → ✓, all on **1–2 step** margins. The keystone was asserted on a 2-step margin (35 vs
  37) and flips with a hair of reward intensity. The grounded NA nudged the rew=0.8 case over.

**The finding:** `teen ≤ adult` is robust (39 vs 47, wide) — the reward-peak-vs-late-control-maturation signal is
real. `teen ≤ child` is a **thin, reward-intensity-sensitive margin that is not a reliable assertion**. Per the
ruling I will **not** silently re-baseline it. **Proposed handling (your decide):** assert the robust part
(`teen ≤ adult`) and re-characterise the child-vs-teen comparison as *comparable, thin-margin* (documented
finding), rather than a strict ordering — OR your preferred treatment.

## 4. Registered (per §6) — the general finding
Added to the gaps register: **several behavioural read-outs were validated while NA was structurally dead (LC
unafferented → NA flat 0.05); a correct, live NA can expose them as conflating tonic NA tone with the measured
signal.** Punishment = a pinned+fixed instance (sums LC-driven circuits → fixed with the yoked control).
Acting-readiness = candidate (a real mechanism on a thin margin). Golden = a real coherent consequence (regen).
Per-read-out question for each future case: real NA consequence (re-baseline honestly) vs tone/signal conflation
(fix the read-out, validated). Will recur as BF-ACh / SNc are completed.

## Holding — the decision I need
The CU read-out is fixed + validated + read (I can land it per your method). Before I rewrite the committed
tests + commit, I need your call on:
1. **The CU test update** (§2) — assert "no failure-to-learn" (strong), drop the confounded spread/monotonicity
   assertions, document the non-robust graded deficit. OK?
2. **Acting-readiness** (§3) — the "surface → decide": re-characterise to the robust `teen ≤ adult` + thin-margin
   child comparison, or your preferred handling? (Not silently re-baselining.)

Then I finalise both tests, regen the golden (authorized), full suite green **with every failure understood**,
commit + push + STOP. Nothing committed. **No result is a target — both ways:** I did not pick the read-out that
manufactures or erases the CU signature (I picked the one that passes the tone-invariance validation), and the
CU answer is reported as it came out (no robust punishment deficit; dissociation remains the signature).
