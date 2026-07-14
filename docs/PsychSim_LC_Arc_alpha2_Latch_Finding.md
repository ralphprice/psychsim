# LC Arc — the α2 brake at moderate/plastic FAILS (CeA↔LC latch) — finding + resolutions (HOLDING commit)

Building the ruled arc (**phasic fix + `CeA→LC` via CRF-R1 + `CeA↔LC` α2-autoreceptor brake**) surfaced that the
α2 brake **as anticipated** (a single moderate, plastic edge) does **not** stabilise the loop. Diagnosed to the
root, confirmed a resolution, **holding the commit** because the fix needs two refinements the ruling didn't
specify and the load-bearing one is a "no result is a target" tripwire.

## What built cleanly
- **Phasic teaching signal** (engine.py, R5 gate → `neuromod_teaching`): DA/OT fire phasically, `test_substrate_learning`
  passes, tonic-NA artifact gone (NA-rest teaching ≈ 0). Solid.
- **`CeA→LC` via CRF-R1** (cited, excitatory): LC is afferented, NA now has a teaching signal. `test_coactive_connection_strengthens`
  (NA-gated `LA→BA`) passes again — driving LA → CeA → LC → phasic NA tunes the edge. The whole point.
- **BF-ACh + SNc registered** (not bundled), per ruling.

## The finding: the CeA↔LC loop LATCHES CeA at saturation
`CeA→LC` (+, new) closes a positive-feedback loop with the existing `LC→CeA` (+, α1). The α2 autoreceptor brake
(`LC→LC`, −) as first built — **moderate weight, plastic** — does NOT break it. Verified against the code, HEAD vs arc:

| threat, then 12 neutral episodes | CeA after threat | CeA after neutral | verdict |
|---|---|---|---|
| **HEAD** (no loop) | 1.000 | **0.33** | recovers (healthy habituation) |
| **arc** (moderate, plastic α2) | 1.000 | **1.00** | **LATCHED** — never recovers |

Once threat maxes CeA, the loop **self-sustains** it: `CeA(1.0)→LC(0.61)→CeA(1.0)`, indefinitely, through neutral
episodes. That is *persistent saturation* → arena `viable()` fails (`test_newborn_grown_banked_all_build`, banked
agent K tail-mean max-act 0.657→**0.984**) → the full suite goes red and ~10× slower (agents driven pathological).

### Root cause — two mechanism faults, both traced (not tuned)
1. **The α2 edge is plastic → BCM DEPRESSES it** (0.50 → 0.27 over development) while the excitatory arms
   strengthen (`CeA→LC` 0.50→0.71). An autoreceptor is a **structural regulatory element, not a learned
   association** — it must not Hebbian-learn. Making it plastic was a category error.
2. **Even non-plastic, "moderate" (0.5) is insufficient.** The brake must hold LC low enough that `LC→CeA` can't
   overwhelm CeA's native (leaky-decay) recovery — i.e. loop-gain < 1. Sweep (non-plastic, pinned):

   | α2 (non-plastic) | CeA after threat+12 neutral | |
   |---|---|---|
   | 0.5 | 1.000 | LATCHED |
   | **0.7** | 0.509 | recovers |
   | **0.85** | 0.381 | recovers (≈ HEAD's 0.33) |
   | 0.95–1.0 | 0.34 | recovers |

## Candidate resolution (A) — complete the α2 autoreceptor FAITHFULLY  *(confirmed, recommended)*
Make the `LC→LC` α2 edge **non-plastic** (structural; `weight_bounds=[w,w]` pins it against BCM/homeo/normalise —
verified it holds at 0.850 through 30 threat episodes) at the **strong** band.
- **Grounded, not tuned:** (i) autoreceptors are fixed regulatory elements, not learned — non-plasticity is a
  category correction; (ii) α2 autoinhibition is the **dominant** brake on LC firing — clonidine (α2 agonist)
  silences LC, yohimbine (antagonist) powerfully disinhibits it — so "strong" is the physiological band.
- **Confirmed:** latch breaks (CeA 1.0→0.376 ≈ HEAD), arena viable again (K 0.984→0.637 ≈ HEAD 0.657), NA still
  fires phasically (rest 0.032 / aversive 0.159), `test_coactive`, `test_substrate_learning`,
  `test_weights_stay_bounded`, arena viability tests — **all green** (10/10 targeted).
- **Honest caveat (why I'm not just committing):** the band **is load-bearing** (0.5 latches, 0.85 recovers).
  What it's really setting is loop-gain < 1, and the loop's *other* weights (`CeA→LC`, `LC→CeA`) are scaffold.
  So "α2 must be strong" is partly the α2 value carrying the loop's stability — the classic *value-compensates-
  for-a-mechanism* pattern. That's exactly what I don't get to decide alone.

## Candidate resolution (B) — the deeper missing element: CeA-side feedback inhibition
The reason HEAD's CeA recovers is its leaky decay; the loop defeats that. In reality CeA *also* has strong
**intra-amygdala GABAergic feedback inhibition** (CeAl→CeAm; CeA is ~95% GABAergic) that actively drives
habituation — and the model's CeA has **no activity-driven self-inhibition** (`CeA-GABA→CeA` exists but is
PVN-OT-driven, not CeA-driven). So the α2-strong value in (A) may be **compensating for this absent CeA brake**.
Adding it is the more complete fix but a **new cited structural element beyond this arc's scope** (same class as
the hubs we register).

## The decision I need (holding — nothing committed; candidate A sits uncommitted in the tree)
1. **(A) faithful α2** — non-plastic + strong band — as the arc's stabiliser (my recommendation: it's faithful
   completion of the mechanism you already ruled, both refinements are grounded, and it's confirmed sufficient);
   OR
2. **(A) + also add (B)** the CeA intra-amygdala feedback inhibition now (more complete; the α2 value then isn't
   carrying the loop alone); OR
3. **(B) instead**, and register/revisit the α2 band; OR
4. register (B) and take (A), noting the α2 band as load-bearing scaffold to revisit when the loop weights are
   calibrated.

Then: full suite is the gate (golden regen honestly if behaviour shifted — it will have), commit + push + STOP,
and only *then* the two CU-shift re-examinations on the clean mechanism.

**No result is a target — both ways.** The arena went viable again under (A), which is the *wanted* look; I'm
surfacing rather than accepting it because the load-bearing band could be the value masking the missing CeA
brake (B). Your call on which mechanism carries the loop.
