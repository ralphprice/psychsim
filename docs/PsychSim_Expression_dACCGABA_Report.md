# `dACC-GABA` built — the brake is grounded and it works. Three tests stay red BY THE RULING'S CONSTRUCTION.

Built as ruled: `dACC-GABA` only, rate grounded from cortical FS/PV electrophysiology **before** looking at the
tests, setpoint paired, nothing else touched. **The silence-the-element test proves the brake carries. Two of
the three original reds are *unchanged by it* — and that is a FINDING the ruling explicitly anticipated, not a
brake failure.** Holding the commit.

> **⛔ NOT COMMITTED.** The three remaining reds are precisely the three fixes the ruling FORBADE this pass
> (regen golden / re-express read-out / retire earned negative). The suite cannot be green until those are
> ruled on. This is a surface-and-await checkpoint, not a commit checkpoint.

---

## 1. The grounding — and why it is NOT a second `dPAG-GABA`
The ruling said *"rate grounded from cortical FS/PV electrophysiology BEFORE looking at what restores the
tests."* The electrophysiology gives a **different** answer from `dPAG-GABA` **on purpose**:

- `dPAG-GABA` / `LC` fire **tonically under synaptic blockade** — autonomous pacemakers; their grounded rate is
  a deviant setpoint (0.19 / 0.15).
- **Neocortical PV⁺ fast-spiking interneurons are NOT autonomous pacemakers.** Under synaptic isolation they
  are largely **silent** — they lack the persistent-Na/HCN pacemaker conductances the `dPAG-GABA` citation
  rests on. Their high *in-vivo* rate is synaptically **driven** feedback, not intrinsic tone.

So the honest grounded baseline (the *no-synaptic-input relaxation target*) is **~0 → the scaffold default
(0.05) stands**, and `dACC-GABA` is **correctly NOT a grounded-setpoint deviant** (the reconciliation guard
confirms this — `_GROUNDED_SETPOINT_CIRCUITS` is unchanged, and it passes). **The grounded content is the
recurrent E-I loop, not a tonic rate** — the brake engages *in proportion to* `dACC`'s own activity, damping
exactly the saturation it must and doing nothing at rest.

**This mirrors `dlPFC-GABA` exactly** — the model's own already-correct cortical interneuron (Ferguson & Gao
2018). Built as its structural twin:

| | `dACC → dACC-GABA` | `dACC-GABA ⊣ dACC` |
|---|---|---|
| receptor / sign | AMPA (+) | GABA-A (−) |
| band | `moderate` (0.50) | `moderate-strong` (0.70) |
| basis | the cited cortical-E/I bands, **byte-identical to `dlPFC-GABA`'s loop** — NOT tuned to the tests | |

`dACC-GABA`: `structural_element: true`, τ=100 (fast-spiking), online 5.0 (with `dACC`), scaffold 0.05/0.1.

## 2. The brake WORKS — silence-the-element (principle 1)
| | `dACC` warm/harsh | `dlPFC` warm/harsh |
|---|---|---|
| **no brake** (pre-build) | 0.435 / 0.894 | 0.755 / **1.000** ← ceiling |
| **with brake** (grounded, untuned) | 0.291 / 0.597 | 0.663 / **0.858** ← off ceiling |
| **silence the brake** (lesion `dACC-GABA`) | 0.495 / **1.000** | 0.796 / **1.000** ← hot again |

The grounded loop pulls `dACC` off 0.894 and `dlPFC` **off the 1.000 ceiling**; lesion it and both run hot to
1.000. **The saturation artifact is removed.** And the divergence interaction confirms it from the other side:

| | interaction_at(500) | earned-negative threshold |
|---|---|---|
| no brake | **−0.0755** (saturation artifact) | < 0.05 |
| with brake | **−0.0534** | < 0.05 |

