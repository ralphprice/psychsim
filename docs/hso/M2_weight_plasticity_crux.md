# HSO M2 — Weight-Plasticity Crux Test (diagnosis only)

**Design authority:** `docs/PsychSim_Homeostatic_SelfOrganization_SPEC.md` (sealed).
**Scope:** M2 of the audit-first gate. DIAGNOSIS ONLY — no seed/engine/test/data changed; two markdown ledgers are the only files added.
**Substrate tested:** origin/main commit `b626c06` (v14 Phase 1.1).
**Method:** develop agents with the engine's own `divergence.develop` (a 400-tick childhood over a rich multi-channel environment), then run two tests. No substrate value is changed — the perturbations are in-memory on transient engine state, exactly as the spec's crux test prescribes. Reproducible by the reviewer against the remote.

**The decisive question (spec §2.3):** do weights *genuinely self-organize* (development determines the developed weight → plastic), or are they *effectively static* (the seed default determines it → nominally plastic, actually frozen)?

---

## Verdict: **FULL REBUILD** (the machinery is present-but-hollow)

The existing homeostatic machinery exists on paper (`homeostatic_setpoint`, R4-HOMEO) but **does not function**: weights are seed-default-dominated, single-weight perturbations do not self-correct, and — the clincher — **circuit activity does not reach its setpoint** (the setpoints are decorative). R4-HOMEO at `HOMEO_RATE=0.002` is roughly an order of magnitude too weak to regulate. This confirms the spec's central suspicion and the a-priori signature (the VTA weight threaded into a narrow window *because* a barely-moving weight can be threaded). **M3 is large — the homeostatic rule needs real replacement, not a tweak.**

---

## Confounds addressed first (why the naive tests mislead)

- **Uniform-scale perturbation is confounded by R8 normalization.** Multiplying *all* incoming weights ×3 and continuing, then observing them "return," is trivially explained by competitive normalization (`NORMALISE=True`) renormalizing a scalar multiple — it does **not** demonstrate homeostatic self-organization. (A first pass showed a spurious 0.96 mean "return" this way.) The real test uses **single-weight, non-uniform** perturbations.
- **Activation coverage is confounded by the environment.** A weight whose circuits are never active can't move for lack of drive, not weak homeostasis. Addressed by a **rich multi-channel environment** (touch/warmth/sweet/contact-loss/nociception/vision/audition) and by restricting the dominance analysis to the **active subset** (weights that actually moved from *either* start).

---

## Test B — seed-default dominance (the decisive test)

Develop two agents identically, one spawned with the **seed-default** weights, one with **uniform 0.3** weights. Converge → development determines the weight (plastic). Split → the seed default carries through (static).

- **Active weights:** 82/180 moved from either start under the rich environment (98 never move — they sit at their spawn value by construction).
- **Of the active weights with different starts (71 informative): 61 SPLIT, 10 converged.**

The developed weight ≈ the spawn weight, from *both* starts:

| edge | seed-start → developed | uniform-start → developed |
|---|---|---|
| CeA→PAG | 0.70 → **0.603** | 0.30 → **0.303** |
| VTA→NAc-core | 0.70 → **0.665** | 0.30 → **0.290** |
| LC→LA | 0.50 → **0.539** | 0.30 → **0.357** |
| SC-Pv→PAG | 0.50 → **0.431** | 0.30 → **0.304** |
| StN→CeA | 0.20 → **0.135** | 0.30 → **0.288** |
| vmPFC→ITC | 0.20 → **0.213** | 0.30 → **0.302** |

Each weight barely moves from where it spawned. **Development does not organize the weights toward a common target — where you start is where you end.** This is the effectively-static signature.

---

## Test A′ — single-weight perturbation self-correction

Perturb one developed weight to the *opposite* extreme (0.5-band → 0.9, or high → 0.1), continue development, measure return and whether the target circuit's activity reaches its setpoint.

