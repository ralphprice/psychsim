# Phasic teaching signal — mechanism approach (for review; NOTHING built)

Per the ruling: the tonic-NA elevation from `CeA→LC` is a mechanism artifact — the neuromodulator **teaching
signal** must be **phasic** (a deviation from baseline), so a tonically-elevated source (CeA→LC holding LC up)
does not produce a tonic teaching signal. Solve it **generally** for the teaching-signal architecture (which
also resolves the deferred VTA-DA tonic/phasic case), **not** by tuning `CeA→LC`. This is the approach,
brought for review before building — it touches the teaching-signal path.

## The problem (recap, verified)
`neuromod_output(nmod)` = the **absolute** mean activation of the neuromodulator's source circuit(s), and it
gates R5 consolidation (`consolidate() = lr·eta·modulator·eligibility`, engine.py:178). DA "works" only
because VTA sits near baseline at rest and is *driven up* by a reward event. `CeA→LC` breaks that: CeA is
tonically elevated (~0.40 at rest, held up by its own afferents), so `CeA→LC` holds LC up continuously →
resting NA 0.05→0.22 → the NA-gated edges over-consolidate **at baseline**, not just on the aversive event.
A teaching signal must be a *deviation* ("something bad happened NOW"); a tonic level is not one.

## The precedent (already in the substrate)
Behaviour selection **already** measures drives phasically: `_phasic_drive = max(0, activation −
resting_baseline)` so "tonic activation cancels, hub circuits don't swamp" (social.py). The engine **already
tracks a running baseline per circuit**: `mean_activity[cid] = 0.99·mean + 0.01·activation` (engine.py:167,
used for the BCM θ threshold). So the phasic machinery exists; the teaching signal just isn't using it.

## The approach
**Make the R5 teaching signal the source's activation ABOVE its running baseline, not the absolute
activation:**

```
teaching(nmod) = max(0,  mean(source activations)  −  mean(source running baselines) )
```

using the engine's existing `mean_activity` as the running baseline (already tracked, adaptive, available in
`step()`). At rest, activation ≈ baseline → teaching ≈ 0 (tonic cancels). On an event, activation > baseline →
teaching = the phasic deviation, which then adapts (correct — a phasic burst decays as the baseline catches
up). Grounded: phasic DA/NA teaching signals **are** deviations from tonic firing.

## Prototype confirmation (deviation-from-baseline, measured)
|  | absolute (current) | phasic (the fix) |
|---|---|---|
| NA rest | 0.220 | **0.000** — tonic `CeA→LC` cancels (artifact gone) |
| NA aversive (nociception) | 0.558 | **0.287** — fires on the event |
| DA rest | 0.049 | **0.000** |
| DA reward (sweet) | 0.382 | **0.331** — reward learning preserved |

So it removes the tonic-NA artifact, preserves DA-gated learning, and resolves the VTA-DA tonic/phasic case —
one general mechanism, no `CeA→LC` tune.

## Two design decisions for your steer (before I build)
1. **Baseline reference — running `mean_activity` (recommended) vs a fixed resting-baseline capture.**
   `mean_activity` is already in the engine, adaptive, and matches the θ machinery — cleanest. Caveat: it
   adapts (0.01/step), so a *sustained* signal decays (correct for phasic, and it converges from the design
   baseline over the first ~100 steps of a life — a minor early-development transient). The alternative (a
   fixed `resting_baseline` capture, the `_phasic_drive` precedent) doesn't adapt but must be captured/passed
   into the engine. I recommend `mean_activity`.
2. **Scope — only the consolidation gate, or also the read-out / behaviour gain?** The ruling is about the
   *teaching* signal, so the minimal change is the R5 consolidation gate (engine.py:178) → a phasic
   `neuromod_teaching(nmod)`, leaving `neuromod_output` (absolute) for the behaviour DA-gain (behaviour.py:60,
   Go vigor) and read-outs. **But** `reward_signal() = neuromod_output("DA")` is described as "the RPE" — and
   an RPE *is* phasic — so consistency might argue for making that read-out phasic too. I lean **minimal**
   (only the consolidation gate) to avoid perturbing behaviour selection, and flag `reward_signal` as a
   consistency question for you. Which scope?

## Verify (once you approve the approach + decisions, at build)
- The phasic teaching signal is the deviation-above-baseline (the tonic-NA artifact gone: NA-rest teaching ≈
  0); NA fires on aversive, DA on reward.
- **DA-gated learning still passes** (`test_substrate_learning` — the paired/unpaired discrimination; phasic
  DA fires during the 12-tick pairing because `mean_activity` adapts slowly). This is the load-bearing
  regression check.
- Then **re-run the LC foundation** with the phasic signal and **re-examine the two shifts** (the CU
  punishment-deficit flip; the classification flip) — do they persist (real CU signature, now un-confounded)
  or dissolve (they were the tonic artifact)? That is the honest test the ruling set up.
- Full suite green; plasticity semantics otherwise intact.

**Nothing built.** Approach + prototype + the two decisions, for your review — same discipline. This is a
real teaching-signal-path change, so it lands as its own reviewed step (and it retires the VTA-DA tonic/phasic
deferral too). How do you want the two decisions, and shall I build it?