The saturation's contribution (~0.022) is **gone**. What remains is a small, well-posed structural interaction
(`test_interaction_is_stable_across_durations` now **passes** — stable sign + magnitude across 350/500/600),
sitting **just 7% over** the arbitrary 0.05 "does-not-emerge" line.

## 3. What HOLDS
- The **grounded brake removes the saturation** (silence-test; `dlPFC` off ceiling).
- The **divergence interaction is no longer an artifact** — it dropped to −0.053 and is now *well-posed*
  (stability test passes). It is a small real structural value, not a ceiling effect.
- `dACC-GABA` is grounded, not tuned, and correctly **not** a setpoint deviant (reconciliation passes).
- Count pins re-baselined 89→90 (both: circuit count + live-at-adult). Regrown.
- **The face still moves** (Phase B win, unchanged): pain→face, separation→voice, vicarious<direct emergent.

## 4. What does NOT hold — and why each is a RULING decision, not a brake failure
The suite has **3 failures**. Every one is a fix the ruling forbade this pass:

### (a) `test_environment_differentially_engages_the_executive` — the read-out conflation, CONFIRMED
warm 0.410 **<** harsh 0.545 — still fails **with the brake in**. Decomposed:

| term | construct | warm | harsh | warm>harsh? |
|---|---|---|---|---|
| `dlPFC` | control | 0.663 | 0.858 | **no** |
| `OFC` | control | 0.276 | 0.179 | yes |
| `dACC` | **monitoring** | 0.291 | 0.597 | **no** |
| control-only (dlPFC+OFC) | | 0.469 | 0.519 | **no** |

**This is exactly the case the ruling anticipated:** *"If it still conflates once the brake is in, re-express
it."* It still conflates. `dACC` (conflict/error **monitoring**) is correctly higher under a harsh,
unpredictable environment — and it drives `dlPFC` via the grounded `dACC→dlPFC` edge, so even **control-only**
is warm<harsh. The read-out sums **monitoring** with **control** as one quantity; they are different
constructs. **The brake did its job (removed saturation); the residual is the read-out construct, which the
ruling reserved: "the re-expression must separate monitoring from control." I have NOT re-expressed it —
that is your call now that the brake is in.**

### (b) `test_divergence_does_not_robustly_emerge` — marginal, and NOT retired
|interaction| = **0.0534** > 0.05. The **earned negative**. Per the ruling I have **not retired it, not moved
the threshold, not tuned toward it.** The honest statement: with the brake in, the interaction is *well-posed
and stable* but sits **7% over** the near-zero line. It is no longer a saturation artifact; whether 0.053
counts as "emerges" is the threshold **you** set at 0.05. **Reporting the number, not adjusting the line.**

### (c) `test_matches_committed_baseline` (golden) — shifted, NOT regenerated
`dACC-GABA` changes cortical dynamics and `dACC→PAG-PANIC` feeds back, so develop() diverges from the committed
snapshot. **I have NOT run `PSYCHSIM_REGEN_CHAR=1`** — regenerating would bless the new state as baseline, and
the ruling forbade it this pass.

## 5. The decision back to you
The brake is built, grounded, and verified. The suite stays red **only** on the three items the ruling
reserved. To green it, one ruling each:
1. **Read-out** — re-express `EXECUTIVE` to separate monitoring (`dACC`) from control (`dlPFC`/`OFC`)? (The
   ruling's own condition — *"if it still conflates once the brake is in"* — is now met.)
2. **Earned negative** — is 0.053 (well-posed, stable, 7% over) still "does not emerge", or does the small real
   interaction change the finding? **I will not touch the threshold either way without a ruling.**
3. **Golden** — regenerate now that the brake is grounded (the new state is honest), or hold?

**Nothing committed. Nothing tuned. `BA→dACC` band untouched. Earned negative not retired.** Registered:
S18 (cortical brake 82% absent + the effect-sizes-biased-upward caveat), S19 (read-out audit as a class),
S20 (defensive columns wired for permission not drive; `MeA→VMH` fallback the immediate suspect), CV#4 (pSTS).