| edge | developed → perturbed → after | return frac | target activity (setpoint 0.1) |
|---|---|---|---|
| LC→BA | 0.516 → 0.100 → **0.100** | 0.00 (stayed) | 0.272 |
| vmPFC→ITC | 0.213 → 0.900 → **0.907** | −0.01 (stayed) | 0.447 |
| LC→LA | 0.539 → 0.100 → **0.097** | −0.01 (stayed) | 0.452 |
| ITC→CeA | 0.558 → 0.100 → **0.087** | −0.03 (stayed) | 0.723 |
| BA→CeA | 0.315 → 0.900 → **0.757** | 0.24 | **0.775** |
| LA→CeA | 0.317 → 0.900 → **0.730** | 0.29 | **0.839** |
| SC-Pv→CeA | 0.402 → 0.900 → **0.714** | 0.37 | 0.830 |

- **Weights mostly stay perturbed** (return 0.00–0.37; a couple reach ~0.6 via normalization/BCM, not homeostasis).
- **The clincher — activity does not reach setpoint.** Every CeA-input perturbation leaves CeA pinned at **0.67–0.84** with setpoint **0.1**, and homeostasis never pulls it back. A circuit sitting ~8× above its setpoint, indefinitely, is a homeostatic rule that isn't running. **The setpoints are decorative** — nothing regulates activity to them.

---

## Direct homeo-strength quantification

`homeo_factor = 1 − HOMEO_RATE·(mean_activity − setpoint)`, `HOMEO_RATE = 0.002`, applied every 20 steps ≈ **60 applications** over a 400-tick / settle(3) development. A circuit pinned **0.8 above** its setpoint scales its incoming weights by **0.908** over an *entire development* — a **9.2% correction**. To pull a saturated circuit (0.9) down to setpoint (0.1) needs ~89% correction. **The rule is ~an order of magnitude too weak to regulate**, quantitatively consistent with Tests A′/B.

---

## What M2 decides

1. **Weight plasticity is NOT real** — weights are effectively static, seed-default-dominated; the developed weight is set at spawn, not organized by development. → **full rebuild**, M3 is large.
2. **The setpoints are decorative** — activity does not converge to them; R4-HOMEO is present-but-hollow. This is *why* M1 found the setpoints uniform-scaffold and it didn't matter behaviourally: nothing was homeostibating toward them anyway.
3. **The a-priori signature is confirmed** — the VTA narrow-window thread was possible precisely because weights barely move from spawn; a genuinely homeostatic weight could not have been threaded.

---

## Spawn-default scheme (sealed ruling #3): **not decidable from M2 — premature**

The handover asked M2 to output the spawn-default recommendation (uniform vs class-uniform) via the rule *"weights self-organize regardless of start → uniform works; start-point matters → class-uniform."* **That rule cannot be applied here**, because its premise is a *working* self-organizing system exhibiting legitimate path-dependence. In this substrate the start-point matters for the opposite reason: **homeostasis is hollow, so NOTHING self-organizes from ANY start.** Concluding "class-uniform" from a broken homeostasis would be a category error.

**Honest output:** the spawn-default scheme is an **M3 verification, not an M2 result.** Once M3 installs a homeostatic rule strong enough that a perturbed weight self-corrects and activity reaches setpoint, re-run Test B: if uniform-spawn then converges to the same developed state as other starts, uniform-spawn works (spec §5's expectation); if a residual start-dependence remains on a *working* rule, that is the legitimate signal for class-uniform. Provisionally, since even active weights are fully seed-dominated today, M3's strengthening must be substantial.

---

## Hand to M3 (scoping, not building)

- The homeostatic rule needs replacement toward the cross-homeostatic + inhibitory-homeostatic form (spec §2.1) with relative scaling (§2.2) — strong enough that (a) a perturbed weight self-corrects and (b) activity converges to setpoint. `HOMEO_RATE` an order of magnitude too weak is one lever, but the ×3-normalization confound warns that raising a scalar rate is not the whole story — the rule's *form* (two-term cross-homeostatic, inhibition-stabilized) is what the literature says yields setpoint convergence.
- M3's acceptance test is exactly Tests A′/B re-run: perturbation self-corrects; uniform-spawn converges; activity reaches setpoint; and (spec §2.1) the DRN/vmPFC/dlPFC/CeA saturations self-resolve **without** the hand-tuned interneuron stabilizer weights M1 flagged (Appendix A: `DRN-GABA→DRN`, `vmPFC-GABA→vmPFC`, `dlPFC-GABA→dlPFC`).
- **Do not build M3 until the reviewer independently re-derives M1 + M2 against the remote and rules.**
