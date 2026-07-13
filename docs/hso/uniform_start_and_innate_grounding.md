# The associative-weight arc — final record (HSO → uniform → near-zero → the connectome answer)

**What this ledger records:** a long investigation into "the arbitrary neural-pathway weights" that ended by
finding the arbitrariness was never in the *values* — it was two *disconnected pathways*. The net change to
the substrate is **two grounded connectome corrections plus provenance-only basis re-marks. No starting
weight was changed from the seed's original bands.**

---

## 1. The dead ends (recorded so we don't repeat them)

- **HSO (homeostatic self-organization) — SHELVED.** A cross-homeostatic rule + grounded setpoints + a
  measured timescale hierarchy, to make weights self-organize. It was compensatory machinery for a problem
  the design had already solved; each fix spawned the next (learning-vs-homeo conflict → timescale
  separation → ~8× development). Its M1/M2 audit (`M1_fixed_values_audit.md`, `M2_weight_plasticity_crux.md`)
  stands as the record of *why* the earlier machinery was hollow.
- **Uniform-everything (all weights → 0.5) — REVERTED.** A diagnostic that flattened *all* categories to one
  value. It flattened the reinforcer + backbone categories too, breaking aggression closure and serotonin
  regulation (17 failures). Wrong: it erased the design's coded distinctions.
- **Near-zero associative override (assumption-basis edges → 0.05) — REVERTED.** The subtlest error, and the
  most instructive. We read §2.11's "near-zero associative sites that experience grows" as "push the
  associative bands *below* themselves, to 0.05." We did it to fix the learning tests. **Learning turned out
  to be a connectome problem, not a value problem** (§3), so the value change was a solution to a problem that
  didn't exist — and it *starved* functional pathways that worked fine at the original bands (§4).

## 2. The actual fix — two grounded connectome corrections

The learning failure (`test_substrate_learning`: a visual cue fails to acquire anticipatory reward value) was
traced, edge by edge, to **two real anatomical gaps in the cortical cue→reward circuit** — both grounded
backbone, previously missing or mislabelled. BCM plasticity needs *both* endpoints of an associative site
driven; the connectome was starving both:

| correction | what it is | grounding |
|---|---|---|
| **`IN-VIS → RET` (added, +1 input edge)** | routes the visual cue INTO the cortical stream (RET→LGN→V1→V-ventral→OFC), which existed but was *starved* — the cue reached only `SC-Pv` (subcortical threat). Presynaptic drive. | retinogeniculostriate / primary visual pathway — textbook anatomy (retina→LGN→V1), like `IN-OLF→OB` |
| **`VTA→OFC` + `VTA→vmPFC` (re-marked assumption→anatomy)** | the mesocortical DOPAMINE projection — delivers the DA teaching signal to the cortex (postsynaptic drive + DA gate). Weight UNCHANGED at its band. | mesocortical DA is one of the four classical DA systems; **every other DA projection** (`VTA→NAc-core/shell`, `SNc→DStr`, sibling `VTA→dlPFC`) is already `anatomy`; the split was an internal inconsistency with no anatomical basis |

The `VTA→OFC/vmPFC` re-mark is a **provenance correction**: those edges were already at their bands (0.35 /
0.20) in the original seed; the re-mark fixes the mislabel (they are backbone, not associative). It only
became *load-bearing* while the near-zero override was flattening them to 0.05 — with the override gone, the
edges load at their bands regardless, and the re-mark documents what they are.

## 3. Why the value change was never needed

With the two connectome corrections in place, learning forms through experience **at the associative sites'
ORIGINAL bands** (`V-ventral→OFC` = 0.20, its `low` band — no near-zero): `test_cue_acquires` rises,
`paired > unpaired` (DA-gated discrimination intact), the reinforcer-gating control holds. The starting value
was not the problem and did not need touching. §2.11's "near-zero associative site that experience grows" is
satisfied by the original `low`/`low-moderate` band: a *small* start that the existing use-dependent
plasticity grows. The band **is** the design's category-3 value.

## 4. Why near-zero was breaking everything

Near-zero (0.05) starved every functional pathway that depends on an associative site carrying a real driving
signal — the *same* mechanism as the cue→reward failure, replicated across systems. Confirmed regressions
(pass at HEAD, fail under near-zero, pass again once reverted to bands):
- `test_matrices_engine::sociometer_tracks_belonging` — affiliation→appetitive-response starved → belonging
  never accrues → esteem flat at 0.
- `test_aggression_pathway::…maturationally_restrained` — the PFC control pathway weakened → `aggress` instead
  of the matured `restrain`.
- `test_group_matrix` — group synchrony/belonging, same affiliation mechanism.

These were the diagnostic that the assumption→near-zero override was too broad — and, ultimately, unnecessary.

## 5. What landed (the honest net change)

- **No starting weight changed.** Every edge loads at its seed `default_weight` band (original band-lookup;
  the near-zero override and `ASSOCIATIVE_START_WEIGHT` are removed).
- **Two grounded connectome corrections:** `IN-VIS→RET` added; `VTA→OFC`+`VTA→vmPFC` re-marked to
  mesocortical-DA backbone (weight unchanged).
- **Provenance-only basis re-marks:** the 22 structural-regulatory edges (DRN serotonergic system, interneuron
  E/I feedback, Allen afferents) + the 2 mesocortical-DA edges, `assumption`→`anatomy`. Under band-lookup these
  are weight-neutral; they correct the category label (and the scaffold flag), nothing else.
- **Library regrown** on the corrected connectome; **characterisation golden regenerated** — a small, uniform,
  `develop`-only shift (≈0.002–0.01 per profile fraction, **no classification changed**; relations/group/
  environment identical) — the fingerprint of the one new input edge, not a regression.

## 6. The lesson (banked)

The "arbitrary associative weight" was a phantom. Three times the learning failure *looked* like a value
problem and three times the honest answer was the connectome, not the value — and the final answer was that
the value never needed changing at all: the original bands were §2.11's three categories the whole time, and
the only real bugs were two disconnected pathways. When a value seems load-bearing for a functional result,
the arbitrariness is almost never in the value — it is in a mechanism the value is compensating for. Trace the
mechanism; don't tune the value. And when your *own* layered change (near-zero) starts generating a
compensatory-failure cascade, that change is the thing to re-examine — not the substrate under it.
