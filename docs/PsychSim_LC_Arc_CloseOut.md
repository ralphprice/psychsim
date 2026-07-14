# LC Arc — Close-Out: the CU punishment "signature" was an artifact, caught by the discipline

## The headline (the arc's result)
The graded punishment-learning **CU deficit was an artifact**, and the honesty discipline caught it. It appeared
under a **tonic-NA-confounded teaching signal** read through a **tonic-NA-confounded measurement** — *doubly*
confounded — and was held as suspect precisely because **it looked like the finding we most wanted**. Cleaned
through the full cascade, the answer is: **every throttle learns; no CU-style failure-to-learn; "weak, not a
failure" HOLDS on a trustworthy read-out.** The robust CU signature is the **reads-but-doesn't-feel
dissociation**, not the punishment deficit. The tonic-NA scare is retired as an artifact, reasoning recorded.

## The cascade (what was built, each grounded/cited, each gated)
1. **CRF-R1 → RECEPTOR_SIGN** — CeA-CRF→LC signs excitatory (Van Bockstaele); the real route by which a
   GABAergic CeA drives noradrenergic arousal.
2. **Phasic teaching signal** (`neuromod_teaching`, R5 gate) — the teaching signal is the source's deviation
   above its running baseline, not its absolute level. Removes the tonic-NA teaching artifact; resolves the
   deferred VTA-DA tonic/phasic case. `test_substrate_learning` preserved.
3. **`CeA→LC` afferent** (CRF-R1) — completes the unafferented LC hub, so NA finally has a teaching signal
   (the `test_coactive` NA-gated edge learns again).
4. **Latch found + A+B ruled + A+B FALSIFIED** — `CeA→LC` + `LC→CeA` latched CeA at saturation. The ruled fix
   (α2 strong + a tonic CeA self-brake B) was falsified by data: B breaks the v9 reactive-aggression keystone
   (CeA→PAG/HYPdm are inhibitory) and doesn't de-load-bear α2. Held, surfaced, corrected.
5. **Phasic `CeA→LC`** (per-edge `phasic_drive`, existing `mean_activity` machinery; grounded in phasic CRF
   release) — dissolves the latch at its source (drive→0 at plateau), **regardless of α2**; aggression keystone
   untouched. α2 (`LC→LC`) kept non-plastic at its grounded value, **verified NOT load-bearing** (loop stable
   across α2 0.0–0.85).
6. **LC intrinsic pacemaker** (baseline 0.05→0.15, grounded in LC tonic firing ~1–3 Hz / burst ~10–15 Hz ≈ 0.15;
   Aston-Jones & Cohen 2005; Berridge & Waterhouse 2003; PROVISIONAL) — phasic `CeA→LC` had removed the (wrong)
   tonic prop of LC's tone; the pacemaker supplies LC's real tonic NA, restoring DA-gated learning.
   Value grounded from electrophysiology, NOT the stability window.

## The measurement fix (on principle, validated)
The full-suite gate exposed that the LC pacemaker's tonic-NA lift broke the CU punishment read-out. Root:
`punishment_learning` summed `DEFENSIVE_OUTPUT=(CeA,PAG,BA)` while **LC projects directly into CeA and BA** —
confounded **by construction**, valid only while LC was structurally dead.
- Fixed on principle: **yoked unpaired control** (conditioned vs an identical copy given the same cues + same
  punishments UNPAIRED; only the CS→US contingency differs). Tonic tone + non-associative sensitization cancel.
- **Validated tone-invariant** (the mandatory gate): exactly **0.0000** when nothing associative is learned, at
  LC 0.05/0.15/0.25. (The reviewer's own CS+/CS− differential was tried first and **failed** this check —
  +0.136 with nothing learned — and was rejected. The check did its job on the reviewer's proposal.)

## The CU answer (multi-seed, 12 temperaments, then assert only survivors)
- **No failure-to-learn is SEED-ROBUST**: every value > −0.02 across all seeds/throttles (min −0.003). Throttling
  affective empathy does **not** produce a CU-style failure to learn punishment.
- **The throttle→learning relation is ROBUSTLY NON-MONOTONE** (U-shaped: 0.5 the dip, 1.0 recovers) in **12/12**
  seeds — a real feature, not noise; mechanism not yet traced (registered).
- The old `spread < 0.06` / monotonicity assertions were reading the confounded compression → **dropped**.

## Acting-readiness (diagnosed; robust half asserted, non-robust half registered)
The tonic-NA lift flipped `teen ≤ child`. Diagnosed: **(b)** a real mechanism — tonic NA → LC→dlPFC →
executive_hold ↑, age-graded by dlPFC late maturation (reviewer-verified) — on **(c)** a too-thin margin
(`teen ≤ child` flips with reward intensity, 1–2 steps). Asserted the robust half (`teen ≤ adult`); **registered**
the child-comparison + candidates (real gap / read-out mismatch / partial-assembly fragility), not silently
re-baselined.

## Registered (the durable findings)
- **NA-robustness of behavioural read-outs** (general): read-outs validated while NA was structurally dead may
  conflate tonic tone with signal; audit each as the other dead hubs (BF-ACh, SNc) are completed.
- CU punishment artifact retirement (with reasoning); the robust non-monotone U-shape.
- Acting-readiness child-comparison gap + candidates + the LC→dlPFC mechanism.
- Provisional neuromod-hub baselines; the future faithful self-regulation mechanism (homeostatic-plasticity
  core, developmentally staged, maturing inhibition, executive as later contributor).
- B (CeA tonic self-inhibition) deferred (keystone-breaking if tonic); per-edge `phasic_drive` as a general
  option; PBN/NTS→LC; BF-ACh; SNc.

## Discipline record — no result is a target, both ways
Rejected the reviewer's read-out proposal when it failed validation; chose the one that passed; reported a CU
answer that **dissolved the wanted finding**. Held the commit at every juncture where a value looked load-bearing
(α2 strong, LC baseline, the punishment inversion) until the *mechanism* was clean and the *measurement* was
validated. The wanted-looking CU deficit was distrusted precisely because it was wanted — and it did not survive.

## Gate status
All four previously-failing tests verified green in isolation (the two rewritten CU tests + `cu_profile`,
acting-readiness, and the regenerated characterisation golden). The scan tests are structural (they use the
signature name, not its value) and were green in the prior full run. The final full-suite re-run is pending —
the WSL environment is currently out of RAM (an unrelated 5.6 GB process), so the suite OOMs; it will be run to
green before commit + push.
